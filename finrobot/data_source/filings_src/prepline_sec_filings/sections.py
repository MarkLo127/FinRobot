"""定義/列舉 SEC 表格中常見章節的模組"""

from enum import Enum
import re
from typing import List


class SECSection(Enum):
    PROSPECTUS_SUMMARY = re.compile(r"^(?:prospectus )?summary$")
    ABOUT_PROSPECTUS = re.compile(r"about this prospectus")
    FORWARD_LOOKING_STATEMENTS = re.compile(r"forward[ -]looking statements")
    RISK_FACTORS = re.compile(r"risk factors")
    USE_OF_PROCEEDS = re.compile(r"use of proceeds")
    DIVIDEND_POLICY = re.compile(r"^dividend policy")
    CAPITALIZATION = re.compile(r"^capitalization$")
    DILUTION = re.compile(r"^dilution$")
    MANAGEMENT_DISCUSSION = re.compile(r"^management(?:[\u2019']s)? discussion")
    BUSINESS = re.compile(r"^business$")
    MANAGEMENT = re.compile(r"^(?:(?:our )?management)|(?:executive officers)$")
    COMPENSATION = re.compile(r"compensation")
    RELATED_PARTY_TRANSACTIONS = re.compile(r"(?:relationships|related).*transactions")
    PRINCIPAL_STOCKHOLDERS = re.compile(
        r"(?:principal.*(?:stockholder|shareholder)s?)|(?:(security|stock|share) "
        r"ownership .*certain)"
    )
    DESCRIPTION_OF_STOCK = re.compile(
        r"^description of (?:capital stock|share capital|securities)"
    )
    DESCRIPTION_OF_DEBT = re.compile(r"^description of .*debt")
    FUTURE_SALE = re.compile(r"(?:shares|stock) eligible for future sale")
    US_TAX = re.compile(
        r"(?:us|u\.s\.|united states|material federal).* tax (?:consideration|consequence)"
    )
    UNDERWRITING = re.compile(r"underwrit")
    LEGAL_MATTERS = re.compile(r"legal matters")
    EXPERTS = re.compile(r"^experts$")
    MORE_INFORMATION = re.compile(r"(?:additional|more) information")
    FINANCIAL_STATEMENTS = r"financial statements"
    MARKET_RISK_DISCLOSURES = (
        r"(?:quantitative|qualitative) disclosures? about market risk"
    )
    CONTROLS_AND_PROCEDURES = r"controls and procedures"
    LEGAL_PROCEEDINGS = r"legal proceedings"
    DEFAULTS = r"defaults (?:up)?on .*securities"
    MINE_SAFETY = r"mine safety disclosures?"
    OTHER_INFORMATION = r"other information"
    UNRESOLVED_STAFF_COMMENTS = r"unresolved staff comments"
    PROPERTIES = r"^properties$"
    MARKET_FOR_REGISTRANT_COMMON_EQUITY = (
        r"market for(?: the)? (?:registrant|company)(?:['\u2019]s)? common equity"
    )
    ACCOUNTING_DISAGREEMENTS = r"disagreements with accountants"
    FOREIGN_JURISDICTIONS = r"diclosure .*foreign jurisdictions .*inspection"
    EXECUTIVE_OFFICERS = r"executive officers"
    ACCOUNTING_FEES = r"accounting fees"
    EXHIBITS = r"^exhibits?(.*financial statement schedules)?$"
    FORM_SUMMARY = r"^form .*summary$"
    # 注意(yuming)：在 test_real_examples.py 中使用的其他章節標題，
    # 當允許自訂 regex 字串參數時，可能會變更此項。
    CERTAIN_TRADEMARKS = r"certain trademarks"
    OFFER_PRICE = r"(?:determination of )offering price"

    @property
    def pattern(self):
        return self.value


ALL_SECTIONS = "_ALL"

section_string_to_enum = {enum.name: enum for enum in SECSection}

# 注意(robinson) - 章節列在 SEC 的下列文件中
# 參考：https://www.sec.gov/files/form10-k.pdf
SECTIONS_10K = (
    SECSection.BUSINESS,  # 項目 1
    SECSection.RISK_FACTORS,  # 項目 1A
    SECSection.UNRESOLVED_STAFF_COMMENTS,  # 項目 1B
    SECSection.PROPERTIES,  # 項目 2
    SECSection.LEGAL_PROCEEDINGS,  # 項目 3
    SECSection.MINE_SAFETY,  # 項目 4
    SECSection.MARKET_FOR_REGISTRANT_COMMON_EQUITY,  # 項目 5
    # 注意(robinson) - 項目 6 為「保留」
    SECSection.MANAGEMENT_DISCUSSION,  # 項目 7
    SECSection.MARKET_RISK_DISCLOSURES,  # 項目 7A
    SECSection.FINANCIAL_STATEMENTS,  # 項目 8
    SECSection.ACCOUNTING_DISAGREEMENTS,  # 項目 9
    SECSection.CONTROLS_AND_PROCEDURES,  # 項目 9A
    # 注意(robinson) - 項目 9B 為其他資訊
    SECSection.FOREIGN_JURISDICTIONS,  # 項目 9C
    SECSection.MANAGEMENT,  # 項目 10
    SECSection.COMPENSATION,  # 項目 11
    SECSection.PRINCIPAL_STOCKHOLDERS,  # 項目 12
    SECSection.RELATED_PARTY_TRANSACTIONS,  # 項目 13
    SECSection.ACCOUNTING_FEES,  # 項目 14
    SECSection.EXHIBITS,  # 項目 15
    SECSection.FORM_SUMMARY,  # 項目 16
)

# 注意(robinson) - 章節列在 SEC 的下列文件中
# 參考：https://www.sec.gov/files/form10-q.pdf
SECTIONS_10Q = (
    # 第 I 部分 - 財務資訊
    SECSection.FINANCIAL_STATEMENTS,  # 項目 1
    SECSection.MANAGEMENT_DISCUSSION,  # 項目 2
    SECSection.MARKET_RISK_DISCLOSURES,  # 項目 3
    SECSection.CONTROLS_AND_PROCEDURES,  # 項目 4
    # 第 II 部分 - 其他資訊
    SECSection.LEGAL_PROCEEDINGS,  # 項目 1
    SECSection.RISK_FACTORS,  # 項目 1A
    SECSection.USE_OF_PROCEEDS,  # 項目 2
    SECSection.DEFAULTS,  # 項目 3
    SECSection.MINE_SAFETY,  # 項目 4
    SECSection.OTHER_INFORMATION,  # 項目 5
)

SECTIONS_S1 = (
    SECSection.PROSPECTUS_SUMMARY,
    SECSection.ABOUT_PROSPECTUS,
    SECSection.FORWARD_LOOKING_STATEMENTS,
    SECSection.RISK_FACTORS,
    SECSection.USE_OF_PROCEEDS,
    SECSection.DIVIDEND_POLICY,
    SECSection.CAPITALIZATION,
    SECSection.DILUTION,
    SECSection.MANAGEMENT_DISCUSSION,
    SECSection.BUSINESS,
    SECSection.MANAGEMENT,
    SECSection.COMPENSATION,
    SECSection.RELATED_PARTY_TRANSACTIONS,
    SECSection.PRINCIPAL_STOCKHOLDERS,
    SECSection.DESCRIPTION_OF_STOCK,
    SECSection.DESCRIPTION_OF_DEBT,
    SECSection.FUTURE_SALE,
    SECSection.US_TAX,
    SECSection.UNDERWRITING,
    SECSection.LEGAL_MATTERS,
    SECSection.EXPERTS,
    SECSection.MORE_INFORMATION,
)


def validate_section_names(section_names: List[str]):
    """傳回與定義的列舉不對應的章節名稱。"""
    if len(section_names) == 1 and section_names[0] == ALL_SECTIONS:
        return None
    elif len(section_names) > 1 and ALL_SECTIONS in section_names:
        raise ValueError(f"{ALL_SECTIONS} 不得與其他章節一起指定")

    invalid_names = [
        name for name in section_names if name not in section_string_to_enum
    ]
    if invalid_names:
        raise ValueError(f"下列章節名稱無效：{invalid_names}")
    return None