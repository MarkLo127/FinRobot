# -*- coding: utf-8 -*-
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent
from typing import Annotated


PROMPT_RAG_FUNC = """以下是根據您的查詢從所需檔案中檢索的內容。
如果您無法使用當前內容回答問題，您應該嘗試根據您的需求使用更精確的搜索查詢，或要求更多的上下文。

您當前的查詢是：{input_question}

檢索到的內容是：{input_context}
"""


def get_rag_function(retrieve_config, description=""):

    def termination_msg(x):
        return (
            isinstance(x, dict)
            and "TERMINATE" == str(x.get("content", ""))[-9:].upper()
        )

    if "customized_prompt" not in retrieve_config:
        retrieve_config["customized_prompt"] = PROMPT_RAG_FUNC

    rag_assitant = RetrieveUserProxyAgent(
        name="RAG_Assistant",
        is_termination_msg=termination_msg,
        human_input_mode="NEVER",
        default_auto_reply="如果任務完成，請回覆 `TERMINATE`。",
        max_consecutive_auto_reply=3,
        retrieve_config=retrieve_config,
        code_execution_config=False,  # 在這種情況下，我們不想執行程式碼。
        description="擁有額外內容檢索能力以解決困難問題的助手。",
    )

    def retrieve_content(
        message: Annotated[
            str,
            "保持原意並可用於從提供的檔案中檢索內容以進行程式碼生成或問題回答的精確查詢訊息。"
            "例如：'利潤率的同比比較'、'NVIDIA 第四季度的風險因素'、'使用 YFinance 檢索歷史股價數據'",
        ],
        n_results: Annotated[int, "要檢索的結果數量，預設為 3"] = 3,
    ) -> str:

        rag_assitant.n_results = n_results  # 設定要檢索的結果數量。
        # 檢查是否需要更新上下文。
        update_context_case1, update_context_case2 = rag_assitant._check_update_context(
            message
        )
        if (
            update_context_case1 or update_context_case2
        ) and rag_assitant.update_context:
            rag_assitant.problem = (
                message
                if not hasattr(rag_assitant, "problem")
                else rag_assitant.problem
            )
            _, ret_msg = rag_assitant._generate_retrieve_user_reply(message)
        else:
            _context = {"problem": message, "n_results": n_results}
            ret_msg = rag_assitant.message_generator(rag_assitant, None, _context)
        return ret_msg if ret_msg else message

    if description:
        retrieve_content.__doc__ = description
    else:
        retrieve_content.__doc__ = "從文件中檢索內容以協助回答問題或生成程式碼。"
        docs = retrieve_config.get("docs_path", [])
        if docs:
            docs_str = "\n".join(docs if isinstance(docs, list) else [docs])
            retrieve_content.__doc__ += f"可用文件：\n{docs_str}"

    return retrieve_content, rag_assitant  # 用於調試
