# -*- coding: utf-8 -*-
from typing import List
import re
from finrobot.data_source.filings_src.sec_filings import SECExtractor
import concurrent.futures
from functools import partial
from finrobot.data_source.filings_src.prepline_sec_filings.fetch import get_cik_by_ticker
import requests
from finrobot.data_source.filings_src.prepline_sec_filings.fetch import get_filing
import pandas as pd
from datetime import datetime
from langchain.schema import Document


def sec_main(
    ticker: str,
    year: str,
    filing_types: List[str] = ["10-K", "10-Q"],
    include_amends=True,
):
    """
    主要的 SEC 文件處理函數
    
    參數：
        ticker (str): 股票代碼
        year (str): 年份
        filing_types (List[str]): 申報類型列表
        include_amends (bool): 是否包含修正案
    """
    cik = get_cik_by_ticker(ticker)
    rgld_cik = int(cik.lstrip("0"))

    forms = []
    if include_amends:
        for ft in filing_types:
            forms.append(ft)
            forms.append(ft + "/A")

    url = f"https://data.sec.gov/submissions/CIK{cik}.json"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    # 向 URL 發送帶有標頭的 GET 請求
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        json_data = response.json()
    else:
        print(f"錯誤：無法獲取數據。狀態碼：{response.status_code}")

    form_lists = []
    filings = json_data["filings"]
    recent_filings = filings["recent"]
    sec_form_names = []
    for acc_num, form_name, filing_date, report_date in zip(
        recent_filings["accessionNumber"],
        recent_filings["form"],
        recent_filings["filingDate"],
        recent_filings["reportDate"],
    ):
        if form_name in forms and report_date.startswith(str(year)):
            if form_name == "10-Q":
                datetime_obj = datetime.strptime(report_date, "%Y-%m-%d")
                quarter = pd.Timestamp(datetime_obj).quarter
                form_name += str(quarter)
                if form_name in sec_form_names:
                    form_name += "-1"
            no_dashes_acc_num = re.sub("-", "", acc_num)
            form_lists.append(
                {
                    "accession_number": no_dashes_acc_num,
                    "form_name": form_name,
                    "filing_date": filing_date,
                    "report_date": report_date,
                }
            )
            sec_form_names.append(form_name)
    acc_nums_list = [fl["accession_number"] for fl in form_lists]

    get_filing_partial = partial(
        get_filing,
        cik=rgld_cik,
        company="Unstructured Technologies",
        email="support@unstructured.io",
    )
    sec_extractor = SECExtractor(ticker=ticker)
    print("開始爬取")
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        results = executor.map(get_filing_partial, acc_nums_list)
    results_texts = []
    for res in results:
        if res != "":
            results_texts.append(res)
    assert len(results_texts) == len(
        acc_nums_list
    ), f"爬取的文本數量 {len(results_texts)} 與存取編號文本數量 {len(acc_nums_list)} 不匹配"
    print("爬取完成")
    print("開始提取")
    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
        results = executor.map(sec_extractor.get_section_texts_from_text, results_texts)
    section_texts = []
    for res in results:
        section_texts.append(res)
    assert len(section_texts) == len(
        acc_nums_list
    ), f"章節文本數量 {len(section_texts)} 與存取編號文本數量 {len(acc_nums_list)} 不匹配"

    print("提取完成")
    docs = []
    for idx, val in enumerate(form_lists):
        # val['sec_texts'] = section_texts[idx]
        for sec_name, sec_text in section_texts[idx].items():
            val.update({"section_name": sec_name})
            docs.append(Document(page_content=sec_text, metadata=val))
    return docs, sec_form_names
