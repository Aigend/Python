from cgw.swap import Message, ssl_cert_info, basic_info
from utils.log import log
import http.client
import json
import ssl


def perform(msg=Message.Message()):
    log.info("<Cgw> <door> enter cgw door perform function")
    session_id = msg.get_session_id()

    # Defining parts of the HTTP request
    request_url = basic_info.get_station_authority() + get_path() + '?session_id=' + session_id
    log.debug(f"<Cgw> <door> request_url:{request_url}")
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
        "event_type": "door",
        "event_result": "success",
        "event_message": "1110"
    }
    for k, v in body_temp.items():
        if k in ['event_type', 'event_result', 'event_message'] and v:
            body[k] = v
    body = json.dumps(body)
    connection.request(method="POST", url=request_url, headers=request_headers, body=body)

    # Print the HTTP response from the IOT service endpoint
    response = connection.getresponse()
    print(response.status, response.reason)
    data = response.read()
    #print(data)
    #return json.loads(data)
    rep_json = json.loads(data)
    return rep_json


def get_path():
    return '/v1/api/vehicle_event'
