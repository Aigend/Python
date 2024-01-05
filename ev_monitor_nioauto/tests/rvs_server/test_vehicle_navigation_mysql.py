#!/usr/bin/env python
# coding=utf-8

"""
:author: li.liu2
:Description: 导航上报
"""
import json
import pytest
import allure
import time
from utils.httptool import request

from utils.assertions import assert_equal


class TestVehicleNavigation(object):
    def test_navigation(self, env, account_id, checker):
        with allure.step("验证 车辆上报nav_period,重复上报（与上一次不同）的经纬度数据成功，能落库"):
            # 查询数据库中原来的数据
            vid = env['vehicles']['navigation']['vehicle_id']
            account_id = env['vehicles']['navigation']['account_id']
            vehicle_navigation_district_first = checker.mysql.fetch('vehicle_navigation_district', {"vehicle_id": vid, "area_code": '420107'})[0]
            vehicle_navigation_city_first = checker.mysql.fetch('vehicle_navigation_city', {"vehicle_id": vid, 'city_code': '420100'})[0]
            vehicle_navigation_first = checker.mysql.fetch('vehicle_navigation', {"id": vid, 'area_code': '420107'})[0]

            # 上报新的导航数据
            navigation_report(env['host']['tsp'], vid, account_id, chg=True)
            time.sleep(2)
            navigation_report(env['host']['tsp'], vid, account_id)
            time.sleep(2)

            # 查询数据库更新后的数据
            with allure.step("验证更新vehicle_navigation_district表"):
                vehicle_navigation_district_last = checker.mysql.fetch('vehicle_navigation_district', {"vehicle_id": vid, "area_code": '420107'})[0]
                assert_equal(vehicle_navigation_district_first['update_time'], vehicle_navigation_district_last['last_update_time'])
                # 表中的account_id 表示驾驶人，当前可以默认为车主，
                assert_equal(vehicle_navigation_district_last['account_id'], account_id)

            with allure.step("验证vehicle_navigation_city存入数据count+1，rank不变"):
                # count 表示来过此地方多少次， rank表示你是第多少辆来到此城市的车
                vehicle_navigation_city_last = checker.mysql.fetch('vehicle_navigation_city', {"vehicle_id": vid, 'city_code': '420100'})[0]
                assert_equal(vehicle_navigation_city_first['update_time'], vehicle_navigation_city_last['last_update_time'])
                assert_equal(vehicle_navigation_city_first['count'], vehicle_navigation_city_last['count'] - 1)
                assert_equal(vehicle_navigation_city_first['rank'], vehicle_navigation_city_last['rank'])

            with allure.step("验证更新vehicle_navigation表"):
                vehicle_navigation_last = checker.mysql.fetch('vehicle_navigation', {"id": vid, 'area_code': '420107'})[0]
                assert vehicle_navigation_first['update_time'] < vehicle_navigation_last['update_time']

    def test_navigation_duplicate_position(self, env, vid, account_id, checker):
        # 查询数据库中原来的数据
        vid = env['vehicles']['navigation']['vehicle_id']
        account_id = env['vehicles']['navigation']['account_id']
        with allure.step("验证 车辆上报nav_period,重复上报同一上报过的经纬度数据成功，期望不更新vehicle_navigation_district，vehicle_navigation_city"):
            # 查询数据库中原来的数据
            vehicle_navigation_district_first = checker.mysql.fetch('vehicle_navigation_district', {"vehicle_id": vid, "area_code": '420107'})[0]
            vehicle_navigation_city_first = checker.mysql.fetch('vehicle_navigation_city', {"vehicle_id": vid, 'city_code': '420100'})[0]
            vehicle_navigation_first = checker.mysql.fetch('vehicle_navigation', {"id": vid, 'area_code': '420107'})[0]

            # 上报新的导航数据
            navigation_report(env['host']['tsp'], vid, account_id)
            time.sleep(2)
            navigation_report(env['host']['tsp'], vid, account_id)
            time.sleep(2)

            # 查询数据库更新后的数据
            with allure.step("验证不更新vehicle_navigation_district表"):
                vehicle_navigation_district_last = checker.mysql.fetch('vehicle_navigation_district', {"vehicle_id": vid, "area_code": '420107'})[0]
                assert_equal(vehicle_navigation_district_first['last_update_time'], vehicle_navigation_district_last['last_update_time'])
                assert_equal(vehicle_navigation_district_last['account_id'], account_id)

            with allure.step("验证不更新vehicle_navigation_district表"):
                vehicle_navigation_city_last = checker.mysql.fetch('vehicle_navigation_city', {"vehicle_id": vid, 'city_code': '420100'})[0]
                assert_equal(vehicle_navigation_city_first['last_update_time'], vehicle_navigation_city_last['last_update_time'])
                assert_equal(vehicle_navigation_city_first['count'], vehicle_navigation_city_last['count'])
                assert_equal(vehicle_navigation_city_first['rank'], vehicle_navigation_city_last['rank'])

            with allure.step("验证「会」更新vehicle_navigation的update time"):
                vehicle_navigation_last = checker.mysql.fetch('vehicle_navigation', {"id": vid, 'area_code': '420107'})[0]
                assert vehicle_navigation_first['update_time'] < vehicle_navigation_last['update_time']

    @pytest.mark.skip('manual')
    def test_first_navigation(self):
        """
        验证从未上报过导航信息的车会插入数据，vehicle_navigation_district，vehicle_navigation_city，vehicle_navigation三表更新
        vehicle_navigation_city的count=1，rank代表是第多少辆来到此城市的车， last_update_time为NUll
        """
        pass

    @pytest.mark.skip('manual')
    def test_cdc(self):
        """
        CDC导航上报的数据，且需要持久化到S3

        rvs_server 中 HuMsgProcessor, 目前是保存了导航上报的实时数据到 vehicle_navigation。

        1. 数据上报来源，车机导航，
            文档： http://showdoc.nevint.com/index.php?s=/162&page_id=8109    pwd: share   1.3 节 nav_period 导航周期上报事件。

        2. 新起一个异步线程，将本次导航上报的数据持久化到 S3,  每个小时一个文件,
        aws s3 ls s3://mobile-lifestyle-test/swc/tsp/rvs/vehicle_navigation/20181114/{00-23}，数据格式同数据库，逗号分隔
        TODO 找运维申请s3权限

        """


def navigation_report(host, vid, uid, chg=False):
    api = '/api/1/data/report'
    if chg:
        event = json.dumps(
            [{"longitude": "119.67031",
              "app_ver": "1.0.82.01",
              "city": "扬州市",
              # 此处的area_code会被忽略，落mysql库的area_code是根据province，city，district计算得到
              "area_code": "321012",
              "app_id": "30009",
              "nation": "中国",
              "district": "江都区",
              "event_type": "nav_period",
              "latitude": "32.51539",
              "timestamp": int(time.time() * 1000),
              "province": "江苏省",
              "roadName": "启扬高速公路"
              }])
    else:
        event = json.dumps(
            [{"longitude": "114.37928",
              "app_ver": "1.0.82.01",
              "city": "武汉市",
              # 此处的area_code会被忽略，落mysql库的area_code是根据province，city，district计算得到
              "area_code": "420107",
              "app_id": "30009",
              "nation": "中国",
              "district": "青山区",
              "event_type": "nav_period",
              "latitude": "30.63132",
              "timestamp": int(time.time() * 1000),
              "province": "湖北省",
              "roadName": "旅大街"}])

    data = {
        'model': 'ES8',
        'os': 'android',
        'os_ver': '1.0.0',
        'os_lang': 'unknown',
        'os_timezone': 'unknown',
        'client_timestamp': str(int(time.time() - 8 * 3600)),
        'network': 'unknwon',
        'user_id': uid,
        'vid': vid,
        'events': event

    }

    res = request('POST', url=host + api, params={'app_id': 10016}, data=data)
    return res
