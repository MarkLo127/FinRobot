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
    selected = downloader.dataframe[selected_columns]
    save_output(selected, tag, save_path)
    return selected


def date_range_download(date_range, config, tag, start_date, end_date, stock, selected_columns, save_path):
    downloader = date_range(config)
    if hasattr(downloader, 'download_date_range_stock'):
        downloader.download_date_range_stock(start_date, end_date, stock)
    else:
        downloader.download_date_range_all(start_date, end_date)
    if hasattr(downloader, 'gather_content'):
        downloader.gather_content()
    selected_news = downloader.dataframe[selected_columns]
    save_output(selected_news, tag, save_path)
    return selected_news


class FinNLPUtils:

    """
    串流新聞下載
    """

    def cnbc_news_download(
            keyword: Annotated[str, "在新聞串流中搜尋的關鍵字"],
            rounds: Annotated[int, "搜尋的輪數。預設為 1"] = 1,
            selected_columns: Annotated[list[str], "要返回的新聞欄位名稱列表，應從各種新聞屬性中選擇。預設為 ['author', 'datePublished', 'description' ,'section', 'cn:title', 'summary']"] = ["author", "datePublished", "description" ,"section", "cn:title", "summary"],
            save_path: SavePathType = None
        ) -> DataFrame:
        return streaming_download(CNBC_Streaming, {}, "CNBC 新聞", keyword, rounds, selected_columns, save_path)
    
    def yicai_news_download(
            keyword: Annotated[str, "在新聞串流中搜尋的關鍵字"],
            rounds: Annotated[int, "搜尋的輪數。預設為 1"] = 1,
            selected_columns: Annotated[list[str], "要返回的新聞欄位名稱列表，應從各種新聞屬性中選擇。預設為 ['author', 'creationDate', 'desc' ,'source', 'title']"] = ["author", "creationDate", "desc" ,"source", "title"],
            save_path: SavePathType = None
        ) -> DataFrame:
        return streaming_download(Yicai_Streaming, {}, "第一財經新聞", keyword, rounds, selected_columns, save_path)


    def investor_place_news_download(
            keyword: Annotated[str, "在新聞串流中搜尋的關鍵字"],
            rounds: Annotated[int, "搜尋的輪數。預設為 1"] = 1,
            selected_columns: Annotated[list[str], "要返回的新聞欄位名稱列表，應從新聞屬性中選擇。預設為 ['title', 'time', 'author', 'summary']"] = ['title', 'time', 'author', 'summary'],
            save_path: SavePathType = None
        ) -> DataFrame:
        return streaming_download(InvestorPlace_Streaming, {}, "Investor Place 新聞", keyword, rounds, selected_columns, save_path)


    """
    日期範圍新聞下載
    """

    def sina_finance_news_download(
            start_date: Annotated[str, "要獲取新聞的開始日期，格式為 YYYY-mm-dd"],
            end_date: Annotated[str, "要獲取新聞的結束日期，格式為 YYYY-mm-dd"],
            selected_columns: Annotated[list[str], """
                要返回的新聞欄位名稱列表，應從以下選擇：
                'mediaid'（媒體ID）, 'productid'（產品ID）, 'summary'（摘要）, 
                'ctime'（建立時間）, 'url'（網址）, 'author'（作者）等多個欄位。
                預設為 ['title', 'author', 'content']
                """
            ] = ['title', 'author', 'content'],
            save_path: SavePathType = None
        ) -> DataFrame:
        return date_range_download(Sina_Finance_Date_Range, {}, "新浪財經新聞", start_date, end_date, None, selected_columns, save_path)


    def finnhub_news_download(
            start_date: Annotated[str, "要獲取新聞的開始日期，格式為 YYYY-mm-dd"],
            end_date: Annotated[str, "要獲取新聞的結束日期，格式為 YYYY-mm-dd"],
            stock: Annotated[str, "股票代碼，例如 AAPL"],
            selected_columns: Annotated[list[str], "要返回的新聞欄位名稱列表，應從新聞屬性中選擇。預設為 ['headline', 'datetime', 'source', 'summary']"] = ['headline', 'datetime', 'source', 'summary'],
            save_path: SavePathType = None
        ) -> DataFrame:
        return date_range_download(Finnhub_Date_Range, {"token": os.environ['FINNHUB_API_KEY']}, "Finnhub 新聞", start_date, end_date, stock, selected_columns, save_path)

    """
    社交媒體資料
    """
    def xueqiu_social_media_download(
            stock: Annotated[str, "股票代碼，例如 'AAPL'"],
            rounds: Annotated[int, "搜尋的輪數。預設為 1"] = 1,
            selected_columns: Annotated[list[str], """
                要返回的新聞欄位名稱列表，應從多個社交媒體屬性中選擇，
                包括發文時間、內容描述、標題、正文等多個屬性。
                預設為 ['created_at', 'description', 'title', 'text', 'target', 'source']
            """] = ['created_at', 'description', 'title', 'text', 'target', 'source'],
            save_path: SavePathType = None
        ) -> DataFrame:
        return streaming_download(Xueqiu_Streaming, {}, "雪球社交媒體", stock, rounds, selected_columns, save_path)

    def stocktwits_social_media_download(
            stock: Annotated[str, "股票代碼，例如 'AAPL'"],
            rounds: Annotated[int, "搜尋的輪數。預設為 1"] = 1,
            selected_columns: Annotated[list[str], """
                要返回的新聞欄位名稱列表，應從社交媒體屬性中選擇，
                包括發文時間、內容等多個屬性。
                預設為 ['created_at', 'body']
            """] = ['created_at', 'body'],
            save_path: SavePathType = None
        ) -> DataFrame:
        return streaming_download(Stocktwits_Streaming, {}, "Stocktwits 社交媒體", stock, rounds, selected_columns, save_path)

if __name__ == "__main__":
    print(FinNLPUtils.yicai_news_download("茅台", save_path="yicai_maotai.csv"))