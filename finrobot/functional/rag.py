from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent
from typing import Annotated


PROMPT_RAG_FUNC = """以下是根據您的查詢從所需檔案中擷取的內容。
如果您無法在有或沒有目前內容的情況下回答問題，您應該嘗試根據您的需求使用更精確的搜尋查詢，或要求更多內容。

您目前的查詢是：{input_question}

擷取的內容是：{input_context}
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
        code_execution_config=False,  # 在這種情況下我們不想執行程式碼。
        description="擁有額外內容擷取能力以解決難題的助理。",
    )

    def retrieve_content(
        message: Annotated[
            str,
            "精簡的查詢訊息，保留原始意義，可用於從提供的檔案中擷取內容以進行程式碼產生或問答。"
            "例如，'利潤率的年比比較'、'第四季 NVIDIA 的風險因素'、'使用 YFinance 擷取歷史股價資料'",
        ],
        n_results: Annotated[int, "要擷取的結果數，預設為 3"] = 3,
    ) -> str:

        rag_assitant.n_results = n_results  # 設定要擷取的結果數。
        # 檢查我們是否需要更新內容。
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
        retrieve_content.__doc__ = "從文件中擷取內容以協助問答或程式碼產生。"
        docs = retrieve_config.get("docs_path", [])
        if docs:
            docs_str = "\n".join(docs if isinstance(docs, list) else [docs])
            retrieve_content.__doc__ += f"可用文件：\n{docs_str}"

    return retrieve_content, rag_assitant  # 用於除錯