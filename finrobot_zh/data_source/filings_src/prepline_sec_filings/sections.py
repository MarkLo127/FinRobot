"""Module for defining/enumerating the common sections from SEC forms"""

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
    CERTAIN_TRADEMARKS = r"certain trademarks"
    OFFER_PRICE = r"(?:determination of )offering price"

    # 20-F specific sections
    INTRODUCTION = re.compile(r"^introduction$")
    PRESENTATION_OF_FINANCIAL_AND_OTHER_INFORMATION = re.compile(r"presentation of financial and other information")
    KEY_INFORMATION = re.compile(r"^key information$")
    INFORMATION_ON_THE_COMPANY = re.compile(r"information on the company")
    OPERATING_AND_FINANCIAL_REVIEW_AND_PROSPECTS = re.compile(r"operating and financial review and prospects")
    DIRECTORS_AND_SENIOR_MANAGEMENT = re.compile(r"directors and senior management")
    ADDITIONAL_INFORMATION = re.compile(r"^additional information$")

    @property
    def pattern(self):
        return self.value


ALL_SECTIONS = "_ALL"

section_string_to_enum = {enum.name: enum for enum in SECSection}

# NOTE(robinson) - Sections are listed in the following document from SEC
# ref: https://www.sec.gov/files/form10-k.pdf
SECTIONS_10K = (
    SECSection.BUSINESS,  # ITEM 1
    SECSection.RISK_FACTORS,  # ITEM 1A
    SECSection.UNRESOLVED_STAFF_COMMENTS,  # ITEM 1B
    SECSection.PROPERTIES,  # ITEM 2
    SECSection.LEGAL_PROCEEDINGS,  # ITEM 3
    SECSection.MINE_SAFETY,  # ITEM 4
    SECSection.MARKET_FOR_REGISTRANT_COMMON_EQUITY,  # ITEM 5
    SECSection.MANAGEMENT_DISCUSSION,  # ITEM 7
    SECSection.MARKET_RISK_DISCLOSURES,  # ITEM 7A
    SECSection.FINANCIAL_STATEMENTS,  # ITEM 8
    SECSection.ACCOUNTING_DISAGREEMENTS,  # ITEM 9
    SECSection.CONTROLS_AND_PROCEDURES,  # ITEM 9A
    SECSection.FOREIGN_JURISDICTIONS,  # ITEM 9C
    SECSection.MANAGEMENT,  # ITEM 10
    SECSection.COMPENSATION,  # ITEM 11
    SECSection.PRINCIPAL_STOCKHOLDERS,  # ITEM 12
    SECSection.RELATED_PARTY_TRANSACTIONS,  # ITEM 13
    SECSection.ACCOUNTING_FEES,  # ITEM 14
    SECSection.EXHIBITS,  # ITEM 15
    SECSection.FORM_SUMMARY,  # ITEM 16
)

# NOTE(robinson) - Sections are listed in the following document from SEC
# ref: https://www.sec.gov/files/form10-q.pdf
SECTIONS_10Q = (
    SECSection.FINANCIAL_STATEMENTS,  # ITEM 1
    SECSection.MANAGEMENT_DISCUSSION,  # ITEM 2
    SECSection.MARKET_RISK_DISCLOSURES,  # ITEM 3
    SECSection.CONTROLS_AND_PROCEDURES,  # ITEM 4
    SECSection.LEGAL_PROCEEDINGS,  # ITEM 1
    SECSection.RISK_FACTORS,  # ITEM 1A
    SECSection.USE_OF_PROCEEDS,  # ITEM 2
    SECSection.DEFAULTS,  # ITEM 3
    SECSection.MINE_SAFETY,  # ITEM 4
    SECSection.OTHER_INFORMATION,  # ITEM 5
)

# NOTE - Sections are listed in the following document from SEC
# ref: https://www.sec.gov/files/form20-f.pdf
SECTIONS_20F = (
    SECSection.INTRODUCTION,  # ITEM 1
    SECSection.PRESENTATION_OF_FINANCIAL_AND_OTHER_INFORMATION,  # ITEM 2
    SECSection.KEY_INFORMATION,  # ITEM 3
    SECSection.INFORMATION_ON_THE_COMPANY,  # ITEM 4
    SECSection.OPERATING_AND_FINANCIAL_REVIEW_AND_PROSPECTS,  # ITEM 5
    SECSection.DIRECTORS_AND_SENIOR_MANAGEMENT,  # ITEM 6
    SECSection.ADDITIONAL_INFORMATION,  # ITEM 7
)

def validate_section_names(section_names: List[str]):
    """Return section names that don't correspond to a defined enum."""
    if len(section_names) == 1 and section_names[0] == ALL_SECTIONS:
        return None
    elif len(section_names) > 1 and ALL_SECTIONS in section_names:
        raise ValueError(f"{ALL_SECTIONS} may not be specified with other sections")

    invalid_names = [
        name for name in section_names if name not in section_string_to_enum
    ]
    if invalid_names:
        raise ValueError(f"The following section names are not valid: {invalid_names}")
    return None
