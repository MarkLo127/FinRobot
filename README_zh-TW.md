<div align="center">
<img align="center" width="30%" alt="image" src="https://github.com/AI4Finance-Foundation/FinGPT/assets/31713746/e0371951-1ce1-488e-aa25-0992dafcc139">
</div>

<p align="right">
<a href="README.md">English</a> | <a href="README_zh-TW.md">繁體中文</a>
</p>

# FinRobot：一個使用大型語言模型的開源金融分析AI代理平台
[![Downloads](https://static.pepy.tech/badge/finrobot)](https://pepy.tech/project/finrobot)
[![Downloads](https://static.pepy.tech/badge/finrobot/week)](https://pepy.tech/project/finrobot)
[![Python 3.8](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![PyPI](https://img.shields.io/pypi/v/finrobot.svg)](https://pypi.org/project/finrobot/)
![License](https://img.shields.io/github/license/AI4Finance-Foundation/finrobot.svg?color=brightgreen)
![](https://img.shields.io/github/issues-raw/AI4Finance-Foundation/finrobot?label=Issues)
![](https://img.shields.io/github/issues-closed-raw/AI4Finance-Foundation/finrobot?label=Closed+Issues)
![](https://img.shields.io/github/issues-pr-raw/AI4Finance-Foundation/finrobot?label=Open+PRs)
![](https://img.shields.io/github/issues-pr-closed-raw/AI4Finance-Foundation/finrobot?label=Closed+PRs)

<div align="center">
<img align="center" src=figs/logo_white_background.jpg width="40%"/>
</div>

**FinRobot** 是一個超越 FinGPT 範疇的 AI 代理平台，是專為金融應用精心設計的綜合解決方案。它整合了**多樣化的 AI 技術**，不僅僅是語言模型。這一廣闊的願景突顯了該平台的多功能性和適應性，以滿足金融行業多方面的需求。

**AI 代理的概念**：AI 代理是一個智慧實體，它使用大型語言模型作為其大腦來感知環境、做出決策並執行動作。與傳統的人工智慧不同，AI 代理擁有獨立思考和利用工具逐步實現給定目標的能力。

[FinRobot 白皮書](https://arxiv.org/abs/2405.14767)

[![](https://dcbadge.vercel.app/api/server/trsr8SXpW5)](https://discord.gg/trsr8SXpW5)

![Visitors](https://api.visitorbadge.io/api/VisitorHit?user=AI4Finance-Foundation&repo=FinRobot&countColor=%23B17A)

## FinRobot 生態系統
<div align="center">
<img align="center" src="https://github.com/AI4Finance-Foundation/FinRobot/assets/31713746/6b30d9c1-35e5-4d36-a138-7e2769718f62" width="90%"/>
</div>

### FinRobot 的整體框架分為四個不同的層次，每個層次都旨在處理金融 AI 處理和應用的特定方面：
1. **金融 AI 代理層**：金融 AI 代理層現在包括金融思維鏈（CoT）提示，增強了複雜分析和決策能力。市場預測代理、文件分析代理和交易策略代理利用 CoT 將金融挑戰分解為邏輯步驟，使其先進的演算法和領域專業知識與金融市場不斷變化的動態保持一致，以獲得精確、可行的見解。
2. **金融大型語言模型演算法層**：金融大型語言模型演算法層配置和利用專為特定領域和全球市場分析量身定制的特殊調整模型。
3. **LLMOps 和 DataOps 層**：LLMOps 層實施多源整合策略，為特定金融任務選擇最合適的大型語言模型，利用一系列最先進的模型。
4. **多源大型語言模型基礎模型層**：此基礎層支援各種通用和專用大型語言模型的即插即用功能。

## FinRobot：代理工作流程
<div align="center">
<img align="center" src="https://github.com/AI4Finance-Foundation/FinRobot/assets/31713746/ff8033be-2326-424a-ac11-17e2c9c4983d" width="60%"/>
</div>

1. **感知**：此模組從市場資訊、新聞和經濟指標中捕捉和解釋多模態金融數據，使用複雜的技術將數據結構化以進行徹底分析。
2. **大腦**：作為核心處理單元，此模組利用大型語言模型感知來自感知模組的數據，並利用金融思維鏈（CoT）過程生成結構化指令。
3. **行動**：此模組執行來自大腦模組的指令，應用工具將分析見解轉化為可行的結果。行動包括交易、投資組合調整、生成報告或發送警報，從而積極影響金融環境。

## FinRobot：智慧排程器
<div align="center">
<img align="center" src="https://github.com/AI4Finance-Foundation/FinRobot/assets/31713746/06fa0b78-ac53-48d3-8a6e-98d15386327e" width="60%"/>
</div>

智慧排程器是確保模型多樣性並優化整合和為每個任務選擇最合適的大型語言模型的關鍵。
* **指導代理**：此組件協調任務分配過程，確保根據代理的性能指標和對特定任務的適用性將任務分配給代理。
* **代理註冊**：管理系統內代理的註冊並跟踪其可用性，促進高效的任務分配過程。
* **代理適配器**：為特定任務量身定制代理功能，增強其在整個系統中的性能和整合。
* **任務管理器**：管理和儲存為各種金融任務量身定制的不同通用和微調的大型語言模型代理，並定期更新以確保相關性和有效性。

## 檔案結構

主資料夾 **finrobot** 有三個子資料夾 **agents、data_source、functional**。

```
FinRobot
├── finrobot (主資料夾)
│   ├── agents
│   │   ├── agent_library.py
│   │   └── workflow.py
│   ├── data_source
│   │   ├── finnhub_utils.py
│   │   ├── finnlp_utils.py
│   │   ├── fmp_utils.py
│   │   ├── sec_utils.py
│   │   └── yfinance_utils.py
│   ├── functional
│   │   ├── analyzer.py
│   │   ├── charting.py
│   │   ├── coding.py
│   │   ├── quantitative.py
│   │   ├── reportlab.py
│   │   └── text.py
│   ├── toolkits.py
│   └── utils.py
│
├── configs
├── experiments
├── tutorials_beginner (入門教學)
│   ├── agent_fingpt_forecaster.ipynb
│   └── agent_annual_report.ipynb
├── tutorials_advanced (給潛在 finrobot 開發者的進階教學)
│   ├── agent_trade_strategist.ipynb
│   ├── agent_fingpt_forecaster.ipynb
│   ├── agent_annual_report.ipynb
│   ├── lmm_agent_mplfinance.ipynb
│   └── lmm_agent_opt_smacross.ipynb
├── setup.py
├── OAI_CONFIG_LIST_sample
├── config_api_keys_sample
├── requirements.txt
└── README.md
```

## 安裝：

**1. (建議) 建立一個新的虛擬環境**
```shell
conda create --name finrobot python=3.10
conda activate finrobot
```
**2. 使用終端機或手動下載 FinRobot 儲存庫**
```shell
git clone https://github.com/AI4Finance-Foundation/FinRobot.git
cd FinRobot
```
**3. 從原始碼或 pypi 安裝 finrobot 及相依套件**

從 pypi 取得我們最新的版本
```bash
pip install -U finrobot
```
或直接從此儲存庫安裝
```
pip install -e .
```
**4. 修改 OAI_CONFIG_LIST_sample 檔案**
```shell
1) 將 OAI_CONFIG_LIST_sample 重新命名為 OAI_CONFIG_LIST
2) 移除 OAI_CONFIG_LIST 檔案中的四行註解
3) 加入您自己的 openai api-key <your OpenAI API key here>
```
**5. 修改 config_api_keys_sample 檔案**
```shell
1) 將 config_api_keys_sample 重新命名為 config_api_keys
2) 移除 config_api_keys 檔案中的註解
3) 加入您自己的 finnhub-api "YOUR_FINNHUB_API_KEY"
4) 加入您自己的 financialmodelingprep 和 sec-api 金鑰 "YOUR_FMP_API_KEY" 和 "YOUR_SEC_API_KEY" (用於生成財務報告)
```
**6. 開始瀏覽下面的教學或示範：**
```
# 在 tutorials 中找到這些筆記本
1) agent_annual_report.ipynb
2) agent_fingpt_forecaster.ipynb
3) agent_trade_strategist.ipynb
4) lmm_agent_mplfinance.ipynb
5) lmm_agent_opt_smacross.ipynb
```

## 示範
### 1. 市場預測代理 (預測股價走勢方向)
輸入公司的股票代碼、近期基本財務數據和市場新聞，預測其股價走勢。

1. 匯入
```python
import autogen
from finrobot.utils import get_current_date, register_keys_from_json
from finrobot.agents.workflow import SingleAssistant
```
2. 設定
```python
# 從 JSON 檔案讀取 OpenAI API 金鑰
llm_config = {
    "config_list": autogen.config_list_from_json(
        "../OAI_CONFIG_LIST",
        filter_dict={"model": ["gpt-4-0125-preview"]},
    ),
    "timeout": 120,
    "temperature": 0,
}

# 註冊 FINNHUB API 金鑰
register_keys_from_json("../config_api_keys")
```
3. 執行
```python
company = "NVDA"

assitant = SingleAssistant(
    "Market_Analyst",
    llm_config,
    # 如果您想聊天而不是僅接收預測，請設定為 "ALWAYS"
    human_input_mode="NEVER",
)
assitant.chat(
    f"使用所有提供的工具來檢索 {company} 在 {get_current_date()} 時的可用資訊。分別用 2-4 個最重要的因素簡潔地分析 {company} 的積極發展和潛在擔憂。大多數因素應從公司相關新聞中推斷。"
    f"然後對 {company} 下週的股價走勢做出粗略預測（例如上漲/下跌 2-3%）。提供摘要分析以支持您的預測。"
)
```
4. 結果
<div align="center">
<img align="center" src="https://github.com/AI4Finance-Foundation/FinRobot/assets/31713746/812ec23a-9cb3-4fad-b716-78533ddcd9dc" width="40%"/>
<img align="center" src="https://github.com/AI4Finance-Foundation/FinRobot/assets/31713746/9a2f9f48-b0e1-489c-8679-9a4c530f313c" width="41%"/>
</div>

### 2. 用於報告撰寫的金融分析師代理 (股票研究報告)
輸入公司的 10-K 表格、財務數據和市場數據，輸出一份股票研究報告。

1. 匯入
```python
import os
import autogen
from textwrap import dedent
from finrobot.utils import register_keys_from_json
from finrobot.agents.workflow import SingleAssistantShadow
```
2. 設定
```python
llm_config = {
    "config_list": autogen.config_list_from_json(
        "../OAI_CONFIG_LIST",
        filter_dict={
            "model": ["gpt-4-0125-preview"],
        },
    ),
    "timeout": 120,
    "temperature": 0.5,
}
register_keys_from_json("../config_api_keys")

# 中間策略模組將保存在此目錄中
work_dir = "../report"
os.makedirs(work_dir, exist_ok=True)

assistant = SingleAssistantShadow(
    "Expert_Investor",
    llm_config,
    max_consecutive_auto_reply=None,
    human_input_mode="TERMINATE",
)

```
3. 執行
```python
company = "Microsoft"
fyear = "2023"

message = dedent(
    f"""
    使用您被提供的工具，根據 {company} 的 {fyear} 10-K 報告撰寫一份年度報告，並將其格式化為 pdf。
    請注意以下事項：
    - 在開始之前明確解釋您的工作計劃。
    - 為求清晰，請逐一使用工具，尤其是在請求指示時。
    - 您所有的檔案操作都應在 "{work_dir}" 中完成。
    - 一旦生成任何圖片，請在聊天中顯示。
    - 所有段落的字數應在 400 到 450 字之間，在明確滿足此要求之前不要生成 pdf。
    """
)

assistant.chat(message, use_cache=True, max_turns=50,
               summary_method="last_msg")
```
4. 結果
<div align="center">
<img align="center" src="https://github.com/AI4Finance-Foundation/FinRobot/assets/31713746/d2d999e0-dc0e-4196-aca1-218f5fadcc5b" width="60%"/>
<img align="center" src="https://github.com/AI4Finance-Foundation/FinRobot/assets/31713746/3a21873f-9498-4d73-896b-3740bf6d116d" width="60%"/>
</div>

**金融思維鏈 (Financial CoT)**：
1. **收集初步數據**：10-K 報告、市場數據、財務比率
2. **分析財務報表**：資產負債表、損益表、現金流量表
3. **公司概況與績效**：公司描述、業務亮點、部門分析
4. **風險評估**：評估風險
5. **財務績效視覺化**：繪製本益比和每股盈餘圖表
6. **將發現綜合為段落**：將所有部分組合成連貫的摘要
7. **生成 PDF 報告**：使用工具自動生成 PDF
8. **品質保證**：檢查字數

### 3. 具備多模態能力的交易策略師代理

## AI 代理論文

+ [史丹佛大學 + 微軟研究院] [Agent AI: Surveying the Horizons of Multimodal Interaction](https://arxiv.org/abs/2401.03568)
+ [史丹佛大學] [Generative Agents: Interactive Simulacra of Human Behavior](https://arxiv.org/abs/2304.03442)
+ [復旦大學自然語言處理組] [The Rise and Potential of Large Language Model Based Agents: A Survey](https://arxiv.org/abs/2309.07864)
+ [復旦大學自然語言處理組] [LLM-Agent-Paper-List](https://github.com/WooooDyy/LLM-Agent-Paper-List)
+ [清華大學] [Large Language Models Empowered Agent-based Modeling and Simulation: A Survey and Perspectives](https://arxiv.org/abs/2312.11970)
+ [中國人民大學] [A Survey on Large Language Model-based Autonomous Agents](https://arxiv.org/pdf/2308.11432.pdf)
+ [南洋理工大學] [FinAgent: A Multimodal Foundation Agent for Financial Trading: Tool-Augmented, Diversified, and Generalist](https://arxiv.org/abs/2402.18485)

## AI 代理部落格與影片
+ [Medium] [An Introduction to AI Agents](https://medium.com/humansdotai/an-introduction-to-ai-agents-e8c4afd2ee8f)
+ [Medium] [Unmasking the Best Character AI Chatbots | 2024](https://medium.com/@aitrendorbit/unmasking-the-best-character-ai-chatbots-2024-351de43792f4#the-best-character-ai-chatbots)
+ [big-picture] [ChatGPT, Next Level: Meet 10 Autonomous AI Agents](https://blog.big-picture.com/en/chatgpt-next-level-meet-10-autonomous-ai-agents-auto-gpt-babyagi-agentgpt-microsoft-jarvis-chaosgpt-friends/)
+ [TowardsDataScience] [Navigating the World of LLM Agents: A Beginner’s Guide](https://towardsdatascience.com/navigating-the-world-of-llm-agents-a-beginners-guide-3b8d499db7a9)
+ [YouTube] [Introducing Devin - The "First" AI Agent Software Engineer](https://www.youtube.com/watch?v=iVbN95ica_k)

## AI 代理開源框架與工具
+ [AutoGPT (163k stars)](https://github.com/Significant-Gravitas/AutoGPT) 是一個供所有人使用的工具，旨在普及 AI，讓每個人都能使用和建立。
+ [LangChain (87.4k stars)](https://github.com/langchain-ai/langchain) 是一個用於開發由語言模型驅動的情境感知應用程式的框架，使其能夠連接到情境來源並依賴模型的推理能力進行回應和行動。
+ [MetaGPT (41k stars)](https://github.com/geekan/MetaGPT) 是一個多代理開源框架，為 GPT 分配不同角色，形成一個協作的軟體實體來執行複雜任務。
+ [dify (34.1.7k stars)](https://github.com/langgenius/dify) 是一個 LLM 應用開發平台。它整合了後端即服務和 LLMOps 的概念，涵蓋了建構生成式 AI 原生應用所需的核心技術堆疊，包括內建的 RAG 引擎。
+ [AutoGen (27.4k stars)](https://github.com/microsoft/autogen) 是一個用於開發 LLM 應用程式的框架，其中包含協作解決任務的對話代理。這些代理是可自訂的，支援人類互動，並在結合 LLM、人類輸入和工具的模式下運作。
+ [ChatDev (24.1k stars)](https://github.com/OpenBMB/ChatDev) 是一個專注於開發能夠進行對話和問答的對話式 AI 代理的框架。它提供一系列預訓練模型和互動式介面，方便使用者開發自訂的聊天代理。
+ [BabyAGI (19.5k stars)](https://github.com/yoheinakajima/babyagi) 是一個由 AI 驅動的任務管理系統，致力於建立具有初步通用智慧的 AI 代理。
+ [CrewAI (16k stars)](https://github.com/joaomdmoura/crewAI) 是一個用於協調角色扮演、自主 AI 代理的框架。透過促進協作智慧，CrewAI 使代理能夠無縫協作，處理複雜任務。
+ [SuperAGI (14.8k stars)](https://github.com/TransformerOptimus/SuperAGI) 是一個以開發者為優先的開源自主 AI 代理框架，使開發人員能夠建立、管理和運行有用的自主代理。
+ [FastGPT (14.6k stars)](https://github.com/labring/FastGPT) 是一個基於 LLM 的知識庫平台，提供開箱即用的數據處理和模型調用功能，並允許透過流程視覺化進行工作流程編排。
+ [XAgent (7.8k stars)](https://github.com/OpenBMB/XAgent) 是一個開源的實驗性大型語言模型（LLM）驅動的自主代理，可以自動解決各種任務。
+ [Bisheng (7.8k stars)](https://github.com/dataelement/bisheng) 是一個領先的開發 LLM 應用程式的開源平台。
+ [Voyager (5.3k stars)](https://github.com/OpenBMB/XAgent) 一個具有大型語言模型的開放式實體代理。
+ [CAMEL (4.7k stars)](https://github.com/camel-ai/camel) 是一個提供一套全面的工具和演算法來建立多模態 AI 代理的框架，使其能夠處理文本、圖像和語音等多種數據形式。
+ [Langfuse (4.3k stars)](https://github.com/langfuse/langfuse) 是一個語言融合框架，可以整合多個 AI 代理的語言能力，使其能夠同時具備多語言理解和生成能力。

## 引用 FinRobot
```
@inproceedings{
zhou2024finrobot,
title={FinRobot: {AI} Agent for Equity Research and Valuation with Large Language Models},
author={Tianyu Zhou and Pinqiao Wang and Yilin Wu and Hongyang Yang},
booktitle={ICAIF 2024: The 1st Workshop on Large Language Models and Generative AI for Finance},
year={2024}
}

@article{yang2024finrobot,
  title={FinRobot: An Open-Source AI Agent Platform for Financial Applications using Large Language Models},
  author={Yang, Hongyang and Zhang, Boyu and Wang, Neng and Guo, Cheng and Zhang, Xiaoli and Lin, Likun and Wang, Junlin and Zhou, Tianyu and Guan, Mao and Zhang, Runjia and others},
  journal={arXiv preprint arXiv:2405.14767},
  year={2024}
}

@inproceedings{han2024enhancing,
  title={Enhancing Investment Analysis: Optimizing AI-Agent Collaboration in Financial Research},
  author={Han, Xuewen and Wang, Neng and Che, Shangkun and Yang, Hongyang and Zhang, Kunpeng and Xu, Sean Xin},
  booktitle={ICAIF 2024: Proceedings of the 5th ACM International Conference on AI in Finance},
  pages={538--546},
  year={2024}
}
```
**免責聲明**：此處提供的程式碼和文件根據 Apache-2.0 授權條款發布。它們不應被視為財務建議或即時交易的建議。在進行任何交易或投資行動之前，必須謹慎行事並諮詢合格的金融專業人士。
