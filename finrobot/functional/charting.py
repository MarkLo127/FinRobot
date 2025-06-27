import os
import mplfinance as mpf
import pandas as pd

from matplotlib import pyplot as plt
from matplotlib.font_manager import fontManager
from typing import Annotated, List, Tuple
from pandas import DateOffset
from datetime import datetime, timedelta

from ..data_source.yfinance_utils import YFinanceUtils

# 設定中文字體
font_dir = os.path.join(os.path.dirname(__file__), 'LXGW_WenKai_TC,Noto_Serif_TC')

# 註冊 Noto Serif TC 字體
noto_serif_tc_path = os.path.join(font_dir, 'Noto_Serif_TC', 'static')
fontManager.addfont(os.path.join(noto_serif_tc_path, 'NotoSerifTC-Regular.ttf'))
fontManager.addfont(os.path.join(noto_serif_tc_path, 'NotoSerifTC-Bold.ttf'))

# 註冊 LXGW WenKai TC 字體
lxgw_wenkai_tc_path = os.path.join(font_dir, 'LXGW_WenKai_TC')
fontManager.addfont(os.path.join(lxgw_wenkai_tc_path, 'LXGWWenKaiTC-Regular.ttf'))
fontManager.addfont(os.path.join(lxgw_wenkai_tc_path, 'LXGWWenKaiTC-Bold.ttf'))

# 設置預設字體，可以根據需要更改為 'LXGW WenKai TC'
plt.rcParams['font.family'] = 'Noto Serif TC'
plt.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題


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
            str, "是否在控制台輸出股票數據。預設為 False。"
        ] = False,
        type: Annotated[
            str,
            "圖表類型，可選 'candle'（蠟燭圖）,'ohlc'（開高低收）,'line'（線圖）,'renko'（磚形圖）,'pnf'（點數圖）,'hollow_and_filled'（空心和實心蠟燭圖）。預設為 'candle'。",
        ] = "candle",
        style: Annotated[
            str,
            "圖表風格，可選 'default'（預設）,'classic'（經典）,'charles'（查爾斯）,'yahoo'（雅虎）,'nightclouds'（夜雲）,'sas'（SAS）,'blueskies'（藍天）,'mike'（邁克）。預設為 'default'。",
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
            "title": f"{ticker_symbol} {type} 圖表",
            "ylabel": "價格",
            "volume": True,
            "ylabel_lower": "成交量",
            "mav": mav,
            "show_nontrading": show_nontrading,
            "savefig": save_path,
        }
        # 使用字典推導式過濾掉 None 值（MplFinance 不接受 None 值）
        filtered_params = {k: v for k, v in params.items() if v is not None}

        # 繪製圖表
        mpf.plot(stock_data, **filtered_params)

        return f"{type} 圖表已儲存至 <img {save_path}>"


class ReportChartUtils:

    def get_share_performance(
        ticker_symbol: Annotated[
            str, "股票代碼（例如：'AAPL' 代表蘋果公司）"
        ],
        filing_date: Annotated[str | datetime, "申報日期，格式為 'YYYY-MM-DD'"],
        save_path: Annotated[str, "圖表儲存的檔案路徑"],
    ) -> str:
        """繪製公司股票與標普500指數過去一年的表現比較圖。"""
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
            label=f'{info["shortName"]} 變化百分比',
            color="blue",
        )
        plt.plot(
            sp500_change.index, sp500_change, label="標普500 變化百分比", color="red"
        )

        # 設置標題和標籤
        plt.title(f'{info["shortName"]} 與標普500 - 過去一年變化百分比')
        plt.xlabel("日期")
        plt.ylabel("變化百分比")

        # 設置x軸刻度標籤
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
        return f"過去一年股票表現圖表已儲存至 <img {plot_path}>"

    def get_pe_eps_performance(
        ticker_symbol: Annotated[
            str, "股票代碼（例如：'AAPL' 代表蘋果公司）"
        ],
        filing_date: Annotated[str | datetime, "申報日期，格式為 'YYYY-MM-DD'"],
        years: Annotated[int, "要查詢的年數，預設為 4"] = 4,
        save_path: Annotated[str, "圖表儲存的檔案路徑"] = None,
    ) -> str:
        """繪製公司過去 n 年的本益比和每股盈餘表現圖。"""
        if isinstance(filing_date, str):
            filing_date = datetime.strptime(filing_date, "%Y-%m-%d")

        ss = YFinanceUtils.get_income_stmt(ticker_symbol)
        eps = ss.loc["Diluted EPS", :]

        # 獲取過去幾年的歷史數據
        days = round((years + 1) * 365.25)
        start = (filing_date - timedelta(days=days)).strftime("%Y-%m-%d")
        end = filing_date.strftime("%Y-%m-%d")
        historical_data = YFinanceUtils.get_stock_data(ticker_symbol, start, end)

        # 指定的日期，並確保它們都是UTC時區的
        dates = pd.to_datetime(eps.index[::-1], utc=True)

        # 為了確保我們能夠找到最接近的股市交易日，我們將轉換日期並查找最接近的日期
        results = {}
        for date in dates:
            # 如果指定日期不是交易日，使用bfill和ffill找到最近的交易日股價
            if date not in historical_data.index:
                close_price = historical_data.asof(date)
            else:
                close_price = historical_data.loc[date]

            results[date] = close_price["Close"]

        pe = [p / e for p, e in zip(results.values(), eps.values[::-1])]
        dates = eps.index[::-1]
        eps = eps.values[::-1]

        info = YFinanceUtils.get_stock_info(ticker_symbol)

        # 創建圖形和軸對象
        fig, ax1 = plt.subplots(figsize=(14, 7))
        plt.rcParams.update({"font.size": 20})  # 調整為更大的字體大小

        # 繪製本益比
        color = "tab:blue"
        ax1.set_xlabel("日期")
        ax1.set_ylabel("本益比", color=color)
        ax1.plot(dates, pe, color=color)
        ax1.tick_params(axis="y", labelcolor=color)
        ax1.grid(True)

        # 創建與ax1共享x軸的第二個軸對象
        ax2 = ax1.twinx()
        color = "tab:red"
        ax2.set_ylabel("每股盈餘", color=color)  # 第二個y軸的標籤
        ax2.plot(dates, eps, color=color)
        ax2.tick_params(axis="y", labelcolor=color)

        # 設置標題和x軸標籤角度
        plt.title(f'{info["shortName"]} 過去 {years} 年的本益比和每股盈餘')
        plt.xticks(rotation=45)

        # 設置x軸刻度標籤
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
    # 使用範例：
    start_date = "2024-03-01"
    end_date = "2024-04-01"
    save_path = "AAPL_candlestick_chart.png"
    MplFinanceUtils.plot_candlestick_chart("AAPL", start_date, end_date, save_path)
