#####################################################################
# 此檔案由 UNSTRUCTURED API 工具自動產生。
# 請勿直接修改
#####################################################################

import io
import os
import gzip
import mimetypes
from typing import List, Union
from fastapi import (
    status,
    FastAPI,
    File,
    Form,
    Request,
    UploadFile,
    APIRouter,
    HTTPException,
)
from fastapi.responses import PlainTextResponse
import json
from fastapi.responses import StreamingResponse
from starlette.datastructures import Headers
from starlette.types import Send
from base64 import b64encode
from typing import Optional, Mapping, Iterator, Tuple
import secrets
from prepline_sec_filings.sections import (
    section_string_to_enum,
    validate_section_names,
    SECSection,
)
from prepline_sec_filings.sec_document import (
    SECDocument,
    REPORT_TYPES,
    VALID_FILING_TYPES,
)
from enum import Enum
import re
import signal
from unstructured.staging.base import convert_to_isd
from prepline_sec_filings.sections import (
    ALL_SECTIONS,
    SECTIONS_10K,
    SECTIONS_10Q,
    SECTIONS_S1,
)
import csv
from typing import Dict
from unstructured.documents.elements import Text, NarrativeText, Title, ListItem
from unstructured.staging.label_studio import stage_for_label_studio


app = FastAPI()
router = APIRouter()


def is_expected_response_type(media_type, response_type):
    if media_type == "application/json" and response_type not in [dict, list]:
        return True
    elif media_type == "text/csv" and response_type != str:
        return True
    else:
        return False


# pipeline-api


class timeout:
    def __init__(self, seconds=1, error_message="Timeout"):
        self.seconds = seconds
        self.error_message = error_message

    def handle_timeout(self, signum, frame):
        raise TimeoutError(self.error_message)

    def __enter__(self):
        try:
            signal.signal(signal.SIGALRM, self.handle_timeout)
            signal.alarm(self.seconds)
        except ValueError:
            pass

    def __exit__(self, type, value, traceback):
        try:
            signal.alarm(0)
        except ValueError:
            pass


def get_regex_enum(section_regex):
    class CustomSECSection(Enum):
        CUSTOM = re.compile(section_regex)

        @property
        def pattern(self):
            return self.value

    return CustomSECSection.CUSTOM


def convert_to_isd_csv(results: dict) -> str:
    """
    以 CSV 格式返回文件元素的初始結構化文件 (ISD) 表示。
    """
    csv_fieldnames: List[str] = ["section", "element_type", "text"]
    new_rows = []
    for section, section_narrative in results.items():
        rows: List[Dict[str, str]] = convert_to_isd(section_narrative)
        for row in rows:
            new_row_item = dict()
            new_row_item["section"] = section
            new_row_item["element_type"] = row["type"]
            new_row_item["text"] = row["text"]
            new_rows.append(new_row_item)

    with io.StringIO() as buffer:
        csv_writer = csv.DictWriter(buffer, fieldnames=csv_fieldnames)
        csv_writer.writeheader()
        csv_writer.writerows(new_rows)
        return buffer.getvalue()


# 有效回應結構描述列表
LABELSTUDIO = "labelstudio"
ISD = "isd"


def pipeline_api(
    text,
    response_type="application/json",
    response_schema="isd",
    m_section=[],
    m_section_regex=[],
):
    """支援多個章節，包括：RISK_FACTORS、MANAGEMENT_DISCUSSION 等"""
    validate_section_names(m_section)

    sec_document = SECDocument.from_string(text)
    if sec_document.filing_type not in VALID_FILING_TYPES:
        raise ValueError(
            f"不支援 SEC 文件申報類型 {sec_document.filing_type}，"
            f"必須是 {','.join(VALID_FILING_TYPES)} 中的一種"
        )
    results = {}
    if m_section == [ALL_SECTIONS]:
        filing_type = sec_document.filing_type
        if filing_type in REPORT_TYPES:
            if filing_type.startswith("10-K"):
                m_section = [enum.name for enum in SECTIONS_10K]
            elif filing_type.startswith("10-Q"):
                m_section = [enum.name for enum in SECTIONS_10Q]
            else:
                raise ValueError(f"無效的報告類型：{filing_type}")

        else:
            m_section = [enum.name for enum in SECTIONS_S1]
    for section in m_section:
        results[section] = sec_document.get_section_narrative(
            section_string_to_enum[section]
        )
    for i, section_regex in enumerate(m_section_regex):
        regex_enum = get_regex_enum(section_regex)
        with timeout(seconds=5):
            section_elements = sec_document.get_section_narrative(regex_enum)
            results[f"REGEX_{i}"] = section_elements
    if response_type == "application/json":
        if response_schema == LABELSTUDIO:
            return {
                section: stage_for_label_studio(section_narrative)
                for section, section_narrative in results.items()
            }
        elif response_schema == ISD:
            return {
                section: convert_to_isd(section_narrative)
                for section, section_narrative in results.items()
            }
        else:
            raise ValueError(
                f"不支援 output_schema '{response_schema}' 的 {response_type}"
            )
    elif response_type == "text/csv":
        if response_schema != ISD:
            raise ValueError(
                f"不支援 output_schema '{response_schema}' 的 {response_type}"
            )
        return convert_to_isd_csv(results)
    else:
        raise ValueError(f"不支援 response_type '{response_type}'")


def get_validated_mimetype(file):
    """
    返回檔案的 mimetype，可透過 file.content_type 或 mimetypes 函式庫（如果前者過於通用）取得。
    如果使用者設定了 UNSTRUCTURED_ALLOWED_MIMETYPES，則根據此列表進行驗證，
    對於無效類型返回 HTTP 400。
    """
    content_type = file.content_type
    if not content_type or content_type == "application/octet-stream":
        content_type = mimetypes.guess_type(str(file.filename))[0]

        # 此函式庫缺少某些檔案類型，暫時直接寫死
        if not content_type:
            if file.filename.endswith(".md"):
                content_type = "text/markdown"
            elif file.filename.endswith(".msg"):
                content_type = "message/rfc822"

    allowed_mimetypes_str = os.environ.get("UNSTRUCTURED_ALLOWED_MIMETYPES")
    if allowed_mimetypes_str is not None:
        allowed_mimetypes = allowed_mimetypes_str.split(",")

        if content_type not in allowed_mimetypes:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"無法處理 {file.filename}： "
                    f"不支援檔案類型 {content_type}。"
                ),
            )

    return content_type


class MultipartMixedResponse(StreamingResponse):
    CRLF = b"\r\n"

    def __init__(self, *args, content_type: str = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.content_type = content_type

    def init_headers(self, headers: Optional[Mapping[str, str]] = None) -> None:
        super().init_headers(headers)
        self.boundary_value = secrets.token_hex(16)
        content_type = f'multipart/mixed; boundary="{self.boundary_value}"'
        self.raw_headers.append((b"content-type", content_type.encode("latin-1")))

    @property
    def boundary(self):
        return b"--" + self.boundary_value.encode()

    def _build_part_headers(self, headers: dict) -> bytes:
        header_bytes = b""
        for header, value in headers.items():
            header_bytes += f"{header}: {value}".encode() + self.CRLF
        return header_bytes

    def build_part(self, chunk: bytes) -> bytes:
        part = self.boundary + self.CRLF
        part_headers = {
            "Content-Length": len(chunk),
            "Content-Transfer-Encoding": "base64",
        }
        if self.content_type is not None:
            part_headers["Content-Type"] = self.content_type
        part += self._build_part_headers(part_headers)
        part += self.CRLF + chunk + self.CRLF
        return part

    async def stream_response(self, send: Send) -> None:
        await send(
            {
                "type": "http.response.start",
                "status": self.status_code,
                "headers": self.raw_headers,
            }
        )
        async for chunk in self.body_iterator:
            if not isinstance(chunk, bytes):
                chunk = chunk.encode(self.charset)
                chunk = b64encode(chunk)
            await send(
                {
                    "type": "http.response.body",
                    "body": self.build_part(chunk),
                    "more_body": True,
                }
            )

        await send({"type": "http.response.body", "body": b"", "more_body": False})


def ungz_file(file: UploadFile, gz_uncompressed_content_type=None) -> UploadFile:
    def return_content_type(filename):
        if gz_uncompressed_content_type:
            return gz_uncompressed_content_type
        else:
            return str(mimetypes.guess_type(filename)[0])

    filename = str(file.filename) if file.filename else ""
    if filename.endswith(".gz"):
        filename = filename[:-3]

    gzip_file = gzip.open(file.file).read()
    return UploadFile(
        file=io.BytesIO(gzip_file),
        size=len(gzip_file),
        filename=filename,
        headers=Headers({"content-type": return_content_type(filename)}),
    )


@router.post("/sec-filings/v0/section")
@router.post("/sec-filings/v0.2.1/section")
def pipeline_1(
    request: Request,
    gz_uncompressed_content_type: Optional[str] = Form(default=None),
    text_files: Union[List[UploadFile], None] = File(default=None),
    output_format: Union[str, None] = Form(default=None),
    output_schema: str = Form(default=None),
    section: List[str] = Form(default=[]),
    section_regex: List[str] = Form(default=[]),
):
    if text_files:
        for file_index in range(len(text_files)):
            if text_files[file_index].content_type == "application/gzip":
                text_files[file_index] = ungz_file(text_files[file_index])

    content_type = request.headers.get("Accept")

    default_response_type = output_format or "application/json"
    if not content_type or content_type == "*/*" or content_type == "multipart/mixed":
        media_type = default_response_type
    else:
        media_type = content_type

    default_response_schema = output_schema or "isd"

    if isinstance(text_files, list) and len(text_files):
        if len(text_files) > 1:
            if content_type and content_type not in [
                "*/*",
                "multipart/mixed",
                "application/json",
            ]:
                raise HTTPException(
                    detail=(
                        f"媒體類型 {content_type} 與回應類型 'multipart/mixed' 衝突。\n"
                    ),
                    status_code=status.HTTP_406_NOT_ACCEPTABLE,
                )

        def response_generator(is_multipart):
            for file in text_files:
                get_validated_mimetype(file)

                text = file.file.read().decode("utf-8")

                response = pipeline_api(
                    text,
                    m_section=section,
                    m_section_regex=section_regex,
                    response_type=media_type,
                    response_schema=default_response_schema,
                )

                if is_expected_response_type(media_type, type(response)):
                    raise HTTPException(
                        detail=(
                            f"媒體類型 {media_type} 與回應類型 {type(response)} 衝突。\n"
                        ),
                        status_code=status.HTTP_406_NOT_ACCEPTABLE,
                    )

                valid_response_types = [
                    "application/json",
                    "text/csv",
                    "*/*",
                    "multipart/mixed",
                ]
                if media_type in valid_response_types:
                    if is_multipart:
                        if type(response) not in [str, bytes]:
                            response = json.dumps(response)
                    yield response
                else:
                    raise HTTPException(
                        detail=f"不支援的媒體類型 {media_type}。\n",
                        status_code=status.HTTP_406_NOT_ACCEPTABLE,
                    )

        if content_type == "multipart/mixed":
            return MultipartMixedResponse(
                response_generator(is_multipart=True), content_type=media_type
            )
        else:
            return (
                list(response_generator(is_multipart=False))[0]
                if len(text_files) == 1
                else response_generator(is_multipart=False)
            )
    else:
        raise HTTPException(
            detail='請求參數 "text_files" 是必需的。\n',
            status_code=status.HTTP_400_BAD_REQUEST,
        )


app.include_router(router)
