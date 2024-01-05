#!/usr/bin/env python
# coding=utf-8

"""
:author: li.liu
"""
import pytest


class TestDidUpdateMsg(object):
    @pytest.mark.skip('stg')
    def test_did_update_msg(self, publish_msg, checker):
        # 构造并上报消息
        nextev_message, did_update_obj = publish_msg('did_update_event', did_data_num=1)

        # 校验FOTA Mysql的vehicle_dids表
        tables = ['vehicle_dids']
        checker.check_mysql_tables(did_update_obj, tables)


