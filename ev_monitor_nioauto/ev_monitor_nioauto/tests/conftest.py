#!/usr/bin/env python
# coding=utf-8
import copy
import importlib
import os
import pathlib
import sys
import tarfile
import time
import pytest

from utils.db import DB
from utils.logger import logger
from utils.commonlib import show_json
from utils.mqtt_client import MqttClient
import yaml
from utils.checker import Checker
from nio_messages.nextev_msg import extend_nextev_message_header
import allure


def pytest_addoption(parser):
    # hermes  odx_server rvs_server slythrein tsp_message_api tsp_patron
    parser.addoption("--env", action="store", default="test", help="environment: dev ,test ,stg or test_marcopolo")
    parser.addoption("--bvt", action="store_true", default=False, help="run bvt tests")
    # parser.addoption("--env", action="store", default="dev", help="environment: dev ,test ,stg or test_marcopolo")
    # parser.addoption("--env", action="store", default="test_marcopolo",
    #                  help="environment: dev ,test ,stg or test_marcopolo")


@pytest.fixture(scope="session", autouse=False)
def cmdopt(request):
    return request.config.getoption("--env")


@pytest.fixture(scope="session", autouse=False)
def only_bvt(request):
    return request.config.getoption("--bvt")


@pytest.fixture(scope="session", autouse=False)
def redis_key_front(cmdopt):
    # 支持马克波罗服务测试,支持staging环境
    redis_key_front = {}
    redis_data_types = ['remote_vehicle', 'data_collection']
    for redis_data_type in redis_data_types:
        if redis_data_type == 'remote_vehicle':
            cmdopt = 'staging' if cmdopt.startswith('st') else cmdopt
        else:
            cmdopt = 'stg' if cmdopt.startswith('st') else cmdopt
        redis_key_front[redis_data_type] = f'mp_{redis_data_type}_{cmdopt.split("_")[0]}' if 'marcopolo' in cmdopt \
            else f'{redis_data_type}_{cmdopt}'
    return redis_key_front


@pytest.fixture(scope="session", autouse=False)
def env(request, cmdopt, only_bvt):
    """
    Parse env config info
    :param request:
    :param cmdopt:
    :return: 返回环境
    """
    if only_bvt:
        config_path = f'{request.config.rootdir}/config/{cmdopt}/{cmdopt}_bvt_config.yml'
    else:

        config_path = f'{request.config.rootdir}/config/{cmdopt}/{cmdopt}_config.yml'
    with open(config_path, mode="r", encoding="utf-8") as f:
        env_config = yaml.load(f, Loader=yaml.FullLoader)
        # env_config['vehicles']['normal']=env_config['vehicles']['future']
    return env_config


@pytest.fixture(scope="session", autouse=False)
def api(request, cmdopt):
    config_path = '{0}/config/api.yml'.format(request.config.rootdir, cmdopt)
    with open(config_path, mode="r", encoding="utf-8") as f:
        return yaml.load(f, Loader=yaml.FullLoader)


@pytest.fixture(scope="session", autouse=False)
def mysql(cmdopt):
    return DB(cmdopt).mysql


@pytest.fixture(scope='session', autouse=False)
def mongodb(cmdopt):
    return DB(cmdopt).mongodb


@pytest.fixture(scope="session", autouse=False)
def cassandra(cmdopt):
    return DB(cmdopt).cassandra


@pytest.fixture(scope="session", autouse=False)
def redis(cmdopt):
    return DB(cmdopt).redis


@pytest.fixture(scope="session", autouse=False)
def kafka(cmdopt):
    return DB(cmdopt).kafka


@pytest.fixture(scope="session", autouse=False)
def s3(cmdopt):
    return DB(cmdopt).s3


@pytest.fixture(scope="session", autouse=False)
def tsp_agent(env, request, cmdopt):
    """
    实例化mqtt_client，生成对象在test引用
    :param env:
    :param request:
    :param cmdopt:
    :return:
    """
    client_id = env['vehicles']['normal']['client_id']
    cert_path = '{0}/config/{1}/{2}/'.format(request.config.rootdir, cmdopt, client_id)
    client = MqttClient(client_id,
                        cert_path + "ca/tls_tsp_trustchain.pem",
                        cert_path + "client/tls_lion_cert.pem",
                        cert_path + "client/tls_lion_priv_key.pem")

    client.connect(env['message']['host'], env['message']['port'])
    client.loop_start()

    def fin():
        client.loop_stop()
        client.disconnect()

    request.addfinalizer(fin)

    return client


@pytest.fixture(scope="function", autouse=False)
def tsp_agent_once(env, request, cmdopt, tag):
    """
    实例化mqtt_client，生成对象在test引用
    :param tag:
    :param env:
    :param request:
    :param cmdopt:
    :return:
    """
    client_id = env['vehicles'][tag]['client_id']
    cert_path = '{0}/config/{1}/{2}/'.format(request.config.rootdir, cmdopt, client_id)
    client = MqttClient(client_id,
                        cert_path + "ca/tls_tsp_trustchain.pem",
                        cert_path + "client/tls_lion_cert.pem",
                        cert_path + "client/tls_lion_priv_key.pem")

    client.connect(env['message']['host'], env['message']['port'])
    client.loop_start()

    def fin():
        client.loop_stop()
        client.disconnect()

    request.addfinalizer(fin)

    return client


@pytest.fixture(scope="session", autouse=False)
def tsp_agent_cdc(env, request, cmdopt):
    """
    实例化mqtt_client模拟cdc，生成对象在test引用
    :param env:
    :param request:
    :param cmdopt:
    :return:
    """
    client_id = env['vehicles']['normal']['cdc_client_id']
    cert_path = '{0}/config/{1}/{2}/'.format(request.config.rootdir, cmdopt, env['vehicles']['normal']['client_id'])
    client = MqttClient(client_id,
                        cert_path + "ca/tls_tsp_trustchain.pem",
                        cert_path + "client/tls_airbender_cert.pem",
                        cert_path + "client/tls_airbender_priv_key.pem")

    client.connect(env['message']['host_public'], env['message']['port_public'])
    client.loop_start()

    def fin():
        client.loop_stop()
        client.disconnect()

    request.addfinalizer(fin)

    return client


@pytest.fixture(scope="session", autouse=False)
def tsp_agent_for_sample(env, request, cmdopt):
    """
    实例化mqtt_client，生成对象在test引用
    :param env:
    :param request:
    :param cmdopt:
    :return:
    """
    client_id = env['vehicles']['vehicle_for_sample']['client_id']
    cert_path = '{0}/config/{1}/{2}/'.format(request.config.rootdir, cmdopt, client_id)
    client = MqttClient(client_id,
                        cert_path + "ca/tls_tsp_trustchain.pem",
                        cert_path + "client/tls_lion_cert.pem",
                        cert_path + "client/tls_lion_priv_key.pem")

    client.connect(env['message']['host'], env['message']['port'])

    def fin():
        client.disconnect()

    request.addfinalizer(fin)

    return client


@pytest.fixture(scope="function", autouse=False)
def publish_msg(env, tsp_agent, cmdopt, vin, vid):
    def _publish_msg(event_name, tsp_agent=tsp_agent, vin=vin, vid=vid, sleep_time=2, *args, **kwargs):
        module = importlib.import_module('nio_messages.' + event_name, ".")
        gen_function = getattr(module, "generate_message")
        args_list = gen_function.__code__.co_varnames
        kw = {}
        for k in list(kwargs.keys()):
            if k not in args_list:
                kw[k] = kwargs.pop(k)

        with allure.step("用mqtt上报 {0} 事件".format(event_name)):
            nextev_message, obj = gen_function(vin, vid, *args, **kwargs)
            if kw:
                nextev_message = extend_nextev_message_header(nextev_message, **kw)
            allure.attach(show_json(obj), "事件内容")
            tsp_agent.publish(bytearray(nextev_message))

        logger.debug("Generated {} message and publish by mqtt:\n{}".format(event_name, show_json(obj)))

        time.sleep(sleep_time)

        return nextev_message, obj

    return _publish_msg


@pytest.fixture(scope="function", autouse=False)
def publish_msg_cdc(env, tsp_agent_cdc, cmdopt, vin, vid):
    def _publish_msg(event_name, sleep_time=2, *args, **kwargs):
        module = importlib.import_module('nio_messages.' + event_name, ".")
        gen_function = getattr(module, "generate_message")

        with allure.step("用mqtt上报 {0} 事件".format(event_name)):
            nextev_message, obj = gen_function(vin, vid, *args, **kwargs)
            allure.attach(show_json(obj), "事件内容")
            tsp_agent_cdc.publish(bytearray(nextev_message))

        logger.debug("Generated {} message and publish by mqtt:\n{}".format(event_name, show_json(obj)))

        time.sleep(sleep_time)

        return nextev_message, obj

    return _publish_msg


@pytest.fixture(scope="function", autouse=False)
def publish_msg_by_kafka(env, cmdopt, kafka, vid, vin):
    def _publish_msg(event_name, vin=vin, vid=vid, sleep_time=2, *args, **kwargs):
        """
        当用消息平台上报时，accound_id所对应的vid不重要，tsp会通过证书自动填写对应的vid，但是通过kafka上报时，vid必须填写正确
        """
        module = importlib.import_module('nio_messages.' + event_name, ".")  # 动态导入模块
        gen_function = getattr(module, "generate_message")  # getattr返回一个对象属性值。这里用来返回generate_message方法
        args_list = gen_function.__code__.co_varnames
        kw = {}
        for k in list(kwargs.keys()):
            if k not in args_list:
                kw[k] = kwargs.pop(k)

        with allure.step("用kafka上报 {} 事件".format(event_name)):
            nextev_message, obj = gen_function(vin, vid, *args, **kwargs)  # nextev代表蔚来汽车
            if kw:
                nextev_message = extend_nextev_message_header(nextev_message, **kw)
            allure.attach(show_json(obj), "事件内容")
            if "periodical" in event_name:
                kafka['cvs'].produce(kafka['topics']['data_report_periodical'], nextev_message)
            else:
                kafka['cvs'].produce(kafka['topics']['data_report'], nextev_message)

        logger.debug("Generated {} message and publish by kafka:\n{}".format(event_name, show_json(obj)))

        time.sleep(sleep_time)

        return nextev_message, obj

    return _publish_msg


@pytest.fixture(scope="function", autouse=False)
def publish_msg_by_kafka_adas(env, cmdopt, kafka, vid, vin):
    def _publish_msg(event_name, vin=vin, vid=vid, sleep_time=2, *args, **kwargs):
        """
        当用消息平台上报时，accound_id所对应的vid不重要，tsp会通过证书自动填写对应的vid，但是通过kafka上报时，vid必须填写正确
        """
        module = importlib.import_module('nio_messages.' + event_name, ".")
        gen_function = getattr(module, "generate_message")
        args_list = gen_function.__code__.co_varnames
        kw = {}
        for k in list(kwargs.keys()):
            if k not in args_list:
                kw[k] = kwargs.pop(k)

        with allure.step("用kafka上报 {} 事件".format(event_name)):
            nextev_message, obj = gen_function(vin, vid, *args, **kwargs)
            allure.attach(show_json(obj), "事件内容")
            if kw:
                nextev_message = extend_nextev_message_header(nextev_message, **kw)
                kafka['cvs'].produce(kafka['topics']['data_report_adc'], nextev_message)
            else:
                kafka['adas'].produce(kafka['topics']['data_report_10107'], nextev_message)

        logger.debug("Generated {} message and publish by kafka:\n{}".format(event_name, show_json(obj)))

        time.sleep(sleep_time)

        return nextev_message, obj

    return _publish_msg


@pytest.fixture(scope="session", autouse=False)
def vid(env):
    return env['vehicles']['normal']['vehicle_id']


@pytest.fixture(scope="session", autouse=False)
def vin(env):
    return env['vehicles']['normal']['vin']


@pytest.fixture(scope="session", autouse=False)
def account_id(env):
    return env['vehicles']['normal']['account_id']


@pytest.fixture(scope="session", autouse=False)
def checker(vid, vin, cmdopt, redis_key_front, env, api, request):
    checker = Checker(vid=vid,
                      vin=vin,
                      cmdopt=cmdopt,
                      redis_key_front=redis_key_front,
                      env=env,
                      api=api
                      )
    return checker


def pytest_collection_modifyitems(items):
    """
    show unicode name and nodeid for item
    :return:
    """
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode_escape")
        item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")
