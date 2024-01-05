import http.client
import ssl
import json
from utils.log import log
from cgw.swap import Message, ssl_cert_info, basic_info
import time
from multiprocessing import Queue
import threading

def perform(msg=Message.Message()):
    # Defining parts of the HTTP request
    log.info("<Cgw> <heartbeat> enter cgw heartbeat perform function")
    log.info(msg.get_body())
    log.info(f"<Cgw> <heartbeat> request_url:{msg.get_body()}")
    session_id = msg.get_session_id()
    # Define the client certificate settings for https connection
    context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    context.load_verify_locations(cafile=ssl_cert_info.get_trust_chain())
    # Create a connection to submit HTTP requests
    connection = http.client.HTTPSConnection(host='192.168.43.1', port=443, key_file=ssl_cert_info.get_private_key(),
                                             cert_file=ssl_cert_info.get_cert(), context=context, timeout=60)
    request_url = basic_info.get_station_authority() + '/v1/api/heartbeat' + '?session_id=' + session_id
    log.info(f"<Cgw> <heartbeat> request_url:{request_url}")
    # request_headers = {
    #     'Content-Type': 'application/json'
    # }
    #while True:
    connection.request(method="GET", url=request_url)
    log.info(f"<Cgw> <heartbeat> request_url:{request_url}")
    # Print the HTTP response from the IOT service endpoint
    response = connection.getresponse()
    log.info(f"<Cgw> <heartbeat> response code:{response.status}, response reason:{response.reason}")
    data = response.read()
    log.info(f"<Cgw> <heartbeat> response data:{str(data)}")
    time.sleep(1)
    rep_json = json.loads(data)
    return rep_json



#def hb_threads(hb_q_return,msg=Message.Message()):
    #hb_q_send = Queue()
    #threads = [threading.Thread(target=perform, args=(hb_q_send,hb_q_return,msg), name="hb")]
    #for th in threads:
        #th.daemon = True
        #th.start()
    #return hb_q_return.get()
         
   
    
        
        
        