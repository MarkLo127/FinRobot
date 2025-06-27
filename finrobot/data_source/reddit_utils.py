# -*- coding: utf-8 -*-
import os
import praw
import pandas as pd
from typing import Annotated, List
from functools import wraps
from datetime import datetime, timezone
from ..utils import decorate_all_methods, save_output, SavePathType


def init_reddit_client(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        global reddit_client
        if not all(
            [os.environ.get("REDDIT_CLIENT_ID"), os.environ.get("REDDIT_CLIENT_SECRET")]
        ):
            print("請設定 Reddit API 憑證的環境變數。")
            return None
        else:
            reddit_client = praw.Reddit(
                client_id=os.environ["REDDIT_CLIENT_ID"],
                client_secret=os.environ["REDDIT_CLIENT_SECRET"],
                user_agent="python:finrobot:v0.1 (by /u/finrobot)",
            )
            print("Reddit 客戶端已初始化")
            return func(*args, **kwargs)

    return wrapper


@decorate_all_methods(init_reddit_client)
class RedditUtils:

    def get_reddit_posts(
        query: Annotated[
            str, "搜尋查詢，例如：'AAPL OR Apple Inc OR #AAPL OR (Apple AND stock)'"
        ],
        start_date: Annotated[str, "開始日期，格式：yyyy-mm-dd"],
        end_date: Annotated[str, "結束日期，格式：yyyy-mm-dd"],
        limit: Annotated[
            int, "要獲取的貼文最大數量，預設為 1000"
        ] = 1000,
        selected_columns: Annotated[
            List[str],
            "結果中要包含的欄位，應從以下選項中選擇：'created_utc', 'id', 'title', 'selftext', 'score', 'num_comments', 'url'，預設為 ['created_utc', 'title', 'score', 'num_comments']",
        ] = ["created_utc", "title", "score", "num_comments"],
        save_path: SavePathType = None,
    ) -> pd.DataFrame:
        """
        根據搜尋查詢和日期範圍從 r/wallstreetbets、r/stocks 和 r/investing 獲取 Reddit 貼文。
        """

        post_data = []

        start_timestamp = int(
            datetime.strptime(start_date, "%Y-%m-%d")
            .replace(tzinfo=timezone.utc)
            .timestamp()
        )
        end_timestamp = int(
            datetime.strptime(end_date, "%Y-%m-%d")
            .replace(tzinfo=timezone.utc)
            .timestamp()
        )

        for subreddit_name in ["wallstreetbets", "stocks", "investing"]:
            print("正在搜尋子版塊：", subreddit_name)
            subreddit = reddit_client.subreddit(subreddit_name)
            posts = subreddit.search(query, limit=limit)

            for post in posts:
                if start_timestamp <= post.created_utc <= end_timestamp:
                    post_data.append(
                        [
                            datetime.fromtimestamp(
                                post.created_utc, tz=timezone.utc
                            ).strftime("%Y-%m-%d %H:%M:%S"),
                            post.id,
                            post.title,
                            post.selftext,
                            post.score,
                            post.num_comments,
                            post.url,
                        ]
                    )

        output = pd.DataFrame(
            post_data,
            columns=[
                "created_utc",
                "id",
                "title",
                "selftext",
                "score",
                "num_comments",
                "url",
            ],
        )
        output = output[selected_columns]

        save_output(output, f"與 {query} 相關的 Reddit 貼文", save_path=save_path)

        return output


# 使用範例
if __name__ == "__main__":

    from finrobot.utils import register_keys_from_json

    register_keys_from_json("../../config_api_keys")

    # df = RedditUtils.get_reddit_posts(query="AAPL OR Apple Inc OR #AAPL OR (Apple AND stock)", start_date="2023-05-01", end_date="2023-06-01", limit=1000)
    df = RedditUtils.get_reddit_posts(
        query="NVDA", start_date="2023-05-01", end_date="2023-06-01", limit=1000
    )
    print(df.head())
    df.to_csv("reddit_posts.csv", index=False)
