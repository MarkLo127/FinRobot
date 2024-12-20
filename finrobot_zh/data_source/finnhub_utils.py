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
                "請設置環境變數 FINNHUB_API_KEY 以使用 Finnhub API。"
            )
            return None
        else:
            finnhub_client = finnhub.Client(api_key=os.environ["FINNHUB_API_KEY"])
            print("Finnhub 客戶端已初始化")
            return func(*args, **kwargs)

    return wrapper


@decorate_all_methods(init_finnhub_client)
class FinnHubUtils:

    def get_company_profile(symbol: Annotated[str, "股票代碼"]) -> str:
        """
        獲取公司簡介資訊
        """
        profile = finnhub_client.company_profile2(symbol=symbol)
        if not profile:
            return f"無法從 finnhub 找到股票代碼 {symbol} 的公司簡介！"

        formatted_str = (
            "[公司簡介]：\n\n{name} 是 {finnhubIndustry} 產業的領先企業。"
            "自 {ipo} 成立並上市以來，公司已在市場上建立了良好的聲譽，"
            "成為行業中的主要參與者之一。截至今日，{name} 的市值"
            "為 {marketCapitalization:.2f} {currency}，流通股數為 {shareOutstanding:.2f}。"
            "\n\n{name} 主要在 {country} 營運，以 {ticker} 為代碼在 {exchange} 交易。"
            "作為 {finnhubIndustry} 領域的主要力量，公司持續創新並推動"
            "產業進步。"
        ).format(**profile)

        return formatted_str

    def get_company_news(
        symbol: Annotated[str, "股票代碼"],
        start_date: Annotated[
            str,
            "搜尋公司基本財務資訊的開始日期，格式為 yyyy-mm-dd",
        ],
        end_date: Annotated[
            str,
            "搜尋公司基本財務資訊的結束日期，格式為 yyyy-mm-dd",
        ],
        max_news_num: Annotated[
            int, "要返回的最大新聞數量，預設為 10"
        ] = 10,
        save_path: SavePathType = None,
    ) -> pd.DataFrame:
        """
        獲取與指定公司相關的市場新聞
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
        # 如果新聞數量超過最大值，隨機選擇一部分新聞
        if len(news) > max_news_num:
            news = random.choices(news, k=max_news_num)
        news.sort(key=lambda x: x["date"])
        output = pd.DataFrame(news)
        save_output(output, f"公司新聞 {symbol}", save_path=save_path)

        return output
    
    def get_basic_financials_history(
        symbol: Annotated[str, "股票代碼"],
        freq: Annotated[
            str,
            "公司基本財務報告頻率：年度 / 季度",
        ],
        start_date: Annotated[
            str,
            "搜尋公司基本財務資訊的開始日期，格式為 yyyy-mm-dd",
        ],
        end_date: Annotated[
            str,
            "搜尋公司基本財務資訊的結束日期，格式為 yyyy-mm-dd",
        ],
        selected_columns: Annotated[
            list[str] | None,
            "要返回的新聞欄位名稱列表，應從以下選擇：'assetTurnoverTTM'（資產週轉率）, 'bookValue'（帳面價值）, 'cashRatio'（現金比率）, 'currentRatio'（流動比率）, 'ebitPerShare'（每股EBIT）, 'eps'（每股盈餘）, 'ev'（企業價值）, 'fcfMargin'（自由現金流利潤率）, 'fcfPerShareTTM'（每股自由現金流）, 'grossMargin'（毛利率）等",
        ] = None,
        save_path: SavePathType = None,
    ) -> pd.DataFrame:

        if freq not in ["annual", "quarterly"]:
            return f"無效的報告頻率 {freq}。請指定 'annual'（年度）或 'quarterly'（季度）。"

        basic_financials = finnhub_client.company_basic_financials(symbol, "all")
        if not basic_financials["series"]:
            return f"無法從 finnhub 找到股票代碼 {symbol} 的基本財務資訊！請嘗試其他股票代碼。"

        output_dict = defaultdict(dict)
        for metric, value_list in basic_financials["series"][freq].items():
            if selected_columns and metric not in selected_columns:
                continue
            for value in value_list:
                if value["period"] >= start_date and value["period"] <= end_date:
                    output_dict[metric].update({value["period"]: value["v"]})

        financials_output = pd.DataFrame(output_dict)
        financials_output = financials_output.rename_axis(index="date")
        save_output(financials_output, "基本財務資訊", save_path=save_path)

        return financials_output

    def get_basic_financials(
        symbol: Annotated[str, "股票代碼"],
        selected_columns: Annotated[
            list[str] | None,
            "要返回的新聞欄位名稱列表，應從以下選擇：'assetTurnoverTTM'（資產週轉率）, 'bookValue'（帳面價值）等多個財務指標",
        ] = None,
    ) -> str:
        """
        獲取指定公司的最新基本財務資訊
        """
        basic_financials = finnhub_client.company_basic_financials(symbol, "all")
        if not basic_financials["series"]:
            return f"無法從 finnhub 找到股票代碼 {symbol} 的基本財務資訊！請嘗試其他股票代碼。"

        output_dict = basic_financials["metric"]
        for metric, value_list in basic_financials["series"]["quarterly"].items():
            value = value_list[0]
            output_dict.update({metric: value["v"]})

        for k in output_dict.keys():
            if selected_columns and k not in selected_columns:
                output_dict.pop(k)

        return json.dumps(output_dict, indent=2)


if __name__ == "__main__":

    from finrobot_zh.utils import register_keys_from_json

    register_keys_from_json("../../config_api_keys")
    # print(FinnHubUtils.get_company_profile("AAPL"))
    # print(FinnHubUtils.get_basic_financials_history("AAPL", "annual", "2019-01-01", "2021-01-01"))
    print(FinnHubUtils.get_basic_financials("AAPL"))