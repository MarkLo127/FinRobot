# FinRobot: 使用大型語言模型進行財務分析的開源人工智慧代理平台

<div align="center">
</div>

**FinRobot** is an AI Agent Platform that transcends the scope of FinGPT, representing a comprehensive solution meticulously designed for financial applications. It integrates **a diverse array of AI technologies**, extending beyond mere language models. This expansive vision highlights the platform's versatility and adaptability, addressing the multifaceted needs of the financial industry.

## FinRobot Ecosystem
<div align="center">
<img align="center" src="https://github.com/AI4Finance-Foundation/FinRobot/assets/31713746/6b30d9c1-35e5-4d36-a138-7e2769718f62" width="90%"/>
</div>

### The overall framework of FinRobot is organized into four distinct layers, each designed to address specific aspects of financial AI processing and application:
1. **Financial AI Agents Layer**: The Financial AI Agents Layer now includes Financial Chain-of-Thought (CoT) prompting, enhancing complex analysis and decision-making capacity. Market Forecasting Agents, Document Analysis Agents, and Trading Strategies Agents utilize CoT to dissect financial challenges into logical steps, aligning their advanced algorithms and domain expertise with the evolving dynamics of financial markets for precise, actionable insights.
2. **Financial LLMs Algorithms Layer**: The Financial LLMs Algorithms Layer configures and utilizes specially tuned models tailored to specific domains and global market analysis. 
3. **LLMOps and DataOps Layers**: The LLMOps layer implements a multi-source integration strategy that selects the most suitable LLMs for specific financial tasks, utilizing a range of state-of-the-art models. 
4. **Multi-source LLM Foundation Models Layer**: This foundational layer supports the plug-and-play functionality of various general and specialized LLMs. 


## FinRobot: Agent Workflow
<div align="center">
<img align="center" src="https://github.com/AI4Finance-Foundation/FinRobot/assets/31713746/ff8033be-2326-424a-ac11-17e2c9c4983d" width="60%"/>
</div>

1. **Perception**: This module captures and interprets multimodal financial data from market feeds, news, and economic indicators, using sophisticated techniques to structure the data for thorough analysis.

2. **Brain**: Acting as the core processing unit, this module perceives data from the Perception module with LLMs and utilizes Financial Chain-of-Thought (CoT) processes to generate structured instructions.

3. **Action**: This module executes instructions from the Brain module, applying tools to translate analytical insights into actionable outcomes. Actions include trading, portfolio adjustments, generating reports, or sending alerts, thereby actively influencing the financial environment.

## FinRobot: Smart Scheduler
<div align="center">
<img align="center" src="https://github.com/AI4Finance-Foundation/FinRobot/assets/31713746/06fa0b78-ac53-48d3-8a6e-98d15386327e" width="60%"/>
</div>

The Smart Scheduler is central to ensuring model diversity and optimizing the integration and selection of the most appropriate LLM for each task.
* **Director Agent**: This component orchestrates the task assignment process, ensuring that tasks are allocated to agents based on their performance metrics and suitability for specific tasks.
* **Agent Registration**: Manages the registration and tracks the availability of agents within the system, facilitating an efficient task allocation process.
* **Agent Adaptor**: Tailor agent functionalities to specific tasks, enhancing their performance and integration within the overall system.
* **Task Manager**: Manages and stores different general and fine-tuned LLMs-based agents tailored for various financial tasks, updated periodically to ensure relevance and efficacy.

## File Structure

The main folder **finrobot** has three subfolders **agents, data_source, functional**. 

```
FinRobot
├── finrobot_zh (main folder)
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
├── tutorials_beginner (hands-on tutorial)
│   ├── agent_fingpt_forecaster.ipynb
│   └── agent_annual_report.ipynb 
├── tutorials_advanced (advanced tutorials for potential finrobot developers)
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

## Installation:

**1. (Recommended) Create a new virtual environment**
```shell
conda create --name finrobot python=3.10
conda activate finrobot
```
**2. download the FinRobot repo use terminal or download it manually**
```shell
git clone https://github.com/AI4Finance-Foundation/FinRobot.git
cd FinRobot
```
**3. install finrobot & dependencies from source or pypi**

get our latest release from pypi
```bash
pip install -U finrobot
```
or install from this repo directly
```
pip install -e .
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
**6. start navigating the tutorials or the demos below:**
```
# find these notebooks in tutorials
1) agent_annual_report.ipynb
2) agent_fingpt_forecaster.ipynb
3) agent_trade_strategist.ipynb
4) lmm_agent_mplfinance.ipynb
5) lmm_agent_opt_smacross.ipynb
```

## Demos
### 1. Market Forecaster Agent (Predict Stock Movements Direction)
Takes a company's ticker symbol, recent basic financials, and market news as input and predicts its stock movements.

1. Import 
```python
import autogen
from finrobot.utils import get_current_date, register_keys_from_json
from finrobot.agents.workflow import SingleAssistant
```
2. Config
```python
# Read OpenAI API keys from a JSON file
llm_config = {
    "config_list": autogen.config_list_from_json(
        "../OAI_CONFIG_LIST",
        filter_dict={"model": ["gpt-4-0125-preview"]},
    ),
    "timeout": 120,
    "temperature": 0,
}

# Register FINNHUB API keys
register_keys_from_json("../config_api_keys")
```
3. Run
```python
company = "NVDA"

assitant = SingleAssistant(
    "Market_Analyst",
    llm_config,
    # set to "ALWAYS" if you want to chat instead of simply receiving the prediciton
    human_input_mode="NEVER",
)
assitant.chat(
    f"Use all the tools provided to retrieve information available for {company} upon {get_current_date()}. Analyze the positive developments and potential concerns of {company} "
    "with 2-4 most important factors respectively and keep them concise. Most factors should be inferred from company related news. "
    f"Then make a rough prediction (e.g. up/down by 2-3%) of the {company} stock price movement for next week. Provide a summary analysis to support your prediction."
)
```
4. Result
<div align="center">
<img align="center" src="https://github.com/AI4Finance-Foundation/FinRobot/assets/31713746/812ec23a-9cb3-4fad-b716-78533ddcd9dc" width="40%"/>
<img align="center" src="https://github.com/AI4Finance-Foundation/FinRobot/assets/31713746/9a2f9f48-b0e1-489c-8679-9a4c530f313c" width="41%"/>
</div>

### 2. Financial Analyst Agent for Report Writing (Equity Research Report)
Take a company's 10-k form, financial data, and market data as input and output an equity research report

1. Import 
```python
import os
import autogen
from textwrap import dedent
from finrobot.utils import register_keys_from_json
from finrobot.agents.workflow import SingleAssistantShadow
```
2. Config
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

# Intermediate strategy modules will be saved in this directory
work_dir = "../report"
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
company = "Microsoft"
fyear = "2023"

message = dedent(
    f"""
    With the tools you've been provided, write an annual report based on {company}'s {fyear} 10-k report, format it into a pdf.
    Pay attention to the followings:
    - Explicitly explain your working plan before you kick off.
    - Use tools one by one for clarity, especially when asking for instructions. 
    - All your file operations should be done in "{work_dir}". 
    - Display any image in the chat once generated.
    - All the paragraphs should combine between 400 and 450 words, don't generate the pdf until this is explicitly fulfilled.
"""
)

assistant.chat(message, use_cache=True, max_turns=50,
               summary_method="last_msg")
```
4. Result
<div align="center">
<img align="center" src="https://github.com/AI4Finance-Foundation/FinRobot/assets/31713746/d2d999e0-dc0e-4196-aca1-218f5fadcc5b" width="60%"/>
<img align="center" src="https://github.com/AI4Finance-Foundation/FinRobot/assets/31713746/3a21873f-9498-4d73-896b-3740bf6d116d" width="60%"/>
</div>

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
