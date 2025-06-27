# -*- coding: utf-8 -*-
# 10-K 表格的章節定義
SECTIONS_10K = (
    "BUSINESS",  # 項目 1 - 業務
    "RISK_FACTORS",  # 項目 1A - 風險因素
    "UNRESOLVED_STAFF_COMMENTS",  # 項目 1B - 未解決的員工意見
    "PROPERTIES",  # 項目 2 - 物業
    "LEGAL_PROCEEDINGS",  # 項目 3 - 法律程序
    "MINE_SAFETY",  # 項目 4 - 礦山安全
    "MARKET_FOR_REGISTRANT_COMMON_EQUITY",  # 項目 5 - 註冊人普通股市場
    # 注意：項目 6 是「保留」
    "MANAGEMENT_DISCUSSION",  # 項目 7 - 管理層討論
    "MARKET_RISK_DISCLOSURES",  # 項目 7A - 市場風險披露
    "FINANCIAL_STATEMENTS",  # 項目 8 - 財務報表
    "ACCOUNTING_DISAGREEMENTS",  # 項目 9 - 會計分歧
    "CONTROLS_AND_PROCEDURES",  # 項目 9A - 控制和程序
    # 注意：項目 9B 是其他信息
    "FOREIGN_JURISDICTIONS",  # 項目 9C - 外國司法管轄區
    "MANAGEMENT",  # 項目 10 - 管理層
    "COMPENSATION",  # 項目 11 - 薪酬
    "PRINCIPAL_STOCKHOLDERS",  # 項目 12 - 主要股東
    "RELATED_PARTY_TRANSACTIONS",  # 項目 13 - 關聯方交易
    "ACCOUNTING_FEES",  # 項目 14 - 會計費用
    "EXHIBITS",  # 項目 15 - 附件
    "FORM_SUMMARY",  # 項目 16 - 表格摘要
)

# 注意：章節列在 SEC 的以下文件中
# 參考：https://www.sec.gov/files/form10-q.pdf
SECTIONS_10Q = (
    # 第一部分 - 財務信息
    "FINANCIAL_STATEMENTS",  # 項目 1 - 財務報表
    "MANAGEMENT_DISCUSSION",  # 項目 2 - 管理層討論
    "MARKET_RISK_DISCLOSURES",  # 項目 3 - 市場風險披露
    "CONTROLS_AND_PROCEDURES",  # 項目 4 - 控制和程序
    # 第二部分 - 其他信息
    "LEGAL_PROCEEDINGS",  # 項目 1 - 法律程序
    "RISK_FACTORS",  # 項目 1A - 風險因素
    "USE_OF_PROCEEDS",  # 項目 2 - 資金用途
    "DEFAULTS",  # 項目 3 - 違約
    "MINE_SAFETY",  # 項目 4 - 礦山安全
    "OTHER_INFORMATION",  # 項目 5 - 其他信息
)

# S-1 表格的章節定義
SECTIONS_S1 = [
    "PROSPECTUS_SUMMARY",  # 招股說明書摘要
    "ABOUT_PROSPECTUS",  # 關於招股說明書
    "FORWARD_LOOKING_STATEMENTS",  # 前瞻性陳述
    "RISK_FACTORS",  # 風險因素
    "USE_OF_PROCEEDS",  # 資金用途
    "DIVIDEND_POLICY",  # 股利政策
    "CAPITALIZATION",  # 資本化
    "DILUTION",  # 稀釋
    "MANAGEMENT_DISCUSSION",  # 管理層討論
    "BUSINESS",  # 業務
    "MANAGEMENT",  # 管理層
    "COMPENSATION",  # 薪酬
    "RELATED_PARTY_TRANSACTIONS",  # 關聯方交易
    "PRINCIPAL_STOCKHOLDERS",  # 主要股東
    "DESCRIPTION_OF_STOCK",  # 股票描述
    "DESCRIPTION_OF_DEBT",  # 債務描述
    "FUTURE_SALE",  # 未來銷售
    "US_TAX",  # 美國稅務
    "UNDERWRITING",  # 承銷
    "LEGAL_MATTERS",  # 法律事務
    "EXPERTS",  # 專家
    "MORE_INFORMATION",  # 更多信息
]
