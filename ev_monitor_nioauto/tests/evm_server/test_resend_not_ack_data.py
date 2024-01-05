""" 
@author:dun.yuan
@time: 2021/3/31 5:18 下午
@contact: dun.yuan@nio.com
@description: 1.EVM Server会有一个线程轮询过滤出Cassandra中evm message的ack=-1的消息，向政府平台进行重发，每秒重发一条
              2.该线程只要平台注册vms后就会开始轮询
              3.轮询需要补发的数据的时间范围可配置，默认为1天
@showdoc：
"""
import pytest


class TestResendNotAckData(object):
    @pytest.mark.skip('manual')
    def test_resend_not_ack_data(self):
        """
        1. 在vms平台配置，将要车辆数据上报的对应平台处于离线状态
        2. 开始模拟车辆上报数据
        3. 确认Cassandra已保存到对应的数据，ack字段为 -1
        4. 在vms平台上将平台恢复在线状态
        5. 查询Cassandra之前的数据，ack字段为1，并且验证平台已经收到

        """
        pass
