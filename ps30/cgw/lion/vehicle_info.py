import json
from cgw.swap import Message, ssl_cert_info, basic_info
from utils.log import log
import http.client
import ssl


def perform(msg=Message.Message()):
    log.info("<Cgw> <vehicle_info> enter cgw nextstep perform function")
    session_id = msg.get_session_id()

    # Defining parts of the HTTP request
    request_url = basic_info.get_station_authority() + get_path() + '?session_id=' + session_id
    #log.debug(f"<Cgw> <vehicle_info> request_url:{request_url}")
    log.info(f"<Cgw> <vehicle_info> request_url:{request_url}")
    msg_body = msg.get_body()
    request_headers = {
        'Content-Type': 'application/json'
    }

    # Define the client certificate settings for https connection
    context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    context.load_verify_locations(cafile=ssl_cert_info.get_trust_chain())
    # Create a connection to submit HTTP requests
    connection = http.client.HTTPSConnection(host='192.168.43.1', port=443, key_file=ssl_cert_info.get_private_key(),
                                             cert_file=ssl_cert_info.get_cert(), context=context, timeout=60)

    # Use connection to submit a HTTP POST request
    body_temp = json.loads(msg.get_body())
    body = {
        "event_result": "success",
        "event_message": "vehicle_info success",
        "vehicle_info": {
            "battery_customer_soc": "",
            "battery_pack_cap": 3, 
            "battery_package_number": "",           
            "battery_soc": 90.5,
            "battery_soh": 80.5,
            "bms_fota_part_number": "",
            "bms_hardware_version": "",
            "bms_software_version": "",
            "spm_hardware_version": "",
            "spm_software_version": "",
            "csg_hardware_version": "",
            "csg_software_version": "",
            "hw_part_number": "",
            "sw_part_number": "",
            "vid_code": "",
            "lv_battery_soc": 99,
            "lv_battery_soc_status": 1,
            "front_left_wheel_pressure": 210,
            "front_right_wheel_pressure": 210,
            "rear_left_wheel_pressure": 210,
            "rear_right_wheel_pressure": 210
        }
    }
    for k, v in body_temp.items():
        if k in ['event_result', 'event_message', ] and v:
            body[k] = v
        elif k in ['vehicle_info'] and v:
            if isinstance(v, dict):
                for name, val in v.items():
                    body[k][name] = val
    body = json.dumps(body)
    log.info(f"<Cgw>:vehicle_info request 数据:{str(body)}")
    connection.request(method="POST", url=request_url, headers=request_headers, body=body)

    # Print the HTTP response from the IOT service endpoint
    response = connection.getresponse()
    log.info(f"<Cgw> <vehicle_info> response code:{response.status}, response reason:{response.reason}")
    data = response.read()
    log.info(f"<Cgw> <vehicle_info> response data:{str(data)}")
    rep_json = json.loads(data)
    #return data
    log.info(rep_json)
    return rep_json


def get_path():
    return '/v1/api/vehicle_info'
