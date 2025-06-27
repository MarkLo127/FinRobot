# -*- coding: utf-8 -*-
from typing import List
import asyncio
import aiohttp
from collections import defaultdict
from finrobot.data_source.filings_src.prepline_sec_filings.sections import (
    section_string_to_enum,
    validate_section_names,
    SECSection,
)
from finrobot.data_source.filings_src.prepline_sec_filings.sec_document import (
    SECDocument,
    REPORT_TYPES,
    VALID_FILING_TYPES,
)

from finrobot.data_source.filings_src.prepline_sec_filings.fetch import (
    get_form_by_ticker,
    open_form_by_ticker,
    get_filing,
)
import concurrent.futures
import time
from datetime import date
from enum import Enum
import re
import signal
import requests
from typing import Union, Optional
from ratelimit import limits, sleep_and_retry
import os
from unstructured.staging.base import convert_to_isd
from finrobot.data_source.filings_src.prepline_sec_filings.sections import (
    ALL_SECTIONS,
    SECTIONS_10K,
    SECTIONS_10Q,
    SECTIONS_S1,
)
import json

DATE_FORMAT_TOKENS = "%Y-%m-%d"
DEFAULT_BEFORE_DATE = date.today().strftime(DATE_FORMAT_TOKENS)
DEFAULT_AFTER_DATE = date(2000, 1, 1).strftime(DATE_FORMAT_TOKENS)


class timeout:
    def __init__(self, seconds=1, error_message="超時"):
        self.seconds = seconds
        self.error_message = error_message

    def handle_timeout(self, signum, frame):
        raise TimeoutError(self.error_message)

    def __enter__(self):
        signal.signal(signal.SIGALRM, self.handle_timeout)
        signal.alarm(self.seconds)

    def __exit__(self, type, value, traceback):
        signal.alarm(0)


def get_regex_enum(section_regex):
    """將章節正則表達式轉換為枚舉"""
    return section_string_to_enum(section_regex)


class SECExtractor:
    """SEC 文件提取器類別"""

    def __init__(
        self,
        ticker: str,
        filing_type: str = "10-K",
        sections: List[str] = ["BUSINESS", "RISK_FACTORS", "MANAGEMENT_DISCUSSION"],
    ):
        """
        初始化 SEC 提取器
        
        參數：
            ticker (str): 股票代碼
            filing_type (str): 申報類型
            sections (List[str]): 要提取的章節列表
        """
        self.filing_type = filing_type
        self.ticker = ticker
        self.sections = sections

    def get_year(self, filing_details: str) -> str:
        """
        獲取 10-K 的年份和 10-Q 的年份、月份

        參數：
            filing_details (str): 申報 URL

        返回：
            str: 10-K 的年份和 10-Q 的年份、月份
        """
        details = filing_details.split("/")[-1]
        if self.filing_type == "10-K":
            matches = re.findall("20\d{2}", details)
        elif self.filing_type == "10-Q":
            matches = re.findall("20\d{4}", details)

        if matches:
            return matches[-1]  # 返回第一個匹配
        else:
            return None  # 如果沒有找到匹配

    def get_all_text(self, section, all_narratives):
        """
        連接章節中的所有文本

        參數：
            section (str): 章節名稱
            all_narratives (dict): 章節名稱和文本的字典

        返回：
            str: 連接後的文本
        """
        all_texts = []
        for text_dict in all_narratives[section]:
            for key, val in text_dict.items():
                if key == "text":
                    all_texts.append(val)
        return " ".join(all_texts)

    def get_section_texts_from_text(self, text):
        """
        從申報文件文本中獲取文本

        參數：
            text (str): 文件文本

        返回：
            tuple: 所有章節的文本和文件的申報類型
        """
        all_narratives, filing_type = self.pipeline_api(text, m_section=self.sections)
        section_texts = {}
        for section in self.sections:
            if section in all_narratives:
                section_texts[section] = self.get_all_text(section, all_narratives)
        return section_texts

    def pipeline_api(self, text, m_section):
        """
        處理 SEC 文件的管道 API

        參數：
            text (str): 文件文本
            m_section (List[str]): 要提取的章節列表

        返回：
            tuple: 章節敘述和申報類型
        """
        sec_document = SECDocument.from_text(text)
        results = {}
        
        for i, section_regex in enumerate(m_section):
            regex_num = get_regex_enum(section_regex)
            with timeout(seconds=5):
                section_elements = sec_document.get_section_narrative(regex_num)
                results[f"REGEX_{i}"] = section_elements
        
        return {
            section: convert_to_isd(section_narrative)
            for section, section_narrative in results.items()
        }, sec_document.filing_type

    @sleep_and_retry
    @limits(calls=10, period=1)
    def get_filing(self, url: str, company: str, email: str) -> str:
        """
        從 SEC EDGAR 檔案庫獲取指定的申報文件。符合 SEC 網站上指定的速率限制。
        參考：https://www.sec.gov/os/accessing-edgar-data
        """
        session = self._get_session(company, email)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = session.get(url)
        response.raise_for_status()
        return response.text

    def _get_session(
        self, company: Optional[str] = None, email: Optional[str] = None
    ) -> requests.Session:
        """
        創建具有適當標頭設定的請求會話。如果未設定這些標頭，SEC 將拒絕您的請求。
        參考：https://www.sec.gov/os/accessing-edgar-data
        """
        if company is None:
            company = os.environ.get("SEC_API_ORGANIZATION")
        if email is None:
            email = os.environ.get("SEC_API_EMAIL")
        assert company, "需要公司名稱"
        assert email, "需要電子郵件地址"
        session = requests.Session()
        session.headers.update(
            {
                "User-Agent": f"{company} {email}",
                "Content-Type": "text/html",
            }
        )
        return session
