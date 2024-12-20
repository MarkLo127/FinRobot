import os
import json
import pandas as pd
from datetime import date, timedelta, datetime
from typing import Annotated


# 定義自訂註解型別
# VerboseType = Annotated[bool, "是否將資料列印到主控台。預設為True。"]
SavePathType = Annotated[str, "儲存資料的檔案路徑。如果為None，則不儲存資料。"]


# def process_output(data: pd.DataFrame, tag: str, verbose: VerboseType = True, save_path: SavePathType = None) -> None:
#     if verbose:
#         print(data.to_string())
#     if save_path:
#         data.to_csv(save_path)
#         print(f"{tag} saved to {save_path}")


def save_output(data: pd.DataFrame, tag: str, save_path: SavePathType = None) -> None:
    """
    將 DataFrame 儲存至指定路徑。

    :param data: 要儲存的 DataFrame
    :param tag: 用於標記儲存訊息的標籤
    :param save_path: 儲存檔案的路徑，預設為 None
    """
    if save_path:
        data.to_csv(save_path)
        print(f"{tag} 已儲存至 {save_path}")


def get_current_date():
    """
    取得當前日期。

    :return: 格式為 'YYYY-MM-DD' 的當前日期字串
    """
    return date.today().strftime("%Y-%m-%d")


def register_keys_from_json(file_path):
    """
    從 JSON 檔案載入環境變數。

    :param file_path: JSON 檔案的路徑
    """
    with open(file_path, "r") as f:
        keys = json.load(f)
    for key, value in keys.items():
        os.environ[key] = value


def decorate_all_methods(decorator):
    """
    類的裝飾器，將指定的裝飾器應用於類的所有方法。

    :param decorator: 要應用的裝飾器函數
    :return: 應用裝飾器後的類
    """
    def class_decorator(cls):
        for attr_name, attr_value in cls.__dict__.items():
            if callable(attr_value):
                setattr(cls, attr_name, decorator(attr_value))
        return cls

    return class_decorator


def get_next_weekday(date):
    """
    取得輸入日期的下一個工作日。

    :param date: 輸入的日期（可以是字串或 datetime 物件）
    :return: 下一個工作日的 datetime 物件
    """
    if not isinstance(date, datetime):
        date = datetime.strptime(date, "%Y-%m-%d")

    if date.weekday() >= 5:
        days_to_add = 7 - date.weekday()
        next_weekday = date + timedelta(days=days_to_add)
        return next_weekday
    else:
        return date