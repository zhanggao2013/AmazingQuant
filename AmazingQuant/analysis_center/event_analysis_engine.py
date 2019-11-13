# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2019/11/14
# @Author  : gao
# @File    : event_analysis_engine.py
# @Project : AmazingQuant
# ------------------------------

from AmazingQuant.event_engine.event_backtesting_analysis import *
from AmazingQuant.event_engine.event_engine_base import EventEngineBase


class EmptyClass(object):
    pass


def run_backtesting_analysis_engine(strategy):
    """

    """
    backtesting_analysis_engine = EventEngineBase()
    event_backtesting = EventBacktestingAnalysis()
    event_backtesting.event_data_dict["strategy"] = strategy

    backtesting_analysis_engine.put(event_backtesting)

    backtesting_analysis_engine.register(EventType.EVENT_BACKTESTING_ANALYSIS.value,
                                         EventBacktestingAnalysis.save_backtesting_record_to_csv)
    backtesting_analysis_engine.register(EventType.EVENT_BACKTESTING_ANALYSIS.value,
                                         EventBacktestingAnalysis.show_backtesting_indicator)

    backtesting_analysis_engine.start(timer=False)
    backtesting_analysis_engine.stop()

if __name__ == "__main__":
    run_backtesting_analysis_engine("qweqweqwe")
