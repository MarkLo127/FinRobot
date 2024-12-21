<div align="center">
</div>

# FinRobot : 財務分析的開源 AI 平台

<div align="center">
</div>

**FinRobot** 是一個超越 FinGPT 範疇的 AI 代理平台，代表了一個專為金融應用精心設計的全方位解決方案。它整合了**多種 AI 技術**，不僅僅局限於語言模型。這種宏大的願景突顯了該平台的多功能性與適應性，能夠滿足金融行業多方面的需求。

**AI Agent**的概念：AI Agent是一個智慧實體，它使用大型語言模型作為大腦來感知環境、做出決策和執行行動。與傳統人工智慧不同，AI Agent 具有獨立思考和利用工具逐步實現既定目標的能力。

## FinRobot Ecosystem
<div align="center">
<img align="center" src="https://github.com/AI4Finance-Foundation/FinRobot/assets/31713746/6b30d9c1-35e5-4d36-a138-7e2769718f62" width="90%"/>
</div>

### FinRobot 的整體框架分為四個不同的層，每個層都旨在解決金融人工智慧處理和應用的特定方面:

1. **Financial AI Agents Layer**: 金融AI代理層現包含金融思維鏈（CoT）提示，增強複雜分析與決策能力。市場預測代理、文件分析代理和交易策略代理利用 CoT 將金融挑戰分解為邏輯步驟，將其先進的演算法和領域專業知識與金融市場不斷變化的動態相結合，以獲得精確、可操作的見解。
2. **Financial LLMs Algorithms Layer**: 金融LLMs演算法層：金融LLMs演算法層配置和利用針對特定領域和全球市場分析專門調整的模型。
3. **LLMOps and DataOps Layers**: LLMOps 層實作多源整合策略，利用一系列最先進的模式為特定財務任務選擇最適合的 LLMs。 
4. **Multi-source LLM Foundation Models Layer**: 此基礎層支援各種通用和專用LLMs的即插即用功能。

## FinRobot: Agent Workflow
<div align="center">
<img align="center" src="https://github.com/AI4Finance-Foundation/FinRobot/assets/31713746/ff8033be-2326-424a-ac11-17e2c9c4983d" width="60%"/>
</div>

1. **Perception**: 此模組可擷取並解釋來自市場反饋、新聞和經濟指標的多模式金融數據，使用複雜的技術建立數據以進行徹底分析。

2. **Brain**: 作為核心處理單元，該模組透過LLMs感知來自感知模組的數據，並利用金融思想鏈（CoT）流程產生結構化指令。

3. **Action**: 此模組執行來自大腦模組的指令，應用工具將分析見解轉化為可行的結果。行動包括交易、投資組合調整、產生報告或發送警報，從而積極影響金融環境。

## FinRobot: Smart Scheduler
<div align="center">
<img align="center" src="https://github.com/AI4Finance-Foundation/FinRobot/assets/31713746/06fa0b78-ac53-48d3-8a6e-98d15386327e" width="60%"/>
</div>

智慧調度程序對於確保模型多樣性以及優化整合和選擇最適合每項任務的LLM至關重要。
* **Director Agent**: 此元件協調任務分配過程，確保根據代理人的績效指標和對特定任務的適用性將任務指派給代理人。
* **Agent Registration**: 管理註冊並追蹤系統內代理的可用性，促進高效率的任務分配過程。
* **Agent Adaptor**: 根據特定任務自訂代理功能，增強其效能以及在整個系統中的整合。
* **Task Manager**: 管理和儲存針對各種財務任務量身定制的不同常規和微調的基於 LLMs 的代理，並定期更新以確保相關性和有效性。

## Installation:

**1.創建新的虛擬環境**
```shell
conda create --name finrobot python=3.10
conda activate finrobot
```
**2.使用終端機下載FinRobot**
```shell
git clone https://github.com/MarkLo127/FinRobot.git
cd FinRobot
```
**3.安裝依賴項**
```shell
pip install -r requirements.txt
```
**4.修改OAI_CONFIG_LIST_sample**
```shell
1) rename OAI_CONFIG_LIST_sample to OAI_CONFIG_LIST
2) remove the four lines of comment within the OAI_CONFIG_LIST file
3) add your own openai api-key <your OpenAI API key here>
```
**5.修改config_api_keys_sample**
```shell
1) rename config_api_keys_sample to config_api_keys
2) remove the comment within the config_api_keys file
3) add your own finnhub-api "YOUR_FINNHUB_API_KEY"
4) add your own financialmodelingprep and sec-api keys "YOUR_FMP_API_KEY" and "YOUR_SEC_API_KEY" (for financial report generation)
```

# finrobot_zh

本專案以 [AI4Finance 基金會的 FinRobot](https://github.com/AI4Finance-Foundation/FinRobot) 為基礎，進行功能強化與本地化，特別針對繁體中文使用者進行了優化，並新增了對 20-F 財務文件的支援。

功能增強與特色
1. **20-F 支援**  
   - 增加對美國上市外國公司年報文件（20-F）的解析與關鍵訊息提取功能，幫助投資者快速掌握企業在 SEC 文件中的重要數據。
   
2. **繁體中文本地化**  
   - 提供完整的繁體中文界面及操作說明，讓中文使用者能夠更輕鬆地使用與理解。

3. **使用範例**
   - 請參考example資料夾內的內容

# Financial CoT
1. **收集初步數據**: 10-K、20-F 報告、市場數據、財務比率
2. **分析財務報表**: 資產負債表、損益表、現金流量表
3. **公司概況與績效**: 公司描述、業務亮點、市場分析
4. **風險評估**: 風險評估
5. **財務績效視覺化**:  繪製本益比和每股盈餘
6. **將調查結果綜合成段落**: 將所有部分組合成重點摘要
7. **產生PDF報告**: 使用工具自動產生PDF

#
**免責聲明**: 本文提供的程式碼和文件是在 Apache-2.0 許可下發布的。它們不應被視為財務顧問或即時交易建議。在進行任何交易或投資行動之前，必須謹慎行事並諮詢合格的金融專業人士。
