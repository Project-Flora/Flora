#!/usr/bin/python
# Filename: offline_replayer.py
"""
An offline log replayer for eNB
Author: Zhaowei tan
"""

__all__ = ["OfflineReplayer"]

import sys
import os
import timeit
import time

from .monitor import Monitor, Event
from .decoder import mi_enb_decoder


class OfflineReplayer(Monitor):
    """
    A log replayer for offline analysis.
    """

    def __init__(self):
        Monitor.__init__(self)

        self.is_android = False
        self.service_context = None


        if self.is_android:
            libs_path = self.__get_libs_path()

            prefs = {
                "ws_dissect_executable_path": os.path.join(
                    libs_path,
                    "android_pie_ws_dissector"),
                "libwireshark_path": libs_path}
        else:
            prefs = {}

        #DMLogPacket.init(prefs)

        self._type_names = []

    def __del__(self):
        if self.is_android and self.service_context:
            print ("detaching...")
            from service import mi2app_utils
            mi2app_utils.detach_thread()

    # def __get_cache_dir(self):
    #     if self.is_android:
    #         return str(self.service_context.getCacheDir().getAbsolutePath())
    #     else:
    #         return ""

    def __get_libs_path(self):
        if self.is_android and self.service_context:
            return os.path.join(
                self.service_context.getFilesDir().getAbsolutePath(), "data")
        else:
            return "./data"

    def available_log_types(self):
        """
        Return available log types
        :returns: a list of supported message types
        """
        return self.__class__.SUPPORTED_TYPES

    def enable_log(self, type_name):
        """
        Enable the messages to be monitored. Refer to cls.SUPPORTED_TYPES for supported types.
        If this method is never called, the config file existing on the SD card will be used.
        :param type_name: the message type(s) to be monitored
        :type type_name: string or list
        :except ValueError: unsupported message type encountered
        """
        cls = self.__class__
        if isinstance(type_name, str):
            type_name = [type_name]
        for n in type_name:
            if n not in cls.SUPPORTED_TYPES:
                self.log_warning("Unsupported log message type: %s" % n)
            if n not in self._type_names:
                self._type_names.append(n)
                self.log_info("Enable " + n)
        dm_collector_c.set_filtered(self._type_names)

    def enable_log_all(self):
        """
        Enable all supported logs
        """
        return
        cls = self.__class__
        self.enable_log(cls.SUPPORTED_TYPES)

    def set_input_path(self, path):
        """
        Set the replay trace path
        :param path: the replay file path. If it is a directory, the OfflineReplayer will read all logs under this directory (logs in subdirectories are ignored)
        :type path: string
        """
        self._input_path = path
        # self._input_file = open(path, "rb")

    def save_log_as(self, path):
        """
        Save the log as a mi2log file (for offline analysis)
        :param path: the file name to be saved
        :type path: string
        :param log_types: a filter of message types to be saved
        :type log_types: list of string
        """
        dm_collector_c.set_filtered_export(path, self._type_names)

    def run(self):
        """
        Start monitoring the mobile network. This is usually the entrance of monitoring and analysis.
        """

        # fd = open('./Diag.cfg','wb')
        # dm_collector_c.generate_diag_cfg(fd, self._type_names)
        # fd.close()

        try:

            self.broadcast_info('STARTED',{})
            self.log_info('STARTED: ' + str(time.time()))
            log_list = []
            if os.path.isfile(self._input_path):
                log_list = [self._input_path]
            elif os.path.isdir(self._input_path):
                for file in os.listdir(self._input_path):
                    if file.endswith(".mi2log") or file.endswith(".qmdl"):
                        # log_list.append(self._input_path+"/"+file)
                        log_list.append(os.path.join(self._input_path, file))
            else:
                return

            log_list.sort()  # Hidden assumption: logs follow the diag_log_TIMSTAMP_XXX format

            decoding_inter = 0
            sending_inter = 0
            for file in log_list:
                self.log_info("Loading " + file)
                self.log_info('Loading: ' + str(time.time()))
                self._input_file = open(file, "rb")

                while True:
                    s = self._input_file.readline()
                    if not s:   # EOF encountered
                        break
                    DC = mi_enb_decoder(s)
                    type_id = DC.get_type_id()
                    if (type_id is None):
                        continue
                    d = DC.get_content()
                    if (d is not None):
                        event = Event(timeit.default_timer(),
                                      type_id,
                                      d)
                        self.send(event)
                        
                self._input_file.close()

        except Exception as e:
            import traceback
            sys.exit(str(traceback.format_exc()))
            # sys.exit(e)
        event = Event(timeit.default_timer(), 'Monitor.STOP', None)
        self.send(event)
        self.log_info("Offline replay is completed.")