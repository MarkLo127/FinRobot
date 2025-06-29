# -*- coding: utf-8 -*-
#####################################################################
# 此檔案由 UNSTRUCTURED API 工具自動生成。
# 請勿直接修改
#####################################################################


from fastapi import FastAPI, Request, status
import logging
import os

from .section import router as section_router


app = FastAPI(
    title="Unstructured Pipeline API",
    description="非結構化管道 API",
    version="1.0.0",
    docs_url="/sec-filings/docs",
    openapi_url="/sec-filings/openapi.json",
)

allowed_origins = os.environ.get("ALLOWED_ORIGINS", None)
if allowed_origins:
    from fastapi.middleware.cors import CORSMiddleware

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins.split(","),
        allow_methods=["OPTIONS", "POST"],
        allow_headers=["Content-Type"],
    )

app.include_router(section_router)


# 過濾掉 /healthcheck 的噪音
class HealthCheckFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return record.getMessage().find("/healthcheck") == -1


logging.getLogger("uvicorn.access").addFilter(HealthCheckFilter())


@app.get("/healthcheck", status_code=status.HTTP_200_OK, include_in_schema=False)
def healthcheck(request: Request):
    """健康檢查端點"""
    return {"healthcheck": "健康檢查狀態：一切正常！"}
