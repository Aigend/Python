#!/usr/bin/env python
# coding=utf-8

"""
:file: commonlib.py
:author: chunming.liu
:contact: Chunming.liu@nextev.com
:Date: Created on 2016/10/19 下午5:15
:Description: 
"""
import codecs
import json
import os
import copy
import pprint, yaml, allure
from utils.logger import logger


def show_json(json_obj):
    obj = copy.deepcopy(json_obj)
    _convert_obj(obj)

    json_dump_str = json.dumps(obj, indent=2, ensure_ascii=False)
    return json_dump_str


def _convert_obj(obj):
    # Convert obj to make it can be json dumped. Now we just handle the bytes value
    if isinstance(obj, dict):

        for k,v in obj.items():
            if isinstance(v, bytes):
                obj[k] = codecs.encode(obj[k], 'hex').decode('ascii').upper()
            _convert_obj(v)

    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            if isinstance(item, bytes):
                obj[i] = codecs.encode(item, 'hex').decode('ascii').upper()
            _convert_obj(item)

    else:
        return obj


def print_obj(obj):
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(obj)


def load_json(path):
    content_dic = None
    try:
        with open(path, 'r') as f:
            content_dic = json.loads(f.read(), encoding='utf-8')
    except Exception as e:
        print('Failed to load json file ' + str(e))
    finally:
        return content_dic


def dump_json(path, content):
    if content:
        with open(path, 'w') as f:
            json.dump(content, f, ensure_ascii=False, indent=4)


def string_to_dict(str):
    try:
        str = str.strip().strip('&').split("&")
        return dict([iterm.split("=") for iterm in str])
    except Exception:
        return {}


def remove_items(d, keys):
    """
    删除字典d中的keys
    :param d: 字典
    :param keys: 待删除的key
    :return:
    """
    if isinstance(d, dict):
            for k in keys:
                if k in d:
                    del d[k]
    else:
        logger.debug("{0} is not dict type".format(d))


def dict_equal(src_data, dst_data):
    assert type(src_data) == type(dst_data), "type: '{}' != '{}'".format(type(src_data), type(dst_data))
    if isinstance(src_data, dict):
        assert len(src_data) == len(dst_data), "dict len: '{}' != '{}'".format(len(src_data), len(dst_data))
        for key in src_data:
            assert key in dst_data
            dict_equal(src_data[key], dst_data[key])
    elif isinstance(src_data, list):
        assert len(src_data) == len(dst_data), "list len: '{}' != '{}'".format(len(src_data), len(dst_data))
        for src_list, dst_list in zip(sorted(src_data), sorted(dst_data)):
            dict_equal(src_list, dst_list)
    else:
        assert src_data == dst_data, "value '{}' != '{}'".format(src_data, dst_data)


def dict_contain(src_data, dst_data):
    assert type(src_data) == type(dst_data), "type: '{}' != '{}'".format(type(src_data), type(dst_data))
    if isinstance(src_data, dict):
        for key in src_data:
            assert key in dst_data
            dict_contain(src_data[key], dst_data[key])
    elif isinstance(src_data, list):
        for src_list, dst_list in zip(sorted(src_data), sorted(dst_data)):
            dict_contain(src_list, dst_list)
    else:
        assert src_data == dst_data, "value '{}' != '{}'".format(src_data, dst_data)


def get_test_data(test_data_path):
    """
    Get test data from json
    :param test_data_path:
    :return: case name, precondition data , and test data
    """
    case = []
    start = []
    end = []
    expected = []
    with open(test_data_path) as f:
        dat = json.loads(f.read())
        test = dat['test']
        for td in test:
            case.append(td['case'])
            start.append(td['start'])
            end.append(td['end'])
            expected.append(td['expected'])
    list_parameters = zip(case, start, end, expected)
    return case, list_parameters


def get_test_data1(test_data_path=None, data_dict=None):
    """
    Get test data from json
    :param test_data_path:
    :return: case name, precondition data , and test data
    """
    case = []
    headers = []
    querystring = []
    payload = []
    expected = []

    if test_data_path:
        with open(test_data_path, encoding='utf-8') as f:
            dat = json.loads(f.read())
    elif data_dict:
        dat = data_dict
    else:
        raise Exception("Data was not prepared")

    test = dat['test']
    precondition = dat["precondition"]
    for td in test:
        case.append(td['case'])
        headers.append(td['headers'])
        querystring.append(td['querystring'])
        payload.append(td['payload'])
        expected.append((td['expected']))
    list_parameters = zip(case, headers, querystring, payload, expected)
    return case, precondition, list_parameters


