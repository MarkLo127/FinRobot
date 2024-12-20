from typing import Annotated

class TextUtils:

    def check_text_length(
        text: Annotated[str, "要檢查的文字"],
        min_length: Annotated[int, "文字的最小長度，預設為 0"] = 0,
        max_length: Annotated[int, "文字的最大長度，預設為 100000"] = 100000,
    ) -> str:
        """
        檢查文字長度是否超過最大長度。

        :param text: 要檢查的文字
        :param min_length: 文字的最小長度，預設為 0
        :param max_length: 文字的最大長度，預設為 100000
        :return: 包含文字長度檢查結果的字串
        """
        length = len(text.split())
        if length > max_length:
            return f"文字長度 {length} 超過最大長度 {max_length}。"
        elif length < min_length:
            return f"文字長度 {length} 低於最小長度 {min_length}。"
        else:
            return f"文字長度 {length} 在預期範圍內。"