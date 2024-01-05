"""
@Author: wenlong.jin
@File: analyze.py
@Project: aec-test
@Time: 2023/7/20 10:18
"""
# !/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import argparse
import json
import time

import requests

"""
    用于分析pange下发的数据类型：
    1. tag触发
    2. 定时触发
    3. 手动触发
"""

# aec_3 = [{"test_case_id": "Test_Single_Algorith_001", "test_count": "3"},
#          {"test_case_id": "Test_Single_Algorith_002", "test_count": "3"},
#          {"test_case_id": "Test_Single_Algorith_004", "test_count": "3"},
#          {"test_case_id": "Test_Single_Algorith_005", "test_count": "3"}, ]

aec_3 = [{"test_case_id": "Test_Single_Algorith_001", "test_count": "100"},
         {"test_case_id": "Test_Single_Algorith_002", "test_count": "100"},
         {"test_case_id": "Test_Single_Algorith_004", "test_count": "100"},
         {"test_case_id": "Test_Single_Algorith_005", "test_count": "100"},
         {"test_case_id": "Test_Single_Algorith_006", "test_count": "100"},
         {"test_case_id": "Test_Single_Algorith_013", "test_count": "100"},
         {"test_case_id": "Test_Single_Algorith_015", "test_count": "100"},
         {"test_case_id": "Test_Single_Algorith_017", "test_count": "100"},
         {"test_case_id": "Test_Single_Algorith_020", "test_count": "100"},
         {"test_case_id": "Test_Multiple_Algorith_001", "test_count": "100"},
         # {"test_case_id": "Test_Multiple_Algorith_002", "test_count": "100"},
         {"test_case_id": "Test_Normal_SwapBattery_001", "test_count": "100"},
         # {"test_case_id": "Test_Random_Algorith_001", "test_count": "100"}
         ]

aec_2 = [{"test_case_id": "Test_Single_Algorith_001", "test_count": "100"},
         {"test_case_id": "Test_Single_Algorith_002", "test_count": "100"},
         {"test_case_id": "Test_Single_Algorith_003", "test_count": "100"},
         {"test_case_id": "Test_Single_Algorith_004", "test_count": "100"},
         {"test_case_id": "Test_Single_Algorith_005", "test_count": "100"},
         {"test_case_id": "Test_Single_Algorith_006", "test_count": "100"},
         {"test_case_id": "Test_Single_Algorith_007", "test_count": "100"},
         {"test_case_id": "Test_Single_Algorith_008", "test_count": "100"},
         {"test_case_id": "Test_Single_Algorith_013", "test_count": "100"},
         {"test_case_id": "Test_Single_Algorith_014", "test_count": "100"},
         {"test_case_id": "Test_Single_Algorith_015", "test_count": "100"},
         {"test_case_id": "Test_Single_Algorith_016", "test_count": "100"},
         {"test_case_id": "Test_Single_Algorith_017", "test_count": "100"},
         {"test_case_id": "Test_Single_Algorith_018", "test_count": "100"},
         {"test_case_id": "Test_Single_Algorith_019", "test_count": "100"},
         {"test_case_id": "Test_Single_Algorith_020", "test_count": "100"},
         {"test_case_id": "Test_Normal_SwapBattery_001", "test_count": "100"}]

aec_3_git_url = "git@git.nevint.com:PERD/PowerSwap/powerswap_3.0/aec/023012.git"
aec_2_git_url = "git@git.nevint.com:PERD/PowerSwap/PowerSwap_2.0/ai/cppaec.git"

time_resource = {
    "git_url": aec_3_git_url,
    "site": "time",
    "test_details": aec_3,
}

resource = {"test_id": "",
            "version": "",
            "aec_version": {"version": 3},
            "test_detail": []}

time_url = "https://pangea.nioint.com/pangea/v1/jenkins/sub-system/test"

path = "./resource.json"

result_url = "https://pangea.nioint.com/pangea/v1/sub-system/finish/recall"


def parser_data_args():
    data = os.environ.get("data")
    aec_ver = int(os.environ.get("version", "3"))
    # data = None
    # aec_ver = 2
    if not data:
        # Jenkins定时触发
        if aec_ver == 2:
            time_resource["git_url"] = aec_2_git_url
            time_resource["test_details"] = aec_2
        res = requests.post(url=time_url, json=time_resource)
        res = json.loads(res.content.decode())
        if res["err_code"] != 0:
            print(f"request new tag version error, {res}")
            sys.exit(2)
        resource["test_id"] = res['data'].get("test_id")
        resource["version"] = res['data'].get("file_url")
        resource["aec_version"]["version"] = aec_ver
        resource["test_detail"] = aec_2 if aec_ver == 2 else aec_3
        with open(path, "w+") as f:
            json.dump(resource, f)
        print(res['data'].get("file_url"))
    else:
        # 盘古手动选择用例触发
        obj = json.loads(data)
        if obj.get("test_detail"):
            with open(path, "w+") as f:
                json.dump(obj, f)
            version = obj.get("version")
            if version:
                print(version)  # 打印下载的url
                sys.exit(0)
            print(f"not get version from Jenkins data")
            sys.exit(2)
        else:
            # tag 触发
            pass


def send_pangea_result():
    if not os.path.exists(path):
        return
    try:
        with open(path, 'r') as fp:
            _resource = json.load(fp)
            test_id = _resource["test_id"]
            for case_info in _resource["test_detail"]:
                data = {"test_id": test_id,
                        "test_case_id": case_info["test_case_id"],
                        "success": 0,
                        "failure": case_info["test_count"],
                        "detail": "AEC刷版本失败"}
                response = requests.post(result_url, json=data)
                if response.status_code != 200:
                    print(f"<MCS>:post pangea response error, status_code:{response.status_code}, reason:{response.reason}")
                time.sleep(1)
    except Exception as e:
        print(f"<MCS>:post pangea result data happen error, {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser("define execute function name")
    parser.add_argument('--func', default="parser_data_args", help='parse data args')
    args = parser.parse_args()
    eval(args.func)()