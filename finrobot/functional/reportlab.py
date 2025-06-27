# -*- coding: utf-8 -*-
import os
import traceback
from reportlab.lib import colors
from reportlab.lib import pagesizes
from reportlab.platypus import (
    SimpleDocTemplate,
    Frame,
    Paragraph,
    Image,
    PageTemplate,
    FrameBreak,
    Spacer,
    Table,
    TableStyle,
    NextPageTemplate,
    PageBreak,
)
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from ..data_source import FMPUtils, YFinanceUtils
from .analyzer import ReportAnalysisUtils
from typing import Annotated

# 註冊字體
font_dir = os.path.join(os.path.dirname(__file__), 'LXGW_WenKai_TC,Noto_Serif_TC')

# 註冊 Noto Serif TC 字體
noto_serif_tc_path = os.path.join(font_dir, 'Noto_Serif_TC', 'static')
pdfmetrics.registerFont(TTFont('NotoSerifTC-Regular', os.path.join(noto_serif_tc_path, 'NotoSerifTC-Regular.ttf')))
pdfmetrics.registerFont(TTFont('NotoSerifTC-Bold', os.path.join(noto_serif_tc_path, 'NotoSerifTC-Bold.ttf')))

# 註冊 LXGW WenKai TC 字體
lxgw_wenkai_tc_path = os.path.join(font_dir, 'LXGW_WenKai_TC')
pdfmetrics.registerFont(TTFont('LXGWWenKaiTC-Regular', os.path.join(lxgw_wenkai_tc_path, 'LXGWWenKaiTC-Regular.ttf')))
pdfmetrics.registerFont(TTFont('LXGWWenKaiTC-Bold', os.path.join(lxgw_wenkai_tc_path, 'LXGWWenKaiTC-Bold.ttf')))


class ReportLabUtils:

    def build_annual_report(
        ticker_symbol: Annotated[str, "股票代碼"],
        save_path: Annotated[str, "年度報告 PDF 的儲存路徑"],
        operating_results: Annotated[
            str,
            "文字段落：公司財務報告中的收入摘要",
        ],
        market_position: Annotated[
            str,
            "文字段落：公司的當前狀況和終端市場（地理位置）、主要客戶（是否為藍籌股）、來自財務報告的市場份額，避免與業務概覽部分生成的類似句子，將其分類為兩者之一",
        ],
        business_overview: Annotated[
            str,
            "文字段落：公司的描述和業務亮點，來自其財務報告",
        ],
        risk_assessment: Annotated[
            str,
            "文字段落：公司的風險評估，來自其財務報告",
        ],
        competitors_analysis: Annotated[
            str,
            "文字段落：公司的競爭對手分析，來自其財務報告和競爭對手的財務報告",
        ],
    ) -> str:
        """
        使用 ReportLab 建立公司的年度報告 PDF。
        """
        try:
            # 創建 PDF 文件
            doc = SimpleDocTemplate(
                save_path,
                pagesize=pagesizes.letter,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=18,
            )

            # 獲取樣式表
            styles = getSampleStyleSheet()
            styles.add(
                ParagraphStyle(
                    name="Justify",
                    alignment=TA_JUSTIFY,
                    fontName="NotoSerifTC-Regular",
                    fontSize=10,
                )
            )
            styles.add(
                ParagraphStyle(
                    name="Title",
                    alignment=TA_CENTER,
                    fontName="NotoSerifTC-Bold",
                    fontSize=18,
                )
            )
            styles.add(
                ParagraphStyle(
                    name="Subtitle",
                    alignment=TA_LEFT,
                    fontName="NotoSerifTC-Bold",
                    fontSize=14,
                )
            )

            # 獲取公司資訊
            company_info = YFinanceUtils.get_stock_info(ticker_symbol)
            company_name = company_info.get("shortName", ticker_symbol)
            company_sector = company_info.get("sector", "")
            company_industry = company_info.get("industry", "")
            company_country = company_info.get("country", "")
            company_website = company_info.get("website", "")

            # 創建內容
            content = []

            # 標題
            content.append(Paragraph(f"{company_name} 年度報告", styles["Title"]))
            content.append(Spacer(1, 12))

            # 公司資訊表格
            company_info_data = [
                ["公司名稱", company_name],
                ["產業", company_sector],
                ["行業", company_industry],
                ["國家", company_country],
                ["網站", company_website],
            ]

            company_info_table = Table(company_info_data, colWidths=[100, 300])
            company_info_table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
                        ("TEXTCOLOR", (0, 0), (0, -1), colors.black),
                        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                        ("FONTNAME", (0, 0), (-1, -1), "NotoSerifTC-Regular"),
                        ("FONTSIZE", (0, 0), (-1, -1), 10),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                        ("TOPPADDING", (0, 0), (-1, -1), 6),
                        ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ]
                )
            )
            content.append(company_info_table)
            content.append(Spacer(1, 12))

            # 業務概覽
            content.append(Paragraph("業務概覽", styles["Subtitle"]))
            content.append(Spacer(1, 6))
            content.append(Paragraph(business_overview, styles["Justify"]))
            content.append(Spacer(1, 12))

            # 市場地位
            content.append(Paragraph("市場地位", styles["Subtitle"]))
            content.append(Spacer(1, 6))
            content.append(Paragraph(market_position, styles["Justify"]))
            content.append(Spacer(1, 12))

            # 營運結果
            content.append(Paragraph("營運結果", styles["Subtitle"]))
            content.append(Spacer(1, 6))
            content.append(Paragraph(operating_results, styles["Justify"]))
            content.append(Spacer(1, 12))

            # 競爭對手分析
            content.append(Paragraph("競爭對手分析", styles["Subtitle"]))
            content.append(Spacer(1, 6))
            content.append(Paragraph(competitors_analysis, styles["Justify"]))
            content.append(Spacer(1, 12))

            # 風險評估
            content.append(Paragraph("風險評估", styles["Subtitle"]))
            content.append(Spacer(1, 6))
            content.append(Paragraph(risk_assessment, styles["Justify"]))

            # 建立 PDF
            doc.build(content)
            return f"年度報告已成功建立並儲存至 {save_path}"

        except Exception as e:
            traceback.print_exc()
            return f"建立年度報告時發生錯誤：{str(e)}"
