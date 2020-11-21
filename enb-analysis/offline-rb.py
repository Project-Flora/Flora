#!/usr/bin/python

import os
import sys
import shutil
import traceback
import matplotlib.pyplot as plt
import numpy as np

from mobile_insight_enb.monitor import OfflineReplayer
from rb_analyzer_enb import RBAnalyzer

def rb_analysis():
    # src = OfflineReplayer()
    # src.set_input_path('/sdcard/mobileinsight/plugins/test_analyzer/vr_log.mi2log')
    # cache_directory = mi2app_utils.get_cache_dir()
    # log_directory = os.path.join(cache_directory, "mi2log")

    src = OfflineReplayer()
    src.set_input_path(sys.argv[1])

    analyzer = RBAnalyzer()
    analyzer.set_source(src)

    src.run()
    return analyzer.rb_dict

dic = rb_analysis()
print(dic)