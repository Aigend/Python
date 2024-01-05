# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : parse_pytest_ini.py
# @Author : qiangwei.zhang
# @time: 2021/11/04
# @api: GET_/api/XXX 【必填】
# @showdoc:
# @Description :脚本描述

import configparser
import re
import os
from config.settings import BASE_DIR

def parse_pytest_ini():
    #  实例化configParser对象
    config = configparser.ConfigParser()
    # -read读取ini文件
    config.read(os.sep.join([BASE_DIR, "pytest.ini"]), encoding='GB18030')
    """
    首先得到配置文件的所有分组，然后根据分组逐一展示所有
    """
    pytest_ini_map = {}
    for sections in config.sections():
        sections_map = {}
        for items in config.items(sections):
            sections_map[items[0]] = items[1]
        pytest_ini_map[sections] = sections_map
    cmdopt = re.findall(r'--env\s+(\S+)', pytest_ini_map.get("pytest").get("addopts"))[0]
    pytest_ini_map["cmdopt"] = cmdopt
    return pytest_ini_map


if __name__ == '__main__':
    pytest_ini_map = parse_pytest_ini()
    print(f"{pytest_ini_map}")
    # print(f"{pytest_ini_map}")
