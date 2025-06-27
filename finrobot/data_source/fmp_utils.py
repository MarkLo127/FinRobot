# -*- coding: utf-8 -*-
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
            print("成功找到 FMP API 金鑰。")
            return func(*args, **kwargs)

    return wrapper


@decorate_all_methods(init_fmp_api)
class FMPUtils:

    def get_target_price(
        ticker_symbol: Annotated[str, "股票代碼"],
        date: Annotated[str, "目標價格的日期，格式為 'yyyy-mm-dd'"],
    ) -> str:
        """獲取給定股票在給定日期的目標價格"""
        # API URL
        url = f"https://financialmodelingprep.com/api/v4/price-target?symbol={ticker_symbol}&apikey={fmp_api_key}"

        # 發送 GET 請求
        price_target = "未提供"
        response = requests.get(url)

        # 確保請求成功
        if response.status_code == 200:
            # 解析 JSON 數據
            data = response.json()
            est = []

            date = datetime.strptime(date, "%Y-%m-%d")
            for tprice in data:
                published_date = datetime.strptime(
                    tprice["publishedDate"].split(" ")[0], "%Y-%m-%d"
                )
                if published_date <= date:
                    est.append(tprice["priceTarget"])
            if len(est) > 0:
                price_target = np.mean(est)

        return str(price_target)

    def get_sec_report(
        ticker_symbol: Annotated[str, "股票代碼"],
        fyear: Annotated[str, "財政年度"],
        form_type: Annotated[
            str, "SEC 表格類型，例如 '10-K'（年度報告）或 '10-Q1'（第一季度報告）"
        ] = "10-K",
    ) -> dict:
        """獲取給定股票和財政年度的 SEC 報告 URL 和申報日期"""
        # 解析表格類型
        if form_type == "10-K":
            form_type_api = "10-K"
        elif form_type.startswith("10-Q"):
            quarter = form_type[4:] if len(form_type) > 4 else "1"
            form_type_api = "10-Q"
        else:
            return {"error": f"不支援的表格類型：{form_type}"}

        # API URL
        url = f"https://financialmodelingprep.com/api/v3/sec_filings/{ticker_symbol}?type={form_type_api}&page=0&apikey={fmp_api_key}"

        # 發送 GET 請求
        response = requests.get(url)

        # 確保請求成功
        if response.status_code == 200:
            # 解析 JSON 數據
            data = response.json()
            if not data:
                return {"error": f"未找到 {ticker_symbol} 的 {form_type} 報告"}

            # 根據財政年度和季度（如適用）過濾結果
            filtered_data = []
            for report in data:
                if form_type == "10-K":
                    # 對於 10-K，檢查財政年度
                    if fyear in report["finalLink"]:
                        filtered_data.append(report)
                elif form_type.startswith("10-Q"):
                    # 對於 10-Q，檢查財政年度和季度
                    if fyear in report["finalLink"]:
                        # 檢查季度
                        if quarter == "1" and "q1" in report["finalLink"].lower():
                            filtered_data.append(report)
                        elif quarter == "2" and "q2" in report["finalLink"].lower():
                            filtered_data.append(report)
                        elif quarter == "3" and "q3" in report["finalLink"].lower():
                            filtered_data.append(report)

            if filtered_data:
                # 返回最新的報告
                latest_report = filtered_data[0]
                return {
                    "url": latest_report["finalLink"],
                    "filing_date": latest_report["fillingDate"],
                }
            else:
                return {"error": f"未找到 {ticker_symbol} 在 {fyear} 年的 {form_type} 報告"}
        else:
            return {"error": f"API 請求失敗，狀態碼：{response.status_code}"}

    def get_competitor_financial_metrics(
        ticker_symbol: Annotated[str, "股票代碼"],
        competitors: Annotated[List[str], "競爭對手的股票代碼列表"],
        years: Annotated[int, "要檢索的年數"] = 3,
    ) -> dict:
        """獲取公司及其競爭對手的財務指標，用於比較分析"""
        # 初始化結果字典
        results = {ticker_symbol: pd.DataFrame()}
        for competitor in competitors:
            results[competitor] = pd.DataFrame()

        # 獲取所有公司的財務指標
        companies = [ticker_symbol] + competitors
        for company in companies:
            # API URL
            url = f"https://financialmodelingprep.com/api/v3/key-metrics/{company}?limit={years}&apikey={fmp_api_key}"

            # 發送 GET 請求
            response = requests.get(url)

            # 確保請求成功
            if response.status_code == 200:
                # 解析 JSON 數據
                data = response.json()
                if not data:
                    print(f"未找到 {company} 的財務指標")
                    continue

                # 提取關鍵指標
                metrics = {}
                for i, year_data in enumerate(data):
                    metrics[f"EBITDA Margin_{i}"] = year_data.get("ebitdaratio", None)
                    metrics[f"EV/EBITDA_{i}"] = year_data.get("enterpriseValueOverEBITDA", None)
                    metrics[f"FCF Conversion_{i}"] = year_data.get("freeCashFlowYield", None)
                    metrics[f"Gross Margin_{i}"] = year_data.get("grossProfitMargin", None)
                    metrics[f"ROIC_{i}"] = year_data.get("roic", None)
                    metrics[f"Revenue_{i}"] = year_data.get("revenue", None)
                    metrics[f"Revenue Growth_{i}"] = year_data.get("revenueGrowth", None)

                # 將指標轉換為 DataFrame
                df = pd.DataFrame(metrics, index=[0]).T
                results[company] = df
            else:
                print(f"API 請求失敗，狀態碼：{response.status_code}")

        return results

    def get_financial_metrics(
        ticker_symbol: Annotated[str, "股票代碼"],
        years: Annotated[int, "要搜索的年數，預設為 4"] = 4
    ) -> pd.DataFrame:
        """獲取給定股票在過去 'years' 年的財務指標"""
        # FMP API 的基本 URL 設定
        base_url = "https://financialmodelingprep.com/api/v3"
        # 創建 DataFrame
        df = pd.DataFrame()

        # 遍歷過去 'years' 年的數據
        for year_offset in range(years):
            # 為每年構建收入報表和比率的 URL
            income_statement_url = f"{base_url}/income-statement/{ticker_symbol}?limit={years}&apikey={fmp_api_key}"
            ratios_url = (
                f"{base_url}/ratios/{ticker_symbol}?limit={years}&apikey={fmp_api_key}"
            )
            key_metrics_url = f"{base_url}/key-metrics/{ticker_symbol}?limit={years}&apikey={fmp_api_key}"

            # 從 API 請求數據
            income_data = requests.get(income_statement_url).json()
            key_metrics_data = requests.get(key_metrics_url).json()
            ratios_data = requests.get(ratios_url).json()

            # 提取每年所需的指標
            if income_data and key_metrics_data and ratios_data:
                metrics = {
                    "營收": round(income_data[year_offset]["revenue"] / 1e6),
                    "營收成長": "{}%".format(round(((income_data[year_offset]["revenue"] - income_data[year_offset - 1]["revenue"]) / income_data[year_offset - 1]["revenue"])*100,1)),
                    "毛利": round(income_data[year_offset]["grossProfit"] / 1e6),
                    "毛利率": round((income_data[year_offset]["grossProfit"] / income_data[year_offset]["revenue"]),2),
                    "EBITDA": round(income_data[year_offset]["ebitda"] / 1e6),
                    "EBITDA 利潤率": round((income_data[year_offset]["ebitdaratio"]),2),
                    "自由現金流": round(key_metrics_data[year_offset]["enterpriseValue"] / key_metrics_data[year_offset]["evToOperatingCashFlow"] / 1e6),
                    "自由現金流轉換率": round(((key_metrics_data[year_offset]["enterpriseValue"] / key_metrics_data[year_offset]["evToOperatingCashFlow"]) / income_data[year_offset]["netIncome"]),2),
                    "投資資本回報率":"{}%".format(round((key_metrics_data[year_offset]["roic"])*100,1)),
                    "企業價值/EBITDA": round((key_metrics_data[year_offset][
                        "enterpriseValueOverEBITDA"
                    ]),2),
                    "本益比": round(ratios_data[year_offset]["priceEarningsRatio"],2),
                    "市淨率": round(key_metrics_data[year_offset]["pbRatio"],2),
                }
                # 將年份和指標附加到 DataFrame
                # 從日期中提取年份
                year = income_data[year_offset]["date"][:4]
                df[year] = pd.Series(metrics)

        df = df.sort_index(axis=1)

        return df

    def get_competitor_financial_metrics(
        ticker_symbol: Annotated[str, "股票代碼"], 
        competitors: Annotated[List[str], "競爭對手股票代碼列表"],  
        years: Annotated[int, "要搜索的年數，預設為 4"] = 4
    ) -> dict:
        """獲取公司及其競爭對手的財務指標。"""
        base_url = "https://financialmodelingprep.com/api/v3"
        all_data = {}

        symbols = [ticker_symbol] + competitors  # 將公司和競爭對手合併為一個列表
    
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
                        "營收成長": (
                            "{}%".format((round(income_data[year_offset]["revenue"] - income_data[year_offset - 1]["revenue"] / income_data[year_offset - 1]["revenue"])*100,1))
                            if year_offset > 0 else None
                        ),
                        "毛利率": round((income_data[year_offset]["grossProfit"] / income_data[year_offset]["revenue"]),2),
                        "EBITDA 利潤率": round((income_data[year_offset]["ebitdaratio"]),2),
                        "自由現金流轉換率": round((
                            key_metrics_data[year_offset]["enterpriseValue"] 
                            / key_metrics_data[year_offset]["evToOperatingCashFlow"] 
                            / income_data[year_offset]["netIncome"]
                            if key_metrics_data[year_offset]["evToOperatingCashFlow"] != 0 else None
                        ),2),
                        "投資資本回報率":"{}%".format(round((key_metrics_data[year_offset]["roic"])*100,1)),
                        "企業價值/EBITDA": round((key_metrics_data[year_offset]["enterpriseValueOverEBITDA"]),2),
                    }

            df = pd.DataFrame.from_dict(metrics, orient='index')
            df = df.sort_index(axis=1)
            all_data[symbol] = df

        return all_data



if __name__ == "__main__":
    from finrobot.utils import register_keys_from_json

    register_keys_from_json("config_api_keys")
    FMPUtils.get_sec_report("NEE", "2024")
