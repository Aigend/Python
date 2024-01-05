# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : test_push_sms.py
# @Author : qiangwei.zhang
# @CreateTime : 2021/3/23 11:02 上午
# @Description :
import copy
import time

import allure
import pytest

from tests.app_message_center.clear_rate_limit import clear_rate_limit
from tests.app_message_center.conftest import generate_sms_result, generate_voice_sms_result
from utils.http_client import TSPRequest as hreq
from utils.collection_message_states import collection_message_states
from utils.logger import logger
from utils.assertions import assert_equal
from utils.validation_data_format import validation_e164_mobile, validation_fake_mobile

skip_env_list = ["test_marcopolo", "stg_marcopolo"]
cn_sms_direct_push_path = "/api/2/in/message/cn/sms_direct_push"
cn_sms_voice_message_push_path = "/api/2/in/message/cn/voice_message"
cn_sms_push_path = "/api/2/in/message/cn/sms_push"
app_id = 10001
long_contens = "蔚来第三款量产车——智能电动轿跑SUV EC6全球首秀。EC6采用轿跑式车身设计，整车风阻系数低至0.27Cd。EC6的一体化穹顶式玻璃车顶，总面积达2.1平方米。EC6性能版搭载前160千瓦永磁电机和240千瓦感应电机，百公里加速仅为4.7秒。搭载100千瓦时液冷恒温电池包的EC6 性能版NEDC续航达到615公里。7月24日，蔚来智能电动轿跑SUV EC6在2020成都车展正式上市，即日起蔚来App和官网开启选配。首批车辆将在9月下旬开启交付。蔚来EC6搭载70kWh电池包的运动版车型，补贴前售价为36.8万起；性能版车型，补贴前售价为40.8万起；签名版车型，补贴前售价为46.8万起。蔚来EC6轿跑式车身设计塑造出兼具动感与优雅的车身比例。蓄势待发的流线型设计让EC6的空气动力学表现尤为突出，风阻系数低至0.26Cd。蔚来EC6配备全景天幕式玻璃天窗，拥有超大的透光面积，同时采用双层隔热玻璃，能量透过率仅为15%，并能隔绝99.5%以上紫外线。蔚来EC6车身尺寸2.9米长轴距，内饰延续“第二起居室”蔚来EVE概念车的设计理念。蔚来EC6签名版和性能版搭载前160kW高效能永磁电机+后240kW高性能感应电机组成的双电机智能四驱系统峰值功率544马力，最大扭矩725N·m，造就0-100km/h加速最快4.5秒。运动版则搭载前、后160kW双永磁电机组合，0-100km/h加速可达5.4秒。EC6采用高强度铝合金车身，全系标配CDC动态阻尼控制系统，可选主动式空气悬架，智能识别路况，兼具操控性和舒适性。蔚来EC6性能版和签名版搭载70kWh电池包，综合工况续航里程最高可达440公里；搭载100kWh电池包，综合工况续航里程最高可达615公里。蔚来EC6拥有智能化愉悦数字座舱，9.8英寸超窄边数字仪表、11.3英寸高清多点触控中控屏、全圆AMOLED屏的NOMI Mate 2.0共同打造智能、高效、安全、愉悦的交互体验蔚来第三款量产车——智能电动轿跑SUV EC6全球首秀。EC6采用轿跑式车身设计，整车风阻系数低至0.27Cd。EC6的一体化穹顶式玻璃车顶，总面积达2.1平方米。EC6性能版搭载前160千瓦永磁电机和240千瓦感应电机，百公里加速仅为4.7秒。搭载100千瓦时液冷恒温电池包的EC6 性能版NEDC续航达到615公里。7月24日，蔚来智能电动轿跑SUV EC6在2020成都车展正式上市，即日起蔚来App和官网开启选配。首批车辆将在9月下旬开启交付。蔚来EC6搭载70kWh电池包的运动版车型，补贴前售价为36.8万起；性能版车型，补贴前售价为40.8万起；签名版车型，补贴前售价为46.8万起。蔚来EC6轿跑式车身设计塑造出兼具动感与优雅的车身比例。蓄势待发的流线型设计让EC6的空气动力学表现尤为突出，风阻系数低至0.26Cd。蔚来EC6配备全景天幕式玻璃天窗，拥有超大的透光面积，同时采用双层隔热玻璃，能量透过率仅为15%，并能隔绝99.5%以上紫外线。蔚来EC6车身尺寸2.9米长轴距，内饰延续“第二起居室”蔚来EVE概念车的设计理念。蔚来EC6签名版和性能版搭载前160kW高效能永磁电机+后240kW高性能感应电机组成的双电机智能四驱系统峰值功率544马力，最大扭矩725N·m，造就0-100km/h加速最快4.5秒。运动版则搭载前、后160kW双永磁电机组合，0-100km/h加速可达5.4秒。EC6采用高强度铝合金车身，全系标配CDC动态阻尼控制系统，可选主动式空气悬架，智能识别路况，兼具操控性和舒适性。蔚来EC6性能版和签名版搭载70kWh电池包，综合工况续航里程最高可达440公里；搭载100kWh电池包，综合工况续航里程最高可达615公里。蔚来EC6拥有智能化愉悦数字座舱，9.8英寸超窄边数字仪表、11.3英寸高清多点触控中控屏、全圆AMOLED屏的NOMI Mate 2.0共同打造智能、高效、安全、愉悦的交互体验"
"""
notify_sms
    EU
        ✅同步发送接口
            测试场景
                ✅单个发送
                ✅批量发送 多个正常，部分正常，全部异常，有重复
                ✅必填字段校验
                ✅手机号格式校验 单个，多个，多个中部分异常
        ✅异步发送接口
            测试场景
                ✅单个发送
                ✅批量发送 多个正常，部分正常，全部异常，有重复
                ✅必填字段校验
                ✅手机号格式校验 单个，多个，多个中部分异常
    CN
        ✅同步发送接口
            ✅测试场景
                ✅根据user_id发送
                ✅根据account_id发送
                ✅根据recipient发送
                ✅批量发送
        ✅异步发送接口
            ✅测试场景
                ✅根据user_id发送
                ✅根据account_id发送
                ✅根据recipient发送，手机号格式校验 单个，多个，多个中部分异常
                ✅批量发送
        ✅语音短信
            ✅支持中文
            ✅支持英文
            ✅接口仅支持单个人根据recipient发送
            ✅文本长度 最长160个汉字左右
            ✅接电话后不主动挂断，播放三次后自动挂断
            ✅同一账号频率限制LimitExceeded.DeliveryFrequencyLimit


EU+CN服务接口调用限制
    CN
        TOC
            ✅CN上传文件
            ✅CN短信发送
                直接发送
                异步发送
                电话语音短信
            ✅CN飞书发送
            ✅CN邮件发送
                邮件发送接口
                附件邮件发送
            ✅employee邮件发送
                邮件发送接口
                附件邮件发送
            ✅notify
            ✅notify_all
    EU
        TOC
            ✅EU上传文件
            ✅EU短信发送
                直接发送
                异步发送
                电话语音短信
            ✅employee邮件发送
                邮件发送接口
                附件邮件发送
            ✅EU飞书发送
            ✅EU邮件发送
                邮件发送接口
                附件邮件发送
            ✅notify
            ✅notify_all
"""


@pytest.mark.run(order=1)
class TestPushSMS(object):
    """
    接口文档 http://showdoc.nevint.com/index.php?s=/647&page_id=31741
    检查点
        mysql：
            * sms_history 历史消息
            * sms_history_meta_info 消息内容
        redis:
            *无
    user_ids,account_ids,recipients
        * 三选一
        * 批量个数 100（批量发送）
        * 重复用户
        * 异常数据
    content
        * 必填
        * 字符串
        * 长度限制
        * 支持变量，不支持
    category
        * 必填
        * (无限制，目前无业务逻辑处理)
    Q&A:
        Q1.短信频率限制，下游调用的是哪个服务
        dd
        Q2.category 类型，不同有代码逻辑上处理么，
            目前随便传都能发送成功，邮件也是
        Q3.content 支持长度限制，是否支持变量
            目前长度1000字可以收到。2000字未收到
        Q4.重复用户处理
            目前状况是接口会返回两条成功，但是手机一条也未收到
            DD频率限制
    """
    push_sms_cn_keys = "case_name,user_key,content,category,host_key,data_key"
    push_sms_cn_cases = [
        ("正案例_TOC根据account_id发送短信", "account_id", "content", "notification", "app_in", "nmp_app"),
        ("正案例_TOC根据user_id发送短信", "user_id", "content", "ads", "app_in", "nmp_app"),
        ("正案例_TOC根据recipient发送短信", "recipient", "content", "notification", "app_in", "nmp_app"),
        ("正案例_TOB根据recipient发送短信", "recipient", "content", "ads", "app_tob_in", "nmp_app_tob"),
        ("正案例_TOB根据account_id发送短信", "account_id", "content", "ads", "app_tob_in", "nmp_app_tob"),
        ("正案例_TOB根据user_id发送短信", "user_id", "content", "ads", "app_tob_in", "nmp_app_tob"),
    ]
    push_sms_cn_ids = [f"{case[0]}" for case in push_sms_cn_cases]

    @pytest.mark.parametrize(push_sms_cn_keys, push_sms_cn_cases, ids=push_sms_cn_ids)
    def test_push_sms_cn(self, env, cmdopt, mysql, redis, get_sms_path, case_name, user_key, content, category, host_key, data_key, ):
        if cmdopt in skip_env_list:
            logger.debug(f"该测试案例不适用【{cmdopt}】环境")
            return 0
        if get_sms_path == "/api/2/in/message/cn/marketing_sms_push" and user_key != "recipient":
            logger.debug(f"marketing_sms_push接口不支持{user_key}s字段")
            return 0
        recipients = env['push_sms']['recipient']
        inputs = {
            "host": env['host'][host_key],
            "path": get_sms_path,
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "params": {
                "region": "cn",
                "lang": "zh-cn",
                "hash_type": "sha256",
                "app_id": app_id,
                "sign": ""
            },
            "json": {
                f"{user_key}s": env['push_sms'][user_key],
                "content": f"【{cmdopt}】环境sms push接口推送短信{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}{case_name}",
                "category": category,
            }
        }
        if not content:
            inputs.get("json").pop("content")
        if not category:
            inputs.get("json").pop("category")
        response = hreq.request(env, inputs)
        with allure.step(f"【{cmdopt}】环境,清理{app_id}频率限制"):
            if "test" in cmdopt:
                redis["app_message"].delete(f"rate.limiting:cn/sms_push_{app_id}")
        if case_name.startswith("正案例"):
            assert response['result_code'] == 'success'
            message_id = response['data']['message_id']
            expected_states = [21, 22, 23, 24, 26]
            ms_st = f"{message_id}|{expected_states}|{get_sms_path}"
            collection_message_states(cmdopt, ms_st)
            sms_history = mysql[data_key].fetch("sms_history", {"message_id": message_id}, ["recipient"])
            assert str(sms_history[0]['recipient']) == str(f"{recipients}")
            sms_history_info = mysql[data_key].fetch("sms_history_meta_info", {"message_id": message_id}, )
            assert len(sms_history_info) == 1

    push_sms_cn_voice_message_keys = "case_name,recipient,content,category,host_key,data_key"
    push_sms_cn_voice_message_cases = [
        # ("正案例_TOC根据recipient发送短信", "+8617610551933", "content", "notification", "app_in", "nmp_app"),
        ("正案例_TOB根据recipient发送短信", "+8617610551933", "content", "ads", "app_tob_in", "nmp_app_tob"),
    ]
    push_sms_cn_voice_message_ids = [f"{case[0]}" for case in push_sms_cn_voice_message_cases]

    @pytest.mark.skip("manual")
    @pytest.mark.parametrize(push_sms_cn_voice_message_keys, push_sms_cn_voice_message_cases, ids=push_sms_cn_voice_message_ids)
    def test_push_sms_cn_voice_message(self, env, cmdopt, mysql, redis, case_name, recipient, content, category, host_key, data_key):
        if cmdopt in skip_env_list:
            logger.debug(f"该测试案例不适用【{cmdopt}】环境")
            return 0
        inputs = {
            "host": env['host'][host_key],
            "path": cn_sms_voice_message_push_path,
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "params": {
                "region": "cn",
                "lang": "zh-cn",
                "hash_type": "sha256",
                "app_id": app_id,
                "sign": ""
            },
            "json": {
                "recipients": recipient,
                "content": f"你好，蔚来汽车国内测试环境语音短信推送测试; Hello, the domestic test environment voice messages push test;",
                "category": category,
            }
        }
        if not content:
            inputs.get("json").pop("content")
        if not category:
            inputs.get("json").pop("category")
        response = hreq.request(env, inputs)
        with allure.step(f"【{cmdopt}】环境,清理{app_id}频率限制"):
            if "test" in cmdopt:
                redis["app_message"].delete(f"rate.limiting:cn/sms_push_{app_id}")
        if case_name.startswith("正案例"):
            assert response['result_code'] == 'success'
            message_id = response['data']['message_id']
            # expected_states = [21, 22, 23, 24, 26]
            # ms_st = f"{message_id}|{expected_states}|{cn_sms_voice_message_push_path}"
            # collection_message_states(cmdopt, ms_st)
            sms_history = mysql[data_key].fetch("sms_history", {"message_id": message_id}, ["recipient"])
            assert str(sms_history[0]['recipient']) == str(f"{recipient}")
            sms_history_info = mysql[data_key].fetch("sms_history_meta_info", {"message_id": message_id}, )
            assert len(sms_history_info) == 1
        else:
            expected_res = {"result_code": "invalid_param", "debug_msg": "necessary parameters are null."}
            response.pop("request_id")
            response.pop("server_time")
            assert_equal(expected_res, response)

    push_sms_cn_negative_keys = "case_name,user_key,recipient,content,category,host_key,data_key"
    push_sms_cn_negative_cases = [
        ("反案例_content为None", "recipient", "+8617610551933", None, "ads", "app_in", "nmp_app"),
        ("反案例_category为None", "recipient", "+8617610551933", "content", None, "app_in", "nmp_app"),
        ("反案例_recipient为None", "recipient", None, "content", None, "app_in", "nmp_app"),
        ("反案例_account_id为None", "account_id", None, "content", None, "app_in", "nmp_app"),
        ("反案例_user_id为None", "user_id", None, "content", None, "app_in", "nmp_app"),
        # ("反案例_all_invalid_recipient", "recipient", "+86 17610551933,17610551933,we2321113,98761761234,+8698761761234", "content", "ads", "app_in", "nmp_app"),
        ("反案例_部分invalid_recipient", "recipient", "+8617610551933,+86 17610551933", "content", "ads", "app_in", "nmp_app"),
    ]
    push_sms_cn_negative_ids = [f"{case[0]}" for case in push_sms_cn_negative_cases]

    @pytest.mark.parametrize(push_sms_cn_negative_keys, push_sms_cn_negative_cases, ids=push_sms_cn_negative_ids)
    def test_push_sms_negative_case(self, env, cmdopt, redis, get_sms_path, case_name, user_key, recipient, content, category, host_key, data_key):
        clear_rate_limit(redis, cmdopt, 10000)
        if cmdopt in skip_env_list:
            logger.debug(f"该测试案例不适用【{cmdopt}】环境")
            return 0
        if get_sms_path == "/api/2/in/message/cn/marketing_sms_push" and user_key != "recipient":
            logger.debug(f"marketing_sms_push接口不支持{user_key}s字段")
            return 0
        inputs = {
            "host": env['host'][host_key],
            "path": get_sms_path,
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "params": {
                "region": "cn",
                "lang": "zh-cn",
                "hash_type": "sha256",
                "app_id": app_id,
                "sign": ""
            },
            "json": {
                f"{user_key}s": recipient,
                "content": f"【{cmdopt}】环境sms push接口推送短信{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}{case_name}",
                "category": category,
            }
        }
        if not content:
            inputs.get("json").pop("content")
        if not category:
            inputs.get("json").pop("category")
        response = hreq.request(env, inputs)
        with allure.step(f"【{cmdopt}】环境,清理{app_id}频率限制"):
            if "test" in cmdopt:
                redis["app_message"].delete(f"rate.limiting:cn/sms_push_{app_id}")
        if response.get("result_code") == "success":
            response.pop("request_id")
            response.pop("server_time")
            response["data"].pop("message_id")
            expected_res = generate_sms_result(recipient)
            expected_res_sorted = sorted(expected_res["data"]["details"], key=lambda x: x['recipient'])
            response_sorted = sorted(response["data"]["details"], key=lambda x: x['recipient'])
            assert_equal(expected_res_sorted, response_sorted)
        else:
            response.pop("request_id")
            response.pop("server_time")
            expected_res = {"result_code": "invalid_param", "debug_msg": "necessary parameters are null."}
            assert_equal(expected_res, response)

    push_sms_cn_voice_message_negative_keys = "case_name,recipient,content,category,host_key,data_key"
    push_sms_cn_voice_message_negative_cases = [
        ("反案例_recipient带空格", "+86 17610551933", "content", "notification", "app_in", "nmp_app"),
        ("反案例_recipient不加国家码", "17610551933", "content", "notification", "app_in", "nmp_app"),
        # ("反案例_recipient为假手机号", "+8698760551933", "content", "notification", "app_in", "nmp_app"),
        # ("反案例_recipient为假手机号不加国家码", "98760551933", "content", "notification", "app_in", "nmp_app"),
        ("反案例_recipient有非数字", "+86987str_number", "content", "notification", "app_in", "nmp_app"),
        ("反案例_recipient非数字", "+invalid_phone_number", "content", "notification", "app_in", "nmp_app"),
        ("反案例_content为None", "+8617610551933", None, "ads", "app_in", "nmp_app"),
        # ("反案例_category为None", "+8617610551933", "content", None, "app_in", "nmp_app"),
        ("反案例_recipient为None", None, "content", "ads", "app_in", "nmp_app"),
    ]
    push_sms_cn_voice_message_negative_ids = [f"{case[0]}" for case in push_sms_cn_voice_message_negative_cases]

    @pytest.mark.parametrize(push_sms_cn_voice_message_negative_keys, push_sms_cn_voice_message_negative_cases, ids=push_sms_cn_voice_message_negative_ids)
    def test_push_sms_cn_voice_message_negative_case(self, env, cmdopt, redis, case_name, recipient, content, category, host_key, data_key):
        if cmdopt in skip_env_list:
            logger.debug(f"该测试案例不适用【{cmdopt}】环境")
            return 0
        inputs = {
            "host": env['host'][host_key],
            "path": cn_sms_voice_message_push_path,
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "params": {
                "region": "cn",
                "lang": "zh-cn",
                "hash_type": "sha256",
                "app_id": app_id,
                "sign": ""
            },
            "json": {
                "recipients": recipient,
                "content": f"你好，蔚来汽车国内测试环境语音短信推送测试; Hello, the domestic test environment voice messages push test;",
                "category": category,
            }
        }
        if not content:
            inputs.get("json").pop("content")
        if not category:
            inputs.get("json").pop("category")
        response = hreq.request(env, inputs)
        with allure.step(f"【{cmdopt}】环境,清理{app_id}频率限制"):
            if "test" in cmdopt:
                redis["app_message"].delete(f"rate.limiting:cn/sms_push_{app_id}")
        with allure.step("校验返回内容"):
            if response.get("result_code") == "success":
                response.pop("request_id")
                response.pop("server_time")
                response["data"].pop("message_id")
                expected_res = generate_voice_sms_result(recipient)
                expected_res["data"]["details"] = sorted(expected_res["data"]["details"], key=lambda x: x['recipient'])
                response["data"]["details"] = sorted(response["data"]["details"], key=lambda x: x['recipient'])
                assert_equal(expected_res, response)
            else:
                response.pop("request_id")
                response.pop("server_time")
                expected_res = {"result_code": "invalid_param", "debug_msg": "necessary parameters are null."}
                assert_equal(expected_res, response)

    @pytest.mark.skip("manual")
    def test_push_sms_cn_voice_message_tencent_frequency_limit(self, env, cmdopt, redis):
        """
        语音消息频率限制策略是什么？
            为了保障业务安全，语音消息默认的频率限制策略为：
                同一被叫号码30秒内发送上限为1条（语音通知类支持调整发送上限为2条）。
                同一被叫号码10分钟内发送上限为2条（语音通知类支持调整发送上限为10条）。
                同一被叫号码1天内发送上限为3条（语音通知类默认发送上限为5条，支持调整发送上限为50条）。
                同一号码22:00至次日08:00发送上限为1条（语音通知类支持调整发送上限为50条）。
        https://cloud.tencent.com/document/product/1128/38004
        """
        time.sleep(30)  # 该案例执行间隔30s
        if cmdopt in skip_env_list:
            logger.debug(f"该测试案例不适用【{cmdopt}】环境")
            return 0
        recipient, category, host_key = "+86176105519345", "ads", "app_in"
        inputs = {
            "host": env['host'][host_key],
            "path": cn_sms_voice_message_push_path,
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "params": {
                "region": "cn",
                "lang": "zh-cn",
                "hash_type": "sha256",
                "app_id": app_id,
                "sign": ""
            },
            "json": {
                "recipients": recipient,
                "content": f"你好，蔚来汽车国内测试环境语音短信推送测试; Hello, the domestic test environment voice messages push test;",
                "category": category,
            }
        }
        inputs_req2 = copy.deepcopy(inputs)  # 深拷贝用于第二次请求
        with allure.step(f"【{cmdopt}】环境,清理{app_id}频率限制"):
            if "test" in cmdopt:
                redis["app_message"].delete(f"rate.limiting:cn/sms_push_{app_id}")
        with allure.step("第一次呼叫"):
            response = hreq.request(env, inputs)
        with allure.step("校验返回内容"):
            if response.get("result_code") == "success":
                response.pop("request_id")
                response.pop("server_time")
                response["data"].pop("message_id")
                expected_res = generate_voice_sms_result(recipient)
                expected_res["data"]["details"] = sorted(expected_res["data"]["details"], key=lambda x: x['recipient'])
                response["data"]["details"] = sorted(response["data"]["details"], key=lambda x: x['recipient'])
                assert_equal(expected_res, response)
        with allure.step(f"【{cmdopt}】环境,清理{app_id}频率限制"):
            if "test" in cmdopt:
                redis["app_message"].delete(f"rate.limiting:cn/sms_push_{app_id}")
        with allure.step("第二次呼叫"):
            response = hreq.request(env, inputs_req2)
        with allure.step("校验返回内容"):
            if response.get("result_code") == "success":
                response.pop("request_id")
                response.pop("server_time")
                response["data"].pop("message_id")
                expected_res = {
                    "data": {
                        "details": [
                            {
                                "recipient": recipient,
                                "result": "LimitExceeded.DeliveryFrequencyLimit"
                            }
                        ],
                        "success": 0,
                        "failure": 1,
                    },
                    "result_code": "success",
                }
                expected_res["data"]["details"] = sorted(expected_res["data"]["details"], key=lambda x: x['recipient'])
                response["data"]["details"] = sorted(response["data"]["details"], key=lambda x: x['recipient'])
                assert_equal(expected_res, response)

    push_sms_cn_keys1 = "case_name,user_key,content,category,host_key,data_key"
    push_sms_cn_cases1 = [
        ("正案例_TOC根据recipient发送短信", "recipient", "content", "notification", "app_in", "nmp_app"),
    ]
    push_sms_cn_ids1 = [f"{case[0]}" for case in push_sms_cn_cases1]

    @pytest.mark.parametrize(push_sms_cn_keys1, push_sms_cn_cases1, ids=push_sms_cn_ids1)
    def test_push_sms_cn_der(self, env, cmdopt, mysql, redis, case_name, user_key, content, category, host_key, data_key, ):
        if cmdopt in skip_env_list:
            logger.debug(f"该测试案例不适用【{cmdopt}】环境")
            return 0
        # recipients = env['push_sms']['recipient']
        recipients = "+8617610551933"
        # recipients = "+4795861510"
        # recipients = "+85267469067"
        inputs = {
            "host": env['host'][host_key],
            "path": cn_sms_direct_push_path,
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "params": {
                "region": "cn",
                "lang": "zh-cn",
                "hash_type": "sha256",
                "app_id": app_id,
                "sign": ""
            },
            "json": {
                "recipients": recipients,
                "content": "NIO text messages to test if any bother please forgive me, Best wishes for you",
                "category": category,
            }
        }
        if not content:
            inputs.get("json").pop("content")
        if not category:
            inputs.get("json").pop("category")
        response = hreq.request(env, inputs)
        with allure.step(f"【{cmdopt}】环境,清理{app_id}频率限制"):
            if "test" in cmdopt:
                redis["app_message"].delete(f"rate.limiting:cn/sms_push_{app_id}")
        if case_name.startswith("正案例"):
            assert response['result_code'] == 'success'
            message_id = response['data']['message_id']
            sms_history = mysql[data_key].fetch("sms_history", {"message_id": message_id}, ["recipient"])
            assert str(sms_history[0]['recipient']) == str(f"{recipients}")
            sms_history_info = mysql[data_key].fetch("sms_history_meta_info", {"message_id": message_id}, )
            assert len(sms_history_info) == 1


def user_exist_uds(env, ):
    recipient = "17610551933"
    # app_id = 10001
    app_id = 10022
    host = env["host"]["uds_in"]
    inputs = {
        "host": host,
        "path": "/uds/in/user/v2/users",
        "method": "GET",
        "params": {
            "hash_type": "sha256",
            "app_id": app_id,
            # "mobile": recipient,
            # "user_id": "937727",
            "account_ids": "124525756",
            "sign": ""
        }
    }
    response = hreq.request(env, inputs)
    assert response['result_code'] == 'success'
