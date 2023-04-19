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

from cttpunctuator.src.punctuator import (CT_Transformer,
                                          CT_Transformer_VadRealtime)

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
                        logging.info(
                            "Initializing punctuator model with offline mode."
                        )
                        CttPunctuator._offline_model = CT_Transformer()
                        logging.info("Offline model initialized.")
            self.model = CttPunctuator._offline_model

        logging.info("Model initialized.")

    def punctuate(self, text: str):
        if self.online:
            return self.model(text, self.param_dict)
        else:
            return self.model(text)


if __name__ == "__main__":
    punc = CttPunctuator()
    text = "据报道纽约时报使用ChatGPT创建了一个情人节消息生成器用户只需输入几个提示就可以得到一封自动生成的情书"
    logging.info(punc.punctuate(text)[0])

    punc = CttPunctuator(online=True)
    text_in = "跨境河流是养育沿岸|人民的生命之源长期以来为帮助下游地区防灾减灾中方技术人员|" \
              "在上游地区极为恶劣的自然条件下克服巨大困难甚至冒着生命危险|向印方提供汛期水文资料处理" \
              "紧急事件中方重视印方在跨境河流>问题上的关切|愿意进一步完善双方联合工作机制|凡是|中方" \
              "能做的我们|都会去做而且会做得更好我请印度朋友们放心中国在上游的|任何开发利用都会经过科学|" \
              "规划和论证兼顾上下游的利益"

    vads = text_in.split("|")
    rec_result_all = ""
    for vad in vads:
        result = punc.punctuate(vad)
        rec_result_all += result[0]
        logging.info(f"Partial: {rec_result_all}")

    logging.info(f"Final: {rec_result_all}")
