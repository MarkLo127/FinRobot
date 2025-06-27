# -*- coding: utf-8 -*-
"""從 SEC EDGAR 檔案庫獲取數據的模組"""

import json
import os
import re
import requests
from typing import List, Optional, Tuple, Union
import sys

if sys.version_info < (3, 8):
    from typing_extensions import Final
else:
    from typing import Final

import webbrowser

from ratelimit import limits, sleep_and_retry

from finrobot.data_source.filings_src.prepline_sec_filings.sec_document import VALID_FILING_TYPES

SEC_ARCHIVE_URL: Final[str] = "https://www.sec.gov/Archives/edgar/data"
SEC_SEARCH_URL: Final[str] = "http://www.sec.gov/cgi-bin/browse-edgar"
SEC_SUBMISSIONS_URL = "https://data.sec.gov/submissions"


def get_filing(
    accession_number: Union[str, int], cik: Union[str, int], company: str, email: str
) -> str:
    """
    從 SEC EDGAR 檔案庫獲取指定的申報文件。符合 SEC 網站上指定的速率限制。
    參考：https://www.sec.gov/os/accessing-edgar-data
    """
    session = _get_session(company, email)
    return _get_filing(session, cik, accession_number)


@sleep_and_retry
@limits(calls=10, period=1)
def _get_filing(
    session: requests.Session, cik: Union[str, int], accession_number: Union[str, int]
) -> str:
    """包裝函數，以便可以使用現有會話檢索申報文件。"""
    url = archive_url(cik, accession_number)
    company = "Indiana-University-Bloomington"
    email = "athecolab@gmail.com"
    headers = {
        "User-Agent": f"{company} {email}",
        "Content-Type": "text/html",
    }
    response = session.get(url, headers=headers)
    response.raise_for_status()
    return response.text


def archive_url(cik: Union[str, int], accession_number: Union[str, int]) -> str:
    """
    構建 SEC 檔案庫 URL
    
    參數：
        cik: 中央索引鍵
        accession_number: 存取編號
        
    返回：
        str: 檔案庫 URL
    """
    return f"{SEC_ARCHIVE_URL}/{cik}/{accession_number}.txt"


def _get_session(company: str, email: str) -> requests.Session:
    """
    創建具有適當標頭設定的請求會話。如果未設定這些標頭，SEC 將拒絕您的請求。
    參考：https://www.sec.gov/os/accessing-edgar-data
    """
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": f"{company} {email}",
            "Content-Type": "text/html",
        }
    )
    return session


def get_cik_by_ticker(ticker: str) -> str:
    """通過在 SEC 網站上運行搜索，從股票代碼獲取 CIK 編號。"""
    cik_re = re.compile(r".*CIK=(\d{10}).*")
    url = _search_url(ticker)
    company = "Indiana-University-Bloomington"
    email = "athecolab@gmail.com"
    headers = {
        "User-Agent": f"{company} {email}",
        "Content-Type": "text/html",
    }
    response = requests.get(url, stream=True, headers=headers)
    response.raise_for_status()
    results = cik_re.findall(response.text)
    if not results:
        raise ValueError(f"找不到股票代碼 {ticker} 的 CIK")
    return str(results[0])


def _search_url(cik: Union[str, int]) -> str:
    """構建 SEC 搜索 URL"""
    search_string = f"CIK={cik}&Find=Search&owner=exclude&action=getcompany"
    url = f"{SEC_SEARCH_URL}?{search_string}"
    return url


def get_form_by_ticker(
    ticker: str,
    form_type: str,
    company: str,
    email: str,
    after_date: str = "2000-01-01",
    before_date: str = None,
    include_amends: bool = True,
) -> List[dict]:
    """
    根據股票代碼獲取表格列表
    
    參數：
        ticker: 股票代碼
        form_type: 表格類型（如 "10-K"）
        company: 公司名稱
        email: 電子郵件地址
        after_date: 開始日期
        before_date: 結束日期
        include_amends: 是否包含修正案
        
    返回：
        List[dict]: 表格信息列表
    """
    if before_date is None:
        before_date = date.today().strftime("%Y-%m-%d")
    
    cik = get_cik_by_ticker(ticker)
    
    # 獲取提交數據
    url = f"{SEC_SUBMISSIONS_URL}/CIK{cik}.json"
    session = _get_session(company, email)
    response = session.get(url)
    response.raise_for_status()
    
    data = response.json()
    filings = data["filings"]["recent"]
    
    forms = []
    for i, form in enumerate(filings["form"]):
        if form == form_type or (include_amends and form == f"{form_type}/A"):
            filing_date = filings["filingDate"][i]
            if after_date <= filing_date <= before_date:
                forms.append({
                    "accessionNumber": filings["accessionNumber"][i],
                    "form": form,
                    "filingDate": filing_date,
                    "reportDate": filings["reportDate"][i],
                })
    
    return forms


def open_form_by_ticker(
    ticker: str,
    form_type: str,
    company: str,
    email: str,
    after_date: str = "2000-01-01",
    before_date: str = None,
    include_amends: bool = True,
):
    """
    在瀏覽器中打開表格
    
    參數：
        ticker: 股票代碼
        form_type: 表格類型
        company: 公司名稱
        email: 電子郵件地址
        after_date: 開始日期
        before_date: 結束日期
        include_amends: 是否包含修正案
    """
    forms = get_form_by_ticker(
        ticker, form_type, company, email, after_date, before_date, include_amends
    )
    
    if not forms:
        print(f"未找到 {ticker} 的 {form_type} 表格")
        return
    
    # 打開最新的表格
    latest_form = forms[0]
    cik = get_cik_by_ticker(ticker)
    accession_number = latest_form["accessionNumber"].replace("-", "")
    url = archive_url(cik, accession_number)
    
    webbrowser.open(url)
    print(f"已在瀏覽器中打開：{url}")
