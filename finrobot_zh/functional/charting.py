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
            str, "股票代碼（例如：'AAPL' 代表蘋果公司）"
        ],
        start_date: Annotated[
            str, "歷史數據的開始日期，格式為 'YYYY-MM-DD'"
        ],
        end_date: Annotated[
            str, "歷史數據的結束日期，格式為 'YYYY-MM-DD'"
        ],
        save_path: Annotated[str, "圖表儲存的檔案路徑"],
        verbose: Annotated[
            str, "是否在控制台打印股票數據。預設為 False"
        ] = False,
        type: Annotated[
            str,
            "圖表類型，可選 'candle', 'ohlc', 'line', 'renko', 'pnf', 'hollow_and_filled'。預設為 'candle'"
        ] = "candle",
        style: Annotated[
            str,
            "圖表風格，可選 'default', 'classic', 'charles', 'yahoo', 'nightclouds', 'sas', 'blueskies', 'mike'。預設為 'default'"
        ] = "default",
        mav: Annotated[
            int | List[int] | Tuple[int, ...] | None,
            "Moving average window(s) to plot on the chart. Default to None"
        ] = None,
        show_nontrading: Annotated[
            bool, "是否在圖表上顯示非交易日。預設為 False"
        ] = False,
    ) -> str:
        """
        使用 mplfinance 為指定的股票和時間段繪製股價圖表，
        並將圖表儲存到檔案。
        """
        # 獲取歷史數據
        stock_data = YFinanceUtils.get_stock_data(ticker_symbol, start_date, end_date)
        if verbose:
            print(stock_data.to_string())

        params = {
            "type": type,
            "style": style,
            "title": f"{ticker_symbol} {type} chart",
            "ylabel": "Price",
            "volume": True,
            "ylabel_lower": "Volume",
            "mav": mav,
            "show_nontrading": show_nontrading,
            "savefig": save_path,
        }
        filtered_params = {k: v for k, v in params.items() if v is not None}

        mpf.plot(stock_data, **filtered_params)

        return f"{type} chart saved to <img {save_path}>"


class ReportChartUtils:

    def get_share_performance(
        ticker_symbol: Annotated[
            str, "股票代碼（例如：'AAPL' 代表蘋果公司）"
        ],
        filing_date: Annotated[str | datetime, "申報日期，格式為 'YYYY-MM-DD'"],
        save_path: Annotated[str, "圖表儲存的檔案路徑"],
    ) -> str:
        """繪製公司過去一年與 S&P 500 的股價表現比較圖。"""
        if isinstance(filing_date, str):
            filing_date = datetime.strptime(filing_date, "%Y-%m-%d")

        def fetch_stock_data(ticker):
            start = (filing_date - timedelta(days=365)).strftime("%Y-%m-%d")
            end = filing_date.strftime("%Y-%m-%d")
            historical_data = YFinanceUtils.get_stock_data(ticker, start, end)
            return historical_data["Close"]

        target_close = fetch_stock_data(ticker_symbol)
        sp500_close = fetch_stock_data("^GSPC")
        info = YFinanceUtils.get_stock_info(ticker_symbol)

        company_change = (
            (target_close - target_close.iloc[0]) / target_close.iloc[0] * 100
        )
        sp500_change = (sp500_close - sp500_close.iloc[0]) / sp500_close.iloc[0] * 100

        start_date = company_change.index.min()
        four_months = start_date + DateOffset(months=4)
        eight_months = start_date + DateOffset(months=8)
        end_date = company_change.index.max()

        plt.rcParams.update({"font.size": 20})
        plt.figure(figsize=(14, 7))
        plt.plot(
            company_change.index,
            company_change,
            label=f'{info["shortName"]} Change %',
            color="blue",
        )
        plt.plot(
            sp500_change.index, sp500_change, label="S&P 500 Change %", color="red"
        )

        plt.title(f'{info["shortName"]} vs S&P 500 - Change % Over the Past Year')
        plt.xlabel("Date")
        plt.ylabel("Change %")

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
        plot_path = (
            f"{save_path}/stock_performance.png"
            if os.path.isdir(save_path)
            else save_path
        )
        plt.savefig(plot_path)
        plt.close()
        return f"Stock performance chart saved to <img {plot_path}>"

    def get_pe_eps_performance(
        ticker_symbol: Annotated[
            str, "股票代碼（例如：'AAPL' 代表蘋果公司）"
        ],
        filing_date: Annotated[str | datetime, "申報日期，格式為 'YYYY-MM-DD'"],
        years: Annotated[int, "要查詢的年數，預設為 4"] = 4,
        save_path: Annotated[str, "圖表儲存的檔案路徑"] = None,
    ) -> str:
        """繪製公司過去 n 年的 PE ratio 和 EPS 表現圖。"""
        if isinstance(filing_date, str):
            filing_date = datetime.strptime(filing_date, "%Y-%m-%d")

        ss = YFinanceUtils.get_income_stmt(ticker_symbol)
        eps = ss.loc["Diluted EPS", :]

        days = round((years + 1) * 365.25)
        start = (filing_date - timedelta(days=days)).strftime("%Y-%m-%d")
        end = filing_date.strftime("%Y-%m-%d")
        historical_data = YFinanceUtils.get_stock_data(ticker_symbol, start, end)

        dates = pd.to_datetime(eps.index[::-1], utc=True)

        results = {}
        for date in dates:
            if date not in historical_data.index:
                close_price = historical_data.asof(date)
            else:
                close_price = historical_data.loc[date]

            results[date] = close_price["Close"]

        pe = [p / e for p, e in zip(results.values(), eps.values[::-1])]
        dates = eps.index[::-1]
        eps = eps.values[::-1]

        info = YFinanceUtils.get_stock_info(ticker_symbol)

        fig, ax1 = plt.subplots(figsize=(14, 7))
        plt.rcParams.update({"font.size": 20})

        color = "tab:blue"
        ax1.set_xlabel("Date")
        ax1.set_ylabel("PE Ratio", color=color)
        ax1.plot(dates, pe, color=color)
        ax1.tick_params(axis="y", labelcolor=color)
        ax1.grid(True)

        ax2 = ax1.twinx()
        color = "tab:red"
        ax2.set_ylabel("EPS", color=color)
        ax2.plot(dates, eps, color=color)
        ax2.tick_params(axis="y", labelcolor=color)

        plt.title(f'{info["shortName"]} PE Ratios and EPS Over the Past {years} Years')
        plt.xticks(rotation=45)

        plt.xticks(dates, [d.strftime("%Y-%m") for d in dates])

        plt.tight_layout()
        plot_path = (
            f"{save_path}/pe_performance.png" if os.path.isdir(save_path) else save_path
        )
        plt.savefig(plot_path)
        plt.close()
        return f"PE performance chart saved to <img {plot_path}>"


if __name__ == "__main__":
    start_date = "2024-03-01"
    end_date = "2024-04-01"
    save_path = "AAPL_candlestick_chart.png"
    MplFinanceUtils.plot_candlestick_chart("AAPL", start_date, end_date, save_path)