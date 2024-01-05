# !/usr/bin/env python  
# -*- coding:utf-8 -*-  

""" 
@author:colin.li
@time: 2021/10/28
@api: POST_/api/1/in/battery/pack_out
@showdoc: http://showdoc.nevint.com/index.php?s=/252&page_id=11118
@description: 电池出库接口.
"""

import pytest
import allure
from utils.http_client import TSPRequest as restClient
from utils.assertions import assert_equal
from datetime import date, timedelta


"""
因为出库接口需要对接国家平台，所以无法做到完全自动化，所需步骤：
1. 登陆国家平台测试环境http://61.149.8.74:8990/admin/index，进入页面：车辆换电信息-换电入库信息
2. 随意取得一个电池包编码使用
当出库成功时该条记录将从列表中删除，所以随着测试进行，数量会越来越少
如果数据没有了，可以在battery_trace库中添加数据，将logistic_des设置为103（上传到换电电池库和生产电池库），status设置为-2（电池包尚未上传）
BTS后台的task离线任务会定时扫描符合上述信息的电池包信息并上传到国家平台
"""

# 以下两条数据需从http://61.149.8.74:8990/admin/index里取得
code = '03UPE01000011C85A00FTY20'
in_date = date(2020, 10, 29)
early_date = (in_date - timedelta(2)).strftime('%Y-%m-%d %H:%M:%S')
out_date = (in_date + timedelta(1)).strftime('%Y-%m-%d %H:%M:%S')


@pytest.mark.skip("需先从http://61.149.8.74:8990/admin/index里取得数据")
@pytest.mark.parametrize('gbt_code, record_date, unit_code, unit_name, remark, result',
                         [
                             ('123456781234567812345678', out_date, '91110105MA009PJM56', '上海蔚来汽车有限公司北京分公司', 'test', 'internal_error'),
                             (code, early_date, '91110105MA009PJM56', '上海蔚来汽车有限公司北京分公司', 'test', 'internal_error'),
                             (code, out_date, '', '上海蔚来汽车有限公司北京分公司', 'test', 'internal_error'),
                             (code, out_date, '91110105MA009PJM56', '', 'test', 'internal_error'),
                             (code, out_date, '91110105MA009PJM56', '上海蔚来汽车有限公司北京分公司', 'test', 'success'),
                         ],
                         ids=[
                             '使用没有在国家平台入库的电池包编码',
                             '出库时间在入库时间之前',
                             '未填去向单位统一社会信用代码',
                             '未填出库电池包去向单位名称',
                             '所有数据正常',
                         ])
def test_post_battery_pack_out(env, gbt_code, record_date, unit_code, unit_name, remark, result):
    with allure.step('生成电池扩展信息'):
        app_id = 100078
        http = {
            "host": env['host']['tsp_in'],
            "path": "/api/1/in/battery/pack_out",
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "params": {
                "app_id": app_id,
                "sign": ""
            },
            "json": {'out_time': record_date,
                     'code': gbt_code,
                     'destination_unit_code': unit_code,
                     'destination_unit_name': unit_name,
                     'remark': remark}
        }
        response = restClient.request(env, http)
    with allure.step('校验response'):
        assert_equal(response['result_code'], result)

