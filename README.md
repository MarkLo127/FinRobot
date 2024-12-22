<div align="center">
</div>

# FinRobot

<div align="center">
</div>

**FinRobot**/n
開源 AI 代理平台，專為金融應用設計的全方位解決方案，整合多種 AI 技術，滿足金融行業多方面的需求

**AI Agent**/n
使用大型語言模型作為大腦來感知環境、做出決策和執行行動，與傳統人工智慧不同的地方在於AI Agent 具有獨立思考和利用工具逐步實現既定目標的能力

## Ecosystem
<div align="center">
<img align="center" src="https://github.com/AI4Finance-Foundation/FinRobot/assets/31713746/6b30d9c1-35e5-4d36-a138-7e2769718f62" width="90%"/>
</div>

## Framework

1. **Financial AI Agents Layer**: 透過金融思維鏈（CoT），將複雜的金融問題分解為清晰的邏輯步驟，並且結合市場預測、文件分析及交易策略代理，運用先進演算法與專業知識，有效適應市場動態，提供精準且具實用性的洞察與建議
2. **Financial LLMs Algorithms Layer**: 配置和利用針對特定領域和全球市場分析專門調整的模型
3. **LLMOps and DataOps Layers**: 實作多源整合策略，利用一系列最先進的模式為特定財務任務選擇最適合的 LLMs
4. **Multi-source LLM Foundation Models Layer**: 支援各種通用和專用LLMs的即插即用功能

## Financial CoT
1. **收集初步數據**: 10-K、20-F 報告、市場數據、財務比率
2. **分析財務報表**: 資產負債表、損益表、現金流量表
3. **公司概況與績效**: 公司描述、業務亮點、市場分析
4. **風險評估**: 風險評估
5. **財務績效視覺化**:  繪製本益比和每股盈餘
6. **將調查結果綜合成段落**: 將所有部分組合成重點摘要
7. **產生PDF報告**: 使用工具自動產生PDF

## Agent Workflow
<div align="center">
<img align="center" src="https://github.com/AI4Finance-Foundation/FinRobot/assets/31713746/ff8033be-2326-424a-ac11-17e2c9c4983d" width="60%"/>
</div>

1. **Perception**: 擷取並解釋來自市場反饋、新聞和經濟指標的多模式金融數據，使用複雜的技術建立數據以進行分析

2. **Brain**: 核心處理單元，透過LLMs感知來自感知模組的數據，並利用金融思想鏈（CoT）流程產生結構化指令

3. **Action**: 執行來自大腦模組的指令，應用工具將分析見解轉化為可行的結果。行動包括交易、投資組合調整、產生報告或發送警報，從而積極影響金融環境

## Smart Scheduler
<div align="center">
<img align="center" src="https://github.com/AI4Finance-Foundation/FinRobot/assets/31713746/06fa0b78-ac53-48d3-8a6e-98d15386327e" width="60%"/>
</div>

* **Director Agent**: 協調任務分配，根據代理人的績效指標和對特定任務的適用性將任務指派給代理人
* **Agent Registration**: 管理並追蹤系統內代理的可用性，促進高效率的任務分配過程
* **Agent Adaptor**: 根據特定任務自訂代理功能，增強其效能以及在整個系統中的整合
* **Task Manager**: 管理和儲存針對各種財務任務量身定制的不同常規和微調的基於 LLMs 的代理，並定期更新以確保相關性和有效性

## Installation

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
add your own openai api-key <your OpenAI API key here>
```
**5.修改config_api_keys_sample**
```shell
1. add your own finnhub-api "YOUR_FINNHUB_API_KEY"
2. add your own financialmodelingprep and sec-api keys "YOUR_FMP_API_KEY" and "YOUR_SEC_API_KEY" (for financial report generation)
```

## finrobot_zh
本專案以 [AI4Finance 基金會的 FinRobot](https://github.com/AI4Finance-Foundation/FinRobot) 為基礎，進行功能強化與本地化，特別針對繁體中文使用者進行了優化，並新增了對 20-F 財務文件的支援。

功能增強與特色
1. **20-F 支援**  
   - 增加對美國上市外國公司年報文件（20-F）的解析與關鍵訊息提取功能，幫助投資者快速掌握企業在 SEC 文件中的重要數據
   
2. **繁體中文本地化**  
   - 提供完整的繁體中文界面及操作說明，讓中文使用者能夠更輕鬆地使用與理解

3. **使用範例**
   - 請參考example資料夾內的內容

## Demos
### 1.市場預測代理（預測股票走勢方向）
以公司的股票代碼、近期基本財務狀況和市場新聞作為輸入並預測其股票走勢。

1. Import 
```python
import sys
sys.path.append("/path/FinRobot") #替換成實際路徑位置

import autogen
from finrobot_zh.utils import get_current_date, register_keys_from_json
from finrobot_zh.agents.workflow import SingleAssistant
```
2. Config
```python
llm_config = {
    "config_list": autogen.config_list_from_json(
        "/path/OAI_CONFIG_LIST", #替換成實際路徑位置
        filter_dict={
            "model": ["gpt-4o-mini"],
        },
    ),
    "timeout": 120,
    "temperature": 0.5,
}
register_keys_from_json("/path/config_api_keys") #替換成實際路徑位置
```
3. Run
```python
company = "META"

assistant = SingleAssistant(
    "Market_Analyst",
    llm_config,
    # 如果希望進行對話而不僅僅是接收預測，請設置為 "ALWAYS"
    human_input_mode="NEVER",
)
assistant.chat(
    f"""
    請使用所有提供的工具，檢索截至{get_current_date()}有關{company}的最新資訊。請從以下幾個方面進行分析：

    1. **正面發展**：列出2至4個與{company}相關的正面因素，這些因素應主要基於公司最新的新聞和公告。
    2. **潛在風險**：列出2至4個與{company}相關的潛在風險或擔憂，這些因素應包括市場競爭、政策變動或其他可能影響公司表現的因素。
    3. **市場趨勢分析**：分析當前市場趨勢如何影響{company}，包括行業發展、技術創新等。
    4. **財務狀況評估**：簡要評估{company}的財務表現，如收入增長、利潤率、現金流等指標。

    最後，根據上述分析，對{company}的股票在下週的走勢做出大致預測（例如，上漲/下跌2-3%），並提供支持該預測的摘要分析。請保持整體分析簡潔明瞭。
"""
)
```
4. Result
```python
--------------------------------------------------------------------------------
Market_Analyst (to User_Proxy):

### META 最新資訊分析（截至2024-12-22）

#### 1. 正面發展
- **AI工具推出**：META最近推出了一個新的AI工具，旨在提升合作和機器智能的能力，這顯示了公司在技術創新方面的持續努力，可能會吸引更多客戶和合作夥伴。
- **市場反彈**：儘管整體市場波動，META的股票在近期內表現良好，顯示出投資者對公司未來增長的信心。
- **與政策的良好關係**：META的CEO馬克·祖克伯格正在積極與即將上任的特朗普政府建立良好關係，這可能會對公司未來的政策環境產生正面影響。

#### 2. 潛在風險
- **市場競爭加劇**：META在社交媒體和數字廣告領域面臨來自其他科技巨頭（如Google和Amazon）的激烈競爭，這可能會壓縮其市場份額和利潤。
- **政策不確定性**：隨著新政府的上任，可能會出現新的監管政策，這對META的運營和盈利能力構成潛在風險。
- **經濟放緩**：全球經濟增長放緩可能影響廣告支出，進而影響META的收入增長。

#### 3. 市場趨勢分析
- **數字廣告市場的回暖**：隨著經濟逐漸復甦，數字廣告市場有望回暖，這對META的業務是利好消息。
- **技術創新**：META在虛擬現實和擴增實境技術上的持續投資，可能會在未來數年內開創新的收入來源。
- **社交媒體使用趨勢**：隨著年輕一代對社交媒體的持續需求，META有機會在這一領域穩固其市場地位。

#### 4. 財務狀況評估
- **資產週轉率**：META的資產週轉率顯示出其資源的有效使用，這對於未來的利潤增長是積極信號。
- **帳面價值**：公司帳面價值的增長表明其資本結構的穩定性，這對投資者來說是個好消息。
- **收入增長**：儘管面臨挑戰，META的收入仍保持增長，顯示出其業務模式的韌性。

### 股票預測
基於以上分析，預計META的股票在下週可能會上漲約2-3%。這一預測基於以下幾點：
- **技術創新和新產品的推出可能會吸引更多的市場關注和投資者信心。**
- **市場對數字廣告的需求回暖可能會進一步推動META的收入增長。**
- **雖然存在競爭和政策風險，但公司在管理層的策略和市場定位上顯示出穩定性。**

### 總結
META在技術創新、財務穩定性和市場需求回暖的背景下，展現出良好的增長潛力，儘管面臨一些外部挑戰，但整體前景依然積極。

TERMINATE
```

### 2. 金融分析師代理報告撰寫（股票研究報告）
以公司的10-k、20-F、財務數據和市場數據作為輸入並輸出股權研究報告

1. Import 
```python
import sys
sys.path.append("/path/FinRobot") #替換成實際路徑位置

import os
import autogen
from textwrap import dedent
from finrobot_zh.utils import register_keys_from_json
from finrobot_zh.agents.workflow import SingleAssistantShadow
```
2. Config
```python
llm_config = {
    "config_list": autogen.config_list_from_json(
        "/path/OAI_CONFIG_LIST", #替換成實際路徑位置
        filter_dict={
            "model": ["gpt-4o"],
        },
    ),
    "timeout": 120,
    "temperature": 0.5,
}
register_keys_from_json("/path/config_api_keys") #替換成實際路徑位置

# Intermediate results will be saved in this directory
work_dir = "/path/report" #替換成實際路徑位置
os.makedirs(work_dir, exist_ok=True)

assistant = SingleAssistantShadow(
    "Expert_Investor",
    llm_config,
    max_consecutive_auto_reply=None,
    human_input_mode="TERMINATE",
)
```
3. Run
```python
company = "APPLE"
fyear = "2024"
message = dedent(
    f"""
        請根據 {company} 在 {fyear} 年的 10-K 報告資料，撰寫年度報告並將其最終以 PDF 格式呈現。請詳細閱讀並遵守下列要求與執行計劃：

        1. 工作計劃聲明：
        - 在正式開始生成報告內容前，請先以清晰、邏輯且逐步的方式解釋您的整體工作計劃，包括如何取得、分析與彙整 10-K 報告中的資訊。
        - 說明您將使用的工具，以及每個工具的用途與目的。

        2. 工具使用流程說明：
        - 在整個任務過程中，請務必在每次使用工具時先進行充分解釋與請求指令描述。例如，當您需要存取檔案、執行文字處理或格式轉換時，請在對話中明確說明您的計劃與目的。
        - 在對話中請一律使用繁體中存進行回覆。
        - 一旦獲得許可後再使用工具，並在操作完成後彙報結果。

        3. 工作目錄規範：
        - 所有檔案處理、文字儲存與文件生成必須在 "{work_dir}" 目錄中進行。
        - 請在操作前後清楚標示工作目錄路徑與行為，使操作可追溯且透明化。

        4. 圖像顯示要求：
        - 在生成任何圖像後，請立即於對話中進行顯示（例如可將圖像以內嵌方式傳回或描述生成的圖像內容與檔案位置）。
。
        5. 段落字數規定：
        - 第一頁（業務概覽、市場地位和營運結果）的每個段落應在 150 到 160 字之間，第二頁（風險評估和競爭對手分析）的每個段落應在 500 到 600 字之間。
        - 請在完全確認所有內容敲定、且經最終檢視無誤後，再生成 PDF 檔案，以避免反覆更改。

        6. 最終 PDF 輸出：
        - 完成文本初稿、審閱與確認後，再進行 PDF 檔案的格式化與輸出，確保文件結構、字數規範與語氣專業性皆符合要求。
        - 在生成 PDF 前，請先於對話中明確聲明「將進行 PDF 輸出」並等待確認，確認後再執行最終生成動作。

        請依序遵照上述指令，以高專業度與清晰可辨的程序，協助完成 10-K 年度報告的撰寫與 PDF 格式輸出。
    """
    )
assistant.chat(message, use_cache=True, max_turns=50,
               summary_method="last_msg")
```
4. Result
<div style="display: flex; justify-content: center; align-items: center; gap: 20px;">
  <img src="https://github.com/MarkLo127/FinRobot/blob/main/assets/Apple_Annual_Report_2024-1.png" style="width: 45%;" />
  <img src="https://github.com/MarkLo127/FinRobot/blob/main/assets/Apple_Annual_Report_2024-2.png" style="width: 45%;" />
</div>

##
**免責聲明**: 本文提供的程式碼和文件是在 Apache-2.0 許可下發布的。它們不應被視為財務顧問或即時交易建議。在進行任何交易或投資行動之前，必須謹慎行事並諮詢合格的金融專業人士
