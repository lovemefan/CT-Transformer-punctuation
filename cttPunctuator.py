# -*- coding:utf-8 -*-
# @FileName  :ctt-punctuator.py
# @Time      :2023/4/13 15:03
# @Author    :lovemefan
# @Email     :lovemefan@outlook.com


__author__ = "lovemefan"
__copyright__ = "Copyright (C) 2023 lovemefan"
__license__ = "MIT"
__version__ = "v0.0.1"

import logging
import threading

from cttpunctuator.src.punctuator import CT_Transformer, CT_Transformer_VadRealtime

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s %(levelname)s] [%(filename)s:%(lineno)d %(module)s.%(funcName)s] %(message)s",
)

lock = threading.RLock()


class CttPunctuator:
    _offline_model = None
    _online_model = None

    def __init__(self, online: bool = False):
        """
        punctuator with singleton pattern
        :param online:
        """
        self.online = online

        if online:
            if CttPunctuator._online_model is None:
                with lock:
                    if CttPunctuator._online_model is None:
                        logging.info("Initializing punctuator model with online mode.")
                        CttPunctuator._online_model = CT_Transformer_VadRealtime()
                        self.param_dict = {"cache": []}
                        logging.info("Online model initialized.")
            self.model = CttPunctuator._online_model

        else:
            if CttPunctuator._offline_model is None:
                with lock:
                    if CttPunctuator._offline_model is None:
                        logging.info("Initializing punctuator model with offline mode.")
                        CttPunctuator._offline_model = CT_Transformer()
                        logging.info("Offline model initialized.")
            self.model = CttPunctuator._offline_model

        logging.info("Model initialized.")

    def punctuate(self, text: str, param_dict=None):
        if self.online:
            param_dict = param_dict or self.param_dict
            return self.model(text, self.param_dict)
        else:
            return self.model(text)
