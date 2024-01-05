import time
from flask import Flask, jsonify, request
# from flask_script import Manager

from log import log

from oss_utils import get_oss_data_real_time, get_oss_data_alarm, get_oss_data_event
from tk_utils import get_tk_data_real_time

app = Flask(__name__)

# manger = Manager(app)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/kylin/cloud/realtime/set', methods=["POST"])
def rec_realtime_data():
    """
        kafka 请求实时数据
    :return:
    """
    response = {
        'datetime': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        'result_code': "0",
        'message': "OK",
        'data': {
            'point_data': []
        }
    }
    body = request.get_json()
    log.info(body)
    station_id = body.get('resource_id')
    site = body.get("site")
    if not station_id or not site:
        log.error(f"<OSS_TK>:station_id and site is null")
        return jsonify(response)
    for key in body['keys']:
        r = get_oss_data_real_time(station_id, str(key)) if site == "oss" else get_tk_data_real_time(station_id,
                                                                                                     str(key))
        response['data']['point_data'].append(r)
    time.sleep(1)
    return jsonify(response)


@app.route('/kylin/cloud/alarm/set', methods=["POST"])
def rec_alarm_info_data():
    """
    请求告警数据
    :return:
    """
    response = {
        'datetime': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        'result_code': "0",
        'message': "",
        'data': {
            'point_data': []
        }
    }
    body = request.get_json()
    log.info(body)
    station_id = body.get('resource_id')
    site = body.get("site")
    state = body.get("state")
    if not station_id or not site or not state:
        log.error(f"<OSS_TK>:station_id and site is null")
        return jsonify(response)
    state = True if int(state) > 0 else False
    for key in body['keys']:
        r = get_oss_data_alarm(station_id, str(key), state)
        response['data']['point_data'].append(r)
    time.sleep(1)
    return jsonify(response)


@app.route('/kylin/cloud/event/set', methods=["POST"])
def rec_event_data():
    """

    :return:
    """
    response = {
        'datetime': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        'result_code': "0",
        'message': "OK",
        'data': {
            'point_data': []
        }
    }
    body = request.get_json()
    log.info(body)
    station_id = body.get('resource_id')
    site = body.get("site")
    if not station_id or not site:
        log.error(f"<OSS_TK>:station_id and site is null")
        return jsonify(response)
    for key in body['keys']:
        r = get_oss_data_event(station_id, str(key))
        if r:
            response['data']['point_data'].append(r)
    time.sleep(1)
    return jsonify(response)


@app.route('/kylin/oss_order_info/set', methods=["POST"])
def rec_oss_order_info_data():
    """

    :return:
    """
    response = {
        'datetime': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        'result_code': "0",
        'message': "OK"
    }
    body = request.get_json()
    log.info(body)
    station_id = body.get('resource_id')
    site = body.get("site")
    if not station_id or not site:
        log.error(f"<OSS_TK>:station_id and site is null")
        return jsonify(response)
    for key in body['keys']:
        r = get_oss_data_event(station_id, str(key))
        if r:
            response['data']['point_data'].append(r)
    time.sleep(1)
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
    # manger.run()
