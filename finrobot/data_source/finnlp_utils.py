# -*- coding: utf-8 -*-
import os
from typing import Annotated
from pandas import DataFrame

from finnlp.data_sources.news.cnbc_streaming import CNBC_Streaming
from finnlp.data_sources.news.yicai_streaming import Yicai_Streaming
from finnlp.data_sources.news.investorplace_streaming import InvestorPlace_Streaming
# from finnlp.data_sources.news.eastmoney_streaming import Eastmoney_Streaming

from finnlp.data_sources.social_media.xueqiu_streaming import Xueqiu_Streaming
from finnlp.data_sources.social_media.stocktwits_streaming import Stocktwits_Streaming
# from finnlp.data_sources.social_media.reddit_streaming import Reddit_Streaming

from finnlp.data_sources.news.sina_finance_date_range import Sina_Finance_Date_Range
from finnlp.data_sources.news.finnhub_date_range import Finnhub_Date_Range

from ..utils import save_output, SavePathType


US_Proxy = {
    "use_proxy": "us_free",
    "max_retry": 5,
    "proxy_pages": 5,
}
CN_Proxy = {
    "use_proxy": "china_free",
    "max_retry": 5,
    "proxy_pages": 5,
}


def streaming_download(streaming, config, tag, keyword, rounds, selected_columns, save_path):
    downloader = streaming(config)
    if hasattr(downloader, 'download_streaming_search'):
        downloader.download_streaming_search(keyword, rounds)
    elif hasattr(downloader, 'download_streaming_stock'):
        downloader.download_streaming_stock(keyword, rounds)
    else:
        downloader.download_streaming_all(rounds)
    # print(downloader.dataframe.columns)
    selected = downloader.dataframe[selected_columns]
    save_output(selected, tag, save_path)
    return selected


def date_range_download(date_range, config, tag, start_date, end_date, stock, selected_columns, save_path):
    downloader = date_range(config)
    if hasattr(downloader, 'download_date_range_stock'):
        downloader.download_date_range_stock(start_date, end_date, stock)
    else:
        downloader.download_date_range_all(start_date, end_date)
    selected = downloader.dataframe[selected_columns]
    save_output(selected, tag, save_path)
    return selected


class FinNLPUtils:

    def cnbc_streaming_download(
        keyword: Annotated[str, "搜尋關鍵字"],
        rounds: Annotated[int, "下載輪數"] = 10,
        selected_columns: Annotated[list, "選定的欄位"] = ["time", "title", "content"],
        save_path: SavePathType = None,
    ) -> DataFrame:
        """
        從 CNBC 串流下載新聞數據
        """
        return streaming_download(
            CNBC_Streaming, US_Proxy, "CNBC 新聞", keyword, rounds, selected_columns, save_path
        )

    def yicai_streaming_download(
        keyword: Annotated[str, "搜尋關鍵字"],
        rounds: Annotated[int, "下載輪數"] = 10,
        selected_columns: Annotated[list, "選定的欄位"] = ["time", "title", "content"],
        save_path: SavePathType = None,
    ) -> DataFrame:
        """
        從第一財經串流下載新聞數據
        """
        return streaming_download(
            Yicai_Streaming, CN_Proxy, "第一財經新聞", keyword, rounds, selected_columns, save_path
        )

    def investorplace_streaming_download(
        keyword: Annotated[str, "搜尋關鍵字"],
        rounds: Annotated[int, "下載輪數"] = 10,
        selected_columns: Annotated[list, "選定的欄位"] = ["time", "title", "content"],
        save_path: SavePathType = None,
    ) -> DataFrame:
        """
        從 InvestorPlace 串流下載新聞數據
        """
        return streaming_download(
            InvestorPlace_Streaming, US_Proxy, "InvestorPlace 新聞", keyword, rounds, selected_columns, save_path
        )

    def xueqiu_streaming_download(
        keyword: Annotated[str, "搜尋關鍵字"],
        rounds: Annotated[int, "下載輪數"] = 10,
        selected_columns: Annotated[list, "選定的欄位"] = ["time", "title", "content"],
        save_path: SavePathType = None,
    ) -> DataFrame:
        """
        從雪球串流下載社交媒體數據
        """
        return streaming_download(
            Xueqiu_Streaming, CN_Proxy, "雪球社交媒體", keyword, rounds, selected_columns, save_path
        )

    def stocktwits_streaming_download(
        keyword: Annotated[str, "搜尋關鍵字"],
        rounds: Annotated[int, "下載輪數"] = 10,
        selected_columns: Annotated[list, "選定的欄位"] = ["time", "title", "content"],
        save_path: SavePathType = None,
    ) -> DataFrame:
        """
        從 StockTwits 串流下載社交媒體數據
        """
        return streaming_download(
            Stocktwits_Streaming, US_Proxy, "StockTwits 社交媒體", keyword, rounds, selected_columns, save_path
        )

    def sina_finance_date_range_download(
        start_date: Annotated[str, "開始日期，格式：YYYY-MM-DD"],
        end_date: Annotated[str, "結束日期，格式：YYYY-MM-DD"],
        stock: Annotated[str, "股票代碼"],
        selected_columns: Annotated[list, "選定的欄位"] = ["time", "title", "content"],
        save_path: SavePathType = None,
    ) -> DataFrame:
        """
        從新浪財經下載指定日期範圍的新聞數據
        """
        return date_range_download(
            Sina_Finance_Date_Range, CN_Proxy, "新浪財經新聞", start_date, end_date, stock, selected_columns, save_path
        )

    def finnhub_date_range_download(
        start_date: Annotated[str, "開始日期，格式：YYYY-MM-DD"],
        end_date: Annotated[str, "結束日期，格式：YYYY-MM-DD"],
        stock: Annotated[str, "股票代碼"],
        selected_columns: Annotated[list, "選定的欄位"] = ["time", "title", "content"],
        save_path: SavePathType = None,
    ) -> DataFrame:
        """
        從 Finnhub 下載指定日期範圍的新聞數據
        """
        return date_range_download(
            Finnhub_Date_Range, US_Proxy, "Finnhub 新聞", start_date, end_date, stock, selected_columns, save_path
        )


# 使用範例
if __name__ == "__main__":
    # 串流下載範例
    # FinNLPUtils.cnbc_streaming_download("Apple", rounds=5, save_path="cnbc_news.csv")
    # FinNLPUtils.yicai_streaming_download("蘋果", rounds=5, save_path="yicai_news.csv")
    # FinNLPUtils.investorplace_streaming_download("AAPL", rounds=5, save_path="investorplace_news.csv")
    # FinNLPUtils.xueqiu_streaming_download("蘋果", rounds=5, save_path="xueqiu_posts.csv")
    # FinNLPUtils.stocktwits_streaming_download("AAPL", rounds=5, save_path="stocktwits_posts.csv")
    
    # 日期範圍下載範例
    # FinNLPUtils.sina_finance_date_range_download("2020-01-01", "2020-06-01", "AAPL", save_path="sina_news.csv")
    # FinNLPUtils.finnhub_date_range_download("2020-01-01", "2020-06-01", "AAPL", save_path="finnhub_news.csv")
    pass
