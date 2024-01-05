# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : img_path.py
# @Author : qiangwei.zhang
# @time: 2021/08/18
# @api: GET_/api/XXX 【必填】
# @showdoc:
# @Description :脚本描述
"""
CN环境支持
    CN上传文件
    CN短信发送
    CN飞书发送
    CN邮件发送
    notify
    notify_all
    employee邮件发送
EU环境支持
    EU上传文件
    EU短信发送
    employee邮件发送
    CN飞书发送
    EU邮件发送
    notify
    notify_all

"""

from config.settings import BASE_DIR

img_path_map = {
    "img_9_5M_path": f"{BASE_DIR}/tests/app_message_center/test_data/img/type/9.5M.jpg",
    "img_9M_path": f"{BASE_DIR}/tests/app_message_center/test_data/img/type/9M.jpg",
    "img_10M_path": f"{BASE_DIR}/tests/app_message_center/test_data/img/type/10M.jpg",
    "img_16M_path": f"{BASE_DIR}/tests/app_message_center/test_data/img/type/16M.jpg",
    "img_bmp_path": f"{BASE_DIR}/tests/app_message_center/test_data/img/type/bmp_picture.bmp",
    "img_4M_path": f"{BASE_DIR}/tests/app_message_center/test_data/img/type/EP9_4M.jpg",
    "img_jpeg_path": f"{BASE_DIR}/tests/app_message_center/test_data/img/type/ET7.jpeg",
    "img_25M_path": f"{BASE_DIR}/tests/app_message_center/test_data/img/type/ET7_25M.jpg",
    "img_gif_path": f"{BASE_DIR}/tests/app_message_center/test_data/img/type/gif_picture.gif",
    "img_png_path": f"{BASE_DIR}/tests/app_message_center/test_data/img/type/png_picture.png",
    "img_tiff_path": f"{BASE_DIR}/tests/app_message_center/test_data/img/type/tiff_picture.tiff",
    "img_webp_path": f"{BASE_DIR}/tests/app_message_center/test_data/img/type/webp_picture.webp",
    "not_img_path": f"{BASE_DIR}/tests/app_message_center/test_data/img/type/500.xls",
}
# img_9_5M_path,img_9M_path,img_10M_path,img_16M_path,img_bmp_path,img_4M_path,img_49K_path,img_25M_path,img_gif_path,img_png_path,img_tiff_path,img_webp_path
