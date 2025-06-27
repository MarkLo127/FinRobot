import os
from typing_extensions import Annotated
from IPython import get_ipython

default_path = "coding/"


class IPythonUtils:

    def exec_python(cell: Annotated[str, "要執行的 Python 程式碼。"]) -> str:
        """
        在 IPython 中執行程式碼並返回執行結果。
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


class CodingUtils:

    def list_dir(directory: Annotated[str, "要檢查的目錄。"]) -> str:
        """
        列出指定目錄中的檔案。
        """
        files = os.listdir(default_path + directory)
        return str(files)

    def see_file(filename: Annotated[str, "要檢查的檔案名稱和路徑。"]) -> str:
        """
        檢查指定檔案的內容。
        """
        with open(default_path + filename, "r") as file:
            lines = file.readlines()
        formatted_lines = [f"{i+1}:{line}" for i, line in enumerate(lines)]
        file_contents = "".join(formatted_lines)

        return file_contents

    def modify_code(
        filename: Annotated[str, "要修改的檔案名稱和路徑。"],
        start_line: Annotated[int, "要替換的起始行號。"],
        end_line: Annotated[int, "要替換的結束行號。"],
        new_code: Annotated[
            str,
            "用於替換的新程式碼。請注意提供正確的縮排。",
        ],
    ) -> str:
        """
        用新程式碼替換舊程式碼。正確的縮排很重要。
        """
        with open(default_path + filename, "r+") as file:
            file_contents = file.readlines()
            file_contents[start_line - 1 : end_line] = [new_code + "\n"]
            file.seek(0)
            file.truncate()
            file.write("".join(file_contents))
        return "程式碼已修改"

    def create_file_with_code(
        filename: Annotated[str, "要創建的檔案名稱和路徑。"],
        code: Annotated[str, "要寫入檔案的程式碼。"],
    ) -> str:
        """
        使用提供的程式碼創建新檔案。
        """
        directory = os.path.dirname(default_path + filename)
        os.makedirs(directory, exist_ok=True)
        with open(default_path + filename, "w") as file:
            file.write(code)
        return "檔案創建成功"
