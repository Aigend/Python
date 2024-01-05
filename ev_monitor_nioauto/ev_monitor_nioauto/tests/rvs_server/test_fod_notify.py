#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author:hongzhen.bi 
@time: 2020/08/12 19:16
@contact: hongzhen.bi@nio.com
@description: 接受到fod的command_result时,可以推送swc-cvs-tsp-${env}-80001-fod通知
"""

class TestFodNotify(object):
    def test_fod_notify(self):
        """
        调用 /api/1/in/vehicle/command/pub_fod 接口下发FoD配置到车后 (http://showdoc.nevint.com/index.php?s=/11&page_id=8609)
        车机返回执行结果后，rvs_server接受到fod的command_result后，到fod_recode表中，通过command_id获取fod记录，
        将其推送到Kafka：swc-cvs-tsp-${env}-80001-fod

        fod命令超时后,也可以触发fod的kafka消息推送
        """
        pass