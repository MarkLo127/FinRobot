from tenacity import retry, stop_after_attempt, wait_random_exponential
import requests
import json
from datetime import datetime
import re
from typing import List


def correct_date(yr, dt):
    """部分文字記錄日期有誤，予以更正

    Args:
        yr (int): 實際年份
        dt (datetime): 給定日期

    Returns:
        datetime: 更正後的日期
    """
    dt = datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
    if dt.year != yr:
        dt = dt.replace(year=yr)
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def extract_speakers(cont: str) -> List[str]:
    """擷取發言人清單

    Args:
        cont (str): 文字記錄內容

    Returns:
        List[str]: 發言人清單
    """
    pattern = re.compile(r"\n(.*?):")
    matches = pattern.findall(cont)

    return list(set(matches))


@retry(wait=wait_random_exponential(min=1, max=5), stop=stop_after_attempt(2))
def get_earnings_transcript(quarter: str, ticker: str, year: int):
    """取得財報電話會議記錄

    Args:
        quarter (str)
        ticker (str)
        year (int)
    """
    response = requests.get(
        f"https://discountingcashflows.com/api/transcript/{ticker}/{quarter}/{year}/",
        auth=("user", "pass"),
    )

    resp_text = json.loads(response.text)
    # speakers_list = extract_speakers(resp_text[0]["content"])
    corrected_date = correct_date(resp_text[0]["year"], resp_text[0]["date"])
    resp_text[0]["date"] = corrected_date
    return resp_text[0]