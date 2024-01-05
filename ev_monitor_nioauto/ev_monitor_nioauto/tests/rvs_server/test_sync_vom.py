#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author:chunming.liu 
@time: 2020/07/30 11:57
@contact: chunming.liu@nio.com
@description: 从vom系统同步订单相关数据。主要是两种机制：1、定时拉取vom的接口；2、消费vom的kafka的topic。
"""
import uuid
import hashlib
import json
import time
import allure
from datetime import datetime

import requests
import pytest

from pprint import pprint
from utils.assertions import assert_equal


class TestVOM(object):
    @pytest.mark.skip("Manual")
    def test_sync_do_vom_appadmin_syncappointment(self):
        """
        消费do-vom-appadmin-syncappointment-{test|dev|stg}写入到vehicle_owner_history，
        再通过/api/1/in/vehicle/common_view提供给应用方，比如权益平台freyr
        """
        pass

    @pytest.mark.skip("Manual")
    def test_sync_do_vom_info_syncappointment(self):
        """
        消费do-vom-appadmin-syncappointment-{test|dev|stg}中channel=order_appAdmin_upsert_orderInfo的消息。
        写入到order_info，order_person，order_money，order_deliver_info,order_registration_city,order_registration_person,optionList,order_registration_company,order_finance
        再通过xxx提供给应用方
        """
        pass

    @pytest.mark.skip("Manual")
    def test_update_machineno_in_vehicle_profile(self):
        """
        消费do-vom-appadmin-syncappointment-{test|dev|stg}中channel=order_appAdmin_upsert_orderInfo的消息。
        写入到vehicle_profile的电机号machineno
        再通过xxx提供给应用方public static final String VOM_ORDER_TYPE_MAJOR_ENTERPRISE = "80";
        """
        pass

    @pytest.mark.skip("Manual")
    def test_vehicle_profile_info_major_customer(self):
        """
        消费do-vom-appadmin-syncappointment-{test|dev|stg}中channel=order_appAdmin_upsert_orderInfo的消息。
        当ordertype=80时（public static final String VOM_ORDER_TYPE_MAJOR_ENTERPRISE = "80"）
        写入到vehicle_profile_info_major_customer
        再通过xxx提供给应用方
        """
        pass

    @pytest.mark.skip("Manual")
    def test_vehicle_owner_history(self):
        """
        消费do-vom-appadmin-syncappointment-{test|dev|stg}中channel=order_appAdmin_upsert_orderInfo的消息。
        写入到vehicle_profile_info_major_customer
        参考 https://git.nevint.com/greatwall/rvs_server/blob/master/src/main/java/com/nio/cvs/rvs/server/engine/DoOrderInfoEngine.java#L118
        再通过xxx提供给应用方
        """
        pass

    @pytest.mark.skip("Manual")
    def test_sync_vom_uds_upsert_orderInfo(self):
        """
        消费do-vom-appadmin-syncappointment-{test|dev|stg}中channel=vom_uds_upsert_orderInfo的消息。更新到vehicle_profile的order_status字段
        参考 https://git.nevint.com/greatwall/rvs_server/blob/master/src/main/java/com/nio/cvs/rvs/server/engine/DoOrderStatusUpdateEngine.java
        再通过xxx提供给应用方
        """
        pass

    @pytest.mark.skip("Manual")
    def test_vehicle_group(self):
        """
        功能：
            vinbom录入车辆信息,当该车有对应订单时,可以自动创建对应上牌地虚拟分组,并加入该分组
        逻辑：
            1、造一辆订单车辆，vinbom会调取/vinbom/batch_save接口，补充vehicle_profile表
            2、校验vehicle_profile_info_extend记录该车辆对应register_area_code,register_province,register_city字段
            3、如果缺失订单信息，校验vehicle_profile_info_extend录入其他静态数据,register_are_code为空
            4、校验vehicle_group中如果没有对应的虚拟组,则创建
            5、UDS同步订单和车辆信息,触发对应车辆人称绑定时,rvs自动创建订单对应上牌城市虚拟组,并更新对应车辆的虚拟组信息

        """
        pass

    @pytest.mark.skip("Manual")
    def test_vehicle_binding(self):
        """
        功能：
            UDS录入订单和人信息,vinbom录入车辆和订单信息(UDS和vinbom不分先后),rvs_server能够正确消费并记录人车关系(插入和更新)
        逻辑：
            1、UDS推送订单和人关系消息,tsp消费后记录人订单关系到history_owner_change和relation_order_account表
            2、vinbom调用remote vehicle的batch_save接口，推送对应订单和车辆信息到kafka: swc-cvs-tsp-{env}-80001-vb_sync_insert/update
            3、rvs_server消费后记录到vehicle_profile表,并推送insert消息到kafka
            3、rvs_server可以正确消费对应消息,并记录history_vinbom_change表和relation_order_vehicle表
            4、rvs_server可以根据relation_order_vehicle表和relation_order_account确定人车关系并且写入relation_user_vehicle表中
            5、之后,rvs_server调用用车人变更消息通知poseidon系统
            6、poseidon系统更新vehicle_auth_info表设置主用车人信息并推送对应kafka消息
            7、人车关系绑定后,UDS发送重复用车人消息(订单和人关系和已记录信息一致),rvs_server只记录history_owner_change不做其他变更
            8、人车关系绑定后,vinbom发送重复订单和车辆信息(订单和车辆信息一致),rvs_server只记录history_vinbom_change不做其他变更

        """
        pass

    @pytest.mark.skip("Manual")
    def test_vehicle_optional_config(self):
        """
        功能：
            1、定时job：凌晨4点从vehicle_profile表查找vehicle_optional_config没有的vid，调取vinbom接口(http://showdoc.nevint.com/index.php?s=/77&page_id=16962)
            获取配置信息，如果vinbom没有该车信息则跳过
            2、触发：vinbom修改物料号推送kafka do-vehicle-config-change-qa，rvs_server消费，通过vid调取vinbom接口，插入或更新vehicle_optional_config
        需求：
            1、VMS/车辆监控/车辆信息/详情/车辆配置详情（直接查vehicle_optional_config库）
            2、后期APP（调用/api/1/vehicle/vinbom/optional_config接口）
        """
        pass

    @pytest.mark.skip("Manual")
    def test_sync_material_num(self):
        """
        功能：
            从vinbom同步物料号
        逻辑：
            1、定时job
                从vehicle_profile中搜索material_num为空的vid，
                调用vinbom接口 http://showdoc.nevint.com/index.php?s=/77&page_id=16962 (密码：nio_12345)获取物料号进行补充
            2、实时消费kafka
                do-vom-appadmin-syncappointment-{env} 更新vehicle_profile表的material_num
        """
        pass

    @pytest.mark.skip("Manual")
    def test_sync_order_info(self):
        """
        功能：
            从vinbom同步订单信息（插入或更新）
        逻辑：
            1、部署后1分钟运行job：
                从relation_order_vehicle中获取新增（order_info表中不存在）的订单号，
                调用vom接口 api/v1/vom/order/select/detail 查询订单明细(http://showdoc.nevint.com/index.php?s=/71&page_id=3499)
                插入order_company、order_deliver_info、order_enterprise_info、order_finance、order_info、order_money、
                order_person、order_registration_city、order_registration_company、order_registration_person、order_vehicle
                这11个表中。

                case：接口的查询方法见下方代码，如token过期，可使用下方的 _get_detail_api_token 方法生成新的token使用

            2、实时消费vinbom Kafka：
                do-vom-appadmin-syncappointment-sit (http://showdoc.nevint.com/index.php?s=/71&page_id=7861)
                根据Kafka消息中的order_id查找vehicle_profile中对应order_id的条目，若条目中vehicle_id与Kafka消息中的vinId一致，
                则更新或插入kafka中的订单明细到11个表中。

                case：Kafka推送方式可参考测试用例 test_owner_and_license.py 中的 test_license_update 中的步骤1-4
        """

        userAccount = ''
        orderNo = '810001523962621310',
        env = 'uat'
        token = self._get_detail_api_token(env),

        url = 'http://vom-api-{env}.nio.com/api/v1/vom/order/select/detail'.format(env=env)
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            "userAccount": userAccount,
            'orderNo': orderNo,
            'token': token
        }
        res = requests.request('POST', url=url, data=data, headers=headers)
        pprint(res.json())

    def _get_detail_api_token(self, env):
        url = 'http://vom-api-{env}.nio.com/api/v1/createtoken'.format(env=env)
        # url = 'http://vom-api.nio.com/api/v1/createtoken'
        # url = 'http://vom-api-qa.nio.com/api/v1/createtoken'# qa环境
        # url = 'http://vom-api-uat.nio.com/api/v1/createtoken'# uat环境
        # url = 'http://vom-api-stg.nio.com/api/v1/createtoken'# stg环境
        # app_id=50001，app_secret=ae7e58fa302e4660b9f24dc57d21cc12
        # headers = {
        #     'Content-Type':'application/x-www-form-urlencoded'
        # }
        if env in ['uat', 'qa']:
            data = {
                'application': '10026',
                # 'application':'10018',#stg
                # 'application':'10005',
                'timestamp': str(int(time.time())),
                'digest': ''
            }
            # appsec = '1INTEMYJKIJC120'
            appsec = '1INTEMG6200JC1P1'
        else:
            data = {
                # 'application':'10020',
                'application': '10018',  # stg
                # 'application':'10005',
                'timestamp': str(int(time.time())),
                'digest': ''
            }
            appsec = 'BNRT45DAFO0PM'
        # appsec = app_sec['test'][data['application']]
        # appsec = '1INTEMYJKIJC120'
        # appsec = 'BNRT45DAFO0PM'#stg
        # appsec = 'YUITGF6785TGF5F'

        sig_pre = 'application=' + data['application'] + '&' + 'timestamp=' + data['timestamp'] + appsec
        print(sig_pre)
        md = hashlib.md5(sig_pre.encode('utf-8')).hexdigest()
        sig = md.upper()
        data['digest'] = sig
        res = json.loads(requests.request('POST', url=url, data=data).text)
        token = res['resultData']
        return token

    @pytest.mark.marcopolo_skip
    @pytest.mark.test
    def test_sync_info_from_vinbom(self, vid, vin, kafka, checker, mysql):
        """
        功能：
            从vinbom同步物料号
        逻辑：
            1、定时job
                从vehicle_profile中搜索material_num为空的vid，
                调用vinbom接口 http://showdoc.nevint.com/index.php?s=/77&page_id=16962 (密码：nio_12345)获取物料号进行补充
            2、实时消费kafka do-vom-appadmin-syncappointment-{env} 更新vehicle_profile表的material_num
            1、定时job：凌晨4点从vehicle_profile表查找vehicle_optional_config没有的vid，调取vinbom接口(http://showdoc.nevint.com/index.php?s=/77&page_id=16962)
            获取配置信息，如果vinbom没有该车信息则跳过
            2、触发：vinbom修改物料号推送kafka do-vehicle-config-change-qa，rvs_server消费，通过vid调取vinbom接口，插入或更新vehicle_optional_config
        """
        data = {
            'vid': '001d3439e0b841a5a00cd8eec095e514',
            'vin': 'SQETEST0048154662',
            'new_material_num': 'GE2201SGAFCPK003B4020401010700HCBLA1',
            'timestamp': int(time.time() * 1000)
        }

        mysql['rvs'].update('vehicle_profile', {'id': data['vid']},
                            {'material_num': '', 'platform': '', 'key_option_code': 'EC01'})
        mysql['rvs'].delete('vehicle_optional_config', {'vehicle_id': data['vid']})
        kafka['do'].produce(kafka['topics']['vinbom'], json.dumps(data))
        time.sleep(5)
        v_info = mysql['rvs'].fetch_one('vehicle_profile', {'id': data['vid']})
        assert_equal(v_info['material_num'], data['new_material_num'])
        assert_equal(v_info['platform'], 'NT2.0')
        assert_equal(v_info['key_option_code'], '')
        assert len(mysql['rvs'].fetch('vehicle_optional_config', {'vehicle_id': data['vid']})) == 1


    @pytest.mark.marcopolo_skip
    @pytest.mark.test
    def test_sync_order_status(self, kafka, checker, mysql):
        # TODO 马克波罗服务暂不支持，先跳过
        """
        更新order_info表中的 order_status 和 current_status_timestamp 字段。
        使用的vom kafka的channel为 order_appAdmin_order_visual
        """
        order_no = '810001594696890886'
        order_status = 'intention_contract_signed'
        sample_ts = int(time.time() * 1000)

        mysql['rvs'].update('order_info', {'order_no': order_no}, {'order_status': 'cancel'})
        data = {
            "id": str(uuid.uuid4()),
            "version": 'v1',
            "sendSys": 'order_server',
            "channel": 'order_appAdmin_order_visual',
            "msg": json.dumps(
                {
                    "visualType": "OrderUserVisual",
                    "orderNo": order_no,
                    "status": order_status,
                    "statusUpdateTime": str(sample_ts)
                }
            )
        }

        kafka['do'].produce(kafka['topics']['vom_sync'], json.dumps(data))
        time.sleep(2)
        order_status_mysql = mysql['rvs'].fetch('order_info', {'order_no': order_no})[0]
        assert_equal(order_status_mysql['order_status'], order_status)
        assert_equal(order_status_mysql['current_status_timestamp'], datetime.utcfromtimestamp(sample_ts // 1000).strftime('%Y-%m-%d %H:%M:%S'))

    @pytest.mark.marcopolo_skip
    @pytest.mark.test
    def test_sync_owner_info_push_kafka(self, kafka, checker, mysql):
        # TODO 马克波罗服务暂不支持，先跳过
        """
        更新车主信息，触发rvs向swc-cvs-tsp-${env}-80001-owner-change。
        使用的vom kafka的channel为 order_appAdmin_upsert_orderInfo
        """
        # 重置offset
        kafka['comn'].set_offset_to_end(kafka['topics']['owner_change'])

        order_no = '810001523949822303'
        order_short_no = '179767173'
        vin = 'SQETESTG611R10F09'
        # order_status = 'intention_contract_signed'
        # sample_ts = int(time.time() * 1000)
        #
        # mysql['rvs'].update('order_info', {'order_no': order_no}, {'order_status': 'cancel'})
        data = {
            "id": str(uuid.uuid4()),
            "version": 'v1',
            "sendSys": 'order_server',
            "channel": 'order_appAdmin_upsert_orderInfo',
            "msg": json.dumps(
                {
                    "orderNo": order_no,
                    #"orderShortNo": order_short_no,
                    "vin": vin,
                    "registrationType": 1,
                    "registrationPerson": {
                        "name": "张三" + str(uuid.uuid4())[:5],
                        "identityCardTypeName": "护照",
                        "identityCard": "10003902023",
                        "email": "san.zhang.o@nio.com",
                        "telephone": "2424224",
                        "provinceId": "110000",
                        "provinceName": "北京市",
                        "cityId": "110100",
                        "cityName": "北京市",
                        "districtId": "",
                        "districtName": "",
                        "address": "望京",
                        "postCode": ""
                    }
                }
            )
        }

        kafka['do'].produce(kafka['topics']['vom_sync'], json.dumps(data))
        # time.sleep(2)
        # order_status_mysql = mysql['rvs'].fetch('order_info', {'order_no': order_no})[0]
        # assert_equal(order_status_mysql['order_status'], order_status)
        # assert_equal(order_status_mysql['current_status_timestamp'], datetime.utcfromtimestamp(sample_ts // 1000).strftime('%Y-%m-%d %H:%M:%S'))
        with allure.step('校验 {}'.format(kafka['topics']['owner_change'])):
            kafka_msg = None
            is_found = False
            for data in kafka['comn'].consume(kafka['topics']['owner_change'], timeout=30):
                kafka_msg = json.loads(str(data, encoding='utf-8'))
                is_found = True
                break
            print(kafka_msg)
            assert_equal(True, is_found)

    @pytest.mark.marcopolo_skip
    @pytest.mark.test
    def test_sync_nio_doc_push_kafka(self, kafka, checker, mysql):
        # TODO 马克波罗服务暂不支持，先跳过
        """
        更新车主信息，触发rvs向swc-cvs-tsp-${env}-80001-owner-change。
        使用的vom kafka的channel为 order_appAdmin_upsert_orderInfo
        """
        # 重置offset
        kafka['comn'].set_offset_to_end(kafka['topics']['owner_change'])

        order_no = '810001523949822303'
        order_short_no = '179767173'
        vin = 'SQETESTG611R10F09'
        order_status = 'intention_contract_signed'
        sample_ts = int(time.time() * 1000)

        mysql['rvs'].update('order_info', {'order_no': order_no}, {'order_status': 'cancel'})
        data = {
                "channelSources": "10086",
                "docNo": "VEH1622103841377664",
                "documentType": "VehicleLicense",
                "optionTime": int(time.time() * 1000),
                "optionType": "UPDATE",
                }

        kafka['do'].produce(kafka['topics']['nio_doc'], json.dumps(data))
        # time.sleep(2)
        # order_status_mysql = mysql['rvs'].fetch('order_info', {'order_no': order_no})[0]
        # assert_equal(order_status_mysql['order_status'], order_status)
        # assert_equal(order_status_mysql['current_status_timestamp'], datetime.utcfromtimestamp(sample_ts // 1000).strftime('%Y-%m-%d %H:%M:%S'))
        with allure.step('校验 {}'.format(kafka['topics']['owner_change'])):
            kafka_msg = None
            is_found = False
            for data in kafka['comn'].consume(kafka['topics']['owner_change'], timeout=10):
                kafka_msg = json.loads(str(data, encoding='utf-8'))
                is_found = True
                break
            print(kafka_msg)
            assert_equal(True, is_found)
