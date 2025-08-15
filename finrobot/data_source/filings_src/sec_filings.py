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
    def __init__(self, seconds=1, error_message="Timeout"):
        self.seconds = seconds
        self.error_message = error_message

    def handle_timeout(self, signum, frame):
        raise TimeoutError(self.error_message)

    def __enter__(self):
        try:
            signal.signal(signal.SIGALRM, self.handle_timeout)
            signal.alarm(self.seconds)
        except ValueError:
            pass

    def __exit__(self, type, value, traceback):
        try:
            signal.alarm(0)
        except ValueError:
            pass


# pipeline-api
def get_regex_enum(section_regex):
    """使用正規表示式取得章節

    Args:
        section_regex (str): 章節名稱的正規表示式

    Returns:
        CustomSECSection.CUSTOM: 自訂正規表示式章節名稱
    """

    class CustomSECSection(Enum):
        CUSTOM = re.compile(section_regex)

        @property
        def pattern(self):
            return self.value

    return CustomSECSection.CUSTOM


class SECExtractor:
    def __init__(self, ticker: str, sections: List[str] = ["_ALL"]):
        """_summary_

        Args:
            tickers (List[str]): 股票代碼清單
            amount (int): 文件數量
            filing_type (str): 10-K 或 10-Q
            start_date (str, optional): 取得檔案的開始日期。預設為 DEFAULT_AFTER_DATE。
            end_date (str, optional): 取得檔案的結束日期。預設為 DEFAULT_BEFORE_DATE。
            sections (List[str], optional): 需要的章節，請檢查章節名稱。預設為 ["_ALL"]。
        """

        self.ticker = ticker
        self.sections = sections

    def get_year(self, filing_details: str) -> str:
        """取得 10-K 的年份和 10-Q 的年份、月份

        Args:
            filing_details (str): 申報文件網址

        Returns:
            str: 10-K 的年份和 10-Q 的年份、月份
        """
        details = filing_details.split("/")[-1]
        if self.filing_type == "10-K":
            matches = re.findall("20\d{2}", details)
        elif self.filing_type == "10-Q":
            matches = re.findall("20\d{4}", details)

        if matches:
            return matches[-1]  # 傳回第一個相符項目
        else:
            return None  # 如果找不到相符項目

    def get_all_text(self, section, all_narratives):
        """將章節中的所有文字合併

        Args:
            section (str): 章節名稱
            all_narratives (dict): 章節名稱和文字的字典

        Returns:
            _type_: _description_
        """
        all_texts = []
        for text_dict in all_narratives[section]:
            for key, val in text_dict.items():
                if key == "text":
                    all_texts.append(val)
        return " ".join(all_texts)

    def get_section_texts_from_text(self, text):
        """從申報文件 URL 取得文字

        Args:
            url (str): url 連結

        Returns:
            _type_: 文件中所有章節的文字和申報類型
        """
        all_narratives, filing_type = self.pipeline_api(text, m_section=self.sections)
        all_narrative_dict = dict.fromkeys(all_narratives.keys())

        for section in all_narratives:
            all_narrative_dict[section] = self.get_all_text(section, all_narratives)

        # return all_narrative_dict, filing_type
        return all_narrative_dict

    def pipeline_api(self, text, m_section=[], m_section_regex=[]):
        """Unsturcured API to get the text

        Args:
            text (str): 從申報文件 URL 取得的文字
            m_section (list, optional): 需要的章節。預設為 []。
            m_section_regex (list, optional): 使用 regex 需要的自訂章節。預設為 []。

        Raises:
            ValueError: 無效的文件名稱
            ValueError: 無效的章節名稱

        Returns:
                章節和對應的文字
        """
        validate_section_names(m_section)

        sec_document = SECDocument.from_string(text)
        if sec_document.filing_type not in VALID_FILING_TYPES:
            raise ValueError(
                f"SEC 文件申報類型 {sec_document.filing_type} 不受支援，"
                f"必須是 {','.join(VALID_FILING_TYPES)} 其中之一"
            )
        results = {}
        if m_section == [ALL_SECTIONS]:
            filing_type = sec_document.filing_type
            if filing_type in REPORT_TYPES:
                if filing_type.startswith("10-K"):
                    m_section = [enum.name for enum in SECTIONS_10K]
                elif filing_type.startswith("10-Q"):
                    m_section = [enum.name for enum in SECTIONS_10Q]
                else:
                    raise ValueError(f"無效的報告類型：{filing_type}")

            else:
                m_section = [enum.name for enum in SECTIONS_S1]
        for section in m_section:
            results[section] = sec_document.get_section_narrative(
                section_string_to_enum[section]
            )

        for i, section_regex in enumerate(m_section_regex):
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
        """從 SEC EDGAR Archives 擷取指定的申報文件。遵循
        SEC 網站上指定的速率限制。
        參考：https://www.sec.gov/os/accessing-edgar-data"""
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
        """建立一個具有適當標頭的 requests session。如果未設定這些標頭，
        SEC 將拒絕您的請求。
        參考：https://www.sec.gov/os/accessing-edgar-data"""
        if company is None:
            company = os.environ.get("SEC_API_ORGANIZATION")
        if email is None:
            email = os.environ.get("SEC_API_EMAIL")
        assert company
        assert email
        session = requests.Session()
        session.headers.update(
            {
                "User-Agent": f"{company} {email}",
                "Content-Type": "text/html",
            }
        )
        return session