# -*- coding: utf-8 -*-
"""數據源模組 - 包含各種財務數據獲取工具"""
import importlib.util

from .finance_data import get_data
from .finnhub_utils import FinnHubUtils
from .yfinance_utils import YFinanceUtils
from .sec_utils import SECUtils
from .fmp_utils import FMPUtils
from .reddit_utils import RedditUtils
from .finnlp_utils import finnlpUtils

__all__ = [
    "get_data",
    "FinnHubUtils",
    "YFinanceUtils",
    "SECUtils",
    "FMPUtils",
    "RedditUtils",
    "finnlpUtils",
]

if importlib.util.find_spec("finnlp") is not None:
    from .finnlp_utils import finnlpUtils
    __all__.append("finnlpUtils")