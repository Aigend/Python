# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : test_push_notify_all.py
# @Author : qiangwei.zhang
# @CreateTime : 2021/5/26 11:55 上午
# @Description :
"""
        用于给APP群发消息
        # /api/2/in/message/app_notify_all
        # http://showdoc.nevint.com/index.php?s=/647&page_id=30882
        接口参数
            * payload
                ✅* 必填
                ✅* json格式
            * scenario
                ✅* 必填
                ✅* string 类型，
                ✅* 透传
            * ttl
                ✅* 必填
                * 存活时间
            * target_app_ids 目标app_id
                ✅* 必填
                ✅* 一个
                ✅* 多个
                ✅* 多个有重复  forbid notify same app
            * category 信息类别
                ✅* 必填
                ✅* default 默认（app中显示在通知里）
                ✅* activity 活动
                ✅* in_box 收件箱（只支持马可波罗环境）
                ✅* red_packet 积分红包（马可波罗不支持）
                ✅* logistics 物流（马可波罗不支持）
                ✅* notification 通知 （马可波罗不支持）
            * include_app_versions 包含的版本
                ✅* 非必填
                ✅* 与exclude_app_versions互斥
                ✅* 只报1个版本
                ✅* 报多个版本
            * exclude_app_versions 不包含的版本
                ✅* 非必填
                ✅* 与include_app_versions互斥
                ✅* 1个版本不报
                ✅* 多个版本不报
            * store_history 是否存入历史信息表
                ✅* 默认 true
                ✅* true
                ✅* false
            * pass_through 是否显示通知
                ✅* 默认 0 显示
                ✅* 0 显示
                ✅* 1 不显示
            * do_push
                ✅* 默认 true
                ✅* true
                ✅* false
            * channel
                ✅* 默认all
                ✅* mqtt
                ✅* mipush
                * apns
                * hwpush
                * fcm
        问题1：notify_all接口do_push字段值为false时也会进行推送
        curl -X POST -H 'Accept: */*' -H 'Accept-Encoding: gzip, deflate' -H 'Connection: keep-alive' -H 'Content-Length: 525' -H 'Content-Type: application/x-www-form-urlencoded' -H 'User-Agent: python-requests/2.21.0' -d 'nonce=MrVIRwkCLBKySgCG&ttl=100000&target_app_ids=10001%2C10002&scenario=ls_system&include_app_versions=4.10.5%2C4.9.5&do_push=False&channel=mipush&category=default&payload=%7B%22target_link%22%3A+%22http%3A%2F%2Fwww.baidu.com%22%2C+%22title%22%3A+%22test%3Anotify_all%3Adefault%3Amipush%5Cu6d4b%5Cu8bd5%5Cu63a8%5Cu9001%2C%5Cu5982%5Cu6709%5Cu8bef%5Cu6536%5Cu8bf7%5Cu5ffd%5Cu7565%5Cuff0c%5Cu6253%5Cu6270%5Cu89c1%5Cu8c05%5Cuff01%5Cuff01%5Cuff01%22%2C+%22description%22%3A+%22%5Cu65f6%5Cu95f4%5Cuff1a2021-05-31+11%3A28%3A19%22%7D' 'https://app-test.nioint.com/api/2/in/message/app_notify_all?region=cn&lang=zh-cn&hash_type=sha256&app_id=10000&sign=6beffb9573469140a55bd2b60c8083a469e57bf421ca1d8c6f16668fc4f21bb5&timestamp=1622431699'
        {
  "data": {
    "message_id": "9b2484c7-93a9-4fc3-ab64-10d47c80e905-notify_all"
  },
  "request_id": "ac19a66ekp552dg4-41901",
  "result_code": "success",
  "server_time": 1622431699
}

http://kibana-test.csapi.cn:2601/app/kibana#/discover?_g=(refreshInterval:(display:Off,pause:!f,value:0),time:(from:'2021-05-31T03:27:51.913Z',mode:absolute,to:'2021-05-31T03:28:34.577Z'))&_a=(columns:!(_source),index:AXgWFRERbr7IAwfgruAX,interval:auto,query:(query_string:(analyze_wildcard:!t,query:%229b2484c7-93a9-4fc3-ab64-10d47c80e905-notify_all%22)),sort:!(logtime,desc))


        """
# /api/2/in/message/app_notify_all
# http://showdoc.nevint.com/index.php?s=/647&page_id=30882

import json
import time
import allure
import random
import pytest

from utils.assertions import assert_equal
from utils.httptool import request as rq
from utils.http_client import TSPRequest as hreq
from utils.logger import logger


@pytest.mark.skip("manual")
class TestMeesageAPI(object):
    push_notify_all_keys = "case_name,category,channel,host_key,data_key,store_history,appointment_time"
    push_notify_all_cases = [
        # ("正案例_TOB_category不为None,store_history为True", 'default', 'all', "app_tob_in", "nmp_app_tob", True, None),
        # ("正案例_TOB_category不为None,store_history为False", 'default', 'all', "app_tob_in", "nmp_app_tob", False, None),
        # ("反案例_TOB_category为None,store_history为True", None, 'all', "app_tob_in", "nmp_app_tob", True, None),
        # ("正案例_TOB_category为None,store_history为False", None, 'all', "app_tob_in", "nmp_app_tob", False, None),
        # ("正案例_TOC_category不为None,store_history为True", 'default', 'all', "app_in", "nmp_app", True, None),
        ("正案例_TOC_category不预约", 'default', 'all', "app_in", "nmp_app", True, None),
        # ("反案例_TOC_category预约时间小于1小时", 'default', 'all', "app_in", "nmp_app", True, int(time.time()) + 60 * 5),
        # ("反案例_TOC_category预约时间等于1小时", 'default', 'all', "app_in", "nmp_app", True, int(time.time()) + 60 * 60),
        # ("正案例_TOC_category预约时间大于1小时_大5秒", 'default', 'all', "app_in", "nmp_app", True, int(time.time()) + 60 * 60 +15),
        # ("正案例_TOC_category预约时间大于1小时_大1小时", 'default', 'all', "app_in", "nmp_app", True, int(time.time()) + 60 * 60 * 2),
        # ("正案例_TOC_category预约时间等于25小时", 'default', 'all', "app_in", "nmp_app", True, int(time.time()) + 60 * 60 * 25),
        # ("反案例_TOC_category预约时间大于25小时", 'default', 'all', "app_in", "nmp_app", True, int(time.time()) + 60 * 60 * 25 + 10),
        #
        # ("正案例_TOB_category不预约", 'default', 'all', "app_tob_in", "nmp_app_tob", True, None),
        # ("反案例_TOB_category预约时间小于1小时", 'default', 'all', "app_tob_in", "nmp_app_tob", True, int(time.time()) + 60 * 5),
        # ("反案例_TOB_category预约时间等于1小时", 'default', 'all', "app_tob_in", "nmp_app_tob", True, int(time.time()) + 60 * 60),
        # ("正案例_TOB_category预约时间大于1小时_大15秒", 'default', 'all', "app_tob_in", "nmp_app_tob", True, int(time.time()) + 60 * 60 + 5),
        # ("正案例_TOB_category预约时间大于1小时_大1小时", 'default', 'all', "app_tob_in", "nmp_app_tob", True, int(time.time()) + 60 * 60 * 2),
        # ("正案例_TOB_category预约时间等于25小时", 'default', 'all', "app_tob_in", "nmp_app_tob", True, int(time.time()) + 60 * 60 * 25),
        # ("反案例_TOB_category预约时间大于25小时", 'default', 'all', "app_tob_in", "nmp_app_tob", True, int(time.time()) + 60 * 60 * 25 + 10),
        # ("正案例_TOC_category不为None,store_history为False", 'default', 'all', "app_in", "nmp_app", False, None),
        # ("反案例_TOC_category为None,store_history为True", None, 'all', "app_in", "nmp_app", True, None),
        # ("正案例_TOC_category为None,store_history为False", None, 'all', "app_in", "nmp_app", False, None),
    ]

    @pytest.mark.skip('manual')
    @pytest.mark.parametrize(push_notify_all_keys, push_notify_all_cases)
    def test_notify_all(self, env, cmdopt, mysql, case_name, category, channel, host_key, data_key, store_history, appointment_time):
        if 'prod' in cmdopt:
            return 0
        if cmdopt in ["test", "stg"] and "tob" in data_key:
            logger.debug("国内暂不支持tob服务")
            return 0
        app_id = 10000
        target_app_ids = '10001,10002'
        if "marcopolo" in cmdopt:
            target_app_ids = '1000003,1000004'
            if "tob" in data_key:
                target_app_ids = "1000014"
        inputs = {
            "host": env['host'][host_key],
            "path": "/api/2/in/message/app_notify_all",
            "method": "POST",
            "headers": {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            "params": {
                "region": "cn",
                "lang": "zh-cn",
                "hash_type": "sha256",
                "app_id": app_id,
                "sign": "",
            },
            "data": {
                'nonce': 'MrVIRwkCLBKySgCG',
                'ttl': 100000,
                'target_app_ids': target_app_ids,
                'scenario': 'ls_link',
                'store_history': store_history,
                'do_push': True,
                'pass_through': 0,
                'channel': channel,
                "category": category,
                'payload': json.dumps({
                    "target_link": "http://www.niohome.com",
                    # "title": f"【{cmdopt}】环境notify_all推送,如有误收请忽略，打扰见谅！！！",
                    "title": f"{cmdopt}notify_all推送",
                    # "description": f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}",
                    "description": f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} description content notify all",
                    # "description": f"时间：{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} message_center notify all推送，长度大于oppo限制",
                }),
            }
        }
        if not category:
            inputs["data"].pop("category")
        if appointment_time:
            inputs["data"]["appointment_time"] = appointment_time
        response = hreq.request(env, inputs)
        if case_name.startswith("正案例"):
            message_id = response['data'].pop('message_id', '')
            assert_equal('success', response['result_code'])
            assert_equal('notify_all' in message_id, True)
        else:
            assert_equal('invalid_param', response['result_code'])
        # user_count_dict = prepare_user_message_count_by_inputs(inputs, mysql)
        # time.sleep(10)
        # user_list = []
        # mutil_user_list =[]
        # with allure.step("校验mysql"):
        #     for user_id, count in user_count_dict.items():
        #         if int(count) == 1:
        #             message_in_mysql = mysql['nmp_app'].fetch(f'history_{str(user_id)[-3:]}', {'user_id': user_id, 'message_id': message_id}, retry_num=1)
        #             if not message_in_mysql:
        #                 user_list.append(user_id)
        #                 logger.error(f"ID为{user_id}的用户，未查到ID为{message_id}的消息记录")
        #         else:
        #             mutil_user_list.append({user_id, count})
        #             continue
        # logger.debug(user_list)
        # assert_equal(len(user_list), 0)


def prepare_user_message_count_by_inputs(inputs, mysql):
    sql = """
select b.user_id as user_id, count(user_id) count_user_id
from clients c,bindings b 
where b.client_id = c.client_id 
and b.visible=1\n"""
    target_app_ids = inputs['data']['target_app_ids']
    include_app_versions = inputs['data'].get('include_app_versions', None)
    exclude_app_versions = inputs['data'].get('exclude_app_versions', None)
    app_id_list = target_app_ids.split(',')
    if app_id_list:
        sql = sql + f"and b.app_id in {app_id_list}\n"
    if include_app_versions:
        app_version_list = include_app_versions.split(',')
        sql = sql + f"and c.app_version in {app_version_list}\n"
    if exclude_app_versions:
        app_version_list = tuple(exclude_app_versions.split(','))
        sql = sql + f"and c.app_version not in {app_version_list}\n"
    sql = sql + "group by b.user_id order by b.user_id"
    sql = sql.replace('[', '(')
    sql = sql.replace(']', ')')
    logger.debug(sql)
    results = mysql['nmp_app'].fetch_by_sql(sql)
    user_count_dict = {str(result['user_id']): result['count_user_id'] for result in results}
    return user_count_dict
