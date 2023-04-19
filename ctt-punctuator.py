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

from cttpunctuator.src.punctuator import CT_Transformer_VadRealtime, CT_Transformer
from cttpunctuator.src.utils.singleton import singleton

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s %(levelname)s] [%(filename)s:%(lineno)d %(module)s.%(funcName)s] %(message)s")

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
                        logging.info(f"Initializing model with online mode.")
                        CttPunctuator._online_model = CT_Transformer_VadRealtime()
                        self.param_dict = {"cache": []}
                        logging.info(f"Online model initialized.")
            self.model = CttPunctuator._online_model

        else:
            if CttPunctuator._offline_model is None:
                with lock:
                    if CttPunctuator._offline_model is None:
                        logging.info(f"Initializing model with online mode.")
                        CttPunctuator._offline_model = CT_Transformer()
                        logging.info(f"Offline model initialized.")
            self.model = CttPunctuator._offline_model

        logging.info("Model initialized.")

    def punctuate(self, text: str):
        if self.online:
            return self.model(text, self.param_dict)
        else:
            return self.model(text)


if __name__ == '__main__':
    punc = CttPunctuator()
    print(punc.punctuate("哈哈不错呀"))

    punc = CttPunctuator()
    print(punc.punctuate("跨境河流是养育沿岸人民的生命之源长期以来为帮助下游地区防灾减灾中方技术人员在上游地区极为恶劣的自然条件下克服巨大困难甚至冒着生命危险向印方提供汛期水文资料处理紧急事件中方重视印方在跨境河流问题上的关切愿意进一步完善双方联合工作机制凡是中方能做的我们都会去做而且会做得更好我请印度朋友们放心中国在上游的任何开发利用都会经过科学规划和论证兼顾上下游的利益"))