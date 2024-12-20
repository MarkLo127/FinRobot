import os
import requests
from sec_api import ExtractorApi, QueryApi, RenderApi
from functools import wraps
from typing import Annotated
from ..utils import SavePathType, decorate_all_methods
from ..data_source import FMPUtils


CACHE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".cache")
PDF_GENERATOR_API = "https://api.sec-api.io/filing-reader"


def init_sec_api(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        global extractor_api, query_api, render_api
        if os.environ.get("SEC_API_KEY") is None:
            print("請設置環境變數 SEC_API_KEY 以使用 SEC API。")
            return None
        else:
            extractor_api = ExtractorApi(os.environ["SEC_API_KEY"])
            query_api = QueryApi(os.environ["SEC_API_KEY"])
            render_api = RenderApi(os.environ["SEC_API_KEY"])
            print("SEC API 已初始化")
            return func(*args, **kwargs)

    return wrapper


@decorate_all_methods(init_sec_api)
class SECUtils:

    def get_filing_metadata(
        ticker: Annotated[str, "股票代碼"],
        start_date: Annotated[
            str, "檔案搜尋範圍的開始日期，格式為 yyyy-mm-dd"
        ],
        end_date: Annotated[
            str, "檔案搜尋範圍的結束日期，格式為 yyyy-mm-dd"
        ],
        form_type: Annotated[str, "申報文件類型，例如 10-K 或 20-F"]
    ):
        """
        在指定時間段內搜尋申報文件，並返回最新一筆的元數據
        """
        query = {
            "query": f'ticker:"{ticker}" AND formType:"{form_type}" AND filedAt:[{start_date} TO {end_date}]',
            "from": 0,
            "size": 10,
            "sort": [{"filedAt": {"order": "desc"}}],
        }
        response = query_api.get_filings(query)
        if response["filings"]:
            return response["filings"][0]
        return None

    def download_filing(
        ticker: Annotated[str, "股票代碼"],
        start_date: Annotated[
            str, "檔案搜尋範圍的開始日期，格式為 yyyy-mm-dd"
        ],
        end_date: Annotated[
            str, "檔案搜尋範圍的結束日期，格式為 yyyy-mm-dd"
        ],
        save_folder: Annotated[
            str, "儲存下載文件的資料夾名稱"
        ],
        form_type: Annotated[str, "申報文件類型，例如 10-K 或 20-F"]
    ) -> str:
        """在指定時間段內下載指定股票代碼的最新申報文件作為 htm 格式。"""
        metadata = SECUtils.get_filing_metadata(ticker, start_date, end_date, form_type)
        if metadata:
            ticker = metadata["ticker"]
            url = metadata["linkToFilingDetails"]

            try:
                date = metadata["filedAt"][:10]
                file_name = date + "_" + metadata["formType"] + "_" + url.split("/")[-1]

                if not os.path.isdir(save_folder):
                    os.makedirs(save_folder)

                file_content = render_api.get_filing(url)
                file_path = os.path.join(save_folder, file_name)
                with open(file_path, "w") as f:
                    f.write(file_content)
                return f"{ticker}：下載成功。已保存至 {file_path}"
            except:
                return f"❌ {ticker}：下載失敗：{url}"
        else:
            return f"找不到 {ticker} 的 {form_type} 申報文件"

    def download_filing_pdf(
        ticker: Annotated[str, "股票代碼"],
        start_date: Annotated[
            str, "檔案搜尋範圍的開始日期，格式為 yyyy-mm-dd"
        ],
        end_date: Annotated[
            str, "檔案搜尋範圍的結束日期，格式為 yyyy-mm-dd"
        ],
        save_folder: Annotated[
            str, "儲存下載 PDF 文件的資料夾名稱"
        ],
        form_type: Annotated[str, "申報文件類型，例如 10-K 或 20-F"]
    ) -> str:
        """在指定時間段內下載指定股票代碼的最新申報文件作為 PDF 格式。"""
        metadata = SECUtils.get_filing_metadata(ticker, start_date, end_date, form_type)
        if metadata:
            ticker = metadata["ticker"]
            filing_url = metadata["linkToFilingDetails"]

            try:
                date = metadata["filedAt"][:10]
                print(filing_url.split("/")[-1])
                file_name = (
                    date
                    + "_"
                    + metadata["formType"].replace("/A", "")
                    + "_"
                    + filing_url.split("/")[-1]
                    + ".pdf"
                )

                if not os.path.isdir(save_folder):
                    os.makedirs(save_folder)

                api_url = f"{PDF_GENERATOR_API}?token={os.environ['SEC_API_KEY']}&type=pdf&url={filing_url}"
                response = requests.get(api_url, stream=True)
                response.raise_for_status()

                file_path = os.path.join(save_folder, file_name)
                with open(file_path, "wb") as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        file.write(chunk)
                return f"{ticker}：下載成功。已保存至 {file_path}"
            except Exception as e:
                return f"❌ {ticker}：下載失敗：{filing_url}, {e}"
        else:
            return f"找不到 {ticker} 的 {form_type} 申報文件"

    def get_filing_section(
        ticker_symbol: Annotated[str, "股票代碼"],
        fyear: Annotated[str, "申報文件的會計年度"],
        section: Annotated[
            str | int,
            "要提取的申報文件章節，須在 [1, 1A, 1B, 2, 3, 4, 5, 6, 7, 7A, 8, 9, 9A, 9B, 10, 11, 12, 13, 14, 15] 之中",
        ],
        report_address: Annotated[
            str,
            "申報文件的 URL，若未指定，將從 FMP API 獲取報告網址",
        ] = None,
        save_path: SavePathType = None,
        form_type: Annotated[str, "申報文件類型，例如 10-K 或 20-F"] = "10-K",
    ) -> str:
        """
        從 SEC API 獲取申報文件的特定章節。
        """
        if isinstance(section, int):
            section = str(section)
        if section not in [
            "1A",
            "1B",
            "7A",
            "9A",
            "9B",
        ] + [str(i) for i in range(1, 16)]:
            raise ValueError(
                "章節必須在 [1, 1A, 1B, 2, 3, 4, 5, 6, 7, 7A, 8, 9, 9A, 9B, 10, 11, 12, 13, 14, 15] 之中"
            )

        if report_address is None:
            report_address = FMPUtils.get_sec_report(ticker_symbol, fyear)
            if report_address.startswith("Link: "):
                report_address = report_address.lstrip("Link: ").split()[0]
            else:
                return report_address  # 除錯資訊

        cache_path = os.path.join(
            CACHE_PATH, f"sec_utils/{ticker_symbol}_{fyear}_{section}_{form_type}.txt"
        )
        if os.path.exists(cache_path):
            with open(cache_path, "r") as f:
                section_text = f.read()
        else:
            section_text = extractor_api.get_section(report_address, section, "text")
            os.makedirs(os.path.dirname(cache_path), exist_ok=True)
            with open(cache_path, "w") as f:
                f.write(section_text)

        if save_path:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            with open(save_path, "w") as f:
                f.write(section_text)

        return section_text
