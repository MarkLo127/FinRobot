from autogen import register_function, ConversableAgent
from .data_source import *
from .functional.coding import CodingUtils

from typing import List, Callable
from functools import wraps
from pandas import DataFrame


def stringify_output(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if isinstance(result, DataFrame):
            return result.to_string()
        else:
            return str(result)

    return wrapper


def register_toolkits(
    config: List[dict | Callable | type],
    caller: ConversableAgent,
    executor: ConversableAgent,
    **kwargs
):
    """從配置列表中註冊工具。"""

    for tool in config:
        if isinstance(tool, type):
            register_tookits_from_cls(caller, executor, tool, **kwargs)
            continue

        tool_dict = {"function": tool} if callable(tool) else tool
        if "function" not in tool_dict or not callable(tool_dict["function"]):
            raise ValueError(
                "在工具配置中找不到函數或函數不可調用。"
            )

        tool_function = tool_dict["function"]
        name = tool_dict.get("name", tool_function.__name__)
        description = tool_dict.get("description", tool_function.__doc__)
        register_function(
            stringify_output(tool_function),
            caller=caller,
            executor=executor,
            name=name,
            description=description,
        )


def register_code_writing(caller: ConversableAgent, executor: ConversableAgent):
    """註冊程式碼編寫工具。"""

    register_toolkits(
        [
            {
                "function": CodingUtils.list_dir,
                "name": "list_files",
                "description": "列出目錄中的檔案。",
            },
            {
                "function": CodingUtils.see_file,
                "name": "see_file",
                "description": "查看選定檔案的內容。",
            },
            {
                "function": CodingUtils.modify_code,
                "name": "modify_code",
                "description": "用新程式碼替換舊程式碼。",
            },
            {
                "function": CodingUtils.create_file_with_code,
                "name": "create_file_with_code",
                "description": "使用提供的程式碼創建新檔案。",
            },
        ],
        caller,
        executor,
    )


def register_tookits_from_cls(
    caller: ConversableAgent,
    executor: ConversableAgent,
    cls: type,
    include_private: bool = False,
):
    """將類別的所有方法註冊為工具。"""
    if include_private:
        funcs = [
            func
            for func in dir(cls)
            if callable(getattr(cls, func)) and not func.startswith("__")
        ]
    else:
        funcs = [
            func
            for func in dir(cls)
            if callable(getattr(cls, func))
            and not func.startswith("__")
            and not func.startswith("_")
        ]
    register_toolkits([getattr(cls, func) for func in funcs], caller, executor)
