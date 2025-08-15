"""從 SEC EDGAR Archives 擷取資料的模組"""

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
    """從 SEC EDGAR Archives 擷取指定的申報文件。遵循 SEC 網站上指定的速率限制。
    參考：https://www.sec.gov/os/accessing-edgar-data"""

    session = _get_session(company, email)
    return _get_filing(session, cik, accession_number)


@sleep_and_retry
@limits(calls=10, period=1)
def _get_filing(
    session: requests.Session, cik: Union[str, int], accession_number: Union[str, int]
) -> str:
    """包裝後，即可使用現有會話擷取申報文件。"""
    url = archive_url(cik, accession_number)
    # headers = {
    # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    # }
    company = "Indiana-University-Bloomington"
    email = "athecolab@gmail.com"
    headers = {
        "User-Agent": f"{company} {email}",
        "Content-Type": "text/html",
    }
    response = session.get(url, headers=headers)
    response.raise_for_status()
    return response.text


@sleep_and_retry
@limits(calls=2, period=1)
def get_cik_by_ticker(ticker: str) -> str:
    """透過在 SEC 網站上執行搜尋，從股票代碼取得 CIK 號碼。"""
    cik_re = re.compile(r".*CIK=(\d{10}).*")
    url = _search_url(ticker)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    # headers =  {
    # 'authority': 'www.google.com',
    # 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    # 'accept-language': 'en-US,en;q=0.9',
    # 'cache-control': 'max-age=0',
    # 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    # # 視需要新增更多標頭
    # }
    company = "Indiana-University-Bloomington"
    email = "athecolab@gmail.com"
    headers = {
        "User-Agent": f"{company} {email}",
        "Content-Type": "text/html",
    }
    response = requests.get(url, stream=True, headers=headers)
    # response = requests.get(url, headers=headers)
    # response = requests.get(url)
    response.raise_for_status()
    results = cik_re.findall(response.text)
    return str(results[0])


@sleep_and_retry
@limits(calls=10, period=1)
def get_forms_by_cik(session: requests.Session, cik: Union[str, int]) -> dict:
    """取得指定 CIK 號碼的最近 SEC 表格申報字典。"""
    json_name = f"CIK{cik}.json"
    response = session.get(f"{SEC_SUBMISSIONS_URL}/{json_name}")
    response.raise_for_status()
    content = json.loads(response.content)
    recent_forms = content["filings"]["recent"]
    form_types = {
        k: v for k, v in zip(recent_forms["accessionNumber"], recent_forms["form"])
    }
    return form_types


def _get_recent_acc_num_by_cik(
    session: requests.Session, cik: Union[str, int], form_types: List[str]
) -> Tuple[str, str]:
    """傳回指定 CIK 的其中一種指定 form_types (又稱申報類型) 的最新申報的存取號碼和表格類型。"""
    retrieved_form_types = get_forms_by_cik(session, cik)
    for acc_num, form_type_ in retrieved_form_types.items():
        if form_type_ in form_types:
            return _drop_dashes(acc_num), form_type_
    raise ValueError(f"找不到 {cik} 的申報，正在尋找任何：{form_types}")


def get_recent_acc_by_cik(
    cik: str,
    form_type: str,
    company: Optional[str] = None,
    email: Optional[str] = None,
) -> Tuple[str, str]:
    """傳回指定 CIK 和 form_type 的 (accession_number, retrieved_form_type)。
    retrieved_form_type 可能是所要求 form_type 的修訂版本，例如 10-Q 的 10-Q/A。
    """
    session = _get_session(company, email)
    return _get_recent_acc_num_by_cik(session, cik, _form_types(form_type))


def get_recent_cik_and_acc_by_ticker(
    ticker: str,
    form_type: str,
    company: Optional[str] = None,
    email: Optional[str] = None,
) -> Tuple[str, str, str]:
    """傳回指定股票代碼和表格類型的 (cik, accession_number, retrieved_form_type)。
    retrieved_form_type 可能是所要求表格類型的修訂版本，例如 10-Q 的 10-Q/A。
    """
    session = _get_session(company, email)
    cik = get_cik_by_ticker(session, ticker)
    acc_num, retrieved_form_type = _get_recent_acc_num_by_cik(
        session, cik, _form_types(form_type)
    )
    return cik, acc_num, retrieved_form_type


def get_form_by_ticker(
    ticker: str,
    form_type: str,
    allow_amended_filing: Optional[bool] = True,
    company: Optional[str] = None,
    email: Optional[str] = None,
) -> str:
    """對於指定的股票代碼，取得指定表格類型的最新表格。"""
    session = _get_session(company, email)
    cik = get_cik_by_ticker(session, ticker)
    return get_form_by_cik(
        cik,
        form_type,
        allow_amended_filing=allow_amended_filing,
        company=company,
        email=email,
    )


def _form_types(form_type: str, allow_amended_filing: Optional[bool] = True):
    """可能擴展以包含修訂後的申報，例如：
    "10-Q" -> "10-Q/A"
    """
    assert form_type in VALID_FILING_TYPES
    if allow_amended_filing and not form_type.endswith("/A"):
        return [form_type, f"{form_type}/A"]
    else:
        return [form_type]


def get_form_by_cik(
    cik: str,
    form_type: str,
    allow_amended_filing: Optional[bool] = True,
    company: Optional[str] = None,
    email: Optional[str] = None,
) -> str:
    """對於指定的 CIK，傳回指定表格類型的最新表格。預設情況下，
    可以擷取表格類型的修訂版本 (allow_amended_filing=True)。
    例如，如果 form_type 為 "10-Q"，則擷取的表格可以是 10-Q 或 10-Q/A。
    """
    session = _get_session(company, email)
    acc_num, _ = _get_recent_acc_num_by_cik(
        session, cik, _form_types(form_type, allow_amended_filing)
    )
    text = _get_filing(session, cik, acc_num)
    return text


def open_form(cik, acc_num):
    """對於指定的 CIK 和存取號碼，在預設瀏覽器中開啟相關 SEC 表格的索引頁面"""
    acc_num = _drop_dashes(acc_num)
    webbrowser.open_new_tab(
        f"{SEC_ARCHIVE_URL}/{cik}/{acc_num}/{_add_dashes(acc_num)}-index.html"
    )


def open_form_by_ticker(
    ticker: str,
    form_type: str,
    allow_amended_filing: Optional[bool] = True,
    company: Optional[str] = None,
    email: Optional[str] = None,
):
    """對於指定的股票代碼，在預設瀏覽器中開啟指定表格類型的最新表格的索引頁面。"""
    session = _get_session(company, email)
    cik = get_cik_by_ticker(session, ticker)
    acc_num, _ = _get_recent_acc_num_by_cik(
        session, cik, _form_types(form_type, allow_amended_filing)
    )
    open_form(cik, acc_num)


def archive_url(cik: Union[str, int], accession_number: Union[str, int]) -> str:
    """建立 SEC 存取號碼的封存 URL。尋找申報的 .txt 檔案，
    其格式為 {accession_number}.txt。"""
    filename = f"{_add_dashes(accession_number)}.txt"
    accession_number = _drop_dashes(accession_number)
    return f"{SEC_ARCHIVE_URL}/{cik}/{accession_number}/{filename}"


def _search_url(cik: Union[str, int]) -> str:
    search_string = f"CIK={cik}&Find=Search&owner=exclude&action=getcompany"
    url = f"{SEC_SEARCH_URL}?{search_string}"
    return url


def _add_dashes(accession_number: Union[str, int]) -> str:
    """將破折號加回存取號碼中"""
    accession_number = str(accession_number)
    return f"{accession_number[:10]}-{accession_number[10:12]}-{accession_number[12:]}"


def _drop_dashes(accession_number: Union[str, int]) -> str:
    """將存取號碼轉換為無破折號的表示法。"""
    accession_number = str(accession_number).replace("-", "")
    return accession_number.zfill(18)


def _get_session(
    company: Optional[str] = "Indiana-University-Bloomington",
    email: Optional[str] = "athecolab@gmail.com",
) -> requests.Session:
    """建立一個設定了適當標頭的 requests 會話。如果未設定這些標頭，
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