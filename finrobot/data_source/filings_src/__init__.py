# -*- coding: utf-8 -*-
"""SEC 申報文件處理模組"""

from .secData import sec_main
from .sec_filings import SECExtractor
from .section_names import SECTIONS_10K, SECTIONS_10Q, SECTIONS_S1

__all__ = [
    "sec_main",
    "SECExtractor",
    "SECTIONS_10K",
    "SECTIONS_10Q",
    "SECTIONS_S1",
]

