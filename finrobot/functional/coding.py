import os
from typing_extensions import Annotated
from IPython import get_ipython

default_path = "coding/"


class IPythonUtils:

    def exec_python(cell: Annotated[str, "要執行的有效 Python 儲存格。"]) -> str:
        """
        在 ipython 中執行儲存格並傳回執行結果。
        """
        ipython = get_ipython()
        result = ipython.run_cell(cell)
        log = str(result.result)
        if result.error_before_exec is not None:
            log += f"\n{result.error_before_exec}"
        if result.error_in_exec is not None:
            log += f"\n{result.error_in_exec}"
        return log

    def display_image(
        image_path: Annotated[str, "要顯示的圖片檔案路徑。"]
    ) -> str:
        """
        在 Jupyter Notebook 中顯示圖片。
        """
        log = __class__.exec_python(
            f"from IPython.display import Image, display\n\ndisplay(Image(filename='{image_path}'))"
        )
        if not log:
            return "圖片顯示成功"
        else:
            return log


class CodingUtils:  # 借用自 https://microsoft.github.io/autogen/docs/notebooks/agentchat_function_call_code_writing

    def list_dir(directory: Annotated[str, "要檢查的目錄。"]) -> str:
        """
        列出所選目錄中的檔案。
        """
        files = os.listdir(default_path + directory)
        return str(files)

    def see_file(filename: Annotated[str, "要檢查的檔案名稱和路徑。"]) -> str:
        """
        檢查所選檔案的內容。
        """
        with open(default_path + filename, "r") as file:
            lines = file.readlines()
        formatted_lines = [f"{i+1}:{line}" for i, line in enumerate(lines)]
        file_contents = "".join(formatted_lines)

        return file_contents

    def modify_code(
        filename: Annotated[str, "要變更的檔案名稱和路徑。"],
        start_line: Annotated[int, "要以新程式碼取代的起始行號。"],
        end_line: Annotated[int, "要以新程式碼取代的結束行號。"],
        new_code: Annotated[
            str,
            "要取代舊程式碼的新程式碼片段。請記得提供縮排。",
        ],
    ) -> str:
        """
        以新程式碼片段取代舊程式碼片段。正確的縮排很重要。
        """
        with open(default_path + filename, "r+") as file:
            file_contents = file.readlines()
            file_contents[start_line - 1 : end_line] = [new_code + "\n"]
            file.seek(0)
            file.truncate()
            file.write("".join(file_contents))
        return "程式碼已修改"

    def create_file_with_code(
        filename: Annotated[str, "要建立的檔案名稱和路徑。"],
        code: Annotated[str, "要寫入檔案的程式碼。"],
    ) -> str:
        """
        使用提供的程式碼建立新檔案。
        """
        directory = os.path.dirname(default_path + filename)
        os.makedirs(directory, exist_ok=True)
        with open(default_path + filename, "w") as file:
            file.write(code)
        return "檔案建立成功"