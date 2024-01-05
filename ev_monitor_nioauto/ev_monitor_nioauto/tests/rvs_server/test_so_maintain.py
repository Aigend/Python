#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author:hongzhen.bi 
@time: 2020/07/23 17:00
@contact: hongzhen.bi@nio.com
@description:

当保养通过topic do-nass-maintianstatus-sit推送时，rvs会消费topic并落库到vehicle_maintain表。该表只新增不修改

从2019/10以后，不再推送保养状态到车机端
也没有推送APP的逻辑，也就是说，维保目前没有推送任务
"""
import json
import random
import time
import pytest

from utils.assertions import assert_equal

@pytest.mark.marcopolo_skip
@pytest.mark.test
class TestSoMaintain(object):
    # TODO 马克波罗服务暂不支持，先跳过
    def test_so_maintain(self, vin, vid, env, kafka, mysql):
        """
        消费so kafka topic do-nass-maintianstatus-sit写入vehicle_maintain表，只新增不修改
        http://showdoc.nevint.com/index.php?s=/218&page_id=18067
        """
        timestamp = str(int(time.time()))
        maintain_msg = {
            "vin": vin,
            "accountId": env['vehicles']['normal']['account_id'],
            "vehicleId": vid,
            # 保养提醒状态 默认0 (0:保养周期未到，不提醒；1:保养周期已到，用户未预约保养服务；2:保养周期已到，用户已预约保养服务；3:保养周期已到，用户选择不要提醒)
            "maintainStatus": random.choice([0, 1, 2, 3]),
            # 消息类型 默认1 （1:保养提醒）
            "messageType": 1,
            "timestamp": timestamp
        }

        kafka['do'].produce(kafka['topics']['maintian'], json.dumps(maintain_msg))
        time.sleep(2)
        maintain_mysql = mysql['rvs'].fetch('vehicle_maintain',
                                            {'vehicle_id': vid,
                                             'account_id': env['vehicles']['normal']['account_id']},
                                            order_by='update_time desc limit 1')[0]
        assert_equal(maintain_mysql['status'], maintain_msg['maintainStatus'])

