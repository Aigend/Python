# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : test_template_cdn_upload.py
# @Author : qiangwei.zhang
# @CreateTime : 2021/6/21 2:50 下午
# @Description :


import pytest
import allure
from utils.http_client import TSPRequest as hreq
from utils.logger import logger
from config.settings import BASE_DIR


@pytest.mark.parametrize("case_name,app_id,file_path", [
    ("正案例_图片", "10000", f"{BASE_DIR}/tests/app_message_portal/file_upload/img/ET7.jpeg"),
    # ("正案例_文件大小_4M", "10000", f"{BASE_DIR}/tests/app_message_portal/file_upload/img/ES8.jpeg"),
    # ("反案例_文件大小_等于5M", "10000", "img/5242880.jpeg"),
    # ("反案例_文件大小_等于8M", "10000", "img/8388608.jpeg"),
    # ("反案例_文件类型_非图片", "10000", "img/dtcQueryBatchTemplate1000.xls"),
])
def test_cdn_upload(env, cmdopt, case_name, app_id, file_path):
    """
    http://showdoc.nevint.com/index.php?s=/647&page_id=31184
    文件限制5M
    网关限制10M
    """
    region = "eu" if "marcopolo" in cmdopt else "cn"
    region = "cn"
    with allure.step("文件上传初始化接口"):
        inputs = {
            "host": env['host']['app_in'],
            "path": f"/api/2/in/message_portal/cdn/{region}/upload",
            "method": "POST",
            "params": {
                "app_id": app_id,
                "sign": "",
            },
            "files": {"file": open(file_path, "rb")},
        }
        response = hreq.request(env, inputs)
        logger.debug(f"response {response}")
        assert response['result_code'] == 'success'
        if region == "cn":
            if cmdopt == "stg":
                assert response.get("data").startswith(f"https://cdn-app.nio.com/user/")
            assert response.get("data").startswith(f"https://cdn-app-{cmdopt.split('_')[0]}.nio.com/account-center")
        else:
            assert response.get("data").startswith(f"https://cdn-app-{cmdopt.split('_')[0]}.eu.nio.com/mp")
