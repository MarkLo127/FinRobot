import os

os.environ["IN_STREAMLIT"] = "true"  # 避免在 surya 內部進行多進程處理
os.environ["PDFTEXT_CPU_WORKERS"] = "1"  # 避免在 pdftext 內部進行多進程處理
SAVE_DIR = "output/SEC_EDGAR_FILINGS_MD"

import pypdfium2  # 需要放在頂部以避免警告
from typing import Optional
import torch.multiprocessing as mp
from tqdm import tqdm
import math

from marker.convert import convert_single_pdf
from marker.output import markdown_exists, save_markdown
from marker.pdf.utils import find_filetype
from marker.pdf.extract_text import get_length_of_text
from marker.models import load_all_models
from marker.settings import settings
from marker.logger import configure_logging
import traceback
import json

configure_logging()
SAVE_DIR = "output/SEC_EDGAR_FILINGS_MD"

def worker_init(shared_model):
    global model_refs
    model_refs = shared_model


def worker_exit():
    global model_refs
    del model_refs


def process_single_pdf(args):
    filepath, out_folder, metadata, min_length = args

    fname = os.path.basename(filepath)
    if markdown_exists(out_folder, fname):
        return
    if not filepath.endswith("pdf"): 
        return
    try:
        # 跳過嘗試轉換那些沒有太多嵌入文字的文件
        # 這可能表明它們是掃描的，且沒有正確進行 OCR
        # 通常這些文件不是最近的/高品質的
        if min_length:
            filetype = find_filetype(filepath)
            if filetype == "other":
                return 0

            length = get_length_of_text(filepath)
            if length < min_length:
                return
        
        full_text, images, out_metadata = convert_single_pdf(
            filepath, model_refs, metadata=metadata
        )
        if len(full_text.strip()) > 0:
            save_markdown(out_folder, fname, full_text, images, out_metadata)
        else:
            print(f"空白檔案：{filepath}。無法轉換。")
    except Exception as e:
        print(f"轉換 {filepath} 時發生錯誤：{e}")
        print(traceback.format_exc())


def run_marker_mp(
    in_folder,
    out_folder,
    chunk_idx=0,
    num_chunks=1,
    max_files=None,
    workers=5,
    metadata_file=None,
    min_length=None,
    inference_ram: Optional[int] = None,
    vram_per_task: Optional[int] = None,
):
    """
    使用提供的參數將多個 PDF 轉換為 markdown。

    參數：
    - in_folder: str
        包含 PDF 文件的輸入資料夾
    - out_folder: str
        儲存 markdown 文件的輸出資料夾
    - chunk_idx: int, optional
        要轉換的區塊索引。預設為 0
    - num_chunks: int, optional
        並行處理的區塊數量。預設為 1
    - max_files: int, optional
        要轉換的 PDF 最大數量。預設為 None（無限制）
    - workers: int, optional
        要使用的工作進程數量。預設為 5
    - metadata_file: str, optional
        用於過濾的中繼資料 JSON 檔案路徑。預設為 None
    - min_length: int, optional
        要轉換的 PDF 最小長度。預設為 None
    """

    in_folder = os.path.abspath(in_folder)
    out_folder = os.path.abspath(out_folder)
    files = [os.path.join(in_folder, f) for f in os.listdir(in_folder)]
    files = [f for f in files if os.path.isfile(f)]
    os.makedirs(out_folder, exist_ok=True)

    # 如果我們正在並行處理，則處理區塊
    # 確保所有文件都進入一個區塊
    chunk_size = math.ceil(len(files) / num_chunks)
    start_idx = chunk_idx * chunk_size
    end_idx = start_idx + chunk_size
    files_to_convert = files[start_idx:end_idx]

    # 如果需要，限制轉換的文件數量
    if max:
        files_to_convert = files_to_convert[:max_files]

    metadata = {}
    if metadata_file:
        metadata_file = os.path.abspath(metadata_file)
        with open(metadata_file, "r") as f:
            metadata = json.load(f)

    total_processes = min(len(files_to_convert), workers)

    # 根據 GPU 記憶體動態設置每個任務的 GPU 分配
    if inference_ram is not None:
        settings.INFERENCE_RAM = inference_ram
    if vram_per_task is not None:
        settings.VRAM_PER_TASK = vram_per_task

    if settings.CUDA:
        tasks_per_gpu = (
            settings.INFERENCE_RAM // settings.VRAM_PER_TASK if settings.CUDA else 0
        )
        total_processes = int(min(tasks_per_gpu, total_processes))
    else:
        total_processes = int(total_processes)

    mp.set_start_method("spawn")  # CUDA 需要，forkserver 不起作用
    model_lst = load_all_models()

    for model in model_lst:
        if model is None:
            continue

        if model.device.type == "mps":
            raise ValueError(
                "無法在 torch 多進程 share_memory 中使用 MPS。您必須使用 CUDA 或 CPU。設置 TORCH_DEVICE 環境變數以更改設備。"
            )

        model.share_memory()

    print(
        f"在區塊 {chunk_idx + 1}/{num_chunks} 中使用 {total_processes} 個進程轉換 {len(files_to_convert)} 個 PDF，並儲存在 {out_folder}"
    )
    task_args = [
        (f, out_folder, metadata.get(os.path.basename(f)), min_length)
        for f in files_to_convert
    ]

    with mp.Pool(
        processes=total_processes, initializer=worker_init, initargs=(model_lst,)
    ) as pool:
        list(
            tqdm(
                pool.imap(process_single_pdf, task_args),
                total=len(task_args),
                desc="處理 PDF 檔案",
                unit="pdf",
            )
        )

        pool._worker_handler.terminate = worker_exit

    # 刪除所有 CUDA 張量
    del model_lst