import http.client
import json
import ssl
from cgw.swap import Message, ssl_cert_info, basic_info
from utils.log import log


def perform(msg=Message.Message()):
    log.info("<Cgw> <auth> enter cgw authenticate perform function")

    # Defining parts of the HTTP request
    request_url = basic_info.get_station_authority() + '/v1/api/authentication'
    # https://PS-NIO-a6352e19-3f143b8b.nio-pe-local.com/v1/api/authentication
    log.info(f"<Cgw> <auth> request_url:{request_url}")
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
        "virtual_key_id": "PS-NIO-VK-001",
        "resource_id": "PS-NIO-00000001-dj842cn4",
        "vehicle_id": "ES8-123456",
        "authentication_info": "GLaMqsL9EF+hdle"
    }
    for k, v in body_temp.items():
        if k in ['virtual_key_id', 'resource_id', 'vehicle_id', 'authentication_info'] and v:
            body[k] = v
    body = json.dumps(body)
    connection.request(method="POST", url=request_url, headers=request_headers, body=body)

    # Print the HTTP response from the IOT service endpoint
    response = connection.getresponse()
    log.info(f"<Cgw> <auth> response code:{response.status}, response reason:{response.reason}")
    data = response.read()
    # b'{"result_code":"fail","message":"auth info is invalid","data":{"session_id":"1658298973930359"}}'
    rep_json = json.loads(data)
    # log.debug(rep_json)
    session_id = rep_json.get('data', {}).get('session_id', "")
    log.info(f"<Cgw> <auth> station authority get session id is {session_id}")
    msg.set_session_id(session_id)
    #return data
    log.info(rep_json)
    return rep_json 


if __name__ == '__main__':
    print(perform())
