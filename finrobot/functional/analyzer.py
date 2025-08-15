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
        save_path: Annotated[str, "寫入傳回指令和資源的 txt 檔案路徑。"]
    ) -> str:
        """
        擷取指定股票代碼的損益表及其 10-K 報告的相關部分。
        然後傳回如何分析損益表的說明。
        """
        # 擷取損益表
        income_stmt = YFinanceUtils.get_income_stmt(ticker_symbol)
        df_string = "損益表：\n" + income_stmt.to_string().strip()

        # 分析說明
        instruction = dedent(
            """
            對公司當前會計年度的損益表進行全面分析。
            從整體營收記錄開始，包括年增率或季增率比較，
            並細分營收來源以識別主要貢獻者和趨勢。檢查銷貨成本
            以找出潛在的成本控制問題。審查毛利率、營業利潤率
            和淨利率等利潤率，以評估成本效率、營運效益和整體獲利能力。
            分析每股盈餘以了解投資者觀點。將這些指標與歷史
            數據和產業或競爭對手基準進行比較，以識別成長模式、獲利趨勢和
            營運挑戰。輸出應為一段關於公司財務狀況的策略性概覽，
            少於 130 字，將先前的分析總結為 4-5 個重點，並在
            各自的副標題下提供具體的討論和強而有力的數據支持。
            """
        )

        # 從 10-K 報告中擷取相關部分
        section_text = SECUtils.get_10k_section(ticker_symbol, fyear, 7)

        # 合併說明、部分文字和損益表
        prompt = combine_prompt(instruction, section_text, df_string)

        save_to_file(prompt, save_path)
        return f"指令和資源已儲存至 {save_path}"

    def analyze_balance_sheet(
        ticker_symbol: Annotated[str, "股票代碼"],
        fyear: Annotated[str, "10-K 報告的會計年度"],
        save_path: Annotated[str, "寫入傳回指令和資源的 txt 檔案路徑。"]
    ) -> str:
        """
        擷取指定股票代碼的資產負債表及其 10-K 報告的相關部分。
        然後傳回如何分析資產負債表的說明。
        """
        balance_sheet = YFinanceUtils.get_balance_sheet(ticker_symbol)
        df_string = "資產負債表：\n" + balance_sheet.to_string().strip()

        instruction = dedent(
            """
            深入詳細審查公司最近一個會計年度的資產負債表，找出
            資產、負債和股東權益的結構，以解讀公司的財務穩定性及
            營運效率。重點評估流動性（透過流動資產與流動負債）、
            償債能力（透過長期負債比率）以及股權狀況，以衡量長期投資潛力。
            將這些指標與前幾年的數據進行對比，以突顯財務趨勢、改善或惡化。
            最後以一段話對公司的財務槓桿、資產管理和資本結構進行策略性評估，
            提供對其財務狀況和未來前景的見解。少於 130 字。
            """
        )

        section_text = SECUtils.get_10k_section(ticker_symbol, fyear, 7)
        prompt = combine_prompt(instruction, section_text, df_string)
        save_to_file(prompt, save_path)
        return f"指令和資源已儲存至 {save_path}"

    def analyze_cash_flow(
        ticker_symbol: Annotated[str, "股票代碼"],
        fyear: Annotated[str, "10-K 報告的會計年度"],
        save_path: Annotated[str, "寫入傳回指令和資源的 txt 檔案路徑。"]
    ) -> str:
        """
        擷取指定股票代碼的現金流量表及其 10-K 報告的相關部分。
        然後傳回如何分析現金流量表的說明。
        """
        cash_flow = YFinanceUtils.get_cash_flow(ticker_symbol)
        df_string = "現金流量表：\n" + cash_flow.to_string().strip()

        instruction = dedent(
            """
            深入全面評估公司最近一個會計年度的現金流量，重點關注營運、投資和融資活動的現金流入
            和流出。檢查營運現金流量以評估
            核心業務的獲利能力，審查投資活動以深入了解資本支出和投資，
            並檢視融資活動以了解債務、股權變動和股利政策。將這些現金變動
            與前期進行比較，以辨別趨勢、可持續性和流動性風險。最後以一段話對公司的
            現金管理效益、流動性狀況以及未來成長或財務挑戰的潛力進行明智的分析。
            少於 130 字。
            """
        )

        section_text = SECUtils.get_10k_section(ticker_symbol, fyear, 7)
        prompt = combine_prompt(instruction, section_text, df_string)
        save_to_file(prompt, save_path)
        return f"指令和資源已儲存至 {save_path}"

    def analyze_segment_stmt(
        ticker_symbol: Annotated[str, "股票代碼"],
        fyear: Annotated[str, "10-K 報告的會計年度"],
        save_path: Annotated[str, "寫入傳回指令和資源的 txt 檔案路徑。"]
    ) -> str:
        """
        擷取指定股票代碼的損益表及其 10-K 報告的相關部分。
        然後傳回如何建立分部分析的說明。
        """
        income_stmt = YFinanceUtils.get_income_stmt(ticker_symbol)
        df_string = (
            "損益表（分部分析）：\n" + income_stmt.to_string().strip()
        )

        instruction = dedent(
            """
            使用管理層的討論與分析以及損益表，識別公司的業務分部並建立分部分析，
            按分部細分並附上明確的標題。以具體數據說明營收和淨利，
            並計算變動。詳細說明策略性合作夥伴關係及其影響，包括公司或組織等細節。
            描述產品創新及其對營收成長的影響。量化市佔率及其變動，或說明市場地位
            及其變動。分析市場動態和利潤挑戰，注意國家政策變動的任何影響。包括成本方面，
            詳細說明營運成本、創新投資和通路擴張等費用。每項陳述均需有證據支持，
            每個分部分析應簡潔，不超過 60 字，並準確引用資訊來源。對於每個分部，將最
            重要的發現整合成一個清晰、簡潔的段落，排除較不重要或描述模糊的方面，以確保清晰度和
            對證據支持資訊的依賴。對於每個分部，輸出應為一個 150 字以內的單一段落。
            """
        )
        section_text = SECUtils.get_10k_section(ticker_symbol, fyear, 7)
        prompt = combine_prompt(instruction, section_text, df_string)
        save_to_file(prompt, save_path)
        return f"指令和資源已儲存至 {save_path}"

    def income_summarization(
        ticker_symbol: Annotated[str, "股票代碼"],
        fyear: Annotated[str, "10-K 報告的會計年度"],
        income_stmt_analysis: Annotated[str, "深入的損益表分析"],
        segment_analysis: Annotated[str, "深入的分部分析"],
        save_path: Annotated[str, "寫入傳回指令和資源的 txt 檔案路徑。"]
    ) -> str:
        """
        使用指定股票代碼的損益表和分部分析。
        然後傳回如何將這些分析綜合為一個連貫段落的說明。
        """
        # income_stmt_analysis = analyze_income_stmt(ticker_symbol)
        # segment_analysis = analyze_segment_stmt(ticker_symbol)

        instruction = dedent(
            f"""
            損益表分析：{income_stmt_analysis}，
            分部分析：{segment_analysis}，
            將深入的損益表分析和分部分析的發現綜合為一個單一、連貫的段落。
            它應該以事實為基礎並以數據為導向。首先，呈現並評估整體營收和利潤狀況，注意重要的
            趨勢和變化。其次，檢查各業務分部的表現，重點關注其營收和
            利潤變化、營收貢獻和市場動態。對於前兩個領域未涵蓋的資訊，識別並
            整合與營運、潛在風險以及成長和穩定性的策略性機會相關的關鍵發現到分析中。
            對於每個部分，整合歷史數據比較並提供相關事實、指標或數據作為證據。整個綜合
            應以連續段落呈現，不使用項目符號。每個重點使用副標題和編號。
            總輸出應少於 160 字。
            """
        )

        section_text = SECUtils.get_10k_section(ticker_symbol, fyear, 7)
        prompt = combine_prompt(instruction, section_text, "")
        save_to_file(prompt, save_path)
        return f"指令和資源已儲存至 {save_path}"

    def get_risk_assessment(
        ticker_symbol: Annotated[str, "股票代碼"],
        fyear: Annotated[str, "10-K 報告的會計年度"],
        save_path: Annotated[str, "寫入傳回指令和資源的 txt 檔案路徑。"]
    ) -> str:
        """
        擷取指定股票代碼的風險因素及其 10-K 報告的相關部分。
        然後傳回如何總結公司前 3 大關鍵風險的說明。
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
            根據 10-k 報告中提供的資訊，總結公司的前 3 大關鍵風險。
            然後，針對每個關鍵風險，將風險評估細分為以下幾個方面：
            1. 產業垂直風險：這個產業垂直與其他產業相比，風險如何？考慮法規、市場波動和競爭格局等因素。
            2. 週期性：這個產業的週期性有多強？討論經濟週期對公司業績的影響。
            3. 風險量化：如果公司或部門被認為有風險，請列舉關鍵風險因素並提供佐證數據。
            4. 下行保護：如果公司或部門風險較小，請討論現有的下行保護措施。考慮多元化、長期合約和政府法規等因素。

            最後，提供詳細且細緻的評估，以反映公司的真實風險狀況。並避免在您的回應中使用任何項目符號。
            """
        )
        prompt = combine_prompt(instruction, section_text, "")
        save_to_file(prompt, save_path)
        return f"指令和資源已儲存至 {save_path}"
        
    def get_competitors_analysis(
        ticker_symbol: Annotated[str, "股票代碼"], 
        competitors: Annotated[List[str], "競爭對手公司"],
        fyear: Annotated[str, "10-K 報告的會計年度"], 
        save_path: Annotated[str, "寫入傳回指令和資源的 txt 檔案路徑。"]
    ) -> str:
        """
        分析公司與其競爭對手之間的財務指標差異。
        準備分析提示並將其儲存到檔案中。
        """
        # 擷取財務資料
        financial_data = FMPUtils.get_competitor_financial_metrics(ticker_symbol, competitors, years=4)

        # 建構財務資料摘要
        table_str = ""
        for metric in financial_data[ticker_symbol].index:
            table_str += f"\n\n{metric}:\n"
            company_value = financial_data[ticker_symbol].loc[metric]
            table_str += f"{ticker_symbol}: {company_value}\n"
            for competitor in competitors:
                competitor_value = financial_data[competitor].loc[metric]
                table_str += f"{competitor}: {competitor_value}\n"

        # 準備分析說明
        instruction = dedent(
          """
          分析 {company}/ticker_symbol 及其競爭對手：{competitors} 在多年（表示為 0、1、2、3，其中 0 為最近一年，3 為最早一年）的財務指標。重點關注以下指標：EBITDA 利潤率、EV/EBITDA、FCF 轉換率、毛利率、ROIC、營收和營收成長率。
          每年：逐年趨勢：識別並討論 {company} 從最早一年 (3) 到最近一年 (0) 的每個指標的趨勢。但在產生分析時，您需要寫成 1：第 3 年 = 2023 年，2：第 2 年 = 2022 年，3：第 1 年 = 2021 年和 4：第 0 年 = 2020 年。突顯這些指標隨時間的任何顯著改善、下降或穩定性。
          競爭對手比較：每年，將 {company} 與其 {competitors} 的每個指標進行比較。評估 {company} 相對於其 {competitors} 的表現，注意其表現優於或落後之處。
          特定指標見解：

          EBITDA 利潤率：討論 {company} 與其 {competitors} 的獲利能力，特別是在最近一年。
          EV/EBITDA：提供有關估值的見解，以及 {company} 在每年與其 {competitors} 相比是否被高估或低估。
          FCF 轉換率：評估 {company} 相對於其 {competitors} 隨時間的現金流量效率。
          毛利率：分析每年的成本效率和獲利能力。
          ROIC：討論投資資本回報率，以及它對公司從其投資中產生回報的效率的建議，特別是關注最近的趨勢。
          營收和營收成長率：提供 {company} 營收表現和成長軌跡的全面檢視，注意任何重大變化或模式。
          結論：根據這些指標總結 {company} 的整體財務狀況。討論 {company} 在這些年和這些指標上的表現如何可能證明或反駁其目前的市場估值（如 EV/EBITDA 比率所示）。
          避免使用任何項目符號。
          """
        )

        # 合併提示
        company_name = ticker_symbol  # 假設股票代碼是公司名稱，否則，請擷取它。
        resource = f"{company_name} 和 {competitors} 的財務指標。"
        prompt = combine_prompt(instruction, resource, table_str)

        # 將說明和資源儲存到檔案中
        save_to_file(prompt, save_path)
        
        return f"指令和資源已儲存至 {save_path}"
        
    def analyze_business_highlights(
        ticker_symbol: Annotated[str, "股票代碼"],
        fyear: Annotated[str, "10-K 報告的會計年度"],
        save_path: Annotated[str, "寫入傳回指令和資源的 txt 檔案路徑。"]
    ) -> str:
        """
        擷取指定股票代碼的業務摘要及其 10-K 報告的相關部分。
        然後傳回如何描述公司各業務績效亮點的說明。
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
            根據給定資訊，描述公司各業務線的績效亮點。
            每個業務描述應包含一句總結和一句解釋。
            """
        )
        prompt = combine_prompt(instruction, section_text, "")
        save_to_file(prompt, save_path)
        return f"指令和資源已儲存至 {save_path}"

    def analyze_company_description(
        ticker_symbol: Annotated[str, "股票代碼"],
        fyear: Annotated[str, "10-K 報告的會計年度"],
        save_path: Annotated[str, "寫入傳回指令和資源的 txt 檔案路徑。"]
    ) -> str:
        """
        擷取指定股票代碼的公司描述及其 10-K 報告的相關部分。
        然後傳回如何描述公司產業、優勢、趨勢和策略性措施的說明。
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
            根據給定資訊，
            1. 簡要描述公司概況和公司產業，使用結構：「成立於 xxxx 年，'公司名稱' 是一家提供 ..... 的 xxxx
            2. 突顯核心優勢和競爭優勢的關鍵產品或服務，
            3. 包括有關終端市場（地理位置）、主要客戶（是否為藍籌股）、市場地位部分的市佔率等主題，
            4. 識別影響公司策略的當前產業趨勢、機會和挑戰，
            5. 概述最近的策略性措施，例如產品發布、收購或新的合作夥伴關係，並描述公司對市場狀況的回應。
            少於 300 字。
            """
        )
        step_prompt = combine_prompt(instruction, section_text, "")
        instruction2 = "總結分析，少於 130 字。"
        prompt = combine_prompt(instruction=instruction2, resource=step_prompt)
        save_to_file(prompt, save_path)
        return f"指令和資源已儲存至 {save_path}"

    def get_key_data(
        ticker_symbol: Annotated[str, "股票代碼"],
        filing_date: Annotated[
            str | datetime, "正在分析的財務報告的申報日期"
        ],
    ) -> dict:
        """
        傳回指定股票代碼和申報日期的年度報告中使用的關鍵財務數據
        """

        if not isinstance(filing_date, datetime):
            filing_date = datetime.strptime(filing_date, "%Y-%m-%d")

        # 擷取過去 6 個月的歷史市場數據
        start = (filing_date - timedelta(weeks=52)).strftime("%Y-%m-%d")
        end = filing_date.strftime("%Y-%m-%d")

        hist = YFinanceUtils.get_stock_data(ticker_symbol, start, end)

        # 取得其他相關資訊
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

        # 轉換回字串以進行函式呼叫
        filing_date = filing_date.strftime("%Y-%m-%d")

        # 列印結果
        # print(f"過去 6 個月，{ticker_symbol} 的平均每日交易量為：{avg_daily_volume_6m:.2f}")
        rating, _ = YFinanceUtils.get_analyst_recommendations(ticker_symbol)
        target_price = FMPUtils.get_target_price(ticker_symbol, filing_date)
        result = {
            "評級": rating,
            "目標價": target_price,
            f"6 個月平均每日成交量 ({info['currency']} 百萬)": "{:.2f}".format(
                avg_daily_volume_6m / 1e6
            ),
            f"收盤價 ({info['currency']})": "{:.2f}".format(close_price),
            f"市值 ({info['currency']} 百萬)": "{:.2f}".format(
                FMPUtils.get_historical_market_cap(ticker_symbol, filing_date) / 1e6
            ),
            f"52 週價格範圍 ({info['currency']})": "{:.2f} - {:.2f}".format(
                fiftyTwoWeekLow, fiftyTwoWeekHigh
            ),
            f"每股帳面價值 ({info['currency']})": "{:.2f}".format(
                FMPUtils.get_historical_bvps(ticker_symbol, filing_date)
            ),
        }
        return result
 result}