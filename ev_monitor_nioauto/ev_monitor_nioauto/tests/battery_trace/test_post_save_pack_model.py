# !/usr/bin/env python  
# -*- coding:utf-8 -*-  

""" 
@author:colin.li
@time: 2021/08/25
@api: POST_/api/1/in/battery/save_pack_model
@showdoc: http://showdoc.nevint.com/index.php?s=/252&page_id=31728
@description: 新增电池包规格信息
"""

import pytest
import allure
import random
import string
from utils.http_client import TSPRequest as restClient
from utils.assertions import assert_equal


# 为了避免脏数据过多，作为主键的model_id保持一致不使用随机值
@pytest.mark.parametrize('upload_now, model_id, pack_type, capacity, capacity_c3, voltage, voltage_max, mass, '
                         'spec_code, cooling_method, termperature_amount, energy_density, power_density, charge_ratio, '
                         'cycl_number, size, manufactory_name, manufactory_id, series_parallerl, item_list, '
                         'expectation, check_db',
                         [
                             (False, 'BAC0702006', 1, 12.5, 55.0, 10.01, 5.00, 525.0, 'AEM', '液冷', 1, 780.0, 350.0, 1.5,
                              2000, '2062*1539*136', '苏州正力蔚来新能源科技有限公司', '91310000329555773R', '1P12S',
                              [{'model_id': 'NCM_280Ah_29.84V_1P8S', 'amount': 12}], 'success', True),
                             # 因为暂时没有上传国家平台接口的访问权限，所以这里暂时报internal_error错误
                             (True, 'BAC0702006', 1, 12.5, 55.0, 10.01, 5.00, 525.0, 'AEM', '液冷', 1, 780.0, 350.0, 1.5,
                              2000, '2062*1539*136', '苏州正力蔚来新能源科技有限公司', '91310000329555773R', '1P12S',
                              [{'model_id': 'NCM_280Ah_29.84V_1P8S', 'amount': 12}], 'internal_error', False),
                             (False,) + (None,)*19 + ('invalid_param', False),
                         ],
                         ids=[
                             '供应商信息不上报国家平台',
                             '供应商信息上报国家平台',
                             '未提供module_id',
                         ])
def test_post_save_pack_model(env, mysql, upload_now, model_id, pack_type, capacity, capacity_c3, voltage, mass,
                                voltage_max, spec_code, cooling_method, termperature_amount, energy_density,
                                power_density, charge_ratio, cycl_number, size, manufactory_name, manufactory_id,
                                series_parallerl, item_list, expectation, check_db):
    app_id = 100078
    with allure.step('添加电池单体规格信息'):
        json = {
            'upload_now': upload_now, 'model_id': model_id, 'pack_type': pack_type, 'spec_code': spec_code,
            'capacity': capacity, 'capacity_c3': capacity_c3, 'voltage': voltage, 'voltage_max': voltage_max,
            'mass': mass, 'energy_density': energy_density, 'power_density': power_density, 'charge_ratio': charge_ratio,
            'cycl_number': cycl_number, 'cooling_method': cooling_method, 'termperature_amount': termperature_amount,
            'manufactory_name': manufactory_name, 'manufactory_id': manufactory_id, 'size': size,
            'series_parallerl': series_parallerl, 'item_list': item_list}
        json = {k: v for k, v in json.items() if v is not None}
        http = {
            "host": env['host']['tsp_in'],
            "path": '/api/1/in/battery/save_pack_model',
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "params": {
                "app_id": app_id,
                "sign": "",
            },
            "json": json
        }
        response = restClient.request(env, http)
    with allure.step('校验response'):
        assert_equal(response['result_code'], expectation)
    if check_db:
        with allure.step('校验db中的值是否正确'):
            record = mysql['battery_trace'].fetch_one('pack_model', {'model_id': model_id})
            assert_equal(record['pack_type'], pack_type)
            assert_equal(record['spec_code'], spec_code)
            assert_equal(record['capacity'], capacity)
            assert_equal(record['capacity_c3'], capacity_c3)
            assert_equal(record['voltage'], voltage)
            assert_equal(record['voltage_max'], voltage_max)
            assert_equal(record['mass'], mass)
            assert_equal(record['energy_density'], energy_density)
            assert_equal(record['power_density'], power_density)
            assert_equal(record['charge_ratio'], charge_ratio)
            assert_equal(record['cycl_number'], cycl_number)
            assert_equal(record['cooling_method'], cooling_method)
            assert_equal(record['termperature_amount'], termperature_amount)
            assert_equal(record['manufactory_name'], manufactory_name)
            assert_equal(record['manufactory_id'], manufactory_id)
            assert_equal(record['size'], size)
            assert_equal(record['series_parallerl'], series_parallerl)
            assert_equal(record['status'], -2)
