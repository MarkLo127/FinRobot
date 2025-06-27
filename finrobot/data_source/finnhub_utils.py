# -*- coding: utf-8 -*-
import os
import finnhub
import pandas as pd
import json
import random
from typing import Annotated
from collections import defaultdict
from functools import wraps
from datetime import datetime
from ..utils import decorate_all_methods, save_output, SavePathType


def init_finnhub_client(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        global finnhub_client
        if os.environ.get("FINNHUB_API_KEY") is None:
            print(
                "請設定環境變數 FINNHUB_API_KEY 以使用 Finnhub API。"
            )
            return None
        else:
            finnhub_client = finnhub.Client(api_key=os.environ["FINNHUB_API_KEY"])
            print("Finnhub 客戶端已初始化")
            return func(*args, **kwargs)

    # wrapper.__annotations__ = func.__annotations__
    return wrapper


@decorate_all_methods(init_finnhub_client)
class FinnHubUtils:

    def get_company_profile(symbol: Annotated[str, "股票代碼"]) -> str:
        """
        取得公司的基本資料資訊
        """
        profile = finnhub_client.company_profile2(symbol=symbol)
        if not profile:
            return f"無法從 finnhub 找到股票代碼 {symbol} 的公司資料！"

        formatted_str = (
            "[公司介紹]：\n\n{name} 是 {finnhubIndustry} 行業的領先企業。"
            "自 {ipo} 年成立並公開上市以來，該公司已確立其作為市場主要參與者之一的聲譽。"
            "截至今日，{name} 的市值為 {marketCapitalization:.2f} {currency}，"
            "流通股數為 {shareOutstanding:.2f} 股。"
            "\n\n{name} 主要在 {country} 營運，在 {exchange} 交易所以股票代碼 {ticker} 交易。"
            "作為 {finnhubIndustry} 領域的主導力量，該公司持續創新並推動行業進步。"
        ).format(**profile)

        return formatted_str

    def get_company_news(
        symbol: Annotated[str, "股票代碼"],
        start_date: Annotated[
            str,
            "搜尋公司基本財務資料的起始日期，格式：yyyy-mm-dd",
        ],
        end_date: Annotated[
            str,
            "搜尋公司基本財務資料的結束日期，格式：yyyy-mm-dd",
        ],
        max_news_num: Annotated[
            int, "返回新聞的最大數量，預設為 10"
        ] = 10,
        save_path: SavePathType = None,
    ) -> pd.DataFrame:
        """
        檢索與指定公司相關的市場新聞
        """
        news = finnhub_client.company_news(symbol, _from=start_date, to=end_date)
        if len(news) == 0:
            print(f"無法從 finnhub 找到股票代碼 {symbol} 的公司新聞！")
        news = [
            {
                "date": datetime.fromtimestamp(n["datetime"]).strftime("%Y%m%d%H%M%S"),
                "headline": n["headline"],
                "summary": n["summary"],
            }
            for n in news
        ]
        # 如果新聞數量超過最大值，隨機選擇子集
        if len(news) > max_news_num:
            news = random.choices(news, k=max_news_num)
        news.sort(key=lambda x: x["date"])
        output = pd.DataFrame(news)
        save_output(output, f"{symbol} 的公司新聞", save_path=save_path)

        return output

    def get_basic_financials_history(
        symbol: Annotated[str, "股票代碼"],
        freq: Annotated[
            str,
            "公司基本財務資料的報告頻率：annual（年度）/ quarterly（季度）",
        ],
        start_date: Annotated[
            str,
            "搜尋公司基本財務資料的起始日期，格式：yyyy-mm-dd",
        ],
        end_date: Annotated[
            str,
            "搜尋公司基本財務資料的結束日期，格式：yyyy-mm-dd",
        ],
        selected_columns: Annotated[
            list[str] | None,
            "要返回的新聞欄位名稱列表，應從以下選項中選擇：'assetTurnoverTTM', 'bookValue', 'cashRatio', 'currentRatio', 'ebitPerShare', 'eps', 'ev', 'fcfMargin', 'fcfPerShareTTM', 'grossMargin', 'inventoryTurnoverTTM', 'longtermDebtTotalAsset', 'longtermDebtTotalCapital', 'longtermDebtTotalEquity', 'netDebtToTotalCapital', 'netDebtToTotalEquity', 'netMargin', 'operatingMargin', 'payoutRatioTTM', 'pb', 'peTTM', 'pfcfTTM', 'pretaxMargin', 'psTTM', 'ptbv', 'quickRatio', 'receivable"
        ] = None,
        save_path: SavePathType = None,
    ) -> pd.DataFrame:

        if freq not in ["annual", "quarterly"]:
            return f"無效的報告頻率 {freq}。請指定 'annual'（年度）或 'quarterly'（季度）。"

        basic_financials = finnhub_client.company_basic_financials(symbol, "all")
        if not basic_financials["series"]:
            return f"無法從 finnhub 找到股票代碼 {symbol} 的基本財務資料！請嘗試不同的股票代碼。"

        output_dict = defaultdict(dict)
        for metric, value_list in basic_financials["series"][freq].items():
            if selected_columns and metric not in selected_columns:
                continue
            for value in value_list:
                if value["period"] >= start_date and value["period"] <= end_date:
                    output_dict[metric].update({value["period"]: value["v"]})

        financials_output = pd.DataFrame(output_dict)
        financials_output = financials_output.rename_axis(index="date")
        save_output(financials_output, "基本財務資料", save_path=save_path)

        return financials_output

    def get_basic_financials(
        symbol: Annotated[str, "股票代碼"],
        selected_columns: Annotated[
            list[str] | None,
            "要返回的新聞欄位名稱列表，應從以下選項中選擇：'assetTurnoverTTM', 'bookValue', 'cashRatio', 'currentRatio', 'ebitPerShare', 'eps', 'ev', 'fcfMargin', 'fcfPerShareTTM', 'grossMargin', 'inventoryTurnoverTTM', 'longtermDebtTotalAsset', 'longtermDebtTotalCapital', 'longtermDebtTotalEquity', 'netDebtToTotalCapital', 'netDebtToTotalEquity', 'netMargin', 'operatingMargin', 'payoutRatioTTM', 'pb', 'peTTM', 'pfcfTTM', 'pretaxMargin', 'psTTM', 'ptbv', 'quickRatio', 'receivable"
        ] = None,
    ) -> str:
        """
        取得指定公司的最新基本財務資料
        """
        basic_financials = finnhub_client.company_basic_financials(symbol, "all")
        if not basic_financials["series"]:
            return f"無法從 finnhub 找到股票代碼 {symbol} 的基本財務資料！請嘗試不同的股票代碼。"

        output_dict = basic_financials["metric"]
        for metric, value_list in basic_financials["series"]["quarterly"].items():
            value = value_list[0]
            output_dict.update({metric: value["v"]})

        for k in output_dict.keys():
            if selected_columns and k not in selected_columns:
                output_dict.pop(k)

        return json.dumps(output_dict, indent=2)


if __name__ == "__main__":

    from finrobot.utils import register_keys_from_json

    register_keys_from_json("../../config_api_keys")
    # print(FinnHubUtils.get_company_profile("AAPL"))
    # print(FinnHubUtils.get_basic_financials_history("AAPL", "annual", "2019-01-01", "2021-01-01"))
    print(FinnHubUtils.get_basic_financials("AAPL"))