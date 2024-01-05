#!/usr/bin/env python
# coding=utf-8
import pytest


class TestLicenseUpdate(object):
    @pytest.mark.skip("Manual")
    def test_sync_uds_job(self):
        """
        功能：
            每天上海时间5点整检索vinbom的推送中没有绑定人的订单,
            通过UDS的接口 /uds/${api_type}/relation/v1/vehicles/relations 查询该订单对应的用车人,然后自动绑定该用户和车辆的关系
            接口文档：http://showdoc.nevint.com/index.php?s=/urm&page_id=6134  (密码：uds@2018)
        逻辑：
            1、relation_order_vehicle中已存在vinbom同步的订单和车辆关系
            2、触发定时任务后，rvs通过UDS的接口获取订单和主用车人信息，
              若"role"为"presupposed_vehicle_owner"或者"vehicle_owner"，则存储到relation_order_account表
              "presupposed_vehicle_owner"和"vehicle_owner"同时存在时，以vehicle_owner指定的用户写入
            3、同时根据订单确定车辆和主用车人关系，插入或更新relation_user_vehicle


        """
        pass

    @pytest.mark.skip("Manual")
    def test_update_nomi_after_sync_uds(self):
        """
        功能：
            验证UDS修改车辆主用车人后触发人车关系变化,rvs_server自动同步新主用车人nomi欢迎词
        逻辑：
            1、relation_order_vehicle、relation_order_account、relation_user_vehicle中已存在订单、主用车人和车辆之间的关系
            2、UDS将该订单绑定新用户
            3、同时根据订单确定车辆和主用车人关系，插入或更新relation_user_vehicle
            4、调api/1/in/profile/driver/data接口（查mongodb），查看新主用车人的drive_profile是否已自动同步nomi欢迎词

        """
        pass

    @pytest.mark.skip("Manual")
    def test_license_update(self):
        """
        VOM 采集订单将车主信息推送 do-vom-appadmin-syncappointment-sit kafka topic（http://showdoc.nevint.com/index.php?s=/71&page_id=7861）,
        RVS_Server消费，将车主信息insert到vehicle_owner_history表中, 如果表中identity_no为空，则更新vom订单时，会update这条数据, 否则不会更新。
        更新后的表中数据，identity_no、identity_type、register_type不为空


        VOD 定时任务调用https://esb-bs-test.nevint.com/api/v1/vom/httpService接口（http://showdoc.nevint.com/index.php?s=/77&page_id=13460  密码nio_12345）
        update vehicle_owner_history表中vehicle_license为null的条目


        App OCR上传行驶证，推送do-pay-niodoc-sit kafka topic（http://showdoc.nevint.com/index.php?s=/71&page_id=21870 密码vom）,
        RVS_Server拿到其中的docNo，调用接口https://vom-api-uat.nio.com/api/v1/nio-document/docV2/queryFileInfo（接口文档 http://showdoc.nevint.com/index.php?s=/71&page_id=21023  密码vom）
        获取nio doc的车主信息和license信息，insert（没有该车辆）或update（存在该车辆）。
        车主名字不一致时，才会覆盖原数据，否则只更新vehicle_license.


        造订单车辆流程：
        1、盘古造车（造好vin、vid）

        2、昆仑造订单车辆：https://kunlun.nevint.com/TestPlanManager/Index

        ----OTD_VOM
            ----OTD_VOM_UAT_每日巡检
                ----VOM_UAT_定时任务_大客户企业单下单-车辆交付_for_TSP
        运行环境：UAT
        userAccount：931263310
        vin：刚刚在盘古上造的车的vin
        保存后运行，在执行的记录上面找到orderNo订单号信息

        3、检查vehicle_owner_history表有该车车主信息

        4、登陆VOM订单管理平台 https://vomadmin-uat.nevint.com/BasePage/HomePage
        用户名：he.guo.o
        密码：ES8_NIODay2017
        在订单管理/用户订单中可以对该订单进行修改

        5、盘古申请手机号、验证码、account_id
        绑定车辆、登陆app、激活车辆

        6、上传行驶证

        7、检查vehicle_owner_history表有驾驶证信息

        8、上传有车牌号变动的新的行驶证信息
        检查vehicle_profile中的plate_number为最新的车牌号，
        检查history_plate_number中新增车牌号变动信息。
        """
        pass

    @pytest.mark.skip("Manual")
    def test_synchronize_owner_job(self):
        """
        功能：定时job从vom同步车主信息
        需求：PE/线上仍然存在车主信息缺失的情况
        逻辑：
            查询vehicle_profile表中的车辆id，如果在vehicle_owner_history表中该vehicle_id不存在
            通过vehicle_profile.order_id，调用VOM接口查询车主信息。 /api/v1/vom/order/select/detail (http://showdoc.nevint.com/index.php?s=/71&page_id=3499)
            将记录插入到vehicle_owner_history表中

        """
        pass