# -*- coding: utf-8 -*-
import os
import json
import importlib
import yfinance as yf
import backtrader as bt
from backtrader.strategies import SMA_CrossOver
from typing import Annotated, List, Tuple
from matplotlib import pyplot as plt
from pprint import pformat
from IPython import get_ipython


class DeployedCapitalAnalyzer(bt.Analyzer):
    def start(self):
        self.deployed_capital = []
        self.initial_cash = self.strategy.broker.get_cash()  # 帳戶初始現金

    def notify_order(self, order):
        if order.status in [order.Completed]:
            if order.isbuy():
                self.deployed_capital.append(order.executed.price * order.executed.size)
            elif order.issell():
                self.deployed_capital.append(order.executed.price * order.executed.size)

    def stop(self):
        total_deployed = sum(self.deployed_capital)
        final_cash = self.strategy.broker.get_value()
        net_profit = final_cash - self.initial_cash
        if total_deployed > 0:
            self.retn = net_profit / total_deployed
        else:
            self.retn = 0

    def get_analysis(self):
        return {"return_on_deployed_capital": self.retn}


class BackTraderUtils:

    def back_test(
        ticker_symbol: Annotated[
            str, "股票代碼（例如：'AAPL' 代表蘋果公司）"
        ],
        start_date: Annotated[
            str, "歷史數據的開始日期，格式為 'YYYY-MM-DD'"
        ],
        end_date: Annotated[
            str, "歷史數據的結束日期，格式為 'YYYY-MM-DD'"
        ],
        strategy: Annotated[
            str,
            "要回測的 BackTrader 策略類別。可以是預定義的或自定義的。預定義選項：'SMA_CrossOver'。如果是自定義的，請提供模組路徑和類別名稱，格式如 'my_module:TestStrategy'。",
        ],
        strategy_params: Annotated[
            str,
            "傳遞給策略類別的額外參數，格式為 JSON 字串。例如：{'fast': 10, 'slow': 30} 用於 SMACross。",
        ] = "",
        sizer: Annotated[
            int | str | None,
            "用於回測的倉位管理器。可以是固定數字或自定義 Sizer 類別。如果輸入是整數，將應用相應的固定倉位管理器。如果是自定義的，請提供模組路徑和類別名稱，格式如 'my_module:TestSizer'。",
        ] = None,
        sizer_params: Annotated[
            str,
            "傳遞給倉位管理器類別的額外參數，格式為 JSON 字串。",
        ] = "",
        indicator: Annotated[
            str | None,
            "添加到策略的自定義指標類別。請提供模組路徑和類別名稱，格式如 'my_module:TestIndicator'。",
        ] = None,
        indicator_params: Annotated[
            str,
            "傳遞給指標類別的額外參數，格式為 JSON 字串。",
        ] = "",
        cash: Annotated[
            float, "回測的初始現金金額。預設為 10000.0"
        ] = 10000.0,
        save_fig: Annotated[
            str | None, "儲存回測結果圖表的路徑。預設為 None。"
        ] = None,
    ) -> str:
        """
        使用 Backtrader 函式庫對歷史股票數據進行交易策略回測。
        """
        cerebro = bt.Cerebro()

        if strategy == "SMA_CrossOver":
            strategy_class = SMA_CrossOver
        else:
            assert (
                ":" in strategy
            ), "自定義策略應該是模組路徑和類別名稱，用冒號分隔。"
            module_path, class_name = strategy.split(":")
            module = importlib.import_module(module_path)
            strategy_class = getattr(module, class_name)

        strategy_params = json.loads(strategy_params) if strategy_params else {}
        cerebro.addstrategy(strategy_class, **strategy_params)

        # 創建數據源
        data = bt.feeds.PandasData(
            dataname=yf.download(ticker_symbol, start_date, end_date, auto_adjust=True)
        )
        cerebro.adddata(data)  # 添加數據源
        # 設定初始現金
        cerebro.broker.setcash(cash)

        # 設定交易規模
        if sizer is not None:
            if isinstance(sizer, int):
                cerebro.addsizer(bt.sizers.FixedSize, stake=sizer)
            else:
                assert (
                    ":" in sizer
                ), "自定義倉位管理器應該是模組路徑和類別名稱，用冒號分隔。"
                module_path, class_name = sizer.split(":")
                module = importlib.import_module(module_path)
                sizer_class = getattr(module, class_name)
                sizer_params = json.loads(sizer_params) if sizer_params else {}
                cerebro.addsizer(sizer_class, **sizer_params)

        # 設定額外指標
        if indicator is not None:
            assert (
                ":" in indicator
            ), "自定義指標應該是模組路徑和類別名稱，用冒號分隔。"
            module_path, class_name = indicator.split(":")
            module = importlib.import_module(module_path)
            indicator_class = getattr(module, class_name)
            indicator_params = json.loads(indicator_params) if indicator_params else {}
            cerebro.addindicator(indicator_class, **indicator_params)

        # 附加分析器
        cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name="sharpe_ratio")
        cerebro.addanalyzer(bt.analyzers.DrawDown, _name="draw_down")
        cerebro.addanalyzer(bt.analyzers.Returns, _name="returns")
        cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="trade_analyzer")

        stats_dict = {"起始投資組合價值：": cerebro.broker.getvalue()}

        results = cerebro.run()  # 執行回測
        first_strategy = results[0]

        # 存取分析結果
        stats_dict["最終投資組合價值"] = cerebro.broker.getvalue()
        stats_dict["夏普比率"] = (
            first_strategy.analyzers.sharpe_ratio.get_analysis()
        )
        stats_dict["回撤"] = first_strategy.analyzers.draw_down.get_analysis()
        stats_dict["報酬率"] = first_strategy.analyzers.returns.get_analysis()
        stats_dict["交易分析"] = (
            first_strategy.analyzers.trade_analyzer.get_analysis()
        )

        if save_fig:
            directory = os.path.dirname(save_fig)
            if directory:
                os.makedirs(directory, exist_ok=True)
            plt.figure(figsize=(12, 8))
            cerebro.plot()
            plt.savefig(save_fig)
            plt.close()

        return "回測完成。結果：\n" + pformat(stats_dict, indent=2)


if __name__ == "__main__":
    # 使用範例：
    start_date = "2011-01-01"
    end_date = "2012-12-31"
    ticker = "MSFT"
    BackTraderUtils.back_test(
        ticker,
        start_date,
        end_date,
        "test_module:TestStrategy",
        {"exitbars": 5},
    )
