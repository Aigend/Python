#!/usr/bin/env python
# coding=utf-8
import copy
import importlib
import os
import tarfile
import time
import pytest

from utils.db import DB
from utils.logger import logger
from utils.commonlib import show_json
from utils.mqtt_client import MqttClient
import yaml
from utils.checker import Checker
import allure



@pytest.fixture(scope="session", autouse=False)
def cmdopt(request):
    # return request.config.getoption("--env")
    return 'prod'


@pytest.fixture(scope="session", autouse=False)
def env(request, cmdopt):
    """
    Parse env config info
    :param request:
    :param cmdopt:
    :return: 返回环境
    """
    config_path = '{0}/config/{1}/{1}_config.yml'.format(request.config.rootdir, cmdopt)
    with open(config_path) as f:
        env_config = yaml.load(f, Loader=yaml.FullLoader)
    return env_config


#
# @pytest.fixture(scope="session", autouse=False)
# def mysql(cmdopt):
#     return DB(cmdopt).mysql
#
#
# @pytest.fixture(scope='session', autouse=False)
# def mongodb(cmdopt):
#     return DB(cmdopt).mongodb
#
#
# @pytest.fixture(scope="session", autouse=False)
# def cassandra(cmdopt):
#     return DB(cmdopt).cassandra
#
#
# @pytest.fixture(scope="session", autouse=False)
# def redis(cmdopt):
#     return DB(cmdopt).redis
#

@pytest.fixture(scope="session", autouse=False)
def kafka(cmdopt):
    print('qc kafka')
    return DB(cmdopt).kafka


@pytest.fixture(scope="session", autouse=False)
def tsp_agent(env, request, cmdopt):
    """
    实例化mqtt_client，生成对象在test引用
    :param env:
    :param request:
    :param cmdopt:
    :return:
    """
    client_id = env['vehicles']['normal_qc']['client_id']
    cert_path = '{0}/config/{1}/{2}/'.format(request.config.rootdir, cmdopt, client_id)
    client = MqttClient(client_id,
                        cert_path + "ca/tls_tsp_trustchain.pem",
                        cert_path + "client/tls_lion_cert.pem",
                        cert_path + "client/tls_lion_priv_key.pem",
                        tls_insecure_set=True)

    client.connect(env['message']['host_qc'], env['message']['port_qc'])
    client.loop_start()

    def fin():
        client.loop_stop()
        client.disconnect()

    request.addfinalizer(fin)

    return client




@pytest.fixture(scope="function", autouse=False)
def publish_msg(env, tsp_agent, cmdopt,vin, vid):
    def _publish_msg(event_name, sleep_time=2, *args, **kwargs):
        module = importlib.import_module('nio_messages.' + event_name, ".")
        gen_function = getattr(module, "generate_message")

        with allure.step("用mqtt上报 {0} 事件".format(event_name)):
            nextev_message, obj = gen_function(vin, vid, *args, **kwargs)
            allure.attach(show_json(obj),"事件内容")
            tsp_agent.publish(bytearray(nextev_message))

        logger.debug("Generated {} message and publish by mqtt:\n{}".format(event_name, show_json(obj)))

        time.sleep(sleep_time)

        return nextev_message, obj

    return _publish_msg



@pytest.fixture(scope="session", autouse=False)
def vid(env):
    return env['vehicles']['normal_qc']['vehicle_id']


@pytest.fixture(scope="session", autouse=False)
def vin(env):
    return env['vehicles']['normal_qc']['vin']



def pytest_collection_modifyitems(items):
    """
    show unicode name and nodeid for item
    :return:
    """
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode_escape")
        item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")

