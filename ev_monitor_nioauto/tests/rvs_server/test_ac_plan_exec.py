#!/usr/bin/env python
# coding=utf-8
"""

https://confluence.nevint.com/display/CVS/Specific+Events+Report


空调预约FDS：https://confluence.nioint.com/display/SHEE/Remote+Cabin+Preconditioning%3AES8
空调预约SCR：https://confluence.nioint.com/display/CVS/Remote+Vehicle+Control

APP上下发空调预约步骤：
 1.APP调用vehicle_control的接口下发命令
    /api/1/vehicle/{vehicle_id}/command/set_ac_plan  http://showdoc.nevint.com/index.php?s=/11&page_id=803

 2.APP调用vehicle_control的结果查询接口查看车机端的命令返回情况
    /api/1/vehicle/command/{command_id}  http://showdoc.nevint.com/index.php?s=/11&page_id=412

 3. 车机返回预约命令成功，则RVS Server服务往remote_vehicle_test.history_ac_plan插入记录。
    * 目前空调预约在15分钟内和15分钟外的预约设置都是能预约成功。
    * 车机在BL240之后的版本会自己判断，如果预约时间在15分钟内，则立即开启空调，如果在15分钟之后，则在预约时间-15分钟开始开启空调。
    * BL240之前可由云端来判断，remote_vehicle_test.hot_config表里rvs.ac.plan.in.15min.push.switch字段配置云端是否判断。目前（BL240之后）该字段配成OFF了。
        OFF  15分钟内和15分钟外的空调预约设置都能预约成功
        ON  15分钟内，会立即开启空调，不算预约，15分钟外，算空调预约，在预约时间-15min开始开启空调。往remote_vehicle_test.history_ac_plan插入记录

 4. 预约到期车机执行开启空调命令
    上报specific_event事件subtype为ac_plan_exec

 5.开启空调失败的话，RVS Server会调用接口往APP push一条空调开启失败的信息。push只会触发一次
    * specific_event上报ac_plan_exec的status='failure'
    * RVS Server调用APP Msg（APP中台）接口api/1/in/app_msg/common 往APP push 信息
    * RVS Server会存调用接口的返回信息到Redis remote_vehicle_test:app_push:ac_plan:4e18c0f0ab734805a802b845a02ad824:10002-1596163317524

 6. 车上开的空调用app没法关
    并没有对oncar操作还是remote操作做区分，而是车机执行远程控制命令会检查precondition，只看当前状态，若车上手动开的空调只要前置条件满足也可以远程关闭


"""
import ast
import json
import random

import allure
import pytest

from utils.assertions import assert_equal
from utils.logger import logger
from utils.time_parse import timestamp_to_utc_strtime


class TestSpecificEventMsg(object):

    @pytest.mark.skip('manual')
    def test_ac_plan_exec_push(self, vid, publish_msg_by_kafka, checker):
        """空调预约详细流程见文件头"""
        with allure.step("校验空调预约到期启动失败会往手机Push一条通知"):
            data = {
                'plan_id': "10002-1596116437840", # plan_id对应vid在history_ac_plan的某条记录
                'status': "failure",
                'operation': random.choice(['0', '1']),
                'fail_reason': random.choice([
                    'vehl_not_parked', # 车辆未在停泊状态，无法按预约开启空调，请尝试手动开启
                    'seat_occp_frnt_le_exist', # 车辆前排有乘客，无法按预约开启空调，请尝试手动开启
                    'seat_occp_frnt_ri_exist', # 车辆前排有乘客，无法按预约开启空调，请尝试手动开启
                    'anti_theft_warn_on', # 防盗模式开启中，无法按预约开启空调，请尝试手动开启
                    'comfort_enable_on', # 车辆未上锁，无法按预约开启空调，请尝试手动开启
                    'soc_low', # 当前电量过低，无法按预约开启空调，请尝试手动开启
                    'door_frnt_le_open', # 检测到左前门未关，无法按预约开启空调，请尝试手动开启
                    'door_frnt_ri_open', # 检测到右前门未关，无法按预约开启空调，请尝试手动开启
                    'door_re_le_open', # 检测到左后门未关，无法按预约开启空调，请尝试手动开启
                    'door_re_ri_open', # 检测到右后门未关，无法按预约开启空调，请尝试手动开启
                    'tailgate_open', # 检测到尾门未关，无法按预约开启空调，请尝试手动开启
                    'invalid', # 无法按预约开启空调，请尝试手动开启
                    'turn_off_malf', # 检测到空调长时间运行，如无需使用请尝试手动关闭
                    'Remote Cabin Control Stop' # 车内空调开启，远程空调预约已退出
                ])
            }

            # 上报
            nextev_message, ac_plan_exec_in_message = publish_msg_by_kafka('specific_event', event_type='ac_plan_exec', data=data)

            # 校验
            """
            1. 空调启动失败会上报Specific_event的ac_plan_exec事件，并往手机Push一条通知
            2. RVS server调用api/1/in/app_msg/common接口推送通知
            3. Redis里会存储接口返回情况。remote_vehicle_test:app_push:ac_plan:4e18c0f0ab734805a802b845a02ad824:10002-1596116437840
            """
