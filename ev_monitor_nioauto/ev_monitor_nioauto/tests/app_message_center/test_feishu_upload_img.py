# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : test_feishu_upload_img.py
# @Author : qiangwei.zhang
# @CreateTime : 2021/7/15 5:38 下午
# @api:POST_/api/2/in/message/employee/feishu_upload
# @showdoc:http://showdoc.nevint.com/index.php?s=/647&page_id=31428
# @Description :
"""
    ❌接口文档:http://showdoc.nevint.com/index.php?s=/647&page_id=31428(需修改文件大小限制)
    path:
    测试案例：
    ✅* 图片大小：
        ✅小于9M(图片+接口请求内容)小于等于10M
        ❌(图片+接口请求内容)大于10M
            (test环境网关限制10M,eu-test环境网关限制128M)
    ✅* 图片类型：
        ✅* bmp
        ✅* tiff
        ✅* JPEG
        ✅* JPG
        ✅* webp
        ✅* Gif
        ✅* Png
    ✅* 非图片文件，不支持上传
    """

import random
import string
import pytest
import allure
from utils.http_client import TSPRequest as hreq
from utils.logger import logger
from tests.app_message_center.test_data.img.img_path import img_path_map


@pytest.mark.run(order=1)
class TestFeishuUploadFile(object):
    fei_shu_upload_keys = 'case_name,except_result, host_key, data_key, file_path'
    fei_shu_upload_cases = [
        # ('TOB_图片大小_9M', "success", 'app_tob_in', 'nmp_app_tob', img_path_map.get("img_9M_path")),
        # ('TOB_图片大小_10M', "invalid_param", 'app_tob_in', 'nmp_app_tob', img_path_map.get("img_10M_path")),
        # ('TOB_图片类型_bmp', "success", 'app_tob_in', 'nmp_app_tob', img_path_map.get("img_bmp_path")),
        # ('TOB_图片类型_png', "success", 'app_tob_in', 'nmp_app_tob', img_path_map.get("img_png_path")),
        # ('TOB_图片类型_jpg', "success", 'app_tob_in', 'nmp_app_tob', img_path_map.get("img_4M_path")),
        ('TOB_图片类型_jpeg', "success", 'app_tob_in', 'nmp_app_tob', img_path_map.get("img_jpeg_path")),
        # ('TOB_图片类型_gif', "success", 'app_tob_in', 'nmp_app_tob', img_path_map.get("img_gif_path")),
        # ('TOB_图片类型_webp', "success", 'app_tob_in', 'nmp_app_tob', img_path_map.get("img_webp_path")),
        # ('TOB_图片类型_tiff', "success", 'app_tob_in', 'nmp_app_tob', img_path_map.get("img_gif_path")),
        # ('TOB_非图片类型_xls', "invalid_param", 'app_tob_in', 'nmp_app_tob', img_path_map.get("not_img_path")),
        # -------------------------------分割线-------------------------------
        # ('TOC_图片大小_9M', "success", 'app_in', 'nmp_app', img_path_map.get("img_9M_path")),
        # ('TOC_图片大小_10M', "invalid_param", 'app_in', 'nmp_app', img_path_map.get("img_10M_path")),
        # ('TOC_图片类型_bmp', "success", 'app_in', 'nmp_app', img_path_map.get("img_bmp_path")),
        # ('TOC_图片类型_png', "success", 'app_in', 'nmp_app', img_path_map.get("img_png_path")),
        # ('TOC_图片类型_jpg', "success", 'app_in', 'nmp_app', img_path_map.get("img_4M_path")),
        ('TOC_图片类型_jpeg', "success", 'app_in', 'nmp_app', img_path_map.get("img_jpeg_path")),
        # ('TOC_图片类型_gif', "success", 'app_in', 'nmp_app', img_path_map.get("img_gif_path")),
        # ('TOC_图片类型_webp', "success", 'app_in', 'nmp_app', img_path_map.get("img_webp_path")),
        # ('TOC_图片类型_tiff', "success", 'app_in', 'nmp_app', img_path_map.get("img_gif_path")),
        # ('TOC_非图片类型_xls', "invalid_param", 'app_in', 'nmp_app', img_path_map.get("not_img_path")),
    ]
    ids = [f"{case[0]}" for case in fei_shu_upload_cases]

    @pytest.mark.parametrize(fei_shu_upload_keys, fei_shu_upload_cases, ids=ids)
    def test_fei_shu_upload(self, env, cmdopt, case_name, except_result, host_key, data_key, file_path):
        with allure.step(f"飞书图片上传接口{case_name}"):
            app_id = 10000
            inputs = {
                "host": env['host']['app_in'],
                "path": "/api/2/in/message/employee/feishu_upload",
                "method": "POST",
                "params": {
                    "app_id": app_id,
                    "sign": "",
                },
                "files": {"file": open(file_path, "rb")},
            }
            response = hreq.request(env, inputs)
            logger.debug(f"response {response}")
            assert response['result_code'] == except_result
            if except_result == "success":
                assert response['data']
