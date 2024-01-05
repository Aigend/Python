#!/usr/bin/env python
# coding=utf-8

"""
"""
import pytest


class TestExpiredVehicle(object):

    @pytest.mark.skip('manual')
    def test_expired_vehicle(self, mysql):
        """
        部分车辆的client到期了，为了不影响车辆的正常连接，在client被更新前，过期的车辆也可以正常连接消息平台上报数据


        过期的车辆如下：
        vehicle_id: 0016927189f4441d9f7e168b10416b35
        client_id: "ChAhrnpEOEJfW_Csf9CSFAouEAEYryUg-04oAg=="
        vin: LNBSCC3H1GF316827

        这辆车在client文件里会说明它将被发送给10107 kafka，连接的消息平台也是tsp消息平台

        校验该车可以正常连接消息平台



        """
        pass

