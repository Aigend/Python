"""
@Author: wenlong.jin
@File: py_cv.py
@Project: aec-test
@Time: 2023/8/29 09:51
"""
# !/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2
# -*- coding: utf-8 -*-

import numpy as np
import urllib
import cv2

# import requests
# from requests.auth import HTTPDigestAuth
#
# url = 'http://admin:wynfee.huang123@192.168.1.213:80/ISAPI/Streaming/Channels/101/picture'
# resp = requests.get(url, auth=HTTPDigestAuth('admin', 'wynfee.huang123'))
# with open("../source/img_car.jpg", "wb") as f:
#     f.write(resp.content)

# url = 'http://admin:wynfee.huang123@192.168.1.10:5000/ISAPI/Streaming/Channels/101/picture'
# resp = requests.get(url)
# img = cv2.imread('img.jpg')
# '.jpg'表示把当前图片img按照jpg格式编码，按照不同格式编码的结果不一样
# img_encode = cv2.imencode('.jpg', img)[1]
# print(type(cv2.imencode('.jpg', img)[1]))
#
# data_encode = np.array(img_encode)
# str_encode = data_encode.tobytes()
#
# image = np.asarray(bytearray(str_encode), dtype="uint8")
# image = cv2.imdecode(image, cv2.IMREAD_COLOR)
# cv2.imshow('img_decode', image)
# cv2.waitKey()

# with open("../source/img_car.jpg", "rb") as f:
#     image_data = f.read()
#     print(len(image_data))
#     print(type(image_data))