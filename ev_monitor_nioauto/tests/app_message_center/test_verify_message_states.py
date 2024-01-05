# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : test_.py
# @Author : qiangwei.zhang
# @CreateTime : 2021/6/29 5:23 下午
# @Description :
"""
用于校验的数据是其它测试案例执行后生成的文件，通过顺序控制执行order越大越靠后执行，该案例最后执行
receive(21),
generate_msg(22),
store_msg(23),
generate_pushTask(24),
send_pushTask(25),
send_to_thirdParty(26)
27

alarm语音短信37
38
"""
import pytest
import os
from config.settings import BASE_DIR
from utils.checker import assert_equal
from utils.logger import logger
from utils.random_tool import format_date_n_day_ago


@pytest.mark.skip("manual")
@pytest.mark.run(order=10)
def test_verify_message_states(cmdopt, mysql):
    file_path = f'{BASE_DIR}/tests/app_message_center/message_states_info_{cmdopt}_{format_date_n_day_ago(0)}.txt'
    error_result = []
    if os.path.exists(file_path):
        with open(file_path, 'r')as f:
            lines = f.readlines()
            os.remove(file_path)
        for line in lines:
            ms_st = line.split("|")
            message_id = ms_st[0]
            expected_states = eval(ms_st[1])
            expected_states.sort()
            path = ms_st[2]
            message_in_mysql = mysql['nmp_app'].fetch('message_state', {'message_id': message_id}, retry_num=60)
            states_in_mysql = [message.get("state") for message in message_in_mysql]
            # 存在一条消息发送给多个用户做一次去重
            states_in_mysql = list(set(states_in_mysql))
            states_in_mysql.sort()
            logger.debug(f"验证{path}接口消息{message_id}状态")
            try:
                assert_equal(states_in_mysql, expected_states)
            except Exception as e:
                error_result.append(e)
                error_file_path = f'{BASE_DIR}/tests/app_message_center/error_message_states_info_{cmdopt}.txt'
                with open(error_file_path, "a", encoding="utf-8") as e_f:
                    e_f.write(f"mysql_status:{states_in_mysql}|{line}")
    else:
        logger.debug(f"【{cmdopt}】环境，需先执行push相关测试案例收集消息状态数据")
    if error_result:
        raise error_result[0]
