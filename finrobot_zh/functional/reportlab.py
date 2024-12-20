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
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase import pdfmetrics


from ..data_source import FMPUtils, YFinanceUtils
from .analyzer import ReportAnalysisUtils
from typing import Annotated

# 取得當前文件的目錄
current_dir = os.path.dirname(os.path.abspath(__file__))

# 直接從當前目錄建構字體路徑
regular_font_path = os.path.join(
    current_dir,
    "Noto_Sans_TC,Noto_Serif_TC",
    "Noto_Serif_TC",
    "NotoSerifTC-VariableFont_wght.ttf"
)

bold_font_path = os.path.join(
    current_dir,
    "Noto_Sans_TC,Noto_Serif_TC",
    "Noto_Serif_TC",
    "static",
    "NotoSerifTC-ExtraLight.ttf"
)

pdfmetrics.registerFont(TTFont("NotoSerifTC", regular_font_path))
pdfmetrics.registerFont(TTFont("NotoSerifTC-Bold", bold_font_path))

class ReportLabUtils:
    def build_annual_report(
        ticker_symbol: Annotated[str, "股票代碼，標識上市公司的唯一符號"],
        save_path: Annotated[str, "年度報告儲存的目標路徑，包含文件名及副檔名"],
        operating_results: Annotated[
            str,
            "來自財務報告的經營業績總結，涵蓋公司收入、利潤及其他關鍵財務指標的段落，字數介於150至550字之間",
        ],
        market_position: Annotated[
            str,
            "描述公司當前市場地位的段落，包括地理市場分佈、主要客戶群（如藍籌股客戶）、市場佔有率等資訊，避免與業務概述部分的內容重複，字數介於150至550字之間",
        ],
        business_overview: Annotated[
            str,
            "來自財務報告的公司業務概述，涵蓋公司描述、核心業務、主要業務亮點及發展戰略的段落，字數介於150至550字之間",
        ],
        risk_assessment: Annotated[
            str,
            "來自財務報告的風險評估段落，包含市場風險、運營風險、財務風險及其他潛在風險因素的分析，字數介於150至550字之間",
        ],
        competitors_analysis: Annotated[
            str,
            "基於公司及其主要競爭對手的財務報告，進行的競爭對手分析段落，涵蓋市場競爭格局、競爭優勢、劣勢及市場趨勢，字數介於150至550字之間",
        ],
        share_performance_image_path: Annotated[
            str, "股票表現圖表的檔案路徑，支援常見圖片格式（如PNG、JPEG）"
        ],
        pe_eps_performance_image_path: Annotated[
            str, "市盈率（P/E Ratio）及每股收益（EPS）表現圖表的檔案路徑，支援常見圖片格式（如PNG、JPEG）"
        ],
        filing_date: Annotated[str, "所分析財務報告的提交日期，格式為YYYY-MM-DD"],
    ) -> str:
        """
        彙總並生成公司的年度報告，內容包括業務概述、市場地位、經營業績、
        風險評估、競爭對手分析，以及股票表現、市盈率和每股收益的圖表。
        最終報告將匯整上述資訊並保存為指定路徑的PDF文件。

        生成的每個段落字數介於150至550字之間，以確保報告內容詳盡且具可讀性。
        """
            
        try:
            # 2. 創建PDF並插入圖像
            # 頁面設置
            page_width, page_height = pagesizes.A4
            left_column_width = page_width * 2 / 3
            right_column_width = page_width - left_column_width
            margin = 4

            # 創建PDF文檔路徑
            pdf_path = (
                os.path.join(save_path, f"{ticker_symbol}_annual_report.pdf")
                if os.path.isdir(save_path)
                else save_path
            )
            os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
            doc = SimpleDocTemplate(pdf_path, pagesize=pagesizes.A4)

            # 定義兩個欄位的框架
            frame_left = Frame(
                margin,
                margin,
                left_column_width - margin * 2,
                page_height - margin * 2,
                id="left",
            )
            frame_right = Frame(
                left_column_width,
                margin,
                right_column_width - margin * 2,
                page_height - margin * 2,
                id="right",
            )

            single_frame = Frame(margin, margin, page_width-margin*2, page_height-margin*2, id='single')
            single_column_layout = PageTemplate(id='OneCol', frames=[single_frame])

            left_column_width_p2 = (page_width - margin * 3) // 2
            right_column_width_p2 = left_column_width_p2
            frame_left_p2 = Frame(
                margin,
                margin,
                left_column_width_p2 - margin * 2,
                page_height - margin * 2,
                id="left",
            )
            frame_right_p2 = Frame(
                left_column_width_p2,
                margin,
                right_column_width_p2 - margin * 2,
                page_height - margin * 2,
                id="right",
            )

            # 創建PageTemplate，並添加到文檔
            page_template = PageTemplate(
                id="TwoColumns", frames=[frame_left, frame_right]
            )
            page_template_p2 = PageTemplate(
                id="TwoColumns_p2", frames=[frame_left_p2, frame_right_p2]
            )

            # 定義單一欄位框架
            single_frame = Frame(
                margin,
                margin,
                page_width - 2 * margin,
                page_height - 2 * margin,
                id="single",
            )

            # 創建單一欄位PageTemplate
            single_column_layout = PageTemplate(id="OneCol", frames=[single_frame])

            doc.addPageTemplates([page_template, single_column_layout, page_template_p2])

            styles = getSampleStyleSheet()

            # 自訂樣式 - 增加了段落間距
            custom_style = ParagraphStyle(
                name="Custom",
                parent=styles["Normal"],
                fontName="NotoSerifTC",
                fontSize=10,
                alignment=TA_LEFT,
                leading=14,  # 行間距
                spaceBefore=12,  # 段落前間距
                spaceAfter=12,  # 段落後間距
            )

            title_style = ParagraphStyle(
                name="TitleCustom",
                parent=styles["Title"],
                fontName="NotoSerifTC-Bold",
                fontSize=16,
                leading=20,
                alignment=TA_LEFT,
                spaceBefore=16,  # 標題前間距
                spaceAfter=20,  # 標題後間距
                wordSpace=0.1,  # 加入字距設定
                charSpace=0,    # 加入字元間距設定
            )

            subtitle_style = ParagraphStyle(
                name="Subtitle",
                parent=styles["Heading2"],
                fontName="NotoSerifTC-Bold",
                fontSize=14,
                leading=16,
                alignment=TA_LEFT,
                spaceBefore=14,  # 子標題前間距
                spaceAfter=10,  # 子標題後間距
            )

            table_style2 = TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), colors.white),
                    ("BACKGROUND", (0, 0), (-1, 0), colors.white),
                    ("FONT", (0, 0), (-1, -1), "NotoSerifTC", 7),
                    ("FONT", (0, 0), (-1, 0), "NotoSerifTC-Bold", 14),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    # 所有單元格左對齊
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    # 標題欄下方添加橫線
                    ("LINEBELOW", (0, 0), (-1, 0), 2, colors.black),
                    # 表格最下方添加橫線
                    ("LINEBELOW", (0, -1), (-1, -1), 2, colors.black),
                ]
            )

            name = YFinanceUtils.get_stock_info(ticker_symbol)["shortName"]

            # 準備左欄和右欄內容
            content = []
            # 標題
            content.append(
                Paragraph(
                    f"{name}",
                    title_style,
                )
            )

            # 子標題和內容，在每個段落後添加間距
            content.append(Paragraph("業務概述", subtitle_style))
            content.append(Paragraph(business_overview, custom_style))
            content.append(Spacer(1, 0.2 * inch))  # 添加額外間距

            content.append(Paragraph("市場地位", subtitle_style))
            content.append(Paragraph(market_position, custom_style))
            content.append(Spacer(1, 0.2 * inch))  # 添加額外間距
            
            content.append(Paragraph("經營業績", subtitle_style))
            content.append(Paragraph(operating_results, custom_style))
            content.append(Spacer(1, 0.2 * inch))  # 添加額外間距

            df = FMPUtils.get_financial_metrics(ticker_symbol, years=5)
            df.reset_index(inplace=True)
            currency = YFinanceUtils.get_stock_info(ticker_symbol)["currency"]
            df.rename(columns={"index": f"年度({currency}/百萬)"}, inplace=True)
            table_data = [["財務指標"]]
            table_data += [df.columns.to_list()] + df.values.tolist()

            col_widths = [(left_column_width - margin * 4) / df.shape[1]] * df.shape[1]
            table = Table(table_data, colWidths=col_widths)
            table.setStyle(table_style2)
            content.append(table)
            content.append(Spacer(1, 0.2 * inch))  # 添加表格後間距

            content.append(FrameBreak())  # 用於從左欄跳到右欄

            table_style = TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), colors.white),
                    ("BACKGROUND", (0, 0), (-1, 0), colors.white),
                    ("FONT", (0, 0), (-1, -1), "NotoSerifTC", 8),
                    ("FONT", (0, 0), (-1, 0), "NotoSerifTC-Bold", 12),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    # 第一欄左對齊
                    ("ALIGN", (0, 1), (0, -1), "LEFT"),
                    # 第二欄右對齊
                    ("ALIGN", (1, 1), (1, -1), "RIGHT"),
                    # 標題欄下方添加橫線
                    ("LINEBELOW", (0, 0), (-1, 0), 2, colors.black),
                ]
            )
            full_length = right_column_width - 2 * margin

            data = [
                ["finrobot_zh"],
                [f"報告日期：{filing_date}"],
            ]
            col_widths = [full_length]
            table = Table(data, colWidths=col_widths)
            table.setStyle(table_style)
            content.append(table)

            content.append(Spacer(1, 0.25 * inch))  # 增加間距

            key_data = ReportAnalysisUtils.get_key_data(ticker_symbol, filing_date)
            # 表格資料
            data = [["關鍵數據", ""]]
            data += [[k, v] for k, v in key_data.items()]
            col_widths = [full_length // 3 * 2, full_length // 3]
            table = Table(data, colWidths=col_widths)
            table.setStyle(table_style)
            content.append(table)
            content.append(Spacer(1, 0.25 * inch))  # 增加間距

            # 歷史股價
            data = [["股票表現"]]
            col_widths = [full_length]
            table = Table(data, colWidths=col_widths)
            table.setStyle(table_style)
            content.append(table)

            plot_path = share_performance_image_path
            width = right_column_width
            height = width // 2
            content.append(Image(plot_path, width=width, height=height))
            content.append(Spacer(1, 0.25 * inch))  # 增加間距

            # 歷史市盈率和每股收益
            data = [["市盈率及每股收益"]]
            col_widths = [full_length]
            table = Table(data, colWidths=col_widths)
            table.setStyle(table_style)
            content.append(table)

            plot_path = pe_eps_performance_image_path
            width = right_column_width
            height = width // 2
            content.append(Image(plot_path, width=width, height=height))
            content.append(Spacer(1, 0.25 * inch))  # 增加間距

            # 開始新的一頁
            content.append(NextPageTemplate("OneCol"))
            content.append(PageBreak())
            
            content.append(Paragraph("風險評估", subtitle_style))
            content.append(Paragraph(risk_assessment, custom_style))
            content.append(Spacer(1, 0.25 * inch))  # 增加間距

            content.append(Paragraph("競爭對手分析", subtitle_style))
            content.append(Paragraph(competitors_analysis, custom_style))

            # 構建PDF文檔
            doc.build(content)

            return "年度報告生成成功。"

        except Exception:
            return traceback.format_exc()