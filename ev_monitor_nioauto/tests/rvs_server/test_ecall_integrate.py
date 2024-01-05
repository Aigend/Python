#!/usr/bin/env python
# coding=utf-8

"""
Description: ecall事件和车机端联调
Case:
        验证通过API配置ecall setting能正常下发到车机端
        验证hard_trigger事件能触发，上报及呼叫所配置的手机
        验证soft_trigger事件能触发，上报及呼叫所配置的手机
        验证airbag_pump_tigger事件能触发，上报及呼叫所配置的手机
        验证nio_call_trigger事件能触发，上报及呼叫所配置的手机
        验证通过API关闭ecall后，ecall事件可以被触发落库，但是不呼叫手机

"""
import pytest


@pytest.mark.skip
class TestEcallCrossDebug(object):
    def test_ecall_setting(self):
        """
        验证通过API配置ecall setting能正常下发到车机端

        通过API配置ecall setting，检查配置能下发到车机端，检查API 查询到的配置与车机端的一致
        API: http://showdoc.nevint.com/index.php?s=/11&page_id=5309

        1.	使用generic API 下发ecall setting配置
            API 返回success

        2.	检查车机端配置
            车机端与下发的配置一致

        3.	再次用generic API 下发ecall setting配置
            API 返回success

        4.	检查车机端配置
            车机端配置更新为最新下发的配置

        """

    def test_hard_trigger(self):
        """
        验证hard_trigger事件能触发，上报及呼叫所配置的手机

        触发hard_trigger, 检查ecall事件落库，调用API能查询到上报的ecall事件。检查ecall触发了手机的呼叫。
        ecall是actived，即处于如下三种状态: Parked(Comfort Enable), Driver Present, Driving.

        1.	模拟按SOS按钮，触发reason_code=hard_trigger的ecall事件
            触发成功

        2.	检查mysql数据库的ecall event表
            ecall事件成功落库

        3.	调用ecall event list API查询ecall事件
            API doc : http://showdoc.nevint.com/index.php?s=/11&page_id=5305
            ecall事件包括在ecall list中，且位于第一条

        4.	调用 ecall query API 传入ecall_id查询ecall事件详情
            API doc：http://showdoc.nevint.com/index.php?s=/11&page_id=5306
            能获取到ecall事件详情

        5.  检查ecall事件触发后会呼叫到ecall setting所配置的手机号
            手机接收到车机的来电

        """

    def test_soft_trigger(self):
        """
        验证soft_trigger事件能触发，上报及呼叫所配置的手机

        触发soft_trigger, 检查ecall事件落库，调用API能查询到上报的ecall事件。检查ecall触发了手机的呼叫。
        ecall是actived，即处于如下三种状态: Parked(Comfort Enable), Driver Present, Driving.

        1.	模拟按CDC中控界面的ecall按钮，触发reason_code=soft_trigger的ecall事件
            触发成功

        2.	检查mysql数据库的ecall event表
            ecall事件成功落库

        3.	调用ecall event list API查询ecall事件
            API doc : http://showdoc.nevint.com/index.php?s=/11&page_id=5305
            ecall事件包括在ecall list中，且位于第一条

        4.	调用 ecall query API 传入ecall_id查询ecall事件详情
            API doc：http://showdoc.nevint.com/index.php?s=/11&page_id=5306
            能获取到ecall事件详情

        5.  检查ecall事件触发后会呼叫到ecall setting所配置的手机号
            手机接收到车机的来电
        """

    def test_airbag_pum_trigger(self):
        """
        验证airbag_pump_tigger事件能触发，上报及呼叫所配置的手机

        触发airbag_pump_tigger, 检查ecall事件落库，调用API能查询到上报的ecall事件。检查ecall触发了手机的呼叫。
        ecall是actived，即处于如下三种状态: Parked(Comfort Enable), Driver Present, Driving.

        1.	模拟安全气囊弹出信号，触发reason_code=airbag_pump_tigger的ecall事件
            触发成功

        2.	检查mysql数据库的ecall event表
            ecall事件成功落库

        3.	调用ecall event list API查询ecall事件
            API doc : http://showdoc.nevint.com/index.php?s=/11&page_id=5305
            ecall事件包括在ecall list中，且位于第一条

        4.	调用 ecall query API 传入ecall_id查询ecall事件详情
            API doc：http://showdoc.nevint.com/index.php?s=/11&page_id=5306
            能获取到ecall事件详情

        5.  检查ecall事件触发后会呼叫到ecall setting所配置的手机号
            手机接收到车机的来电
        """

    def test_nio_call_trigger(self):
        """
        验证nio_call_trigger事件能触发，上报及呼叫所配置的手机

        触发nio_call_trigger, 检查ecall事件落库，调用API能查询到上报的ecall事件。检查ecall触发了手机的呼叫。
        ecall是actived，即处于如下三种状态: Parked(Comfort Enable), Driver Present, Driving.

        1.	CGW模拟向CDC发送nio call，实现nio_call_trigger的触发，触发reason_code=nio_call_trigger的ecall事件
            触发成功

        2.	检查mysql数据库的ecall event表
            ecall事件成功落库

        3.	调用ecall event list API查询ecall事件
            API doc : http://showdoc.nevint.com/index.php?s=/11&page_id=5305
            ecall事件包括在ecall list中，且位于第一条

        4.	调用 ecall query API 传入ecall_id查询ecall事件详情
            API doc：http://showdoc.nevint.com/index.php?s=/11&page_id=5306
            能获取到ecall事件详情

        5.  检查ecall事件触发后会呼叫到ecall setting所配置的手机号
            手机接收到车机的来电
        """

    def test_set_ecall_off(self):
        """
        验证通过API关闭ecall后，ecall事件可以被触发落库，但是不呼叫手机
        ecall是actived，即处于如下三种状态: Parked(Comfort Enable), Driver Present, Driving.

        1.  通过API 下发ecall 的disable
            API doc： http://showdoc.nevint.com/index.php?s=/11&page_id=5309
            下发成功

        2.  检查车机配置
            车机端ecall配置为disable

        3.  触发harder tigger ecall事件
            触发成功

        4.  检查mysql ecall_event 表
            ecall事件成功落库

        5.  检查车机是否呼叫ecall setting配置的手机
            不呼叫手机
        """
