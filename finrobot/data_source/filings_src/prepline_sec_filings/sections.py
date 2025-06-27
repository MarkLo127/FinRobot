# -*- coding: utf-8 -*-
"""定義/枚舉 SEC 表格常見章節的模組"""

from enum import Enum
import re
from typing import List


class SECSection(Enum):
    """SEC 章節枚舉類別"""
    PROSPECTUS_SUMMARY = re.compile(r"^(?:prospectus )?summary$")  # 招股說明書摘要
    ABOUT_PROSPECTUS = re.compile(r"about this prospectus")  # 關於招股說明書
    FORWARD_LOOKING_STATEMENTS = re.compile(r"forward[ -]looking statements")  # 前瞻性陳述
    RISK_FACTORS = re.compile(r"risk factors")  # 風險因素
    USE_OF_PROCEEDS = re.compile(r"use of proceeds")  # 資金用途
    DIVIDEND_POLICY = re.compile(r"^dividend policy")  # 股利政策
    CAPITALIZATION = re.compile(r"^capitalization$")  # 資本化
    DILUTION = re.compile(r"^dilution$")  # 稀釋
    MANAGEMENT_DISCUSSION = re.compile(r"^management(?:[\u2019']s)? discussion")  # 管理層討論
    BUSINESS = re.compile(r"^business$")  # 業務
    MANAGEMENT = re.compile(r"^(?:(?:our )?management)|(?:executive officers)$")  # 管理層
    COMPENSATION = re.compile(r"compensation")  # 薪酬
    RELATED_PARTY_TRANSACTIONS = re.compile(r"(?:relationships|related).*transactions")  # 關聯方交易
    PRINCIPAL_STOCKHOLDERS = re.compile(
        r"(?:principal.*(?:stockholder|shareholder)s?)|(?:(security|stock|share) "
        r"ownership .*certain)"
    )  # 主要股東
    DESCRIPTION_OF_STOCK = re.compile(
        r"^description of (?:capital stock|share capital|securities)"
    )  # 股票描述
    DESCRIPTION_OF_DEBT = re.compile(r"^description of .*debt")  # 債務描述
    FUTURE_SALE = re.compile(r"(?:shares|stock) eligible for future sale")  # 未來銷售
    US_TAX = re.compile(
        r"(?:us|u\.s\.|united states|material federal).* tax (?:consideration|consequence)"
    )  # 美國稅務
    UNDERWRITING = re.compile(r"underwrit")  # 承銷
    LEGAL_MATTERS = re.compile(r"legal matters")  # 法律事務
    EXPERTS = re.compile(r"^experts$")  # 專家
    MORE_INFORMATION = re.compile(r"(?:additional|more) information")  # 更多信息
    FINANCIAL_STATEMENTS = r"financial statements"  # 財務報表
    MARKET_RISK_DISCLOSURES = (
        r"(?:quantitative|qualitative) disclosures? about market risk"
    )  # 市場風險披露
    CONTROLS_AND_PROCEDURES = r"controls and procedures"  # 控制和程序
    LEGAL_PROCEEDINGS = r"legal proceedings"  # 法律程序
    DEFAULTS = r"defaults (?:up)?on .*securities"  # 違約
    MINE_SAFETY = r"mine safety disclosures?"  # 礦山安全
    OTHER_INFORMATION = r"other information"  # 其他信息
    UNRESOLVED_STAFF_COMMENTS = r"unresolved staff comments"  # 未解決的員工意見
    PROPERTIES = r"^properties$"  # 物業
    MARKET_FOR_REGISTRANT_COMMON_EQUITY = (
        r"market for(?: the)? (?:registrant|company)(?:['\u2019]s)? common equity"
    )  # 註冊人普通股市場
    ACCOUNTING_DISAGREEMENTS = r"disagreements with accountants"  # 會計分歧
    FOREIGN_JURISDICTIONS = r"diclosure .*foreign jurisdictions .*inspection"  # 外國司法管轄區
    EXECUTIVE_OFFICERS = r"executive officers"  # 執行官
    ACCOUNTING_FEES = r"accounting fees"  # 會計費用
    EXHIBITS = r"^exhibits?(.*financial statement schedules)?$"  # 附件
    FORM_SUMMARY = r"^form .*summary$"  # 表格摘要
    # 注意：在 test_real_examples.py 中使用的額外章節標題，
    # 當允許自定義正則表達式字串參數時，可能會更改此設定。
    CERTAIN_TRADEMARKS = r"certain trademarks"  # 特定商標
    OFFER_PRICE = r"(?:determination of )offering price"  # 發行價格

    @property
    def pattern(self):
        """返回模式"""
        return self.value


ALL_SECTIONS = "_ALL"

section_string_to_enum = {enum.name: enum for enum in SECSection}

# 注意：章節列在 SEC 的以下文件中
# 參考：https://www.sec.gov/files/form10-k.pdf
SECTIONS_10K = (
    SECSection.BUSINESS,  # 項目 1 - 業務
    SECSection.RISK_FACTORS,  # 項目 1A - 風險因素
    SECSection.UNRESOLVED_STAFF_COMMENTS,  # 項目 1B - 未解決的員工意見
    SECSection.PROPERTIES,  # 項目 2 - 物業
    SECSection.LEGAL_PROCEEDINGS,  # 項目 3 - 法律程序
    SECSection.MINE_SAFETY,  # 項目 4 - 礦山安全
    SECSection.MARKET_FOR_REGISTRANT_COMMON_EQUITY,  # 項目 5 - 註冊人普通股市場
    # 注意：項目 6 是「保留」
    SECSection.MANAGEMENT_DISCUSSION,  # 項目 7 - 管理層討論
    SECSection.MARKET_RISK_DISCLOSURES,  # 項目 7A - 市場風險披露
    SECSection.FINANCIAL_STATEMENTS,  # 項目 8 - 財務報表
    SECSection.ACCOUNTING_DISAGREEMENTS,  # 項目 9 - 會計分歧
    SECSection.CONTROLS_AND_PROCEDURES,  # 項目 9A - 控制和程序
    # 注意：項目 9B 是其他信息
    SECSection.FOREIGN_JURISDICTIONS,  # 項目 9C - 外國司法管轄區
    SECSection.MANAGEMENT,  # 項目 10 - 管理層
    SECSection.COMPENSATION,  # 項目 11 - 薪酬
    SECSection.PRINCIPAL_STOCKHOLDERS,  # 項目 12 - 主要股東
    SECSection.RELATED_PARTY_TRANSACTIONS,  # 項目 13 - 關聯方交易
    SECSection.ACCOUNTING_FEES,  # 項目 14 - 會計費用
    SECSection.EXHIBITS,  # 項目 15 - 附件
    SECSection.FORM_SUMMARY,  # 項目 16 - 表格摘要
)

# 注意：章節列在 SEC 的以下文件中
# 參考：https://www.sec.gov/files/form10-q.pdf
SECTIONS_10Q = (
    # 第一部分 - 財務信息
    SECSection.FINANCIAL_STATEMENTS,  # 項目 1 - 財務報表
    SECSection.MANAGEMENT_DISCUSSION,  # 項目 2 - 管理層討論
    SECSection.MARKET_RISK_DISCLOSURES,  # 項目 3 - 市場風險披露
    SECSection.CONTROLS_AND_PROCEDURES,  # 項目 4 - 控制和程序
    # 第二部分 - 其他信息
    SECSection.LEGAL_PROCEEDINGS,  # 項目 1 - 法律程序
    SECSection.RISK_FACTORS,  # 項目 1A - 風險因素
    SECSection.USE_OF_PROCEEDS,  # 項目 2 - 資金用途
    SECSection.DEFAULTS,  # 項目 3 - 違約
    SECSection.MINE_SAFETY,  # 項目 4 - 礦山安全
    SECSection.OTHER_INFORMATION,  # 項目 5 - 其他信息
)

SECTIONS_S1 = (
    SECSection.PROSPECTUS_SUMMARY,  # 招股說明書摘要
    SECSection.ABOUT_PROSPECTUS,  # 關於招股說明書
    SECSection.FORWARD_LOOKING_STATEMENTS,  # 前瞻性陳述
    SECSection.RISK_FACTORS,  # 風險因素
    SECSection.USE_OF_PROCEEDS,  # 資金用途
    SECSection.DIVIDEND_POLICY,  # 股利政策
    SECSection.CAPITALIZATION,  # 資本化
    SECSection.DILUTION,  # 稀釋
    SECSection.MANAGEMENT_DISCUSSION,  # 管理層討論
    SECSection.BUSINESS,  # 業務
    SECSection.MANAGEMENT,  # 管理層
    SECSection.COMPENSATION,  # 薪酬
    SECSection.RELATED_PARTY_TRANSACTIONS,  # 關聯方交易
    SECSection.PRINCIPAL_STOCKHOLDERS,  # 主要股東
    SECSection.DESCRIPTION_OF_STOCK,  # 股票描述
    SECSection.DESCRIPTION_OF_DEBT,  # 債務描述
    SECSection.FUTURE_SALE,  # 未來銷售
    SECSection.US_TAX,  # 美國稅務
    SECSection.UNDERWRITING,  # 承銷
    SECSection.LEGAL_MATTERS,  # 法律事務
    SECSection.EXPERTS,  # 專家
    SECSection.MORE_INFORMATION,  # 更多信息
)


def validate_section_names(section_names: List[str]):
    """返回不對應於已定義枚舉的章節名稱。"""
    if len(section_names) == 1 and section_names[0] == ALL_SECTIONS:
        return None
    elif len(section_names) > 1 and ALL_SECTIONS in section_names:
        raise ValueError(f"{ALL_SECTIONS} 不能與其他章節一起指定")

    invalid_names = [
        name for name in section_names if name not in section_string_to_enum
    ]
    if invalid_names:
        raise ValueError(f"以下章節名稱無效：{invalid_names}")
    return None
