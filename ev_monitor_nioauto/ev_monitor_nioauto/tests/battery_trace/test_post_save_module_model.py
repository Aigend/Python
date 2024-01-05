# !/usr/bin/env python  
# -*- coding:utf-8 -*-  

""" 
@author:colin.li
@time: 2021/08/25
@api: POST_/api/1/in/battery/save_module_model
@showdoc: http://showdoc.nevint.com/index.php?s=/252&page_id=31739
@description: 新增电池模组规格信息
"""

import pytest
import allure
import random
import string
from utils.http_client import TSPRequest as restClient
from utils.assertions import assert_equal


# 为了避免脏数据过多，作为主键的model_id保持一致不使用随机值
@pytest.mark.parametrize('upload_now, model_id, spec_code, capacity, capacity_c3, voltage, mass, energy_density,'
                         'power_density, charge_ratio, cycl_number, cell_amount, cell_model_id, manufactory_name, '
                         'manufactory_id, size, series_parallerl, expectation, check_db',
                         [
                             (False, 'BAC0702008', 'BAC0702008', 12.15, 55.0, 10.01, 525.0, 780.0, 350.0, 1.5, 2000, 12,
                              'LAE895', '苏州正力蔚来新能源科技有限公司', '91310000329555773R', '2062*1539*136', '1P6S',
                              'success', True),
                             # 因为暂时没有上传国家平台接口的访问权限，所以这里暂时报internal_error错误
                             (True, 'BAC0702004', 'BAC0702004', 12.15, 55.0, 10.01, 525.0, 780.0, 350.0, 1.5, 2000, 12,
                              'LAE895', '苏州正力蔚来新能源科技有限公司', '91310000329555773R', '2062*1539*136', '1P6S',
                              'internal_error', False),
                             (False,) + (None,)*16 + ('invalid_param', False),
                         ],
                         ids=[
                             '供应商信息不上报国家平台',
                             '供应商信息上报国家平台',
                             '未提供module_id',
                         ])
def test_post_save_module_model(env, mysql, upload_now, model_id, spec_code, capacity, capacity_c3, voltage, mass,
                                energy_density, power_density, charge_ratio, cycl_number, cell_amount, cell_model_id,
                                manufactory_name, manufactory_id, size, series_parallerl, expectation, check_db):
    app_id = 100078
    with allure.step('添加电池单体规格信息'):
        json = {
            'upload_now': upload_now, 'model_id': model_id, 'spec_code': spec_code, 'capacity': capacity,
            'capacity_c3': capacity_c3, 'voltage': voltage, 'mass': mass, 'energy_density': energy_density,
            'power_density': power_density, 'charge_ratio': charge_ratio, 'cycl_number': cycl_number,
            'cell_amount': cell_amount, 'cell_model_id': cell_model_id, 'manufactory_name': manufactory_name,
            'manufactory_id': manufactory_id, 'size': size, 'series_parallerl': series_parallerl}
        json = {k: v for k, v in json.items() if v is not None}
        http = {
            "host": env['host']['tsp_in'],
            "path": '/api/1/in/battery/save_module_model',
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
            record = mysql['battery_trace'].fetch_one('module_model', {'model_id': model_id})
            assert_equal(record['spec_code'], spec_code)
            assert_equal(record['capacity'], capacity)
            assert_equal(record['capacity_c3'], capacity_c3)
            assert_equal(record['voltage'], voltage)
            assert_equal(record['mass'], mass)
            assert_equal(record['energy_density'], energy_density)
            assert_equal(record['power_density'], power_density)
            assert_equal(record['charge_ratio'], charge_ratio)
            assert_equal(record['cycl_number'], cycl_number)
            assert_equal(record['cell_amount'], cell_amount)
            assert_equal(record['cell_model_id'], cell_model_id)
            assert_equal(record['manufactory_name'], manufactory_name)
            assert_equal(record['manufactory_id'], manufactory_id)
            assert_equal(record['size'], size)
            assert_equal(record['series_parallerl'], series_parallerl)
            assert_equal(record['status'], -2)
