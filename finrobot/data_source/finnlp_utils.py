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
    if hasattr(downloader, 'gather_content'):
        downloader.gather_content()
    # print(downloader.dataframe.columns)
    selected_news = downloader.dataframe[selected_columns]
    save_output(selected_news, tag, save_path)
    return selected_news


class FinNLPUtils:

    """
    串流新聞下載
    """

    def cnbc_news_download(
            keyword: Annotated[str, "在新聞串流中搜尋的關鍵字"],
            rounds: Annotated[int, "搜尋的次數。預設為 1"] = 1,
            selected_columns: Annotated[list[str], "要傳回的新聞欄位名稱清單，應從 'description', 'cn:lastPubDate', 'dateModified', 'cn:dateline', 'cn:branding', 'section', 'cn:type', 'author', 'cn:source', 'cn:subtype', 'duration', 'summary', 'expires', 'cn:sectionSubType', 'cn:contentClassification', 'pubdateunix', 'url', 'datePublished', 'cn:promoImage', 'cn:title', 'cn:keyword', 'cn:liveURL', 'brand', 'hint', 'hint_detail' 中選擇。預設為 ['author', 'datePublished', 'description' ,'section', 'cn:title', 'summary']"] = ["author", "datePublished", "description" ,"section", "cn:title", "summary"],
            save_path: SavePathType = None
        ) -> DataFrame:
        return streaming_download(CNBC_Streaming, {}, "CNBC 新聞", keyword, rounds, selected_columns, save_path)


    def yicai_news_download(
            keyword: Annotated[str, "在新聞串流中搜尋的關鍵字"],
            rounds: Annotated[int, "搜尋的次數。預設為 1"] = 1,
            selected_columns: Annotated[list[str], "要傳回的新聞欄位名稱清單，應從 'author','channelid','creationDate','desc','id','previewImage','source','tags','title','topics','typeo','url','weight' 中選擇。預設為 ['author', 'creationDate', 'desc' ,'source', 'title']"] = ["author", "creationDate", "desc" ,"source", "title"],
            save_path: SavePathType = None
        ) -> DataFrame:
        return streaming_download(Yicai_Streaming, {}, "第一財經新聞", keyword, rounds, selected_columns, save_path)


    def investor_place_news_download(
            keyword: Annotated[str, "在新聞串流中搜尋的關鍵字"],
            rounds: Annotated[int, "搜尋的次數。預設為 1"] = 1,
            selected_columns: Annotated[list[str], "要傳回的新聞欄位名稱清單，應從 'title', 'time', 'author', 'summary' 中選擇。預設為 ['title', 'time', 'author', 'summary']"] = ['title', 'time', 'author', 'summary'],
            save_path: SavePathType = None
        ) -> DataFrame:
        return streaming_download(InvestorPlace_Streaming, {}, "Investor Place 新聞", keyword, rounds, selected_columns, save_path)


    # def eastmoney_news_download(
    #     stock: Annotated[str, "股票代碼，例如 600519"],
    #     pages: Annotated[int, "要擷取的頁數。預設為 1"] = 1,
    #     selected_columns: Annotated[list[str], "要傳回的新聞欄位名稱清單，應從 'title', 'time', 'author', 'summary' 中選擇。預設為 ['title', 'time', 'author', 'summary']"] = ['title', 'time', 'author', 'summary'],
    #     verbose: Annotated[bool, "是否將下載的新聞列印到主控台。預設為 True"] = True,
    #     save_path: Annotated[str, "如果指定（建議在新聞量很大時使用），下載的新聞將儲存到 save_path，否則新聞將以字串形式傳回。預設為 None"] = None,
    # ) -> str:
    #     return streaming_download(Eastmoney_Streaming, "東方財富", stock, pages, selected_columns, save_path)


    """
    日期範圍新聞下載
    """

    def sina_finance_news_download(
            start_date: Annotated[str, "要擷取的新聞開始日期，YYYY-mm-dd"],
            end_date: Annotated[str, "要擷取的新聞結束日期，YYYY-mm-dd"],
            selected_columns: Annotated[list[str], """
                要傳回的新聞欄位名稱清單，應從 
                'mediaid', 'productid', 'summary', 'ctime', 'url', 'author', 'stitle',
                'authoruid', 'wapsummary', 'images', 'level', 'keywords', 'mlids',
                'wapurl', 'columnid', 'oid', 'img', 'subjectid', 'commentid',
                'ipad_vid', 'vid', 'video_id', 'channelid', 'intime',
                'video_time_length', 'categoryid', 'hqChart', 'intro', 'is_cre_manual',
                'icons', 'mtime', 'media_name', 'title', 'docid', 'urls', 'templateid', 
                'lids', 'wapurls', 'ext', 'comment_reply', 'comment_show', 'comment_total', 'praise',
                'dispraise', 'important', 'content' 中選擇。預設為 ['title', 'author', 'content']
                """
            ] = ['title', 'author', 'content'],
            save_path: SavePathType = None
        ) -> DataFrame:
        return date_range_download(Sina_Finance_Date_Range, {}, "新浪財經新聞", start_date, end_date, None, selected_columns, save_path)


    def finnhub_news_download(
            start_date: Annotated[str, "要擷取的新聞開始日期，YYYY-mm-dd"],
            end_date: Annotated[str, "要擷取的新聞結束日期，YYYY-mm-dd"],
            stock: Annotated[str, "股票代碼，例如 AAPL"],
            selected_columns: Annotated[list[str], "要傳回的新聞欄位名稱清單，應從 'category', 'datetime', 'headline', 'id', 'image', 'related', 'source', 'summary', 'url', 'content' 中選擇。預設為 ['headline', 'datetime', 'source', 'summary']"] = ['headline', 'datetime', 'source', 'summary'],
            save_path: SavePathType = None
        ) -> DataFrame:
        return date_range_download(Finnhub_Date_Range, {"token": os.environ['FINNHUB_API_KEY']}, "Finnhub 新聞", start_date, end_date, stock, selected_columns, save_path)


    """
    社群媒體
    """
    def xueqiu_social_media_download(
            stock: Annotated[str, "股票代碼，例如 'AAPL'"],
            rounds: Annotated[int, "搜尋的次數。預設為 1"] = 1,
            selected_columns: Annotated[list[str], """
                要傳回的新聞欄位名稱清單，應從 blocked', 
                'blocking', 'canEdit', 'commentId', 'controversial',
                'created_at', 'description', 'donate_count', 'donate_snowcoin',
                'editable', 'expend', 'fav_count', 'favorited', 'flags', 'flagsObj',
                'hot', 'id', 'is_answer', 'is_bonus', 'is_refused', 'is_reward',
                'is_ss_multi_pic', 'legal_user_visible', 'like_count', 'liked', 'mark',
                'pic', 'promotion_id', 'reply_count', 'retweet_count',
                'retweet_status_id', 'reward_count', 'reward_user_count', 'rqid',
                'source', 'source_feed', 'source_link', 'target', 'text', 'timeBefore',
                'title', 'trackJson', 'truncated', 'truncated_by', 'type', 'user',
                'user_id', 'view_count', 'firstImg', 'pic_sizes', 'edited_at' 中選擇。 
                預設為 ['created_at', 'description', 'title', 'text', 'target', 'source']
            """] = ['created_at', 'description', 'title', 'text', 'target', 'source'],
            save_path: SavePathType = None
        ) -> DataFrame:
        return streaming_download(Xueqiu_Streaming, {}, "雪球社群媒體", stock, rounds, selected_columns, save_path)


    def stocktwits_social_media_download(
            stock: Annotated[str, "股票代碼，例如 'AAPL'"],
            rounds: Annotated[int, "搜尋的次數。預設為 1"] = 1,
            selected_columns: Annotated[list[str], """
                要傳回的新聞欄位名稱清單，應從 'id', 
                'body', 'created_at', 'user', 'source', 'symbols', 'prices',
                'mentioned_users', 'entities', 'liked_by_self', 'reshared_by_self',
                'conversation', 'links', 'likes', 'reshare_message', 'structurable',
                'reshares' 中選擇。預設為 ['created_at', 'body']
            """] = ['created_at', 'body'],
            save_path: SavePathType = None
        ) -> DataFrame:
        return streaming_download(Stocktwits_Streaming, {}, "Stocktwits 社群媒體", stock, rounds, selected_columns, save_path)


    # def reddit_social_media_download(
    #     pages: Annotated[int, "要擷取的頁數。預設為 1"] = 1,
    #     selected_columns: Annotated[list[str], """
    #         要傳回的新聞欄位名稱清單，應從 'id', 
    #         'body', 'created_at', 'user', 'source', 'symbols', 'prices',
    #         'mentioned_users', 'entities', 'liked_by_self', 'reshared_by_self',
    #         'conversation', 'links', 'likes', 'reshare_message', 'structurable',
    #         'reshares' 中選擇。預設為 ['created_at', 'body']
    #     """] = ['created_at', 'body'],
    #     verbose: Annotated[bool, "是否將下載的新聞列印到主控台。預設為 True"] = True,
    #     save_path: Annotated[str, "如果指定（建議在新聞量很大時使用），下載的新聞將儲存到 save_path。預設為 None"] = None,
    # ) -> DataFrame:
    #     return streaming_download(Reddit_Streaming, {}, "Reddit 社群媒體", None, pages, selected_columns, save_path)


    """
    公司公告
    （運作不佳）
    """

    # from finnlp.data_sources.company_announcement.sec import SEC_Announcement
    # from finnlp.data_sources.company_announcement.juchao import Juchao_Announcement


    # def sec_announcement_download(
    #     start_date: Annotated[str, "要擷取的新聞開始日期，YYYY-mm-dd"],
    #     end_date: Annotated[str, "要擷取的新聞結束日期，YYYY-mm-dd"],
    #     stock: Annotated[str, "股票代碼，例如 AAPL"],
    #     selected_columns: Annotated[list[str], "要傳回的新聞欄位名稱清單，應從 'category', 'datetime', 'headline', 'id', 'image', 'related', 'source', 'summary', 'url', 'content' 中選擇。預設為 ['headline', 'datetime', 'source', 'summary']"] = ['headline', 'datetime', 'source', 'summary'],
    #     verbose: Annotated[bool, "是否將下載的新聞列印到主控台。預設為 True"] = True,
    #     save_path: Annotated[str, "如果指定（建議在新聞量很大時使用），下載的新聞將儲存到 save_path。預設為 None"] = None,
    # ) -> DataFrame:
    #     return date_range_download(SEC_Announcement, {}, "SEC 公告", start_date, end_date, stock, selected_columns, save_path)


    # def juchao_announcement_download(
    #     start_date: Annotated[str, "要擷取的新聞開始日期，YYYY-mm-dd"],
    #     end_date: Annotated[str, "要擷取的新聞結束日期，YYYY-mm-dd"],
    #     stock: Annotated[str, "股票代碼，例如 000001"],
    #     selected_columns: Annotated[list[str], "要傳回的新聞欄位名稱清單，應從 'category', 'datetime', 'headline', 'id', 'image', 'related', 'source', 'summary', 'url', 'content' 中選擇。預設為 ['headline', 'datetime', 'source', 'summary']"] = ['headline', 'datetime', 'source', 'summary'],
    #     verbose: Annotated[bool, "是否將下載的新聞列印到主控台。預設為 True"] = True,
    #     save_path: Annotated[str, "如果指定（建議在新聞量很大時使用），下載的新聞將儲存到 save_path。預設為 None"] = None,
    # ) -> DataFrame:
    #     return date_range_download(Juchao_Announcement, {}, "巨潮公告", start_date, end_date, stock, selected_columns, save_path)


if __name__ == "__main__":

    print(FinNLPUtils.yicai_news_download("茅台", save_path="yicai_maotai.csv"))
    # print(cnbc_news_download("tesla", save_path="cnbc_tesla.csv"))
    # investor_place_news_download("tesla", save_path="invpl_tesla.csv")
    # eastmoney_news_download("600519", save_path="estmny_maotai.csv")
    # sina_finance_news_download("2024-03-02", "2024-03-02", save_path="sina_news.csv")
    # finnhub_news_download("2024-03-02", "2024-03-02", "AAPL", save_path="finnhub_aapl_news.csv")
    # stocktwits_social_media_download("AAPL", save_path="stocktwits_aapl.csv")
    # xueqiu_social_media_download("茅台", save_path="xueqiu_maotai.csv")
    # reddit_social_media_download(save_path="reddit_social_media.csv")
    # juchao_announcement_download("000001", "2020-01-01", "2020-06-01", save_path="sec_announcement.csv")