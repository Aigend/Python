# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : employee_id_converter.py
# @Author : qiangwei.zhang
# @CreateTime : 2021/6/7 11:23 上午
# @Description :

import re
from utils.logger import logger


def employee_id_converter(employee_id):
    employee_id = str(employee_id)
    config = {"C": 101, "CC": 102, "CW": 103, "EU": 104, "NC": 105, "NI": 106, "U": 107, "W": 108}
    result = ''.join(re.findall(r'[A-Za-z]', employee_id))
    if result:
        suffix = int(employee_id.split(result)[1])
        value = int(config[result])
        user_id = value * 1000000 + suffix
    else:
        user_id = 9 * 100000000 + int(employee_id)
    logger.debug(user_id)
    return user_id


if __name__ == '__main__':
    employee_id = "EU90313"
    employee_id = "1079982"
    # employee_id = "1090313"
    account_id = employee_id_converter(employee_id)
