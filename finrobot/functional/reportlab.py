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
from reportlab.pdfgen import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from ..data_source import FMPUtils, YFinanceUtils
from .analyzer import ReportAnalysisUtils
from typing import Annotated


class ReportLabUtils:

    def build_annual_report(
        ticker_symbol: Annotated[str, "股票代碼"],
        save_path: Annotated[str, "儲存年度報告 pdf 的路徑"],
        operating_results: Annotated[
            str,
            "一段文字：公司財務報告中的收入摘要",
        ],
        market_position: Annotated[
            str,
            "一段文字：公司目前的狀況和終端市場（地理位置）、主要客戶（是否為藍籌股）、其財務報告中的市佔率，避免與業務概覽部分中產生的類似句子，將其歸類為兩者之一",
        ],
        business_overview: Annotated[
            str,
            "一段文字：公司財務報告中的公司描述和業務亮點",
        ],
        risk_assessment: Annotated[
            str,
            "一段文字：公司財務報告中的風險評估",
        ],
        competitors_analysis: Annotated[
            str,
            "一段文字：公司財務報告和競爭對手財務報告中的競爭對手分析",
        ],
        share_performance_image_path: Annotated[
            str, "股價表現圖片的路徑"
        ],
        pe_eps_performance_image_path: Annotated[
            str, "本益比和每股盈餘表現圖片的路徑"
        ],
        filing_date: Annotated[str, "所分析財務報告的申報日期"],
    ) -> str:
        """
        將公司的業務概覽、市場地位、營運結果、
        風險評估、競爭對手分析以及股價表現、本益比和每股盈餘表現圖表全部匯總成一份 PDF 報告。
        """
        try:
            # 2. 建立 PDF 並插入圖片
            # 頁面設定
            page_width, page_height = pagesizes.A4
            left_column_width = page_width * 2 / 3
            right_column_width = page_width - left_column_width
            margin = 4

            # 建立 PDF 文件路徑
            pdf_path = (
                os.path.join(save_path, f"{ticker_symbol}_Equity_Research_report.pdf")
                if os.path.isdir(save_path)
                else save_path
            )
            os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
            doc = SimpleDocTemplate(pdf_path, pagesize=pagesizes.A4)
        
            # Register fonts
            font_path = os.path.join(os.path.dirname(__file__), '..', 'LXGW_WenKai_Mono_TC')
            pdfmetrics.registerFont(TTFont('LXGW-Regular', os.path.join(font_path, 'LXGWWenKaiMonoTC-Regular.ttf')))
            pdfmetrics.registerFont(TTFont('LXGW-Bold', os.path.join(font_path, 'LXGWWenKaiMonoTC-Bold.ttf')))
            pdfmetrics.registerFont(TTFont('LXGW-Light', os.path.join(font_path, 'LXGWWenKaiMonoTC-Light.ttf')))


            # 定義兩個欄位的 Frame
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

            #建立PageTemplate，並新增至文件
            page_template = PageTemplate(
                id="TwoColumns", frames=[frame_left, frame_right]
            )
            page_template_p2 = PageTemplate(
                id="TwoColumns_p2", frames=[frame_left_p2, frame_right_p2]
            )

             #定義單欄 Frame
            single_frame = Frame(
                margin,
                margin,
                page_width - 2 * margin,
                page_height - 2 * margin,
                id="single",
            )

            # 建立單欄 PageTemplate
            single_column_layout = PageTemplate(id="OneCol", frames=[single_frame])

            doc.addPageTemplates([page_template, single_column_layout, page_template_p2])

            styles = getSampleStyleSheet()

            # 自訂樣式
            custom_style = ParagraphStyle(
                name="Custom",
                parent=styles["Normal"],
                fontName="LXGW-Regular",
                fontSize=10,
                # leading=15,
                alignment=TA_JUSTIFY,
            )

            title_style = ParagraphStyle(
                name="TitleCustom",
                parent=styles["Title"],
                fontName="LXGW-Bold",
                fontSize=16,
                leading=20,
                alignment=TA_LEFT,
                spaceAfter=10,
            )

            subtitle_style = ParagraphStyle(
                name="Subtitle",
                parent=styles["Heading2"],
                fontName="LXGW-Bold",
                fontSize=14,
                leading=12,
                alignment=TA_LEFT,
                spaceAfter=6,
            )

            table_style2 = TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), colors.white),
                    ("BACKGROUND", (0, 0), (-1, 0), colors.white),
                    ("FONT", (0, 0), (-1, -1), "LXGW-Regular", 7),
                    ("FONT", (0, 0), (-1, 0), "LXGW-Bold", 14),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    # 所有儲存格左對齊
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    # 標題欄下方新增橫線
                    ("LINEBELOW", (0, 0), (-1, 0), 2, colors.black),
                    # 表格最下方新增橫線
                    ("LINEBELOW", (0, -1), (-1, -1), 2, colors.black),
                ]
            )

            name = YFinanceUtils.get_stock_info(ticker_symbol)["shortName"]

            # 準備左欄和右欄內容
            content = []
            # 標題
            content.append(
                Paragraph(
                    f"股票研究報告：{name}",
                    title_style,
                )
            )

            # 子標題
            content.append(Paragraph("業務概覽", subtitle_style))
            content.append(Paragraph(business_overview, custom_style))

            content.append(Paragraph("市場地位", subtitle_style))
            content.append(Paragraph(market_position, custom_style))
            
            content.append(Paragraph("營運結果", subtitle_style))
            content.append(Paragraph(operating_results, custom_style))

            # content.append(Paragraph("Summarization", subtitle_style))
            df = FMPUtils.get_financial_metrics(ticker_symbol, years=5)
            df.reset_index(inplace=True)
            currency = YFinanceUtils.get_stock_info(ticker_symbol)["currency"]
            df.rename(columns={"index": f"會計年度 ({currency} 百萬)"}, inplace=True)
            table_data = [["財務指標"]]
            table_data += [df.columns.to_list()] + df.values.tolist()

            col_widths = [(left_column_width - margin * 4) / df.shape[1]] * df.shape[1]
            table = Table(table_data, colWidths=col_widths)
            table.setStyle(table_style2)
            content.append(table)

            content.append(FrameBreak())  # 用於從左欄跳到右欄

            table_style = TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), colors.white),
                    ("BACKGROUND", (0, 0), (-1, 0), colors.white),
                    ("FONT", (0, 0), (-1, -1), "LXGW-Regular", 8),
                    ("FONT", (0, 0), (-1, 0), "LXGW-Bold", 12),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    # 第一欄左對齊
                    ("ALIGN", (0, 1), (0, -1), "LEFT"),
                    # 第二欄右對齊
                    ("ALIGN", (1, 1), (1, -1), "RIGHT"),
                    # 標題欄下方新增橫線
                    ("LINEBELOW", (0, 0), (-1, 0), 2, colors.black),
                ]
            )
            full_length = right_column_width - 2 * margin

            data = [
                ["FinRobot"],
                ["https://ai4finance.org/"],
                ["https://github.com/MarkLo127/FinRobot"],
                [f"報告日期：{filing_date}"],
            ]
            col_widths = [full_length]
            table = Table(data, colWidths=col_widths)
            table.setStyle(table_style)
            content.append(table)

            # content.append(Paragraph("", custom_style))
            content.append(Spacer(1, 0.15 * inch))
            key_data = ReportAnalysisUtils.get_key_data(ticker_symbol, filing_date)
            # 表格資料
            data = [["關鍵數據", ""]]
            data += [[k, v] for k, v in key_data.items()]
            col_widths = [full_length // 3 * 2, full_length // 3]
            table = Table(data, colWidths=col_widths)
            table.setStyle(table_style)
            content.append(table)

            # 將 Matplotlib 圖片新增至右欄

            # 歷史股價
            data = [["股價表現"]]
            col_widths = [full_length]
            table = Table(data, colWidths=col_widths)
            table.setStyle(table_style)
            content.append(table)

            plot_path = share_performance_image_path
            width = right_column_width
            height = width // 2
            content.append(Image(plot_path, width=width, height=height))

            # 歷史本益比和每股盈餘
            data = [["本益比和每股盈餘"]]
            col_widths = [full_length]
            table = Table(data, colWidths=col_widths)
            table.setStyle(table_style)
            content.append(table)

            plot_path = pe_eps_performance_image_path
            width = right_column_width
            height = width // 2
            content.append(Image(plot_path, width=width, height=height))

            # # 開始新的一頁
            content.append(NextPageTemplate("OneCol"))
            content.append(PageBreak())
            
            content.append(Paragraph("風險評估", subtitle_style))
            content.append(Paragraph(risk_assessment, custom_style))

            content.append(Paragraph("競爭對手分析", subtitle_style))
            content.append(Paragraph(competitors_analysis, custom_style))
            # def add_table(df, title):
            #     df = df.applymap(lambda x: "{:.2f}".format(x) if isinstance(x, float) else x)
            #     # df.columns = [col.strftime('%Y') for col in df.columns]
            #     # df.reset_index(inplace=True)
            #     # currency = ra.info['currency']
            #     df.rename(columns={"index": "segment"}, inplace=True)
            #     table_data = [[title]]
            #     table_data += [df.columns.to_list()] + df.values.tolist()

            #     table = Table(table_data)
            #     table.setStyle(table_style2)
            #     num_columns = len(df.columns)

            #     column_width = (page_width - 4 * margin) / (num_columns + 1)
            #     first_column_witdh = column_width * 2
            #     table._argW = [first_column_witdh] + [column_width] * (num_columns - 1)

            #     content.append(table)
            #     content.append(Spacer(1, 0.15 * inch))

            # if os.path.exists(f"{ra.project_dir}/outer_resource/"):
            #     Revenue10Q = pd.read_csv(
            #         f"{ra.project_dir}/outer_resource/Revenue10Q.csv",
            #     )
            #     # del Revenue10K['FY2018']
            #     # del Revenue10K['FY2019']
            #     add_table(Revenue10Q, "Revenue")

            #     Ratio10Q = pd.read_csv(
            #         f"{ra.project_dir}/outer_resource/Ratio10Q.csv",
            #     )
            #     # del Ratio10K['FY2018']
            #     # del Ratio10K['FY2019']
            #     add_table(Ratio10Q, "Ratio")

            #     Yoy10Q = pd.read_csv(
            #         f"{ra.project_dir}/outer_resource/Yoy10Q.csv",
            #     )
            #     # del Yoy10K['FY2018']
            #     # del Yoy10K['FY2019']
            #     add_table(Yoy10Q, "Yoy")

            #     plot_path = os.path.join(f"{ra.project_dir}/outer_resource/", "segment.png")
            #     width = page_width - 2 * margin
            #     height = width * 3 // 5
            #     content.append(Image(plot_path, width=width, height=height))

            # # 第二頁及之後內容，使用單欄佈局
            # df = ra.get_income_stmt()
            # df = df[df.columns[:3]]
            # def convert_if_money(value):
            #     if np.abs(value) >= 1000000:
            #         return value / 1000000
            #     else:
            #         return value

            # # 應用轉換函式到 DataFrame 的每列
            # df = df.applymap(convert_if_money)

            # df.columns = [col.strftime('%Y') for col in df.columns]
            # df.reset_index(inplace=True)
            # currency = ra.info['currency']
            # df.rename(columns={'index': f'FY ({currency} mn)'}, inplace=True)  # 可選：重命名索引列為「序號」
            # table_data = [["Income Statement"]]
            # table_data += [df.columns.to_list()] + df.values.tolist()

            # table = Table(table_data)
            # table.setStyle(table_style2)
            # content.append(table)

            # content.append(FrameBreak())  # 用於從左欄跳到右欄

            # df = ra.get_cash_flow()
            # df = df[df.columns[:3]]

            # df = df.applymap(convert_if_money)

            # df.columns = [col.strftime('%Y') for col in df.columns]
            # df.reset_index(inplace=True)
            # currency = ra.info['currency']
            # df.rename(columns={'index': f'FY ({currency} mn)'}, inplace=True)  # 可選：重命名索引列為「序號」
            # table_data = [["Cash Flow Sheet"]]
            # table_data += [df.columns.to_list()] + df.values.tolist()

            # table = Table(table_data)
            # table.setStyle(table_style2)
            # content.append(table)
            # # content.append(Paragraph('This is a single column on the second page', custom_style))
            # # content.append(Spacer(1, 0.2*inch))
            # # content.append(Paragraph('More content in the single column.', custom_style))

            # 建構 PDF 文件
            doc.build(content)

            return "年度報告已成功產生。"

        except Exception:
            return traceback.format_exc()