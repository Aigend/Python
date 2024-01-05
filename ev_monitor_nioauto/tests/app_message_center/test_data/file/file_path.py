# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : file_path.py
# @Author : qiangwei.zhang
# @time: 2021/08/18
# @api: GET_/api/XXX 【必填】
# @showdoc:
# @Description :脚本描述

from config.settings import BASE_DIR

pdf_path = f"{BASE_DIR}/tests/app_message_center/test_data/file/Linux.pdf"
apk_path = f"{BASE_DIR}/tests/app_message_center/test_data/file/nio_app_mp_dev_release_v1.0.3_ab3440bb_278.apk"
pptx_path = f"{BASE_DIR}/tests/app_message_center/test_data/file/巧用Soar+perfmance_schem发现和治理sql .pptx"
png_path = f"{BASE_DIR}/tests/app_message_center/test_data/file/提测GIT流程.png"
# xlsx_path = f"{BASE_DIR}/tests/app_message_center/test_data/file/2022-05-10故障统计数据对比故障统计数据对比故障统计数据对比故障统计数据对比故障统计数据对比故障统计数据对比.xlsx"
xlsx_path = f"{BASE_DIR}/tests/app_message_center/test_data/file/2022-05-10二手车收车待付款信息.xlsx"
# xlsx_path = f"{BASE_DIR}/tests/app_message_center/test_data/file/2022-05-10二手车收车待付款信息.xlsx"
doc_path = f"{BASE_DIR}/tests/app_message_center/test_data/file/简历模板.doc"
pdf_path_1 = f"{BASE_DIR}/tests/app_message_center/test_data/file/附件1-着陆计划邀请函 Attachment 1 -Landing Project Invitation.pdf"
zip_path = f"{BASE_DIR}/tests/app_message_center/test_data/file/测试压缩文件.zip"

# 部分文件较大未上传到git,放在本地
# pdf_path, apk_path, pptx_path, png_path, xlsx_path, doc_path, pdf_path_1, zip_path

file_path_map = {
    "pdf_path": pdf_path,
    "apk_path": apk_path,
    "pptx_path": pptx_path,
    "png_path": png_path,
    "xlsx_path": xlsx_path,
    "doc_path": doc_path,
    "pdf_path_1": pdf_path_1,
    "zip_path": zip_path,
}
