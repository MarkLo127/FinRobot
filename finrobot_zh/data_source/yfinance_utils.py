import yfinance as yf
from typing import Annotated, Callable, Any, Optional
from pandas import DataFrame
from functools import wraps

from ..utils import save_output, SavePathType, decorate_all_methods


def init_ticker(func: Callable) -> Callable:
    """裝飾器用於初始化 yf.Ticker 並將其傳遞給函數。"""

    @wraps(func)
    def wrapper(symbol: Annotated[str, "股票代碼"], *args, **kwargs) -> Any:
        ticker = yf.Ticker(symbol)
        return func(ticker, *args, **kwargs)

    return wrapper


@decorate_all_methods(init_ticker)
class YFinanceUtils:

    def get_stock_data(
        symbol: Annotated[str, "股票代碼"],
        start_date: Annotated[
            str, "獲取股價資料的開始日期，格式為 YYYY-mm-dd"
        ],
        end_date: Annotated[
            str, "獲取股價資料的結束日期，格式為 YYYY-mm-dd"
        ],
        save_path: SavePathType = None,
    ) -> DataFrame:
        """獲取指定股票代碼的股價資料"""
        ticker = symbol
        stock_data = ticker.history(start=start_date, end=end_date)
        save_output(stock_data, f"股票 {ticker.ticker} 的股價資料", save_path)
        return stock_data

    def get_stock_info(
        symbol: Annotated[str, "股票代碼"],
    ) -> dict:
        """獲取並返回最新的股票資訊。"""
        ticker = symbol
        stock_info = ticker.info
        return stock_info

    def get_company_info(
        symbol: Annotated[str, "股票代碼"],
        save_path: Optional[str] = None,
    ) -> DataFrame:
        """獲取並以 DataFrame 格式返回公司資訊。"""
        ticker = symbol
        info = ticker.info
        company_info = {
            "公司名稱": info.get("shortName", "不適用"),
            "產業": info.get("industry", "不適用"),
            "產業類別": info.get("sector", "不適用"),
            "國家": info.get("country", "不適用"),
            "網站": info.get("website", "不適用"),
        }
        company_info_df = DataFrame([company_info])
        if save_path:
            company_info_df.to_csv(save_path)
            print(f"已將 {ticker.ticker} 的公司資訊儲存至 {save_path}")
        return company_info_df

    def get_stock_dividends(
        symbol: Annotated[str, "股票代碼"],
        save_path: Optional[str] = None,
    ) -> DataFrame:
        """獲取並以 DataFrame 格式返回最新的股息資料。"""
        ticker = symbol
        dividends = ticker.dividends
        if save_path:
            dividends.to_csv(save_path)
            print(f"已將 {ticker.ticker} 的股息資料儲存至 {save_path}")
        return dividends

    def get_income_stmt(symbol: Annotated[str, "股票代碼"]) -> DataFrame:
        """獲取並以 DataFrame 格式返回公司最新的損益表。"""
        ticker = symbol
        income_stmt = ticker.financials
        return income_stmt

    def get_balance_sheet(symbol: Annotated[str, "股票代碼"]) -> DataFrame:
        """獲取並以 DataFrame 格式返回公司最新的資產負債表。"""
        ticker = symbol
        balance_sheet = ticker.balance_sheet
        return balance_sheet

    def get_cash_flow(symbol: Annotated[str, "股票代碼"]) -> DataFrame:
        """獲取並以 DataFrame 格式返回公司最新的現金流量表。"""
        ticker = symbol
        cash_flow = ticker.cashflow
        return cash_flow

    def get_analyst_recommendations(symbol: Annotated[str, "股票代碼"]) -> tuple:
        """獲取最新的分析師建議，並返回最常見的建議及其計數。"""
        ticker = symbol
        recommendations = ticker.recommendations
        if recommendations.empty:
            return None, 0  # 無可用建議

        # 假設存在 'period' 欄位且需要排除
        row_0 = recommendations.iloc[0, 1:]  # 排除 'period' 欄位（如果需要）

        # 找出最高票數的結果
        max_votes = row_0.max()
        majority_voting_result = row_0[row_0 == max_votes].index.tolist()

        return majority_voting_result[0], max_votes


if __name__ == "__main__":
    print(YFinanceUtils.get_stock_data("AAPL", "2021-01-01", "2021-12-31"))
    # print(YFinanceUtils.get_stock_data())