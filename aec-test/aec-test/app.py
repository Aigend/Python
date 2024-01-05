"""
@Author: wenlong.jin
@File: app.py.py
@Project: aec-test
@Time: 2023/7/17 16:39
"""
# !/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, make_response


app = Flask(__name__)


# 实站下命令行调试
# 三代站:admin:wynfee.huang123, 二代站:admin:Pengming123
# curl --insecure --anyauth  -u admin:wynfee.huang123  -X GET 'http://192.168.1.213:80/ISAPI/Streaming/Channels/101/picture' --output a.jpg


@app.route('/ISAPI/Streaming/Channels/<path:url_path>/picture', methods=["GET"])
def get_picture(url_path):
    # print(f"####{url_path}, {type(url_path)}")
    path = {
        "101": "cam_1.jpg",
        "106": "cam_6.jpg",
        "107": "cam_7.jpg",
        "108": "cam_8.jpg",
        "109": "cam_9.jpg",
        "120": "cam_10.jpg",
        "110": "cam_2_6.jpg",  # 二代站的curl请求，camera6
        "111": "cam_2_7.jpg"  # 二代站的curl请求，camera7
    }
    file = path.get(url_path, "cam_1.jpg")
    with open(f'source/{file}', "rb") as f:
        image_data = f.read()
    response = make_response(image_data)
    response.headers['Content-Type'] = 'image/jpeg; charset=utf-8'
    response.headers['Content-Length'] = str(len(image_data))

    # 和命令行返回的content大小不一致
    # stats = os.stat('./source/img_car.jpg')
    # img = cv2.imread('./source/img_car.jpg')
    # img_encode = cv2.imencode('.jpg', img)[1]
    # data_encode = np.array(img_encode)
    # image_data = data_encode.tobytes()
    # response = make_response(image_data)
    # response.headers['Content-Type'] = 'image/jpeg; charset=utf-8'
    # response.headers['Content-Length'] = str(len(image_data))
    return response


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
