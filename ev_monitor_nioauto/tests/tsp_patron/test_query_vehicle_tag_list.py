""" 
@author:dun.yuan
@time: 2021/11/23 3:42 下午
@contact: dun.yuan@nio.com
@description: vehicle tag api/vehicle list api by tags
@showdoc：http://showdoc.nevint.com/index.php?s=/11&page_id=32339
http://showdoc.nevint.com/index.php?s=/11&page_id=32338
http://showdoc.nevint.com/index.php?s=/11&page_id=32702
"""
import allure
import pytest
from utils.http_client import TSPRequest as hreq
from utils.assertions import assert_equal


class TestQueryVehicleTagList(object):
    @pytest.mark.test
    @pytest.mark.parametrize('key', ['model_type', 'model_series', 'model_type_year', 'register_province',
                                     'register_city', 'nio_pilot_pack', 'package_global_version'])
    def test_query_vehicle_tag_list(self, env, key, mysql):
        with allure.step("获取key对应的app id"):
            app_id = mysql['rvs'].fetch_one("patron_vfield_auth", {'field': key})['app_id']
        with allure.step("通过不同的key，来获取返回结果"):
            inputs = {
                "host": env['host']['tsp_in'],
                "method": "GET",
                "path": "/api/1/in/patron/vehicle/tag",
                "params": {
                    'app_id': 10000,
                    'key': key,
                    "sign": ''
                },
                "timeout": 5.0
            }
            res = hreq.request(env, inputs)
            assert_equal(res['result_code'], 'success')
            data = mysql['vms'].fetch('portrait_tag_name_map',
                                      where_model={'tag_type': 'cgw_f141' if key == 'package_global_version' else key,
                                                   'vehicle_count>': 0},
                                      fields=['tag', 'vehicle_count'])
            tags = list(t['tag'] for t in data)
            assert_equal(res['data']['value'], tags)
        if key == 'model_series':
            return
        with allure.step("通过key，来获取返回vehicle list"):
            inputs = {
                "host": env['host']['tsp_in'],
                "method": "POST",
                "path": "/api/1/in/patron/vehicle/list",
                "params": {
                    'app_id': app_id,
                    "sign": ''
                },
                "data": {
                    key: tags[-1],
                    'offset': 0,
                    'limit': 10
                },
                "timeout": 5.0
            }
            res = hreq.request(env, inputs)
            assert_equal(res['result_code'], 'success')

        with allure.step("在ES查询验证"):
            inputs = {
                "host": 'http://10.10.200.63:9200',
                "method": "POST",
                "path": "/vms_vehicle_portrait_test/_search",
                "headers": {
                    'Content-Type': 'application/json',
                    'Authorization': 'Basic ZWxhc3RpYzp0c3BkYXRhZXM='
                },
                "json": {
                    'query': {'match': {'cgw_f141' if key == 'package_global_version' else key: tags[-1]}},
                    'sort': [{'_id': {'order': 'asc'}}]
                },
                "timeout": 5.0
            }
            response = hreq.request(env, inputs)
            assert_equal(res['data']['total_size'], response['hits']['total']['value'])
            for item in res['data']['vehicle_list']:
                exist = False
                for hit in response['hits']['hits']:
                    if hit['_id'] == item['vehicle_id']:
                        for k in item.keys():
                            assert_equal(item[k], hit['_source']['cgw_f141' if k == 'package_global_version' else k])
                        exist = True
                assert exist

    @pytest.mark.test
    @pytest.mark.parametrize('key', ['model_type', 'model_type_year', 'register_province',
                                     'register_city', 'nio_pilot_pack', 'package_global_version'])
    def test_query_vehicle_list_scroll(self, env, key, mysql):
        with allure.step("获取key对应的app id"):
            app_id = mysql['rvs'].fetch_one("patron_vfield_auth", {'field': key})['app_id']
        with allure.step("通过不同的key，来获取返回结果"):
            inputs = {
                "host": env['host']['tsp_in'],
                "method": "GET",
                "path": "/api/1/in/patron/vehicle/tag",
                "params": {
                    'app_id': 10001,
                    'key': key,
                    "sign": ''
                },
                "timeout": 5.0
            }
            res = hreq.request(env, inputs)
            assert_equal(res['result_code'], 'success')
            data = mysql['vms'].fetch('portrait_tag_name_map',
                                      where_model={'tag_type': 'cgw_f141' if key == 'package_global_version' else key,
                                                   'vehicle_count>': 0},
                                      fields=['tag', 'vehicle_count'])
            tags = list(t['tag'] for t in data)
            assert_equal(res['data']['value'], tags)
        with allure.step("通过key，来获取返回vehicle list"):
            inputs = {
                "host": env['host']['tsp_in'],
                "method": "POST",
                "path": "/api/1/in/patron/vehicle/scroll",
                "params": {
                    'app_id': app_id,
                    "sign": ''
                },
                "data": {
                    key: tags[0],
                    'offset': 0,
                    'limit': 1
                },
                "timeout": 5.0
            }
            res = hreq.request(env, inputs)
            scroll_id = res['data']['scroll_id']
            vehicle_id = res['data']['vehicle_list'][0]['vehicle_id']
            assert_equal(res['result_code'], 'success')
        with allure.step("通过key和scroll_id，来获取接下来的vehicle list"):
            inputs = {
                "host": env['host']['tsp_in'],
                "method": "POST",
                "path": "/api/1/in/patron/vehicle/scroll",
                "params": {
                    'app_id': app_id,
                    "sign": ''
                },
                "data": {
                    key: tags[0],
                    'scroll_id': scroll_id,
                    'offset': 0,
                    'limit': 1
                },
                "timeout": 5.0
            }
            res = hreq.request(env, inputs)
            assert_equal(res['result_code'], 'success')
            assert vehicle_id != res['data']['vehicle_list'][0]['vehicle_id']
        with allure.step("通过key和scroll_id，来获取接下来的vehicle list"):
            inputs = {
                "host": env['host']['tsp_in'],
                "method": "POST",
                "path": "/api/1/in/patron/vehicle/scroll",
                "params": {
                    'app_id': app_id,
                    "sign": ''
                },
                "data": {
                    key: tags[0],
                    'scroll_id': scroll_id,
                    'offset': 0,
                    'limit': 1
                },
                "timeout": 5.0
            }
            res = hreq.request(env, inputs)
            assert_equal(res['result_code'], 'success')
            assert vehicle_id != res['data']['vehicle_list'][0]['vehicle_id']



