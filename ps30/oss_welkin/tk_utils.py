# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @project: PyCharm
# @Author: wenlong.jin
# @Time: 2023/1/28 16:21
# @File: tk_utils.py
import time
import traceback

import requests

from utils.log import log


def get_tk_data_real_time(resource_id, target_key):
    """

    :param resource_id:
    :param target_key:
    :return:
    """
    res = {
        "key": target_key,
        "type": -1,
        'value': -1
    }
    url = r"https://api-welkin-backend-stg.nioint.com/core/realtime/v1/PUS3/" \
          "{resource_id}?data_id={data_id}&start_time={start_time}&end_time={end_time}"
    # url = r"https://api-welkin-backend-stg.nioint.com/diagnosis/v1/realtime/PUS3/" \
    #       "{resource_id}?data_id={data_id}&start_time={start_time}&end_time={end_time}"
    end_time = int(round(time.time() * 1000))
    start_time = end_time - 10 * 1000  # 查询过去10s 数据
    url = url.format(resource_id=resource_id, data_id=target_key, start_time=start_time, end_time=end_time)
    try:
        response = requests.get(url=url)
        data = response.json().get('data')
    except Exception as e:
        res['message'] = {
            'url': url,
            'error': traceback.format_exc(),
            'desc': '<OSS>:GET welkin request happen error!!!'
        }
        log.error(res['message'])
        return res

    def sort_map(elem):
        return int(elem["timestamp"])

    values = data.get(target_key) if data else {}
    if values and values.get("data"):
        values["data"].sort(key=sort_map, reverse=True)
        if values["type"] == "float":
            res["type"] = 4  # 2 为int32 目前返回只有2种
            res["value"] = float(values["data"][0]["value"])
        else:
            res["type"] = 2
            res["value"] = values["data"][0]["value"]
    return res


if __name__ == '__main__':
    pass
    # print(get_tk_data_real_time(resource_id="PS-NIO-ad1100b5-98123ce6", target_key="100768"))
    # print(get_tk_data_real_time(resource_id="PS-NIO-ad1100b5-98123ce6", target_key="100769"))
    print(get_tk_data_real_time(resource_id="PS-NIO-ad1100b5-98123ce6", target_key="722670"))
    # print(get_tk_data_real_time(resource_id="PS-NIO-35014021-268699c2", target_key="100032"))
