#!/usr/bin/python
# Filename: dl_tput_analyzer.py
"""
Analyzer for PDSCH messages
Author: Zhaowei Tan
"""

__all__ = ["RBAnalyzer"]

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

from mobile_insight_enb.analyzer.analyzer import *
from mobile_insight_enb.analyzer import *
import time
import dis


class RBAnalyzer(Analyzer):
    """
    An KPI analyzer to monitor and manage uplink latency breakdown
    """
    def __init__(self):
        Analyzer.__init__(self)
        self.add_source_callback(self.__msg_callback)
        self.rb_dict = {}        

    def set_source(self, source):
        """
        Set the trace source. Enable the cellular signaling messages
        :param source: the trace source (collector).
        """
        Analyzer.set_source(self, source)
        source.enable_log_all()

    def __f_time_diff(self, t1, t2):
        if t1 > t2:
            t_diff = t2 + 10240 - t1
        else:
            t_diff = t2 - t1 + 1
        return t_diff


    def __msg_callback(self, msg):
        if msg.type_id == "LTE_PHY_PDSCH_Stat_Indication":
            # return
            records = msg.data['Records']
            # print (records)
            for record in records:
                sfn = record['Subframe Num']
                fn = record['Frame Num']
                nRB = record['Num RBs']
                self.rb_dict[nRB] = self.rb_dict.get(nRB, 0) + 1