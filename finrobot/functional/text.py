from typing import Annotated

class TextUtils:

    def check_text_length(
        text: Annotated[str, "要檢查的文本"],
        min_length: Annotated[int, "文本最小長度，預設為 0"] = 0,
        max_length: Annotated[int, "文本最大長度，預設為 100000"] = 100000,
    ) -> str:
        """
        檢查文本長度是否超過最大長度限制。
        """
        length = len(text.split())
        if length > max_length:
            return f"文本長度 {length} 超過最大長度限制 {max_length}。"
        elif length < min_length:
            return f"文本長度 {length} 小於最小長度限制 {min_length}。"
        else:
            return f"文本長度 {length} 在預期範圍內。"