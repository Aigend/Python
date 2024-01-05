import http.client
import json
import ssl
from cgw.swap import Message, ssl_cert_info, basic_info
from utils.log import log


def perform(msg=Message.Message()):
    log.info("<Cgw> <nextstep> enter cgw nextstep perform function")
    session_id = msg.get_session_id()
    # Defining parts of the HTTP request
    request_url = basic_info.get_station_authority() + '/v1/api/next_step' + '?session_id=' + session_id
    log.debug(f"<Cgw> <nextstep> request_url:{request_url}")

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
        "last_step": "",
    }
    for k, v in body_temp.items():
        if k in ['last_step', 'version'] and v:
            body[k] = v
    body = json.dumps(body)
    connection.request(method="POST", url=request_url, headers=request_headers, body=body)

    # Print the HTTP response from the IOT service endpoint
    response = connection.getresponse()
    log.info(f"<Cgw> <nextstep> response code:{response.status}, response reason:{response.reason}")
    data = response.read()
    log.info(f"<Cgw> <nextstep> response data:{str(data)}")
    rep_json = json.loads(data)
    return rep_json
