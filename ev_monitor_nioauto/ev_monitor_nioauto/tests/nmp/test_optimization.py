#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author:hongzhen.bi 
@time: 2020/10/16 17:57
@contact: hongzhen.bi@nio.com
@description: 记录tsp消息平台相关优化措施
"""

import pytest


class TestOptimization(object):

    @pytest.mark.skip('manual')
    def test_write_disk(self):
        """
        只要那个发送队列满了，就会触发拒绝策略，拒绝后，需要写磁盘的数据就会写磁盘，不需要写磁盘的就扔掉了
        写磁盘路径：/data/app/greatwall_messaging_server/data/recovery/

        """
        pass

    @pytest.mark.skip('manual')
    def test_priority_connection_strategy(self):
        """
        FDS：https://confluence.nioint.com/display/CVS/Priority+connection+strategy
        积分策略见FDS

        1、APP客户端打开积分：
        指标获取：调用 /api/1/in/message/get_user_status 接口，判断APP当前状态
        积分策略：ONLINE 积分 1；OFFLINE 积分 0

        2、车控积分：
        (1)AllNum：control_online_commmand表中获取该车近1周内操作车控的次数
        (2)OtherNum：redis中取连接时刻前5分钟的非解锁车控数量 ZRANGE remote_vehicle_test_cmd_stat_{vid}_unlock 0 10
        (3)UnlockNum：redis中取连接时刻前5分钟的解锁车控数量 ZRANGE remote_vehicle_test_cmd_stat_{vid}_other 0 10
        积分策略：AllNum + OtherNum * 10 + UnlockNum * 100

        3、车辆状态积分：
        指标获取：调用 /api/1/in/vehicle/{vid}/status 接口，获取车辆当前的锁状态
        积分策略：lock积分 1；unlock积分 0.01

        4、总积分：
        将1、2、3步获得的积分相乘即为该车量的总积分

        在车辆进行连接请求时，tsp_message_server会进行以上积分计算，
        并将总积分计算结果写入redis，某个vid的积分查询及返回结果如下：
        > ZSCORE nmp_ranking_service 74361e94a61846e2a690d2e2a9bf591d
        "1205"

        注意：断线重连的时候才会重新计算，不重新连接的话是不会触发计算逻辑的

        5、积分阈值：
        对缓存的车辆积分进行降序排序，选取2倍的LRU数量处的车辆所获的的积分为积分阈值，如果小于该阈值，则拒绝连接。
        积分阈值初始值为0.01
        """

        pass