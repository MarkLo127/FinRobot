import os
import requests
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from ..utils import decorate_all_methods, get_next_weekday

# from finrobot.utils import decorate_all_methods, get_next_weekday
from functools import wraps
from typing import Annotated, List


def init_fmp_api(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        global fmp_api_key
        if os.environ.get("FMP_API_KEY") is None:
            print("請設定環境變數 FMP_API_KEY 以使用 FMP API。")
            return None
        else:
            fmp_api_key = os.environ["FMP_API_KEY"]
            print("已成功找到 FMP API 金鑰。")
            return func(*args, **kwargs)

    return wrapper


@decorate_all_methods(init_fmp_api)
class FMPUtils:

    def get_target_price(
        ticker_symbol: Annotated[str, "股票代碼"],
        date: Annotated[str, "目標價的日期，應為 'yyyy-mm-dd'"],
    ) -> str:
        """取得指定股票在指定日期的目標價"""
        # API URL
        url = f"https://financialmodelingprep.com/api/v4/price-target?symbol={ticker_symbol}&apikey={fmp_api_key}"

        # 發送GET請求
        price_target = "未提供"
        response = requests.get(url)

        # 確保請求成功
        if response.status_code == 200:
            # 解析JSON資料
            data = response.json()
            est = []

            date = datetime.strptime(date, "%Y-%m-%d")
            for tprice in data:
                tdate = tprice["publishedDate"].split("T")[0]
                tdate = datetime.strptime(tdate, "%Y-%m-%d")
                if abs((tdate - date).days) <= 999:
                    est.append(tprice["priceTarget"])

            if est:
                price_target = f"{np.min(est)} - {np.max(est)} (中位數 {np.median(est)})"
            else:
                price_target = "N/A"
        else:
            return f"擷取資料失敗：{response.status_code}"

        return price_target

    def get_sec_report(
        ticker_symbol: Annotated[str, "股票代碼"],
        fyear: Annotated[
            str,
            "10-K 報告的年份，應為 'yyyy' 或 'latest'。預設為 'latest'",
        ] = "latest",
    ) -> str:
        """取得指定股票和年份的 10-K 報告的網址和申報日期"""

        url = f"https://financialmodelingprep.com/api/v3/sec_filings/{ticker_symbol}?type=10-k&page=0&apikey={fmp_api_key}"

        # 發送GET請求
        filing_url = None
        response = requests.get(url)

        # 確保請求成功
        if response.status_code == 200:
            # 解析JSON資料
            data = response.json()
            # print(data)
            if fyear == "latest":
                filing_url = data[0]["finalLink"]
                filing_date = data[0]["fillingDate"]
            else:
                for filing in data:
                    if filing["fillingDate"].split("-")[0] == fyear:
                        filing_url = filing["finalLink"]
                        filing_date = filing["fillingDate"]
                        break

            return f"連結：{filing_url}\n申報日期：{filing_date}"
        else:
            return f"擷取資料失敗：{response.status_code}"

    def get_historical_market_cap(
        ticker_symbol: Annotated[str, "股票代碼"],
        date: Annotated[str, "市值的日期，應為 'yyyy-mm-dd'"],
    ) -> str:
        """取得指定股票在指定日期的歷史市值"""
        date = get_next_weekday(date).strftime("%Y-%m-%d")
        url = f"https://financialmodelingprep.com/api/v3/historical-market-capitalization/{ticker_symbol}?limit=100&from={date}&to={date}&apikey={fmp_api_key}"

        # 發送GET請求
        mkt_cap = None
        response = requests.get(url)

        # 確保請求成功
        if response.status_code == 200:
            # 解析JSON資料
            data = response.json()
            mkt_cap = data[0]["marketCap"]
            return mkt_cap
        else:
            return f"擷取資料失敗：{response.status_code}"

    def get_historical_bvps(
        ticker_symbol: Annotated[str, "股票代碼"],
        target_date: Annotated[str, "BVPS 的日期，應為 'yyyy-mm-dd'"],
    ) -> str:
        """取得指定股票在指定日期的歷史每股帳面價值"""
        # 從FMP API取得歷史關鍵財務指標資料
        url = f"https://financialmodelingprep.com/api/v3/key-metrics/{ticker_symbol}?limit=40&apikey={fmp_api_key}"
        response = requests.get(url)
        data = response.json()

        if not data:
            return "無可用資料"

        # 找到最接近目標日期的資料
        closest_data = None
        min_date_diff = float("inf")
        target_date = datetime.strptime(target_date, "%Y-%m-%d")
        for entry in data:
            date_of_data = datetime.strptime(entry["date"], "%Y-%m-%d")
            date_diff = abs(target_date - date_of_data).days
            if date_diff < min_date_diff:
                min_date_diff = date_diff
                closest_data = entry

        if closest_data:
            return closest_data.get("bookValuePerShare", "無 BVPS 資料可用")
        else:
            return "找不到接近日期的資料"
        
    def get_financial_metrics(
        ticker_symbol: Annotated[str, "股票代碼"],
        years: Annotated[int, "要搜尋的年數，預設為 4"] = 4
    ) -> pd.DataFrame:
        """取得指定股票過去「年」年的財務指標"""
        # FMP API 的基本 URL 設定
        base_url = "https://financialmodelingprep.com/api/v3"
        # 建立 DataFrame
        df = pd.DataFrame()

        # 迭代過去「年」年的資料
        for year_offset in range(years):
            # 為每年建構損益表和比率的 URL
            income_statement_url = f"{base_url}/income-statement/{ticker_symbol}?limit={years}&apikey={fmp_api_key}"
            ratios_url = (
                f"{base_url}/ratios/{ticker_symbol}?limit={years}&apikey={fmp_api_key}"
            )
            key_metrics_url = f"{base_url}/key-metrics/{ticker_symbol}?limit={years}&apikey={fmp_api_key}"

            # 從 API 請求資料
            income_data = requests.get(income_statement_url).json()
            key_metrics_data = requests.get(key_metrics_url).json()
            ratios_data = requests.get(ratios_url).json()

            # 擷取每年所需的指標
            if income_data and key_metrics_data and ratios_data:
                metrics = {
                    "營收": round(income_data[year_offset]["revenue"] / 1e6),
                    "營收成長率": "{}%".format(round(((income_data[year_offset]["revenue"] - income_data[year_offset - 1]["revenue"]) / income_data[year_offset - 1]["revenue"])*100,1)),
                    "毛利": round(income_data[year_offset]["grossProfit"] / 1e6),
                    "毛利率": round((income_data[year_offset]["grossProfit"] / income_data[year_offset]["revenue"]),2),
                    "EBITDA": round(income_data[year_offset]["ebitda"] / 1e6),
                    "EBITDA 利率": round((income_data[year_offset]["ebitdaratio"]),2),
                    "自由現金流": round(key_metrics_data[year_offset]["enterpriseValue"] / key_metrics_data[year_offset]["evToOperatingCashFlow"] / 1e6),
                    "自由現金流轉換率": round(((key_metrics_data[year_offset]["enterpriseValue"] / key_metrics_data[year_offset]["evToOperatingCashFlow"]) / income_data[year_offset]["netIncome"]),2),
                    "ROIC":"{}%".format(round((key_metrics_data[year_offset]["roic"])*100,1)),
                    "EV/EBITDA": round((key_metrics_data[year_offset][
                        "enterpriseValueOverEBITDA"
                    ]),2),
                    "本益比": round(ratios_data[year_offset]["priceEarningsRatio"],2),
                    "股價淨值比": round(key_metrics_data[year_offset]["pbRatio"],2),
                }
                # 將年份和指標附加到 DataFrame
                # 從日期中擷取年份
                year = income_data[year_offset]["date"][:4]
                df[year] = pd.Series(metrics)

        df = df.sort_index(axis=1)

        return df

    def get_competitor_financial_metrics(
        ticker_symbol: Annotated[str, "股票代碼"], 
        competitors: Annotated[List[str], "競爭對手股票代碼清單"],  
        years: Annotated[int, "要搜尋的年數，預設為 4"] = 4
    ) -> dict:
        """取得公司及其競爭對手的財務指標。"""
        base_url = "https://financialmodelingprep.com/api/v3"
        all_data = {}

        symbols = [ticker_symbol] + competitors  # 將公司和競爭對手合併到一個清單中
    
        for symbol in symbols:
            income_statement_url = f"{base_url}/income-statement/{symbol}?limit={years}&apikey={fmp_api_key}"
            ratios_url = f"{base_url}/ratios/{symbol}?limit={years}&apikey={fmp_api_key}"
            key_metrics_url = f"{base_url}/key-metrics/{symbol}?limit={years}&apikey={fmp_api_key}"

            income_data = requests.get(income_statement_url).json()
            ratios_data = requests.get(ratios_url).json()
            key_metrics_data = requests.get(key_metrics_url).json()

            metrics = {}

            if income_data and ratios_data and key_metrics_data:
                for year_offset in range(years):
                    metrics[year_offset] = {
                        "營收": round(income_data[year_offset]["revenue"] / 1e6),
                        "營收成長率": (
                            "{}%".format((round(income_data[year_offset]["revenue"] - income_data[year_offset - 1]["revenue"] / income_data[year_offset - 1]["revenue"])*100,1))
                            if year_offset > 0 else None
                        ),
                        "毛利率": round((income_data[year_offset]["grossProfit"] / income_data[year_offset]["revenue"]),2),
                        "EBITDA 利率": round((income_data[year_offset]["ebitdaratio"]),2),
                        "自由現金流轉換率": round((
                            key_metrics_data[year_offset]["enterpriseValue"] 
                            / key_metrics_data[year_offset]["evToOperatingCashFlow"] 
                            / income_data[year_offset]["netIncome"]
                            if key_metrics_data[year_offset]["evToOperatingCashFlow"] != 0 else None
                        ),2),
                        "ROIC":"{}%".format(round((key_metrics_data[year_offset]["roic"])*100,1)),
                        "EV/EBITDA": round((key_metrics_data[year_offset]["enterpriseValueOverEBITDA"]),2),
                    }

            df = pd.DataFrame.from_dict(metrics, orient='index')
            df = df.sort_index(axis=1)
            all_data[symbol] = df

        return all_data



if __name__ == "__main__":
    from finrobot.utils import register_keys_from_json

    register_keys_from_json("config_api_keys")
    FMPUtils.get_sec_report("NEE", "2024")