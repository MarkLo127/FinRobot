# -*- coding: utf-8 -*-
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
            print("請設定環境變數 SEC_API_KEY 以使用 sec_api。")
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

    def get_10k_metadata(
        ticker: Annotated[str, "股票代碼"],
        start_date: Annotated[
            str, "10-K 檔案搜索範圍的開始日期，格式為 yyyy-mm-dd"
        ],
        end_date: Annotated[
            str, "10-K 檔案搜索範圍的結束日期，格式為 yyyy-mm-dd"
        ],
    ):
        """
        在給定時間段內搜索 10-K 申報文件，並返回最新一份的元數據
        """
        query = {
            "query": f'ticker:"{ticker}" AND formType:"10-K" AND filedAt:[{start_date} TO {end_date}]',
            "from": 0,
            "size": 10,
            "sort": [{"filedAt": {"order": "desc"}}],
        }
        filings = query_api.get_filings(query)
        if filings["total"]["value"] == 0:
            print(f"未找到 {ticker} 在 {start_date} 至 {end_date} 期間的 10-K 申報文件。")
            return None
        return filings["filings"][0]

    def get_10k_section(
        ticker: Annotated[str, "股票代碼"],
        fyear: Annotated[str, "10-K 報告的財政年度"],
        section: Annotated[
            str | int,
            "要提取的章節，可以是數字（如 1、7、8）或字母數字組合（如 1A、7A、10A）",
        ],
    ):
        """
        從給定公司的 10-K 報告中提取特定章節
        """
        # 獲取 10-K 申報文件的 URL
        sec_report = FMPUtils.get_sec_report(ticker, fyear, "10-K")
        if not sec_report:
            print(f"未找到 {ticker} 在 {fyear} 年的 10-K 申報文件。")
            return ""

        # 提取章節
        section_text = extractor_api.get_section(sec_report["url"], section)
        return section_text

    def get_10q_section(
        ticker: Annotated[str, "股票代碼"],
        fyear: Annotated[str, "10-Q 報告的財政年度"],
        quarter: Annotated[int, "季度（1、2 或 3）"],
        section: Annotated[
            str | int,
            "要提取的章節，可以是數字（如 1、2）或字母數字組合（如 1A、2A）",
        ],
    ):
        """
        從給定公司的 10-Q 報告中提取特定章節
        """
        # 獲取 10-Q 申報文件的 URL
        sec_report = FMPUtils.get_sec_report(ticker, fyear, f"10-Q{quarter}")
        if not sec_report:
            print(f"未找到 {ticker} 在 {fyear} 年第 {quarter} 季度的 10-Q 申報文件。")
            return ""

        # 提取章節
        section_text = extractor_api.get_section(sec_report["url"], section)
        return section_text

    def get_10k_pdf(
        ticker: Annotated[str, "股票代碼"],
        fyear: Annotated[str, "10-K 報告的財政年度"],
        save_path: SavePathType = None,
    ):
        """
        獲取 10-K 報告的 PDF 版本
        """
        # 獲取 10-K 申報文件的 URL
        sec_report = FMPUtils.get_sec_report(ticker, fyear, "10-K")
        if not sec_report:
            print(f"未找到 {ticker} 在 {fyear} 年的 10-K 申報文件。")
            return None

        # 獲取 PDF
        pdf_url = f"{PDF_GENERATOR_API}?token={os.environ['SEC_API_KEY']}&url={sec_report['url']}"
        response = requests.get(pdf_url)
        if response.status_code != 200:
            print(f"獲取 PDF 失敗，狀態碼：{response.status_code}")
            return None

        # 儲存 PDF
        if save_path:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            with open(save_path, "wb") as f:
                f.write(response.content)
            print(f"PDF 已儲存至 {save_path}")

        return response.content

    def get_10q_pdf(
        ticker: Annotated[str, "股票代碼"],
        fyear: Annotated[str, "10-Q 報告的財政年度"],
        quarter: Annotated[int, "季度（1、2 或 3）"],
        save_path: SavePathType = None,
    ):
        """
        獲取 10-Q 報告的 PDF 版本
        """
        # 獲取 10-Q 申報文件的 URL
        sec_report = FMPUtils.get_sec_report(ticker, fyear, f"10-Q{quarter}")
        if not sec_report:
            print(f"未找到 {ticker} 在 {fyear} 年第 {quarter} 季度的 10-Q 申報文件。")
            return None

        # 獲取 PDF
        pdf_url = f"{PDF_GENERATOR_API}?token={os.environ['SEC_API_KEY']}&url={sec_report['url']}"
        response = requests.get(pdf_url)
        if response.status_code != 200:
            print(f"獲取 PDF 失敗，狀態碼：{response.status_code}")
            return None

        # 儲存 PDF
        if save_path:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            with open(save_path, "wb") as f:
                f.write(response.content)
            print(f"PDF 已儲存至 {save_path}")

        return response.content

    def get_section(
        ticker_symbol: Annotated[str, "股票代碼"],
        fyear: Annotated[str, "10-K 報告的財政年度"],
        section: Annotated[
            str | int,
            "要提取的章節，可以是數字（如 1、7、8）或字母數字組合（如 1A、7A、10A）",
        ],
        report_address: Annotated[str | None, "報告的 URL，如果為 None，則會自動獲取"] = None,
        save_path: SavePathType = None,
    ) -> str:
        """
        從 SEC API 獲取 10-K 報告的特定章節。
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
                "章節必須在 [1, 1A, 1B, 2, 3, 4, 5, 6, 7, 7A, 8, 9, 9A, 9B, 10, 11, 12, 13, 14, 15] 中"
            )

        # os.makedirs(f"{self.project_dir}/10k", exist_ok=True)

        # report_name = f"{self.project_dir}/10k/section_{section}.txt"

        # if USE_CACHE and os.path.exists(report_name):
        #     with open(report_name, "r") as f:
        #         section_text = f.read()
        # else:
        if report_address is None:
            report_address = FMPUtils.get_sec_report(ticker_symbol, fyear)
            if report_address.startswith("Link: "):
                report_address = report_address.lstrip("Link: ").split()[0]
            else:
                return report_address  # 調試信息

        cache_path = os.path.join(
            CACHE_PATH, f"sec_utils/{ticker_symbol}_{fyear}_{section}.txt"
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
