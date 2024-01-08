# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @project : py_study
# @File    : logging_02.py
# @Date    : 2022/05/13:19:13
# @Author  : jinwenlong@oppo.com
import logging

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)

handler = logging.FileHandler("log.txt")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

console = logging.StreamHandler()
console.setLevel(logging.WARNING)

logger.addHandler(handler)
logger.addHandler(console)

logger.info("Start print log")
logger.debug("Do something")
logger.warning("Something maybe fail.")
try:
    open("sklearn.txt", "rb")
except (SystemExit, KeyboardInterrupt):
    raise
except Exception:
    logger.error("Faild to open sklearn.txt from logger.error", exc_info=True)
finally:
    logger.info("Whatever it will happen.")

logger.info("Finish")