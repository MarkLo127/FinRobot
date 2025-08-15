import os
import mplfinance as mpf
import pandas as pd

from matplotlib import pyplot as plt
from typing import Annotated, List, Tuple
from pandas import DateOffset
from datetime import datetime, timedelta

from ..data_source.yfinance_utils import YFinanceUtils


class MplFinanceUtils:

    def plot_stock_price_chart(
        ticker_symbol: Annotated[
            str, "股票的代碼（例如，蘋果公司為 'AAPL'）"
        ],
        start_date: Annotated[
            str, "歷史資料的開始日期，格式為 'YYYY-MM-DD'"
        ],
        end_date: Annotated[
            str, "歷史資料的結束日期，格式為 'YYYY-MM-DD'"
        ],
        save_path: Annotated[str, "應儲存繪圖的檔案路徑"],
        verbose: Annotated[
            str, "是否將股票資料列印到主控台。預設為 False。"
        ] = False,
        type: Annotated[
            str,
            "繪圖類型，應為 'candle','ohlc','line','renko','pnf','hollow_and_filled' 之一。預設為 'candle'",
        ] = "candle",
        style: Annotated[
            str,
            "繪圖樣式，應為 'default','classic','charles','yahoo','nightclouds','sas','blueskies','mike' 之一。預設為 'default'。",
        ] = "default",
        mav: Annotated[
            int | List[int] | Tuple[int, ...] | None,
            "要在圖表上繪製的移動平均線窗口。預設為 None。",
        ] = None,
        show_nontrading: Annotated[
            bool, "是否在圖表上顯示非交易日。預設為 False。"
        ] = False,
    ) -> str:
        """
        使用 mplfinance 為指定的股票和時間段繪製股價圖，
        並將繪圖儲存到檔案中。
        """
        # 擷取歷史資料
        stock_data = YFinanceUtils.get_stock_data(ticker_symbol, start_date, end_date)
        if verbose:
            print(stock_data.to_string())

        params = {
            "type": type,
            "style": style,
            "title": f"{ticker_symbol} {type} 圖表",
            "ylabel": "價格",
            "volume": True,
            "ylabel_lower": "成交量",
            "mav": mav,
            "show_nontrading": show_nontrading,
            "savefig": save_path,
        }
        # 使用字典推導式篩選掉 None 值（MplFinance 不接受 None 值）
        filtered_params = {k: v for k, v in params.items() if v is not None}

        # 繪製圖表
        mpf.plot(stock_data, **filtered_params)

        return f"{type} 圖表已儲存至 <img {save_path}>"


class ReportChartUtils:

    def get_share_performance(
        ticker_symbol: Annotated[
            str, "股票的代碼（例如，蘋果公司為 'AAPL'）"
        ],
        filing_date: Annotated[str | datetime, "申報日期，格式為 'YYYY-MM-DD'"],
        save_path: Annotated[str, "應儲存繪圖的檔案路徑"],
    ) -> str:
        """繪製一家公司與標準普爾 500 指數在過去一年中的股票表現比較圖。"""
        if isinstance(filing_date, str):
            filing_date = datetime.strptime(filing_date, "%Y-%m-%d")

        def fetch_stock_data(ticker):
            start = (filing_date - timedelta(days=365)).strftime("%Y-%m-%d")
            end = filing_date.strftime("%Y-%m-%d")
            historical_data = YFinanceUtils.get_stock_data(ticker, start, end)
            # hist = stock.history(period=period)
            return historical_data["Close"]

        target_close = fetch_stock_data(ticker_symbol)
        sp500_close = fetch_stock_data("^GSPC")
        info = YFinanceUtils.get_stock_info(ticker_symbol)

        # 計算變化率
        company_change = (
            (target_close - target_close.iloc[0]) / target_close.iloc[0] * 100
        )
        sp500_change = (sp500_close - sp500_close.iloc[0]) / sp500_close.iloc[0] * 100

        # 計算額外的日期點
        start_date = company_change.index.min()
        four_months = start_date + DateOffset(months=4)
        eight_months = start_date + DateOffset(months=8)
        end_date = company_change.index.max()

        # 準備繪圖
        plt.rcParams.update({"font.size": 20})  # 調整為更大的字體大小
        plt.figure(figsize=(14, 7))
        plt.plot(
            company_change.index,
            company_change,
            label=f'{info["shortName']} 變動率 %',
            color="blue",
        )
        plt.plot(
            sp500_change.index, sp500_change, label="S&P 500 變動率 %", color="red"
        )

        # 設定標題和標籤
        plt.title(f'{info["shortName']} vs S&P 500 - 過去一年變動率 %')
        plt.xlabel("日期")
        plt.ylabel("變動率 %")

        # 設定 x 軸刻度標籤
        plt.xticks(
            [start_date, four_months, eight_months, end_date],
            [
                start_date.strftime("%Y-%m"),
                four_months.strftime("%Y-%m"),
                eight_months.strftime("%Y-%m"),
                end_date.strftime("%Y-%m"),
            ],
        )

        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        # plt.show()
        plot_path = (
            f"{save_path}/stock_performance.png"
            if os.path.isdir(save_path)
            else save_path
        )
        plt.savefig(plot_path)
        plt.close()
        return f"去年股價表現圖表已儲存至 <img {plot_path}>"

    def get_pe_eps_performance(
        ticker_symbol: Annotated[
            str, "股票的代碼（例如，蘋果公司為 'AAPL'）"
        ],
        filing_date: Annotated[str | datetime, "申報日期，格式為 'YYYY-MM-DD'"],
        years: Annotated[int, "要搜尋的年數，預設為 4"] = 4,
        save_path: Annotated[str, "應儲存繪圖的檔案路徑"] = None,
    ) -> str:
        """繪製一家公司過去 n 年的本益比和每股盈餘表現圖。"""
        if isinstance(filing_date, str):
            filing_date = datetime.strptime(filing_date, "%Y-%m-%d")

        ss = YFinanceUtils.get_income_stmt(ticker_symbol)
        eps = ss.loc["Diluted EPS", :]

        # 取得過去 5 年的歷史資料
        # historical_data = self.stock.history(period="5y")
        days = round((years + 1) * 365.25)
        start = (filing_date - timedelta(days=days)).strftime("%Y-%m-%d")
        end = filing_date.strftime("%Y-%m-%d")
        historical_data = YFinanceUtils.get_stock_data(ticker_symbol, start, end)

        # 指定的日期，並確保它們都是 UTC 時區的
        dates = pd.to_datetime(eps.index[::-1], utc=True)

        # 為了確保我們能夠找到最接近的股市交易日，我們將轉換日期並尋找最接近的日期
        results = {}
        for date in dates:
            # 如果指定日期不是交易日，使用 bfill 和 ffill 找到最近的交易日股價
            if date not in historical_data.index:
                close_price = historical_data.asof(date)
            else:
                close_price = historical_data.loc[date]

            results[date] = close_price["Close"]

        pe = [p / e for p, e in zip(results.values(), eps.values[::-1])]
        dates = eps.index[::-1]
        eps = eps.values[::-1]

        info = YFinanceUtils.get_stock_info(ticker_symbol)

        # 建立圖形和軸物件
        fig, ax1 = plt.subplots(figsize=(14, 7))
        plt.rcParams.update({"font.size": 20})  # 調整為更大的字體大小

        # 繪製本益比
        color = "tab:blue"
        ax1.set_xlabel("日期")
        ax1.set_ylabel("本益比", color=color)
        ax1.plot(dates, pe, color=color)
        ax1.tick_params(axis="y", labelcolor=color)
        ax1.grid(True)

        # 建立與 ax1 共享 x 軸的第二個軸物件
        ax2 = ax1.twinx()
        color = "tab:red"
        ax2.set_ylabel("每股盈餘", color=color)  # 第二個 y 軸的標籤
        ax2.plot(dates, eps, color=color)
        ax2.tick_params(axis="y", labelcolor=color)

        # 設定標題和 x 軸標籤角度
        plt.title(f'{info["shortName"]} 過去 {years} 年的本益比和每股盈餘')
        plt.xticks(rotation=45)

        # 設定 x 軸刻度標籤
        plt.xticks(dates, [d.strftime("%Y-%m") for d in dates])

        plt.tight_layout()
        # plt.show()
        plot_path = (
            f"{save_path}/pe_performance.png" if os.path.isdir(save_path) else save_path
        )
        plt.savefig(plot_path)
        plt.close()
        return f"本益比表現圖表已儲存至 <img {plot_path}>"


if __name__ == "__main__":
    # 範例用法：
    start_date = "2024-03-01"
    end_date = "2024-04-01"
    save_path = "AAPL_candlestick_chart.png"
    MplFinanceUtils.plot_candlestick_chart("AAPL", start_date, end_date, save_path)