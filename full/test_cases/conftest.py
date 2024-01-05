"""
@Author: wenlong.jin
@File: conftest.py
@Project: full
@Time: 2023/10/25 15:27
"""
# !/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os
import time

import pytest
import requests
import yaml

from common.log import log
from config.settings import BASE_DIR, PLC_URL, BMS_URL, ACDC_URL, ACDC_CLOSE_URL, PDU_URL, PDU_KILL_URL, \
    PLC_KILL_URL, BMS_CLOSE_URL, ACDC_KILL_URL, AEC_KILL_URL, PROXIES


def pytest_addoption(parser):
    """

    :param parser:
    :return:
    """
    parser.addoption("--env", action="store", default="dev", help="environment: dev ,stg")
    parser.addoption("--mod", action="store", default="charge", help="module: charge ,swap ,aec")


@pytest.fixture(scope="session", autouse=False)
def envopt(request):
    """

    :param request:
    :return:
    """
    return request.config.getoption("--env")


@pytest.fixture(scope="session", autouse=False)
def modopt(request):
    """

    :param request:
    :return:
    """
    return request.config.getoption("--mod")


@pytest.fixture(scope="session", autouse=False)
def config(request, envopt, modopt):
    """
    Parse env config info
    :param request:
    :param envopt:
    :param modopt:
    :return: 返回环境
    """
    config_path = f'{request.config.rootdir}/config/{envopt}/{envopt}_config.yml'
    with open(config_path, mode="r", encoding="utf-8") as f:
        env_config = yaml.load(f, Loader=yaml.FullLoader)
    return env_config


@pytest.fixture(scope="session", autouse=False)
def init_ps20(request, envopt, modopt):
    """
    init ps20 pdu
    :param request:
    :param envopt:
    :param modopt:
    :return: 返回环境
    """
    pass
    requests.get(AEC_KILL_URL)
    requests.get(ACDC_KILL_URL)
    for branch in range(10, 20):
        requests.get(BMS_CLOSE_URL.format(branch))
        time.sleep(1)
    requests.get(PLC_KILL_URL)
    # time.sleep(1)
    # requests.get(ACDC_KILL_URL)
    time.sleep(10)
    requests.get(PDU_KILL_URL)
    time.sleep(5)
    file_name = "init_pdu.json"
    config_path = f'{request.config.rootdir}/data/{modopt}/init/{file_name}'
    pdu = {}
    with open(config_path, mode="r", encoding="utf-8") as f:
        if file_name.endswith("json"):
            pdu = json.load(f)
        elif file_name.endswith("yml"):
            pdu = yaml.load(f, Loader=yaml.FullLoader)
    requests.post(PDU_URL, json=pdu, proxies=PROXIES)


def read_charge_yaml(module="charge"):
    """

    :return:
    """
    dev_charge_list = os.path.join(BASE_DIR, "config", "dev", "dev_config.yml")
    with open(dev_charge_list, mode="r", encoding="utf-8") as f:
        env_yml_config = yaml.load(f, Loader=yaml.FullLoader)
        return env_yml_config[module]


def init_branch_charge(charge, branch, res):
    """

    :param charge:
    :param branch:
    :param res:
    :return:
    """
    log.info(f"[INIT_CHARGE][BMS{branch}]发送关闭ACDC数据")
    requests.get(ACDC_CLOSE_URL.format(int(charge["branch"]) - 10))
    log.info(f"[INIT_CHARGE][BMS{branch}]发送关闭BMS数据")
    requests.get(url=BMS_CLOSE_URL.format(int(charge["branch"])))
    time.sleep(5)
    log.info(f"[INIT_CHARGE][BMS{branch}]发送充电PLC数据")
    requests.post(url=PLC_URL, json=charge["plc"], proxies=PROXIES)
    time.sleep(15)
    res[branch]["start_time"] = int(time.time() * 1000)
    log.info(f"[INIT_CHARGE][BMS{branch}]发送充电BMS数据")
    requests.post(url=BMS_URL, json=charge["bms"], proxies=PROXIES)
    time.sleep(20)
    log.info(f"[INIT_CHARGE][BMS{branch}]发送充电PDU数据")
    requests.post(PDU_URL, json=charge["pdu"], proxies=PROXIES)
    addr_start = (int(charge["branch"]) - 10) * 3
    for i in range(3):
        addr = addr_start + i
        log.info(f"[INIT_CHARGE][BMS{branch}]发送充电ACDC{addr}数据")
        requests.post(url=ACDC_URL, json=charge[f"acdc{addr}"], proxies=PROXIES)
        time.sleep(1)
    time.sleep(10)


@pytest.fixture(scope="session", autouse=False)
def charge_start(request, config, modopt, init_ps20):
    """

    :param request:
    :param config:
    :param modopt:
    :param init_ps20:
    :return:
    """
    params = read_charge_yaml("charge")
    res = {}
    for param in params:
        branch = param.get("branch")
        charge = {"branch": branch}
        res[branch] = {}
        config_files = param.get("file")
        for module, file_name in config_files.items():
            config_path = f'{request.config.rootdir}/data/{modopt}/{file_name}'
            with open(config_path, mode="r", encoding="utf-8") as f:
                if file_name.endswith("json"):
                    charge[module] = json.load(f)
                elif file_name.endswith("yml"):
                    charge[module] = yaml.load(f, Loader=yaml.FullLoader)
        log.info(f"[INIT_CHARGE][BMS{branch}]BEGIN")
        init_branch_charge(charge, param.get("branch"), res)
        log.info(f"[INIT_CHARGE][BMS{branch}]END")
    log.info(f"[INIT_CHARGE][RES]{res}")
    time.sleep(30)
    return res


@pytest.fixture(scope="session", autouse=False)
def flexible_charge_start(request, config, modopt, init_ps20):
    """

    :param request:
    :param config:
    :param modopt:
    :param init_ps20:
    :return:
    """
    params = read_charge_yaml("flexible_charge")
    res = {}
    for param in params:
        branch = param.get("branch")
        charge = {"branch": branch}
        res[branch] = {}
        config_files = param.get("file")
        for module, file_name in config_files.items():
            config_path = f'{request.config.rootdir}/data/{modopt}/{file_name}'
            with open(config_path, mode="r", encoding="utf-8") as f:
                if file_name.endswith("json"):
                    charge[module] = json.load(f)
                elif file_name.endswith("yml"):
                    charge[module] = yaml.load(f, Loader=yaml.FullLoader)
    log.info(f"[INIT_CHARGE][RES]{res}")
    time.sleep(30)
    return res


@pytest.fixture(params=read_charge_yaml("flexible_charge"), scope="class", autouse=False)
def flexible_charge(request, config, modopt):
    """

    :param request:
    :param config:
    :param modopt:
    :return: 返回modopt测试需要的数据
    """
    param = request.param
    charge_info = {"station": config["station"], "branch": param["branch"]}
    config_files = param.get("file")
    for module, file_name in config_files.items():
        config_path = f'{request.config.rootdir}/data/{modopt}/{file_name}'
        with open(config_path, mode="r", encoding="utf-8") as f:
            if file_name.endswith("json"):
                charge_info[module] = json.load(f)
            elif file_name.endswith("yml"):
                charge_info[module] = yaml.load(f, Loader=yaml.FullLoader)
    return charge_info


@pytest.fixture(params=read_charge_yaml("charge"), scope="class", autouse=False)
def charge(request, config, modopt):
    """

    :param request:
    :param config:
    :param modopt:
    :return: 返回modopt测试需要的数据
    """
    param = request.param
    charge_info = {"station": config["station"], "branch": param["branch"]}
    config_files = param.get("file")
    for module, file_name in config_files.items():
        config_path = f'{request.config.rootdir}/data/{modopt}/{file_name}'
        with open(config_path, mode="r", encoding="utf-8") as f:
            if file_name.endswith("json"):
                charge_info[module] = json.load(f)
            elif file_name.endswith("yml"):
                charge_info[module] = yaml.load(f, Loader=yaml.FullLoader)
    return charge_info
