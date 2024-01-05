# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : conftest.py
# @Author : qiangwei.zhang
# @CreateTime : 2021/6/29 4:51 下午
# @Description :
from config.settings import BASE_DIR
from utils.logger import logger
from utils.random_tool import format_time
from utils.random_tool import format_date_n_day_ago

def collection_message_states(cmdopt, message_states_info):
    with open(f'{BASE_DIR}/tests/app_message_center/message_states_info_{cmdopt}_{format_date_n_day_ago(0)}.txt', 'a+')as f:
        logger.debug(message_states_info)
        f.write(f'{message_states_info}|{format_time()}\n')
