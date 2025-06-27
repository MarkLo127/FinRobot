# -*- coding: utf-8 -*-
import os
from textwrap import dedent
from typing import Annotated, List
from datetime import timedelta, datetime
from ..data_source import YFinanceUtils, SECUtils, FMPUtils


def combine_prompt(instruction, resource, table_str=None):
    if table_str:
        prompt = f"{table_str}\n\n資源：{resource}\n\n指令：{instruction}"
    else:
        prompt = f"資源：{resource}\n\n指令：{instruction}"
    return prompt


def save_to_file(data: str, file_path: str):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as f:
        f.write(data)


class ReportAnalysisUtils:

    def analyze_income_stmt(
        ticker_symbol: Annotated[str, "股票代碼"],
        fyear: Annotated[str, "10-K 報告的會計年度"],
        save_path: Annotated[str, "儲存返回指令與資源的文字檔案路徑"]
    ) -> str:
        """
        檢索給定股票代碼的損益表及其 10-K 報告的相關部分。
        然後返回如何分析損益表的指令。
        """
        # 檢索損益表
        income_stmt = YFinanceUtils.get_income_stmt(ticker_symbol)
        df_string = "損益表：\n" + income_stmt.to_string().strip()

        # 分析指令
        instruction = dedent(
            """
            對公司當前會計年度的損益表進行全面分析。
            從整體營收記錄開始，包括年比年或季比季比較，
            並分解營收來源以識別主要貢獻者和趨勢。檢查銷售成本
            以發現潛在的成本控制問題。審查利潤率，如毛利率、營業利潤率
            和淨利潤率，以評估成本效率、營運效果和整體盈利能力。
            分析每股收益以了解投資者觀點。將這些指標與歷史
            數據以及行業或競爭對手基準進行比較，以識別增長模式、盈利趨勢和
            營運挑戰。輸出應該是公司財務健康狀況的戰略概述，
            在單一段落中，少於 130 字，將前述分析總結為 4-5 個關鍵點，
            在各自的副標題下進行具體討論並提供強有力的數據支持。
            """
        )

        # 從 10-K 報告中檢索相關章節
        section_text = SECUtils.get_10k_section(ticker_symbol, fyear, 7)

        # 結合指令、章節文本和損益表
        prompt = combine_prompt(instruction, section_text, df_string)

        save_to_file(prompt, save_path)
        return f"指令與資源已儲存至 {save_path}"

    def analyze_balance_sheet(
        ticker_symbol: Annotated[str, "股票代碼"],
        fyear: Annotated[str, "10-K 報告的會計年度"],
        save_path: Annotated[str, "儲存返回指令與資源的文字檔案路徑"]
    ) -> str:
        """
        檢索給定股票代碼的資產負債表及其 10-K 報告的相關部分。
        然後返回如何分析資產負債表的指令。
        """
        balance_sheet = YFinanceUtils.get_balance_sheet(ticker_symbol)
        df_string = "資產負債表：\n" + balance_sheet.to_string().strip()

        instruction = dedent(
            """
            深入詳細審查公司最近會計年度的資產負債表，精確定位
            資產、負債和股東權益的結構，以解讀公司的財務穩定性和
            營運效率。重點評估流動性，通過流動資產與流動負債的比較，
            通過長期債務比率評估償債能力，以及權益狀況以衡量長期投資潛力。
            將這些指標與前幾年的數據進行對比，以突出財務趨勢、改善或惡化。
            最後對公司的財務槓桿、資產管理和資本結構進行戰略評估，
            在單一段落中提供對其財務健康和未來前景的洞察。少於 130 字。
            """
        )

        section_text = SECUtils.get_10k_section(ticker_symbol, fyear, 7)
        prompt = combine_prompt(instruction, section_text, df_string)
        save_to_file(prompt, save_path)
        return f"指令與資源已儲存至 {save_path}"

    def analyze_cash_flow(
        ticker_symbol: Annotated[str, "股票代碼"],
        fyear: Annotated[str, "10-K 報告的會計年度"],
        save_path: Annotated[str, "儲存返回指令與資源的文字檔案路徑"]
    ) -> str:
        """
        檢索給定股票代碼的現金流量表及其 10-K 報告的相關部分。
        然後返回如何分析現金流量表的指令。
        """
        cash_flow = YFinanceUtils.get_cash_flow(ticker_symbol)
        df_string = "現金流量表：\n" + cash_flow.to_string().strip()

        instruction = dedent(
            """
            深入全面評估公司最新會計年度的現金流，重點關注營運、投資
            和融資活動的現金流入和流出。檢查營運現金流以評估
            核心業務盈利能力，仔細審查投資活動以洞察資本支出和投資，
            並審查融資活動以了解債務、股權變動和股利政策。將這些現金變動
            與前期進行比較，以辨別趨勢、可持續性和流動性風險。最後對公司的
            現金管理效果、流動性狀況和未來增長或財務挑戰的潛力進行知情分析，
            在單一段落中。少於 130 字。
            """
        )

        section_text = SECUtils.get_10k_section(ticker_symbol, fyear, 7)
        prompt = combine_prompt(instruction, section_text, df_string)
        save_to_file(prompt, save_path)
        return f"指令與資源已儲存至 {save_path}"

    def analyze_segment_stmt(
        ticker_symbol: Annotated[str, "股票代碼"],
        fyear: Annotated[str, "10-K 報告的會計年度"],
        save_path: Annotated[str, "儲存返回指令與資源的文字檔案路徑"]
    ) -> str:
        """
        檢索給定股票代碼的損益表及其 10-K 報告的相關部分。
        然後返回如何創建部門分析的指令。
        """
        income_stmt = YFinanceUtils.get_income_stmt(ticker_symbol)
        df_string = (
            "損益表（部門分析）：\n" + income_stmt.to_string().strip()
        )

        instruction = dedent(
            """
            識別公司的業務部門，並使用管理層討論與分析
            和損益表創建部門分析，按部門細分並有清晰的標題。處理營收和淨利潤的具體數據，
            並計算變化。詳述戰略夥伴關係及其影響，包括公司或組織等詳細信息。
            描述產品創新及其對收入增長的影響。量化市場份額及其變化，或說明市場地位
            及其變化。分析市場動態和利潤挑戰，注意國家政策變化的任何影響。包括成本方面，
            詳述營運成本、創新投資和渠道擴張等費用。用證據支持每個陳述，
            保持每個部門分析簡潔且少於 60 字，準確引用信息。對於每個部門，將最
            重要的發現整合為一個清晰、簡潔的段落，排除不太重要或描述模糊的方面以確保清晰性和
            依賴基於證據的信息。對於每個部門，輸出應該是 150 字以內的單一段落。
            """
        )
        section_text = SECUtils.get_10k_section(ticker_symbol, fyear, 7)
        prompt = combine_prompt(instruction, section_text, df_string)
        save_to_file(prompt, save_path)
        return f"指令與資源已儲存至 {save_path}"

    def income_summarization(
        ticker_symbol: Annotated[str, "股票代碼"],
        fyear: Annotated[str, "10-K 報告的會計年度"],
        income_stmt_analysis: Annotated[str, "深度損益表分析"],
        segment_analysis: Annotated[str, "深度部門分析"],
        save_path: Annotated[str, "儲存返回指令與資源的文字檔案路徑"]
    ) -> str:
        """
        使用給定股票代碼的損益表和部門分析。
        然後返回如何將這些分析綜合為單一連貫段落的指令。
        """
        # income_stmt_analysis = analyze_income_stmt(ticker_symbol)
        # segment_analysis = analyze_segment_stmt(ticker_symbol)

        instruction = dedent(
            f"""
            損益表分析：{income_stmt_analysis}，
            部門分析：{segment_analysis}，
            將深度損益表分析和部門分析的發現綜合為單一、連貫的段落。
            它應該基於事實和數據驅動。首先，呈現和評估整體營收和利潤狀況，注意重要
            趨勢和變化。其次，檢查各業務部門的表現，重點關注其營收和
            利潤變化、營收貢獻和市場動態。對於前兩個領域未涵蓋的信息，識別並
            整合與營運、潛在風險和增長與穩定戰略機會相關的關鍵發現到分析中。
            對於每個部分，整合歷史數據比較並提供相關事實、指標或數據作為證據。整個綜合
            應該呈現為連續段落，不使用項目符號。為每個關鍵點使用副標題和編號。
            總輸出應少於 160 字。
            """
        )

        section_text = SECUtils.get_10k_section(ticker_symbol, fyear, 7)
        prompt = combine_prompt(instruction, section_text, "")
        save_to_file(prompt, save_path)
        return f"指令與資源已儲存至 {save_path}"

    def get_risk_assessment(
        ticker_symbol: Annotated[str, "股票代碼"],
        fyear: Annotated[str, "10-K 報告的會計年度"],
        save_path: Annotated[str, "儲存返回指令與資源的文字檔案路徑"]
    ) -> str:
        """
        檢索給定股票代碼的風險因素及其 10-K 報告的相關部分。
        然後返回如何總結公司前 3 大關鍵風險的指令。
        """
        company_name = YFinanceUtils.get_stock_info(ticker_symbol)["shortName"]
        risk_factors = SECUtils.get_10k_section(ticker_symbol, fyear, "1A")
        section_text = (
            "公司名稱："
            + company_name
            + "\n\n"
            + "風險因素：\n"
            + risk_factors
            + "\n\n"
        )
        instruction = (
            """
            根據 10-K 報告中提供的信息，總結公司的前 3 大關鍵風險。
            然後，對於每個關鍵風險，將風險評估分解為以下方面：
            1. 行業垂直風險：這個行業垂直與其他行業在風險方面如何比較？考慮監管、市場波動和競爭格局等因素。
            2. 週期性：這個行業的週期性如何？討論經濟週期對公司表現的影響。
            3. 風險量化：如果公司或部門被認為有風險，請列舉關鍵風險因素並提供支持數據。
            4. 下行保護：如果公司或部門風險較低，請討論現有的下行保護。考慮多元化、長期合約和政府監管等因素。

            最後，提供詳細且細緻的評估，反映公司真實的風險格局。避免在回應中使用任何項目符號。
            """
        )
        prompt = combine_prompt(instruction, section_text, "")
        save_to_file(prompt, save_path)
        return f"指令與資源已儲存至 {save_path}"
        
    def get_competitors_analysis(
        ticker_symbol: Annotated[str, "股票代碼"], 
        competitors: Annotated[List[str], "競爭對手公司"],
        fyear: Annotated[str, "10-K 報告的會計年度"], 
        save_path: Annotated[str, "儲存返回指令與資源的文字檔案路徑"]
    ) -> str:
        """
        分析公司與其競爭對手之間的財務指標差異。
        準備分析提示並將其保存到檔案中。
        """
        # 檢索財務數據
        financial_data = FMPUtils.get_competitor_financial_metrics(ticker_symbol, competitors, years=4)

        # 構建財務數據摘要
        table_str = ""
        for metric in financial_data[ticker_symbol].index:
            table_str += f"\n\n{metric}：\n"
            company_value = financial_data[ticker_symbol].loc[metric]
            table_str += f"{ticker_symbol}：{company_value}\n"
            for competitor in competitors:
                competitor_value = financial_data[competitor].loc[metric]
                table_str += f"{competitor}：{competitor_value}\n"

        # 準備分析指令
        instruction = dedent(
          """
          分析 {company}/ticker_symbol 及其競爭對手：{competitors} 在多年間（以 0、1、2、3 表示，其中 0 為最新年份，3 為最早年份）的財務指標。重點關注以下指標：EBITDA 利潤率、企業價值/EBITDA、自由現金流轉換率、毛利率、投資資本回報率、營收和營收成長。
          對於每年：年比年趨勢：識別並討論 {company} 從最早年份（3）到最新年份（0）每個指標的趨勢。但在生成分析時，您需要寫明 1：年份 3 = 2023 年，2：年份 2 = 2022 年，3：年份 1 = 2021 年，4：年份 0 = 2020 年。突出這些指標隨時間的任何重大改善、下降或穩定。
          競爭對手比較：對於每年，將 {company} 與其 {competitors} 在每個指標上進行比較。評估 {company} 相對於其 {competitors} 的表現，注意其表現優於或落後的地方。
          指標特定洞察：

          EBITDA 利潤率：討論 {company} 相對於其 {competitors} 的盈利能力，特別是在最近一年。
          企業價值/EBITDA：提供關於估值的洞察，以及 {company} 在每年相對於其 {competitors} 是被高估還是低估。
          自由現金流轉換率：評估 {company} 相對於其 {competitors} 隨時間的現金流效率。
          毛利率：分析每年的成本效率和盈利能力。
          投資資本回報率：討論投資資本回報率以及它對公司從投資中產生回報效率的建議，特別關注最近趨勢。
          營收和營收成長：提供 {company} 營收表現和成長軌跡的全面視圖，注意任何重大變化或模式。
          結論：基於這些指標總結 {company} 的整體財務健康狀況。討論 {company} 在這些年份和這些指標上的表現如何可能證明或反駁其當前市場估值（如企業價值/EBITDA 比率所反映）。
          避免使用任何項目符號。
          """
        )

        # 結合提示
        company_name = ticker_symbol  # 假設股票代碼就是公司名稱，否則檢索它。
        resource = f"{company_name} 和 {competitors} 的財務指標。"
        prompt = combine_prompt(instruction, resource, table_str)

        # 將指令和資源保存到檔案
        save_to_file(prompt, save_path)
        
        return f"指令與資源已儲存至 {save_path}"
        
    def analyze_business_highlights(
        ticker_symbol: Annotated[str, "股票代碼"],
        fyear: Annotated[str, "10-K 報告的會計年度"],
        save_path: Annotated[str, "儲存返回指令與資源的文字檔案路徑"]
    ) -> str:
        """
        檢索給定股票代碼的業務摘要及其 10-K 報告的相關部分。
        然後返回如何描述公司各業務的績效亮點的指令。
        """
        business_summary = SECUtils.get_10k_section(ticker_symbol, fyear, 1)
        section_7 = SECUtils.get_10k_section(ticker_symbol, fyear, 7)
        section_text = (
            "業務摘要：\n"
            + business_summary
            + "\n\n"
            + "管理層對財務狀況和營運結果的討論與分析：\n"
            + section_7
        )
        instruction = dedent(
            """
            根據提供的信息，描述公司各業務線的績效亮點。
            每個業務描述應包含一句總結和一句解釋。
            """
        )
        prompt = combine_prompt(instruction, section_text, "")
        save_to_file(prompt, save_path)
        return f"指令與資源已儲存至 {save_path}"

    def analyze_company_description(
        ticker_symbol: Annotated[str, "股票代碼"],
        fyear: Annotated[str, "10-K 報告的會計年度"],
        save_path: Annotated[str, "儲存返回指令與資源的文字檔案路徑"]
    ) -> str:
        """
        檢索給定股票代碼的公司描述及其 10-K 報告的相關部分。
        然後返回如何描述公司的行業、優勢、趨勢和戰略舉措的指令。
        """
        company_name = YFinanceUtils.get_stock_info(ticker_symbol).get(
            "shortName", "N/A"
        )
        business_summary = SECUtils.get_10k_section(ticker_symbol, fyear, 1)
        section_7 = SECUtils.get_10k_section(ticker_symbol, fyear, 7)
        section_text = (
            "公司名稱："
            + company_name
            + "\n\n"
            + "業務摘要：\n"
            + business_summary
            + "\n\n"
            + "管理層對財務狀況和營運結果的討論與分析：\n"
            + section_7
        )
        instruction = dedent(
            """
            根據提供的信息，
            1. 簡要描述公司概況和公司的行業，使用結構："成立於 xxxx 年，'公司名稱' 是一家 xxxx，提供 .....
            2. 突出核心優勢和競爭優勢、關鍵產品或服務，
            3. 包括關於終端市場（地理位置）、主要客戶（是否為藍籌股）、市場地位部分的市場份額等主題，
            4. 識別影響公司戰略的當前行業趨勢、機會和挑戰，
            5. 概述最近的戰略舉措，如產品發布、收購或新夥伴關係，並描述公司對市場條件的回應。
            少於 300 字。
            """
        )
        step_prompt = combine_prompt(instruction, section_text, "")
        instruction2 = "總結分析，少於 130 字。"
        prompt = combine_prompt(instruction=instruction2, resource=step_prompt)
        save_to_file(prompt, save_path)
        return f"指令與資源已儲存至 {save_path}"

    def get_key_data(
        ticker_symbol: Annotated[str, "股票代碼"],
        filing_date: Annotated[
            str | datetime, "正在分析的財務報告的申報日期"
        ],
    ) -> dict:
        """
        返回給定股票代碼和申報日期在年度報告中使用的關鍵財務數據
        """

        if not isinstance(filing_date, datetime):
            filing_date = datetime.strptime(filing_date, "%Y-%m-%d")

        # 獲取過去 6 個月的歷史市場數據
        start = (filing_date - timedelta(weeks=52)).strftime("%Y-%m-%d")
        end = filing_date.strftime("%Y-%m-%d")

        hist = YFinanceUtils.get_stock_data(ticker_symbol, start, end)

        # 獲取其他相關信息
        info = YFinanceUtils.get_stock_info(ticker_symbol)
        close_price = hist["Close"].iloc[-1]

        # 計算平均每日交易量
        six_months_start = (filing_date - timedelta(weeks=26)).strftime("%Y-%m-%d")
        hist_last_6_months = hist[
            (hist.index >= six_months_start) & (hist.index <= end)
        ]

        # 計算這 6 個月的平均每日交易量
        avg_daily_volume_6m = (
            hist_last_6_months["Volume"].mean()
            if not hist_last_6_months["Volume"].empty
            else 0
        )

        fiftyTwoWeekLow = hist["High"].min()
        fiftyTwoWeekHigh = hist["Low"].max()

        # avg_daily_volume_6m = hist['Volume'].mean()

        # 轉換回字串以供函數調用
        filing_date = filing_date.strftime("%Y-%m-%d")

        # 打印結果
        # print(f"在過去 6 個月中，{ticker_symbol} 的平均每日交易量為：{avg_daily_volume_6m:.2f}")
        rating, _ = YFinanceUtils.get_analyst_recommendations(ticker_symbol)
        target_price = FMPUtils.get_target_price(ticker_symbol, filing_date)
        result = {
            "評級": rating,
            "目標價格": target_price,
            f"6個月平均每日交易量 ({info['currency']}百萬)": "{:.2f}".format(
                avg_daily_volume_6m / 1e6
            ),
            f"收盤價 ({info['currency']})": "{:.2f}".format(close_price),
            f"市值 ({info['currency']}百萬)": "{:.2f}".format(
                FMPUtils.get_historical_market_cap(ticker_symbol, filing_date) / 1e6
            ),
            f"52週價格區間 ({info['currency']})": "{:.2f} - {:.2f}".format(
                fiftyTwoWeekLow, fiftyTwoWeekHigh
            ),
            f"每股帳面價值 ({info['currency']})": "{:.2f}".format(
                FMPUtils.get_historical_bvps(ticker_symbol, filing_date)
            ),
        }
        return result
