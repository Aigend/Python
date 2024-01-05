# !/usr/bin/env python  
# -*- coding:utf-8 -*-  

""" 
@author:colin.li
@time: 2021/08/17
@api: POST_/api/1/in/battery/save_supplier
@showdoc: http://showdoc.nevint.com/index.php?s=/252&page_id=31668
@description: 供应商信息
"""

import pytest
import allure
import random
import string
from utils.http_client import TSPRequest as restClient
from utils.assertions import assert_equal


# 为了避免脏数据过多，作为主键的supplier_id保持一致不使用随机值
@pytest.mark.parametrize('upload_now, supplier_id, supplier_name, factory_code, phone, email, contacts, address, '
                         'expectation, check_db',
                         [
                             (False, '91320481MA1MNYLY9X', '江苏时代新能源科技有限公司',
                              ''.join(random.choices(string.digits, k=3)), ''.join(random.choices(string.digits, k=11)),
                              f"{''.join(random.choices(string.ascii_lowercase, k=5))}@temp.com",
                              '张三', '溧阳市昆仑街道城北大道1000号', 'success', True),
                             # 因为暂时没有上传国家平台接口的访问权限，所以这里暂时报internal_error错误
                             (True, '91320481MA1MNYLY9X', '江苏时代新能源科技有限公司',
                              ''.join(random.choices(string.digits, k=3)), ''.join(random.choices(string.digits, k=11)),
                              f"{''.join(random.choices(string.ascii_lowercase, k=5))}@temp.com",
                              '张三', '溧阳市昆仑街道城北大道1000号', 'internal_error', False),
                             (False, '', 'temp', 'temp', 'temp', 'temp', 'temp', 'temp', 'invalid_param', False),
                             (False, 'temp', '', 'temp', 'temp', 'temp', 'temp', 'temp', 'invalid_param', False),
                             (False, 'temp', 'temp', '', 'temp', 'temp', 'temp', 'temp', 'invalid_param', False),
                             (False, 'temp', 'temp', 'temp', '', 'temp', 'temp', 'temp', 'invalid_param', False),
                             (False, 'temp', 'temp', 'temp', 'temp', '', 'temp', 'temp', 'invalid_param', False),
                             (False, 'temp', 'temp', 'temp', 'temp', 'temp', '', 'temp', 'invalid_param', False),
                             (False, 'temp', 'temp', 'temp', 'temp', 'temp', 'temp', '', 'invalid_param', False),
                         ],
                         ids=[
                             '供应商信息不上报国家平台',
                             '供应商信息上报国家平台',
                             '未提供supplier_id',
                             '未提供supplier_name',
                             '未提供factory_code',
                             '未提供phone',
                             '未提供email',
                             '未提供contacts',
                             '未提供address',
                         ])
def test_post_save_supplier(env, mysql, upload_now, supplier_id, supplier_name, factory_code, phone, email, contacts,
                            address, expectation, check_db):
    app_id = 100078
    with allure.step('添加供应商'):
        json = {
            'upload_now': upload_now, 'id': supplier_id, 'name': supplier_name, 'factory_code': factory_code,
            'phone': phone, 'email': email, 'contacts': contacts, 'address': address}
        json = {k: v for k, v in json.items() if v is not None}
        http = {
            "host": env['host']['tsp_in'],
            "path": '/api/1/in/battery/save_supplier',
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
            record = mysql['battery_trace'].fetch_one('supplier', {'id': supplier_id})
            assert_equal(record['name'], supplier_name)
            assert_equal(record['factory_code'], factory_code)
            assert_equal(record['phone'], phone)
            assert_equal(record['email'], email)
            assert_equal(record['contacts'], contacts)
            assert_equal(record['address'], address)
            assert_equal(record['status'], -2)
