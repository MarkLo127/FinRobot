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
        fyear: Annotated[str, "10-K 報告的財務年度"],
        save_path: Annotated[str, "儲存返回的指令和資源的文字檔路徑"]
    ) -> str:
        """
        獲取指定股票代碼的損益表及其 10-K 報告相關章節。
        然後返回關於如何分析損益表的指令。
        """
        # 獲取損益表
        income_stmt = YFinanceUtils.get_income_stmt(ticker_symbol)
        df_string = "損益表：\n" + income_stmt.to_string().strip()

        # 分析指令
        instruction = dedent(
            """
            請對本財務年度的損益表進行全面且具戰略性的分析，並以清晰易讀、邏輯嚴謹的結構呈現。請務必納入以下要點：

            1. 整體營收與成長趨勢：  
            - 提供營收的整體概況，包含同比（年對年）或環比（季對季）比較。  
            - 詳析各項收入來源，明確識別營收成長的主要驅動因素與新興市場或產品線的貢獻度。  

            2. 銷貨成本與成本控管評估：  
            - 仔細檢視銷貨成本結構，辨識可能的成本上升因素或效率瓶頸。  
            - 針對特定成本組成項目提出控制建議，以提升整體成本效益。  

            3. 利潤率指標與經營績效評估：  
            - 深入分析毛利率、營業利潤率與淨利率，探討成本效率與營運效能是否達標。  
            - 將本期利潤率表現與歷史數據、行業平均值及競爭對手基準進行比較，掌握公司相對地位。  

            4. 投資者視角：每股盈餘（EPS）評估：  
            - 探討EPS之變化趨勢，闡明公司對股東報酬與投資者信心的影響。  
            - 若可行，將EPS表現與同業或指標企業比較，以評估相對投資價值。  

            5. 整體綜合評估與策略建議：  
            - 將上述指標與歷史與產業基準彙整比較，識別公司獲利與成長之長期模式與挑戰。  
            - 根據分析結果，提供具體且可執行的策略建議，以支持管理層決策並促進後續成長。

            內容形式與字數要求：  
            - 請以 150 至 550 字的繁體中文濃縮上述分析，形成一段完整的戰略性概述。  
            - 採用4-5個清晰的重點段落（可適度使用子標題），並以有力的數據與具體指標支撐論點。
            """
        )

        # 獲取 10-K 報告相關章至
        section_text = SECUtils.get_filing_section(ticker_symbol, fyear, 7)

        # 組合指令、章節文本和損益表
        prompt = combine_prompt(instruction, section_text, df_string)

        save_to_file(prompt, save_path)
        return f"指令和資源已儲存至 {save_path}"
    
    def analyze_balance_sheet(
        ticker_symbol: Annotated[str, "股票代碼"],
        fyear: Annotated[str, "10-K 報告的財務年度"],
        save_path: Annotated[str, "儲存返回的指令和資源的文字檔路徑"]
    ) -> str:
        """
        獲取指定股票代碼的資產負債表及其 10-K 報告相關章節。
        然後返回關於如何分析資產負債表的指令。
        """
        balance_sheet = YFinanceUtils.get_balance_sheet(ticker_symbol)
        df_string = "資產負債表：\n" + balance_sheet.to_string().strip()

        instruction = dedent(
            """
            請對本財務年度的資產負債表進行深入且結構化的分析，並以專業觀點解讀公司的財務穩定性和營運效率。請務必包括以下要點：

            1. 流動性評估：  
            - 分析流動資產與流動負債的結構與比例，探討公司是否具備足夠的短期資金彈性。  
            - 若可行，利用流動比率或速動比率等常用指標，闡明公司在短期債務到期時的償付能力。

            2. 償債能力檢視：  
            - 聚焦長期債務狀況，評估公司對長期義務的承擔能力與資本結構的穩健性。  
            - 使用如債務比率（Debt Ratio）、負債權益比（Debt-to-Equity Ratio）等指標，明確說明公司對於長期財務風險的承受度。

            3. **權益結構與長期投資潛力**：  
            - 檢視股東權益構成及增減變化，評估公司是否具備持續投入資金以支持未來成長的潛力。  
            - 若有明顯的股東權益變化，說明其可能原因（如資本增減、股利政策、股東結構重組等）並探討對公司長期投資價值的影響。

            4. 歷史比較與趨勢分析：  
            - 將本年度的資產、負債與股東權益指標與往年數據進行縱向比較，以辨識財務健康狀況的改善、停滯或惡化方向。  
            - 若可行，將這些指標與同業平均或競爭對手基準進行橫向對比，以強化判斷的精準度。

            **整合性結論與字數要求**：  
            - 請以一段150至550字的繁體中文文字，整合上述分析結果，提供對公司財務槓桿運用、資產管理效率與資本結構的總體觀點。  
            - 請在該段文字中明確點出公司目前的財務健康狀況及未來成長潛力，並提出有建設性的策略性見解，以協助管理層與投資者制定決策。
            """
        )

        section_text = SECUtils.get_filing_section(ticker_symbol, fyear, 7)
        prompt = combine_prompt(instruction, section_text, df_string)
        save_to_file(prompt, save_path)
        return f"指令和資源已儲存至 {save_path}"

    def analyze_cash_flow(
        ticker_symbol: Annotated[str, "股票代碼"],
        fyear: Annotated[str, "10-K 報告的財務年度"],
        save_path: Annotated[str, "儲存返回的指令和資源的文字檔路徑"]
    ) -> str:
        """
        獲取指定股票代碼的現金流量表及其 10-K 報告相關章節。
        然後返回關於如何分析現金流量表的指令。
        """
        cash_flow = YFinanceUtils.get_cash_flow(ticker_symbol)
        df_string = "現金流量表：\n" + cash_flow.to_string().strip()

        instruction = dedent(
            """
            請對本財務年度的現金流量表進行全面且深度的分析，並從營運、投資與融資三大面向探討公司整體現金管理實效。請務必包含以下要點：

            1. 營業活動現金流：  
            - 分析核心業務所產生之現金流入與流出，評估公司經營績效與獲利品質。  
            - 若可行，可利用營業現金流/淨利指標，以判斷盈利能力及持續性。

            2. 投資活動現金流：  
            - 審視資本支出、併購、資產處分及長期投資狀況，以了解公司是否積極尋求成長機會或謹慎控制資本配置。  
            - 探討投資現金流的方向與金額對未來產能、競爭力及研發成效的潛在影響。

            3. 融資活動現金流：  
            - 評估公司透過發行股票、舉債或股利分配等方式進行資金調度的策略與成效。  
            - 使用負債權益比或股利政策變化等指標，以判斷公司財務結構的穩健性與對股東報酬的關注度。

            4. 歷史比較與風險評估：  
            - 將本期現金流量表數據與往年資料相比，識別現金流量結構變化與長期趨勢。  
            - 判定現金流量狀況的可持續性與是否存在流動性風險，並相對於產業平均或主要競爭對手進行檢視。

            整合性結論與字數要求：  
            - 請以一段150至550字的繁體中文文字，針對公司現金管理效率、流動性狀況、未來增長潛力與潛在財務挑戰提出深入見解。  
            - 請以策略性角度詮釋分析結果，提供利於管理層與投資者決策的行動建議。
            """
        )

        section_text = SECUtils.get_filing_section(ticker_symbol, fyear, 7)
        prompt = combine_prompt(instruction, section_text, df_string)
        save_to_file(prompt, save_path)
        return f"指令和資源已儲存至 {save_path}"

    def analyze_segment_stmt(
        ticker_symbol: Annotated[str, "股票代碼"],
        fyear: Annotated[str, "10-K 報告的財務年度"],
        save_path: Annotated[str, "儲存返回的指令和資源的文字檔路徑"]
    ) -> str:
        """
        獲取指定股票代碼的損益表及其 10-K 報告相關章節。
        然後返回關於如何進行分部分析的指令。
        """
        income_stmt = YFinanceUtils.get_income_stmt(ticker_symbol)
        df_string = (
            "損益表（分部分析）：\n" + income_stmt.to_string().strip()
        )

        instruction = dedent(
            """
            請根據公司「管理層討論與分析」(Management Discussion and Analysis, MDA) 以及最新損益表資料，清晰識別並逐一分析公司的主要業務分部。分析過程請以明確的標題區分各業務分部，並納入下列重點：

            1. 收入與淨利潤表現：  
            - 提供該分部的收入與淨利潤數據，並註明資料來源（如財報附註或官方披露）。  
            - 計算並說明與前期比較（如同比、環比）的變化率及原因。  
            - 以量化數據與具體事實為基礎，排除非實證性描述。

            2. 戰略合作夥伴關係：  
            - 指名重要合作夥伴（如特定供應商、經銷商或策略聯盟企業），並清楚註明資訊來源（如新聞稿、公司報告）。  
            - 說明此合作關係對分部收入、淨利潤或市場滲透度的影響，並以具體數據或事實佐證。

            3. 產品創新與收入增長：  
            - 陳述近期推出或改良的產品、服務或技術所帶來的營收提升，並引用可驗證的資料（如新產品上市公告、市場調查報告）。  
            - 運用量化數據明確說明創新對本分部財務表現的貢獻度。

            4. 市場份額與地位變化：  
            - 以可核實的市場調查或行業報告為基礎（須明確標示資料來源），對比本分部市場份額的歷史數據與本期表現。  
            - 說明市場地位提升或退步的因素及其對未來競爭力的影響。

            5. 市場動態與盈利挑戰：  
            - 檢視政策變化、宏觀經濟狀況及產業趨勢對該分部盈利的影響，並以官方政策文件、行業分析報告或經濟指標數據為參考。  
            - 針對已出現的挑戰提出實證性的觀察與數據佐證。

            6. 成本分析：  
            - 以財報數據為基礎，詳細說明分部營運成本、研發投資（創新支出）及渠道擴張費用的變化與比例。  
            - 運用數據說明成本變動對該分部整體獲利率的影響。

            形式與字數要求：  
            - 請為每個業務分部單獨撰寫一段150至550字的總結段落，清晰呈現該分部的重要發現。  
            - 每段文字需具體引述數據與來源，避免泛泛而談。  
            - 將次要或無法驗證的內容刪除，確保所有結論都有數據與證據支持。

            最終成果應協助管理層與投資者清晰了解各業務分部的財務表現、成長動能、市場地位及潛在挑戰，從而更精準地制定決策策略。
            """
        )
        section_text = SECUtils.get_filing_section(ticker_symbol, fyear, 7)
        prompt = combine_prompt(instruction, section_text, df_string)
        save_to_file(prompt, save_path)
        return f"指令和資源已儲存至 {save_path}"
    
    def income_summarization(
        ticker_symbol: Annotated[str, "股票代碼"],
        fyear: Annotated[str, "10-K 報告的財務年度"],
        income_stmt_analysis: Annotated[str, "深入的損益表分析"],
        segment_analysis: Annotated[str, "深入的分部分析"],
        save_path: Annotated[str, "儲存返回的指令和資源的文字檔路徑"]
    ) -> str:
        """
        根據損益表和分部分析，為指定的股票代碼生成指令。
        提供如何將這些分析綜合成一個連貫段落的指導。
        """
        instruction = dedent(
            f"""
            損益表分析：{income_stmt_analysis}
            分部分析：{segment_analysis}

            請將前述「損益表分析」與「分部分析」的主要發現整合為一個流暢且連貫的評論性段落。撰寫時請特別注意：

            1. 數據與事實支持：  
            - 所有結論應依據經過驗證的財務數據、歷史紀錄或可信來源。  
            - 引用具體指標（如收入成長率、毛利率、淨利潤率、市場份額變化、投入成本比例）以確保分析具說服力。

            2. 整合整體與分部表現：  
            - 首先評估整體收入、利潤狀況及主要趨勢（如同比、環比增減），並提供相對應的數據。  
            - 接續檢視各業務分部的收入與利潤變化（包括歷史比較），說明該分部在公司整體營運中的貢獻度及市場動態（如客戶需求、競爭對手動向、政策環境影響）。

            3. 補充營運發現與風險機會：  
            - 整合未於前兩部分清晰闡述的資訊，如營運過程中的關鍵挑戰、供應鏈瓶頸或成本控制議題。  
            - 若有政策、經濟環境或技術趨勢等外生因素影響未來增長與穩定性，請據實呈現並提供對應的因應策略建議。

            4. 形式規範：  
            - 請以單一連續段落進行呈現，不使用項目符號。  
            - 可在段落中透過簡明的子標題與編號（如「(1) 整體表現」、「(2) 分部貢獻」、「(3) 營運風險與機會」）來引導讀者理解結構。  
            - 段落字數介於150至550字之間。  
            - 使用繁體中文撰寫，保留高專業度與嚴謹的語氣。

            最終文本應呈現一個整合全面、邏輯清晰且有數據支持的總結，協助管理階層與投資者快速掌握整體營運脈絡與關鍵決策方向。
            """
        )

        section_text = SECUtils.get_filing_section(ticker_symbol, fyear, 7)
        prompt = combine_prompt(instruction, section_text, "")
        save_to_file(prompt, save_path)
        return f"指令和資源已儲存至 {save_path}"

    def get_risk_assessment(
        ticker_symbol: Annotated[str, "股票代碼"],
        fyear: Annotated[str, "10-K 報告的財務年度"],
        save_path: Annotated[str, "儲存返回的指令和資源的文字檔路徑"]
    ) -> str:
        """
        獲取指定股票代碼的風險因素及其 10-K 報告相關章節。
        然後返回關於如何總結公司三大主要風險的指令。
        """
        company_name = YFinanceUtils.get_stock_info(ticker_symbol)["shortName"]
        risk_factors = SECUtils.get_filing_section(ticker_symbol, fyear, "1A")
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
            請根據 10-K 報告中披露的資訊，總結該公司所面臨的三項主要風險。請在分析過程中遵循下列結構與要點，並確保對每項風險的評估均具備事實依據與數據支持：

            1. 產業垂直風險評估：  
            - 將目光聚焦在該產業與其他產業之間的相對風險水準。  
            - 詳實考量監管環境（如法規變動、合規成本）、市場波動性（如原料價格、需求變化）以及競爭格局（如市場集中度、主要競爭者行動）的影響。  
            - 請提供適用的參考數據或歷史案例，並註明資訊來源。

            2. 週期性與經濟敏感度：  
            - 討論該產業的週期性特徵及其與經濟景氣循環的關聯程度。  
            - 分析在過往經濟榮枯下，該公司績效（如營收成長率、利潤率、現金流量）如何隨經濟週期波動。  
            - 提出具體的量化指標或時間序列數據，強調週期變化對公司營運表現的影響。

            3. 風險量化與高風險領域識別：  
            - 若發現公司或特定業務分部顯示高風險特徵，請羅列核心風險因素（如產品集中度、供應鏈脆弱性、財務槓桿偏高），並提供佐證數據（如負債比率、存貨週轉天數、特定客戶依賴度）。  
            - 透過比較行業標準或過往歷史數據，明確界定高風險區域的嚴重程度。

            4. 下行保護與風險緩衝：  
            - 若公司或某業務分部風險相對較低，請討論其下行保護措施，包括但不限於業務多元化策略、長期供應或銷售合約、政府補貼或監管保護等。  
            - 以量化資訊（如不同業務分部收入占比、合約存續年限、政府計畫補貼比例）凸顯下行保護對風險抑制的實質貢獻。

            最終整合分析：  
            - 在綜合前述風險要素後，提供一個反映公司真實風險全貌的整合性評估，包括高風險區域的明確定位、潛在衝擊的量化估計，以及下行防護措施的有效性。  
            - 全文請以嚴謹、專業的語氣撰寫，並確保每項論點皆有明確數據或事實參考，讓管理階層與投資者得以清晰理解公司當前的風險情勢與對策依據。
            """
        )
        prompt = combine_prompt(instruction, section_text, "")
        save_to_file(prompt, save_path)
        return f"指令和資源已儲存至 {save_path}"
        
    def get_competitors_analysis(
        ticker_symbol: Annotated[str, "股票代碼"], 
        competitors: Annotated[List[str], "競爭對手公司"],
        fyear: Annotated[str, "10-K 報告的財務年度"], 
        save_path: Annotated[str, "儲存返回的指令和資源的文字檔路徑"]
    ) -> str:
        """
        分析公司與其競爭對手之間的財務指標差異。
        準備分析提示並儲存至檔案。
        """
        # 獲取財務數據
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

        instruction = dedent(
            f"""
                請對 {ticker_symbol} 與其競爭對手 {competitors} 在歷年（以0、1、2、3代表不同年度，0為最新年度、3為最早年度）之財務指標表現進行深入分析。請在解讀數據時以實際年度標註：年度3 = 2023年、年度2 = 2022年、年度1 = 2021年、年度0 = 2020年。重點財務指標包括：  
                - EBITDA率  
                - EV/EBITDA  
                - 現金流轉換率  
                - 毛利率  
                - 投資報酬率 (ROI)  
                - 營收及營收成長率

                分析要點：

                1. 年度趨勢解析：  
                - 全面檢視自2023年（年度3）至2020年（年度0）的指標變化。  
                - 透過數據明確指出顯著改善、下滑或持穩的走勢。  
                - 使用具體數據（如數值變化率或百分比）支持結論。

                2. 競爭對手比較：  
                - 在每個年度分別將 {ticker_symbol} 的指標與 {competitors} 進行對照分析。  
                - 辨識公司相對競爭對手之優勢（如更佳的盈利能力或更高的現金流效率）或劣勢（如估值過高或利潤率偏低）。  
                - 引述明確數據支持對競爭地位的評估。

                3. 指標專項分析：  
                - EBITDA率：說明該公司相較於競爭對手的獲利能力是否有顯著區別。  
                - EV/EBITDA：探討公司估值水準，評估其是否被市場合理定價。  
                - 現金流轉換率：評量公司將盈餘轉化為實際現金流的效率，並比較競爭對手的表現。  
                - 毛利率：透過數字比較成本控制與營運效率，判斷公司是否具備結構性優勢。  
                - 投資報酬率 (ROI)：關注歷年趨勢，判定公司對於資本投入的使用效率是否改善或惡化。  
                - 營收與營收成長：整合分析公司營收規模及其成長動能，並比較競爭對手的成長軌跡。

                4. 整體結論：  
                - 在匯整各項指標結果後，對公司整體財務健康與競爭地位提供一個高階且具依據的總結評估。  
                - 討論這些指標表現是否合理支持公司目前的市場估值，並說明未來機遇與挑戰。

                請以專業、嚴謹且易於理解的方式撰寫分析報告，確保每項評述皆有數據支持，以協助管理階層及投資者作出更明智的決策。
            """
        )

        company_name = ticker_symbol
        resource = f"{company_name} 和 {competitors} 的財務指標。"
        prompt = combine_prompt(instruction, resource, table_str)

        save_to_file(prompt, save_path)
        
        return f"指令和資源已儲存至 {save_path}"
        
    def analyze_business_highlights(
        ticker_symbol: Annotated[str, "股票代碼"],
        fyear: Annotated[str, "10-K 報告的財務年度"],
        save_path: Annotated[str, "儲存返回的指令和資源的文字檔路徑"]
    ) -> str:
        """
        獲取公司業務概要和 10-K 報告相關章節。
        然後返回關於如何描述公司各業務部門表現亮點的指令。
        """
        business_summary = SECUtils.get_filing_section(ticker_symbol, fyear, 1)
        section_7 = SECUtils.get_filing_section(ticker_symbol, fyear, 7)
        section_text = (
            "業務概要：\n"
            + business_summary
            + "\n\n"
            + "管理層討論與分析：\n"
            + section_7
        )
        instruction = dedent(
            """
            請根據已提供之資訊，針對公司各個業務部門撰寫一段精要而具深度的分析敘述。每個業務部門的描述請包含：

            1. 整體表現摘要：  
            - 提出該部門在本期的營運重點與財務表現。  
            - 引述關鍵指標（如營收、利潤率、客戶數量或市場占有率），並提供適當的對比（如相較上一期或預算目標）以強調其表現亮點。

            2. 主要成因剖析：  
            - 解釋導致該部門整體表現的核心因素，並援引具體實證（如新產品推出、成本控管成效、策略合作夥伴關係、政策環境變動或市場需求提升）。  
            - 若有可量化的數據支持，請明確列出，以增強分析之客觀性和說服力。

            其他規範：  
            - 請確保文字呈現時專業、嚴謹且清晰易讀。  
            - 聚焦於能提供管理階層與投資者有用的見解，避免不必要的冗長描述。  
            - 每個業務部門的描述請維持精煉並直指重點，確保讀者能迅速掌握該部門的關鍵成果與驅動因素。
            """
        )
        prompt = combine_prompt(instruction, section_text, "")
        save_to_file(prompt, save_path)
        return f"指令和資源已儲存至 {save_path}"

    def analyze_company_description(
        ticker_symbol: Annotated[str, "股票代碼"],
        fyear: Annotated[str, "10-K 報告的財務年度"],
        save_path: Annotated[str, "儲存返回的指令和資源的文字檔路徑"]
    ) -> str:
        """
        獲取公司簡介和 10-K 報告相關章節。
        然後返回關於如何描述公司的行業、優勢、趨勢和戰略舉措的指令。
        """
        company_name = YFinanceUtils.get_stock_info(ticker_symbol).get("shortName","不適用")
        try:
            business_summary = SECUtils.get_filing_section(ticker_symbol, fyear, 1)
            if not business_summary:
                raise ValueError(f"無法獲取{ticker_symbol}的業務概要")
            section_7 = SECUtils.get_filing_section(ticker_symbol, fyear, 7)
            if not section_7:
                raise ValueError(f"無法獲取{ticker_symbol}的管理層討論與分析") 
            section_text = (
                "公司名稱："
                + company_name
                + "\n\n"
                + "業務概要：\n"
                + business_summary
                + "\n\n"
                + "管理層討論與分析：\n"
                + section_7
            )
            
            instruction = dedent(
                """
                請根據所提供之資訊，綜合撰寫一段150至550字的繁體中文敘述，以清晰、有條理的方式呈現該公司的概況、行業屬性、核心優勢及策略重點。請包含以下要素：

                1. 公司概況與產業定位：  
                - 以「成立於 XXXX 年，『公司名稱』是一家提供……的公司」為起首句式，簡要描述公司的成立時間、服務或產品定位，以及其所屬產業特性。

                2. 核心與競爭優勢：  
                - 清楚點出公司在營運模式、技術研發、品牌影響力、供應鏈管理或其他關鍵領域的核心強項。  
                - 強調與主要競爭者相比，公司具備的獨特競爭力（如更高的客戶黏性、更低的成本結構或創新產品組合）。

                3. 主要產品或服務與市場佈局：  
                - 概述公司最具代表性的產品或服務線，並說明其對營收或市場地位的貢獻度。  
                - 敘述地理市場分布、主要客戶類型（如是否為藍籌企業或特定產業龍頭）、市場份額及市場地位（如行業前五大供應商之一）。

                4. 行業趨勢與戰略影響因素：  
                - 簡要描述當前行業發展方向（如政策傾向、科技演進、消費習慣改變）。  
                - 識別公司面臨的機遇（如新興市場拓展）與挑戰（如競爭加劇、利潤空間壓縮）以及影響公司長期策略的關鍵因素（如法規、供應鏈中斷風險）。

                5. 近期戰略舉措：  
                - 概述公司近期推出的新產品、擴張計畫、併購活動或策略合作關係。  
                - 若有針對市場動態所作的營運調整或新措施，請予以簡述。

                請以整合性連貫的單一段落呈現，避免使用項目符號列點，並確保敘述邏輯清晰、資訊完整、有助於讀者快速掌握公司的現況及前景。
                """
            )
            
            step_prompt = combine_prompt(instruction, section_text, "")
            instruction2 = "總結分析，內容字數介於 150 至 550 字。"
            prompt = combine_prompt(instruction=instruction2, resource=step_prompt)
            save_to_file(prompt, save_path)
            return f"指令和資源已儲存至 {save_path}"
       
        except Exception as e:
            print(f"分析公司描述時發生錯誤: {str(e)}")
            return None

    def get_key_data(
        ticker_symbol: Annotated[str, "股票代碼"],
        filing_date: Annotated[
            str | datetime, "正在分析的財務報告的申報日期"
        ],
    ) -> dict:
        """
        返回用於年度報告的指定股票代碼和申報日期的關鍵財務數據
        """

        if not isinstance(filing_date, datetime):
            filing_date = datetime.strptime(filing_date, "%Y-%m-%d")

        # 獲取過去 6 個月的歷史市場數據
        start = (filing_date - timedelta(weeks=52)).strftime("%Y-%m-%d")
        end = filing_date.strftime("%Y-%m-%d")

        hist = YFinanceUtils.get_stock_data(ticker_symbol, start, end)

        # 獲取其他相關資訊
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

        filing_date = filing_date.strftime("%Y-%m-%d")

        rating, _ = YFinanceUtils.get_analyst_recommendations(ticker_symbol)
        target_price = FMPUtils.get_target_price(ticker_symbol, filing_date)
        result = {
            "分析評級": rating,
            "目標價": target_price,
            f"6個月平均每日成交量（{info['currency']}百萬）": "{:.2f}".format(
                avg_daily_volume_6m / 1e6
            ),
            f"收盤價（{info['currency']}）": "{:.2f}".format(close_price),
            f"市值（{info['currency']}百萬）": "{:.2f}".format(
                FMPUtils.get_historical_market_cap(ticker_symbol, filing_date) / 1e6
            ),
            f"52週價格區間（{info['currency']}）": "{:.2f} - {:.2f}".format(
                fiftyTwoWeekLow, fiftyTwoWeekHigh
            ),
            f"每股淨值（{info['currency']}）": "{:.2f}".format(
                FMPUtils.get_historical_bvps(ticker_symbol, filing_date)
            ),
        }
        return result