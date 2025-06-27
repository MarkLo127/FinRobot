# -*- coding: utf-8 -*-
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain.schema import Document
from finrobot.data_source.earnings_calls_src import get_earnings_all_docs
from finrobot.data_source.filings_src import sec_main as unstructured_sec_main
from finrobot.data_source.marker_sec_src.sec_filings_to_pdf import sec_save_pdfs
from finrobot.data_source.marker_sec_src.pdf_to_md import run_marker as run_marker_single
from finrobot.data_source.marker_sec_src.pdf_to_md_parallel import run_marker_mp
from finrobot.data_source.finance_data import get_data
from typing import List, Optional
import os
SAVE_DIR = "output/SEC_EDGAR_FILINGS_MD"


def rag_database_earnings_call(
        ticker: str,
        year: str)->str:
        
        #assert quarter in earnings_call_quarter_vals, "季度應該來自 Q1、Q2、Q3、Q4"
        earnings_docs, earnings_call_quarter_vals, speakers_list_1, speakers_list_2, speakers_list_3, speakers_list_4 = get_data(ticker=ticker,year=year,data_source='earnings_calls')

        emb_fn = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

        text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1024,
        chunk_overlap=100,
        length_function=len,)
        earnings_calls_split_docs = text_splitter.split_documents(earnings_docs)

        earnings_call_db = Chroma.from_documents(earnings_calls_split_docs, emb_fn, persist_directory="./earnings-call-db",collection_name="earnings_call")


        quarter_speaker_dict = {
        "Q1":speakers_list_1,
        "Q2":speakers_list_2,
        "Q3":speakers_list_3,
        "Q4":speakers_list_4}
    
        def query_database_earnings_call(
        question: str,
        quarter: str)->str:
            """此工具將針對給定的問題和季度查詢財報電話會議記錄數據庫，並從財報電話會議中檢索相關文本以及處理相關文件的發言者。此工具有助於回答財報電話會議記錄中的問題。

            參數：
            question (str)：要查詢數據庫以獲取相關文件的問題。
            quarter (str)：問題中討論的財務季度，可能的選項為 Q1、Q2、Q3、Q4
            """
            assert quarter in quarter_speaker_dict.keys(), "季度應該來自 Q1、Q2、Q3、Q4"
            docs = earnings_call_db.similarity_search(question, k=3)
            speakers_list = quarter_speaker_dict[quarter]
            result = ""
            for i, doc in enumerate(docs):
                result += f"\n\n文件 {i+1}：\n"
                result += doc.page_content
                result += f"\n\n發言者：{speakers_list[i]}"
            return result
        
        return query_database_earnings_call


def rag_database_sec_filings(
        ticker: str,
        year: str,
        filing_types: List[str] = ["10-K", "10-Q"],
        include_amends: bool = True,
        data_source: str = 'unstructured',
        batch_processing: bool = False,
        batch_multiplier: Optional[int] = None,
        workers: Optional[int] = None,
        inference_ram: Optional[int] = None,
        vram_per_task: Optional[int] = None,
        num_chunks: int = 1,
        )->str:
        
        if data_source == 'unstructured':
            sec_data, sec_form_names = get_data(ticker=ticker,year=year,filing_types=filing_types,include_amends=include_amends,data_source=data_source)
            
            emb_fn = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

            text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1024,
            chunk_overlap=100,
            length_function=len,)
            sec_filings_split_docs = text_splitter.split_documents(sec_data)

            sec_filings_db = Chroma.from_documents(sec_filings_split_docs, emb_fn, persist_directory="./sec-filings-db",collection_name="sec_filings")
            
            def query_database_sec_filings(
            question: str,
            form_name: str)->str:
                """此工具將針對給定的問題和表格名稱查詢 SEC 文件數據庫，並從 SEC 文件中檢索相關文本。此工具有助於回答 SEC 文件中的問題。

                參數：
                question (str)：要查詢數據庫以獲取相關文件的問題。
                form_name (str)：問題中討論的表格名稱，可能的選項為 10-K、10-Q
                """
                assert form_name in sec_form_names, f"表格名稱應該來自 {sec_form_names}"
                docs = sec_filings_db.similarity_search(question, k=3)
                result = ""
                for i, doc in enumerate(docs):
                    result += f"\n\n文件 {i+1}：\n"
                    result += doc.page_content
                    result += f"\n\n表格名稱：{form_name}"
                return result
            
            return query_database_sec_filings
        
        elif data_source == 'marker_pdf':
            get_data(ticker=ticker,year=year,filing_types=filing_types,include_amends=include_amends,data_source=data_source,batch_processing=batch_processing,batch_multiplier=batch_multiplier,workers=workers,inference_ram=inference_ram,vram_per_task=vram_per_task,num_chunks=num_chunks)
            
            output_ticker_year_path = os.path.join(SAVE_DIR, f"{ticker}-{year}")
            
            md_files = []
            for root, dirs, files in os.walk(output_ticker_year_path):
                for file in files:
                    if file.endswith(".md"):
                        md_files.append(os.path.join(root, file))
            
            headers_to_split_on = [
                ("#", "Header 1"),
                ("##", "Header 2"),
                ("###", "Header 3"),
                ("####", "Header 4"),
            ]
            
            markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
            
            docs = []
            for md_file in md_files:
                with open(md_file, "r") as f:
                    markdown_text = f.read()
                    
                    # 獲取文件名稱
                    file_name = os.path.basename(md_file)
                    
                    # 分割文檔
                    splits = markdown_splitter.split_text(markdown_text)
                    
                    # 添加文件名稱到元數據
                    for split in splits:
                        split.metadata["file_name"] = file_name
                        
                    docs.extend(splits)
            
            # 進一步分割文檔
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1024,
                chunk_overlap=100,
                length_function=len,
            )
            docs = text_splitter.split_documents(docs)
            
            # 創建向量數據庫
            emb_fn = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
            sec_filings_db = Chroma.from_documents(docs, emb_fn, persist_directory="./sec-filings-db",collection_name="sec_filings")
            
            def query_database_sec_filings(
            question: str,
            )->str:
                """此工具將針對給定的問題查詢 SEC 文件數據庫，並從 SEC 文件中檢索相關文本。此工具有助於回答 SEC 文件中的問題。

                參數：
                question (str)：要查詢數據庫以獲取相關文件的問題。
                """
                docs = sec_filings_db.similarity_search(question, k=3)
                result = ""
                for i, doc in enumerate(docs):
                    result += f"\n\n文件 {i+1}：\n"
                    result += doc.page_content
                    result += f"\n\n文件名稱：{doc.metadata['file_name']}"
                    if "Header 1" in doc.metadata:
                        result += f"\n標題 1：{doc.metadata['Header 1']}"
                    if "Header 2" in doc.metadata:
                        result += f"\n標題 2：{doc.metadata['Header 2']}"
                    if "Header 3" in doc.metadata:
                        result += f"\n標題 3：{doc.metadata['Header 3']}"
                    if "Header 4" in doc.metadata:
                        result += f"\n標題 4：{doc.metadata['Header 4']}"
                return result
            
            return query_database_sec_filings
            relevant_section_text = ""
            for section, text in relevant_section_dict.items():
                relevant_section_text += section + ": "
                relevant_section_text += text + "\n\n"
            return relevant_section_text

        return query_database_unstructured_sec, sec_form_names
    
    elif FROM_MARKDOWN:
        sec_data,sec_form_names = get_data(ticker=ticker, year=year,data_source='unstructured',include_amends=True,filing_types=filing_types)
        get_data(ticker=ticker,year=year,data_source='marker_pdf',batch_processing=False,batch_multiplier=1)

        headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
        ]
        markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
        markdown_dir = "output/SEC_EDGAR_FILINGS_MD"
        md_content_list = []
        for md_dirs in os.listdir(os.path.join(markdown_dir,f"{ticker}-{year}")):
            md_file_path = os.path.join(markdown_dir,f"{ticker}-{year}",md_dirs,f"{md_dirs}.md")
            with open(md_file_path, 'r') as file:
                content = file.read()
            md_content_list.append([content,'-'.join(md_dirs.split('-')[-2:])])
        
        sec_markdown_docs = []

        for md_content in md_content_list:
            md_header_splits = markdown_splitter.split_text(md_content[0])
            for md_header_docs in md_header_splits:
                md_header_docs.metadata.update({"filing_type":md_content[1]})
            sec_markdown_docs.extend(md_header_splits)

        sec_filings_md_db = Chroma.from_documents(sec_markdown_docs, emb_fn, persist_directory="./sec-filings-md-db",collection_name="sec_filings_md")

        def query_database_markdown_sec(
            question: str,
            sec_form_name: str)->str:
            """此工具將針對給定的問題和表格名稱查詢 SEC 文件數據庫，並從 SEC 文件中檢索相關文本和章節名稱。此工具有助於回答 SEC 文件中的問題。

            參數：
            question (str)：要查詢數據庫以獲取相關文件的問題。
            sec_form_name (str)：問題中討論的 SEC 表格名稱。可以是 10-K（年度數據）或 10-Q（季度數據）。對於季度數據，可以是 10-Q2 表示第二季度，其他季度類似。
            
           

            返回：
            str：從 SEC 文件中與問題相關的上下文
            """
            assert sec_form_name in sec_form_names, f'搜索表格類型應該在 {sec_form_names} 中'

            relevant_docs = sec_filings_md_db.similarity_search(
            question,
            k=3,
            filter={
            "filing_type":{"$eq":sec_form_name}
            }
            )
   
            relevant_section_text = ""
            for relevant_text in relevant_docs:
                relevant_section_text += relevant_text.page_content + "\n\n"

            return relevant_section_text
        return query_database_markdown_sec, sec_form_names
