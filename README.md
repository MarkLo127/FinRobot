<div align="center">
</div>

# FinRobot: 使用大型語言模型進行財務分析的開源人工智慧代理平台 

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

**1. (Recommended) Create a new virtual environment**
```shell
conda create --name finrobot python=3.10
conda activate finrobot
```
**2. download the FinRobot repo use terminal or download it manually**
```shell
git clone https://github.com/MarkLo127/FinRobot.git
cd FinRobot
```
**3.Install dependency items**
```shell
pip install -r requirements.txt
```
**4. modify OAI_CONFIG_LIST_sample file**
```shell
1) rename OAI_CONFIG_LIST_sample to OAI_CONFIG_LIST
2) remove the four lines of comment within the OAI_CONFIG_LIST file
3) add your own openai api-key <your OpenAI API key here>
```
**5. modify config_api_keys_sample file**
```shell
1) rename config_api_keys_sample to config_api_keys
2) remove the comment within the config_api_keys file
3) add your own finnhub-api "YOUR_FINNHUB_API_KEY"
4) add your own financialmodelingprep and sec-api keys "YOUR_FMP_API_KEY" and "YOUR_SEC_API_KEY" (for financial report generation)
```

**Financial CoT**:
1. **Gather Preliminary Data**: 10-K report, market data, financial ratios
2. **Analyze Financial Statements**: balance sheet, income statement, cash flow
3. **Company Overview and Performance**: company description, business highlights, segment analysis
4. **Risk Assessment**: assess risks
5. **Financial Performance Visualization**:  plot PE ratio and EPS
6. **Synthesize Findings into Paragraphs**: combine all parts into a coherent summary
7. **Generate PDF Report**: use tools to generate PDF automatically
8. **Quality Assurance**: check word counts


**Disclaimer**: The codes and documents provided herein are released under the Apache-2.0 license. They should not be construed as financial counsel or recommendations for live trading. It is imperative to exercise caution and consult with qualified financial professionals prior to any trading or investment actions.

