"""uthor: wenlong.jin
@File: rtsp_pull.py
@Project: aec-test
@Time: 2023/8/9 14:39
"""
import multiprocessing

# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 拉取rtsp流
import cv2
import time
import traceback


def delay_time(rtsp_url):
    """
    获取拉取到第一帧数据的时间
    :return:
    """
    start_time = time.time()
    cap = cv2.VideoCapture(rtsp_url)
    if cap.isOpened():
        success, frame = cap.read()
        cost_time = time.time()-start_time
        print(f"拉取到第一帧数据用时：{cost_time}秒")
        return cost_time
    else:
        print("拉取流地址失败")


def pull_rtsp(rtsp_url, save_file="output", run_time=60):
    """
    拉取视频流
    :param run_time: 拉取的时长，单位秒。默认为60秒
    :param save_file: 保存的文件名不带尾缀，格式为avi,默认空时，不保存拉取 视频流
    :return:
    """
    videoWrite = False
    cap = cv2.VideoCapture(rtsp_url)
    # 获取视频分辨率
    if save_file:
        size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        # 获取视频帧率
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        print(f"视频流的分辨率{size}, FPS:{fps}")
        # 设置视频格式
        # fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        fourcc = cv2.VideoWriter_fourcc(*'H264')
        # 调用VideoWrite（）函数
        videoWrite = cv2.VideoWriter(f"{save_file}.mp4", fourcc, fps, size)

    while True:
        try:
            if cap.isOpened():
                success, frame = cap.read()
                if success:
                    if not videoWrite is False:
                        videoWrite.write(frame)
                #     cv2.imshow("frame", frame)
                cv2.waitKey(1)
            # 获取视频流异常后重新拉取
            else:
                print("拉取流地址失败")
        except Exception as e:
            print(multiprocessing.current_process().name)
            print(traceback.format_exc())
            break
            # cap = cv2.VideoCapture(rtsp_url)
            # time.sleep(1)
    print("拉取结束，退出程序")


if __name__ == "__main__":
    url = "rtsp://admin:Pengming123@192.168.1.201:554/Streaming/Channels/101"
    pull_rtsp(url)

    # from multiprocessing import Process
    # camera_1 = "http://admin:wynfee.huang123@192.168.1.213:80/ISAPI/Streaming/Channels/101/picture"
    # camera_2 = "rtsp://admin:wynfee.huang123@192.168.1.212:554/Streaming/Channels/101"
    # camera_3 = "rtsp://admin:wynfee.huang123@192.168.1.211:554/Streaming/Channels/101"
    # camera_4 = "rtsp://admin:wynfee.huang123@192.168.1.209:554/Streaming/Channels/101"
    # camera_5 = "rtsp://admin:wynfee.huang123@192.168.1.210:554/Streaming/Channels/101"
    # # rtsp_url = "rtsp://admin:Pengming123@192.168.1.201:554/Streaming/Channels/101"
    # file_camera_1 = "camera_1"
    # file_camera_2 = "camera_2"
    # file_camera_3 = "camera_3"
    # file_camera_4 = "camera_4"
    # file_camera_5 = "camera_5"
    # camera_1_pro = Process(target=pull_rtsp, name=file_camera_1, args=(camera_1, file_camera_1,))
    # camera_2_pro = Process(target=pull_rtsp, name=file_camera_2, args=(camera_2, file_camera_2,))
    # camera_3_pro = Process(target=pull_rtsp, name=file_camera_3, args=(camera_3, file_camera_3,))
    # camera_4_pro = Process(target=pull_rtsp, name=file_camera_4, args=(camera_4, file_camera_4,))
    # camera_5_pro = Process(target=pull_rtsp, name=file_camera_5, args=(camera_5, file_camera_5,))
    # pros = [camera_1_pro, camera_2_pro, camera_3_pro, camera_4_pro, camera_5_pro]
    # for pro in pros:
    #     pro.daemon = True
    #     pro.start()
    # for pro in pros:
    #     try:
    #         pro.join()
    #     except KeyboardInterrupt as e:
    #         print(f"proc {pro.name} ctrl+c end...")
    #     except Exception:
    #         print(f"proc {pro.name} end...")
