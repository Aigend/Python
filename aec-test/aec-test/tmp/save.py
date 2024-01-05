"""
@Author: wenlong.jin
@File: save.py
@Project: aec-test
@Time: 2023/8/23 17:57
"""
# !/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2

gstream_elemets = (
    'rtspsrc location=rtsp://admin:Pengming123@192.168.1.201:554/Streaming/Channels/101 latency=300 !' 'rtph264depay ! h264parse !'
    'omxh264dec !'
    'nvvidconv ! video/x-raw , format=(string)BGRx !' 'videoconvert ! '
    'appsink')

cap = cv2.VideoCapture(gstream_elemets, cv2.CAP_GSTREAMER)
if not cap.isOpened():
    print("capture failed")

w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
fps = cap.get(cv2.CAP_PROP_FPS)
print('Src opened, %dx%d @ %d fps' % (w, h, fps))
