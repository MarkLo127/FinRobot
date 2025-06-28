<div align="center">
<img align="center" width="30%" alt="image" src="https://github.com/AI4Finance-Foundation/FinGPT/assets/31713746/e0371951-1ce1-488e-aa25-0992dafcc139">
</div>

# FinRobot：基於大型語言模型的開源金融分析 AI 代理平台
[![Downloads](https://static.pepy.tech/badge/finrobot)]([https://pepy.tech/project/finrobot](https://pepy.tech/project/finrobot))
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

**FinRobot** 是一個超越 FinGPT 範疇的 AI 代理平台，代表著一個專為金融應用精心設計的全面解決方案。它整合了**多樣化的 AI 技術**，不僅限於語言模型。這個廣闊的願景突顯了平台的多功能性和適應性，能夠滿足金融行業的多方面需求。

**AI 代理的概念**：AI 代理是一個智能實體，使用大型語言模型作為其大腦來感知環境、做出決策並執行行動。與傳統人工智能不同，AI 代理具有獨立思考和使用工具的能力，以逐步實現既定目標。

[FinRobot 白皮書](https://arxiv.org/abs/2405.14767)

[![](https://dcbadge.vercel.app/api/server/trsr8SXpW5)](https://discord.gg/trsr8SXpW5)

![訪客](https://api.visitorbadge.io/api/VisitorHit?user=AI4Finance-Foundation&repo=FinRobot&countColor=%23B17A)

## FinRobot 生態系統
<div align="center">
<img align="center" src="https://github.com/AI4Finance-Foundation/FinRobot/assets/31713746/6b30d9c1-35e5-4d36-a138-7e2769718f62" width="90%"/>
</div>

### FinRobot 的整體框架分為四個不同層次，每個層次都針對金融 AI 處理和應用的特定方面：
1. **金融 AI 代理層**：金融 AI 代理層現在包括金融思維鏈（CoT）提示，增強了複雜分析和決策能力。市場預測代理、文件分析代理和交易策略代理利用 CoT 將金融挑戰分解為邏輯步驟，將其先進算法和領域專業知識與不斷發展的金融市場動態相結合，以獲得精確、可行的見解。
2. **金融 LLMs 算法層**：金融 LLMs 算法層配置並使用專門針對特定領域和全球市場分析調整的模型。
3. **LLMOps 和 DataOps 層**：LLMOps 層實施多源集成策略，為特定金融任務選擇最合適的 LLMs，利用一系列最先進的模型。
4. **多源 LLM 基礎模型層**：這個基礎層支持各種通用和專業 LLMs 的即插即用功能。

## FinRobot：代理工作流程
<div align="center">
<img align="center" src="https://github.com/AI4Finance-Foundation/FinRobot/assets/31713746/ff8033be-2326-424a-ac11-17e2c9c4983d" width="60%"/>
</div>

1. **感知**：該模組捕獲並解釋來自市場動態、新聞和經濟指標的多模態金融數據，使用複雜的技術來構建數據以進行全面分析。

2. **大腦**：作為核心處理單元，該模組通過 LLMs 感知來自感知模組的數據，並利用金融思維鏈（CoT）過程生成結構化指令。

3. **行動**：該模組執行來自大腦模組的指令，應用工具將分析見解轉化為可行的結果。行動包括交易、投資組合調整、生成報告或發送警報，從而主動影響金融環境。

## FinRobot：智能調度器
<div align="center">
<img align="center" src="https://github.com/AI4Finance-Foundation/FinRobot/assets/31713746/06fa0b78-ac53-48d3-8a6e-98d15386327e" width="60%"/>
</div>

智能調度器是確保模型多樣性並優化每個任務最適合的 LLM 的整合和選擇的核心。
* **指導代理**：該組件協調任務分配過程，確保根據代理的性能指標和對特定任務的適用性分配任務。
* **代理註冊**：管理系統內代理的註冊並跟踪其可用性，促進高效的任務分配過程。
* **代理適配器**：根據特定任務調整代理功能，提升其性能和系統整合。
* **任務管理器**：管理和存儲針對各種金融任務定制的不同通用和微調 LLMs 代理，定期更新以確保相關性和效率。

## 文件結構

主資料夾 **finrobot** 有三個子資料夾 **agents, data_source, functional**。

```
FinRobot
├── finrobot (主資料夾)
│   ├── agents
│   	├── agent_library.py
│   	└── workflow.py
│   ├── data_source
│   	├── finnhub_utils.py
│   	├── finnlp_utils.py
│   	├── fmp_utils.py
│   	├── sec_utils.py
│   	└── yfinance_utils.py
│   ├── functional
│   	├── analyzer.py
│   	├── charting.py
│   	├── coding.py
│   	├── quantitative.py
│   	├── reportlab.py
│   	└── text.py
│   ├── toolkits.py
│   └── utils.py
│
├── configs
├── experiments
├── tutorials_beginner (入門教程)
│   ├── agent_fingpt_forecaster.ipynb
│   └── agent_annual_report.ipynb 
├── tutorials_advanced (進階教程，適用於潛在的 finrobot 開發者)
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

**1. (建議) 創建新的虛擬環境**
```shell
conda create --name finrobot python=3.10
conda activate finrobot
```
**2. 使用終端機下載 FinRobot 倉庫或手動下載**
```shell
git clone https://github.com/MarkLo127/FinRobot.git
cd FinRobot
```
**3. 從源碼或 pypi 安裝 finrobot 及其依賴**

從 pypi 獲取最新版本
```bash
pip install -U finrobot
```
或直接從此倉庫安裝
```
pip install -e .
```

```
cd FinNLP
pip install -e .
```

**4. 修改 OAI_CONFIG_LIST_sample 文件**
```shell
1) 將 OAI_CONFIG_LIST_sample 重命名為 OAI_CONFIG_LIST
2) 移除 OAI_CONFIG_LIST 文件中的四行註釋
3) 添加你自己的 openai api-key <your OpenAI API key here>
```
**5. 修改 config_api_keys_sample 文件**
```shell
1) 將 config_api_keys_sample 重命名為 config_api_keys
2) 移除 config_api_keys 文件中的註釋
3) 添加你自己的 finnhub-api "YOUR_FINNHUB_API_KEY"
4) 添加你自己的 financialmodelingprep 和 sec-api keys "YOUR_FMP_API_KEY" 和 "YOUR_SEC_API_KEY"（用於生成金融報告）
```
**6. 開始瀏覽教程或以下示例：**
```
# 在教程中找到這些筆記本
1) agent_annual_report.ipynb
2) agent_fingpt_forecaster.ipynb
3) agent_trade_strategist.ipynb
4) lmm_agent_mplfinance.ipynb
5) lmm_agent_opt_smacross.ipynb
```

## 示例
### 1. 市場預測代理（預測股票走勢方向）
輸入公司的股票代碼、近期基本財務數據和市場新聞，預測其股票走勢。

1. 導入
```python
import autogen
from finrobot.utils import get_current_date, register_keys_from_json
from finrobot.agents.workflow import SingleAssistant
```
2. 配置
```python
# 從 JSON 文件讀取 OpenAI API 密鑰
llm_config = {
    "config_list": autogen.config_list_from_json(
        "../OAI_CONFIG_LIST",
        filter_dict={"model": ["gpt-4-0125-preview"]},
    ),
    "timeout": 120,
    "temperature": 0,
}

# 註冊 FINNHUB API 密鑰
register_keys_from_json("../config_api_keys")
```
3. 運行
```python
company = "NVDA"

assitant = SingleAssistant(
    "Market_Analyst",
    llm_config,
    # 如果你想聊天而不是簡單地接收預測，設置為 "ALWAYS"
    human_input_mode="NEVER",
)
assitant.chat(
    f"使用所有提供的工具檢索 {company} 在 {get_current_date()} 的可用信息。分析 {company} 的正面發展和潛在問題，"
    "分別列出 2-4 個最重要的因素並保持簡潔。大多數因素應從公司相關新聞中推斷。"
    f"然後對下週 {company} 的股價走勢做出粗略預測（例如上漲/下跌 2-3%）。提供支持你預測的總結分析。"
)
```
4. 結果
<div align="center">
<img align="center" src="https://github.com/AI4Finance-Foundation/FinRobot/assets/31713746/812ec23a-9cb3-4fad-b716-78533ddcd9dc" width="40%"/>
<img align="center" src="https://github.com/AI4Finance-Foundation/FinRobot/assets/31713746/9a2f9f48-b0e1-489c-8679-9a4c530f313c" width="41%"/>
</div>

### 2. 金融分析師代理用於報告撰寫（股票研究報告）
輸入公司的 10-k 表格、財務數據和市場數據，輸出股票研究報告

1. 導入
```python
import os
import autogen
from textwrap import dedent
from finrobot.utils import register_keys_from_json
from finrobot.agents.workflow import SingleAssistantShadow
```
2. 配置
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

# 中間策略模組將保存在此目錄
work_dir = "../report"
os.makedirs(work_dir, exist_ok=True)

assistant = SingleAssistantShadow(
    "Expert_Investor",
    llm_config,
    max_consecutive_auto_reply=None,
    human_input_mode="TERMINATE",
)
```
3. 運行
```python
company = "Microsoft"
fyear = "2023"

message = dedent(
    f"""
    使用提供的工具，基於 {company} 的 {fyear} 10-k 報告撰寫年度報告，並格式化為 pdf。
    請注意以下幾點：
    - 在開始之前明確說明你的工作計劃。
    - 逐一使用工具以保持清晰，特別是在請求指示時。
    - 所有文件操作都應在 "{work_dir}" 中完成。
    - 生成後在聊天中顯示任何圖像。
    - 所有段落應合計在 400 到 450 字之間，在明確達到這個要求之前不要生成 pdf。
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

**金融思維鏈**：
1. **收集初步數據**：10-K 報告、市場數據、財務比率
2. **分析財務報表**：資產負債表、損益表、現金流量表
3. **公司概況和績效**：公司描述、業務亮點、部門分析
4. **風險評估**：評估風險
5. **財務績效可視化**：繪製市盈率和每股收益圖表
6. **將發現整合為段落**：將所有部分組合成連貫的摘要
7. **生成 PDF 報告**：使用工具自動生成 PDF
8. **質量保證**：檢查字數

### 3. 具有多模態能力的交易策略代理


## AI 代理相關論文

+ [史丹佛大學 + 微軟研究院] [代理 AI：探索多模態互動的視野](https://arxiv.org/abs/2401.03568)
+ [史丹佛大學] [生成式代理：人類行為的互動模擬](https://arxiv.org/abs/2304.03442)
+ [復旦大學 NLP 組] [大型語言模型基礎代理的崛起與潛力：一項調查](https://arxiv.org/abs/2309.07864)
+ [復旦大學 NLP 組] [LLM-Agent-Paper-List](https://github.com/WooooDyy/LLM-Agent-Paper-List)
+ [清華大學] [大型語言模型賦能的基於代理的建模與模擬：調查與展望](https://arxiv.org/abs/2312.11970)
+ [中國人民大學] [基於大型語言模型的自主代理調查](https://arxiv.org/pdf/2308.11432.pdf)
+ [南洋理工大學] [FinAgent：用於金融交易的多模態基礎代理：工具增強、多樣化和通用性](https://arxiv.org/abs/2402.18485)

## AI 代理博客和視頻
+ [Medium] [AI 代理簡介](https://medium.com/humansdotai/an-introduction-to-ai-agents-e8c4afd2ee8f)
+ [Medium] [揭秘最佳角色 AI 聊天機器人 | 2024](https://medium.com/@aitrendorbit/unmasking-the-best-character-ai-chatbots-2024-351de43792f4#the-best-character-ai-chatbots)
+ [big-picture] [ChatGPT 的下一個層次：認識 10 個自主 AI 代理](https://blog.big-picture.com/en/chatgpt-next-level-meet-10-autonomous-ai-agents-auto-gpt-babyagi-agentgpt-microsoft-jarvis-chaosgpt-friends/)
+ [TowardsDataScience] [探索 LLM 代理世界：初學者指南](https://towardsdatascience.com/navigating-the-world-of-llm-agents-a-beginners-guide-3b8d499db7a9)
+ [YouTube] [介紹 Devin - "第一個" AI 代理軟體工程師](https://www.youtube.com/watch?v=iVbN95ica_k)


## AI 代理開源框架和工具
+ [AutoGPT (163k stars)](https://github.com/Significant-Gravitas/AutoGPT) 是一個面向所有人的工具，旨在實現 AI 民主化，使每個人都能使用和建立於其上。
+ [LangChain (87.4k stars)](https://github.com/langchain-ai/langchain) 是一個用於開發由語言模型驅動的上下文感知應用程序的框架，使其能夠連接到上下文源並依賴模型的推理能力進行響應和行動。
+ [MetaGPT (41k stars)](https://github.com/geekan/MetaGPT) 是一個多代理開源框架，為 GPTs 分配不同角色，形成協作軟件實體以執行複雜任務。
+ [dify (34.1.7k stars)](https://github.com/langgenius/dify) 是一個 LLM 應用開發平台。它整合了後端即服務和 LLMOps 的概念，涵蓋了構建生成式 AI 原生應用所需的核心技術棧，包括內置的 RAG 引擎。
+ [AutoGen (27.4k stars)](https://github.com/microsoft/autogen) 是一個用於開發具有協作代理的 LLM 應用程序的框架。這些代理可定制，支持人機交互，並在結合 LLMs、人工輸入和工具的模式下運行。
+ [ChatDev (24.1k stars)](https://github.com/OpenBMB/ChatDev) 是一個專注於開發能夠對話和問答的會話式 AI 代理的框架。它提供了一系列預訓練模型和互動界面，方便用戶開發定制化的聊天代理。
+ [BabyAGI (19.5k stars)](https://github.com/yoheinakajima/babyagi) 是一個 AI 驅動的任務管理系統，致力於構建具有初步通用智能的 AI 代理。
+ [CrewAI (16k stars)](https://github.com/joaomdmoura/crewAI) 是一個用於編排角色扮演、自主 AI 代理的框架。通過促進協作智能，CrewAI 使代理能夠無縫協作，處理複雜任務。
+ [SuperAGI (14.8k stars)](https://github.com/TransformerOptimus/SuperAGI) 是一個面向開發者的開源自主 AI 代理框架，使開發者能夠構建、管理和運行有用的自主代理。
+ [FastGPT (14.6k stars)](https://github.com/labring/FastGPT) 是一個基於 LLM 構建的知識平台，提供開箱即用的數據處理和模型調用能力，允許通過 Flow 可視化進行工作流程編排。
+ [XAgent (7.8k stars)](https://github.com/OpenBMB/XAgent) 是一個開源的實驗性大型語言模型（LLM）驅動的自主代理，可以自動解決各種任務。
+ [Bisheng (7.8k stars)](https://github.com/dataelement/bisheng) 是一個領先的開源 LLM 應用開發平台。
+ [Voyager (5.3k stars)](https://github.com/OpenBMB/XAgent) 一個具有大型語言模型的開放式實體代理。
+ [CAMEL (4.7k stars)](https://github.com/camel-ai/camel) 是一個提供全面工具和算法集的框架，用於構建多模態 AI 代理，使其能夠處理文本、圖像和語音等各種數據形式。
+ [Langfuse (4.3k stars)](https://github.com/langfuse/langfuse) 是一個語言融合框架，可以整合多個 AI 代理的語言能力，使其同時具備多語言理解和生成能力。

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
**免責聲明**：此處提供的代碼和文檔根據 Apache-2.0 許可證發布。它們不應被視為金融建議或實盤交易建議。在進行任何交易或投資行為之前，務必謹慎並諮詢合格的金融專業人士。