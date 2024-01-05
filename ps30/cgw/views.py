from cgw.swap import Message
from cgw.lion import authenticate
from cgw.lion import next_step
from cgw.lion import heartbeat
from cgw.lion import prepare
from cgw.lion import diagnosis
from cgw.lion import vehicle_info
from cgw.lion import session_close
from cgw.lion import door
from cgw.lion import sleep
from cgw.lion import ctrl_ps
from cgw.lion import psap_status
from cgw.lion import swap_status
from utils.log import log
from django.http import JsonResponse


cgw_session_id = ''
post_type = ['auth', 'nextstep', 'prepare', 'diagnosis',
             'session_close', 'vehicle_info', 'door', 'sleep', 'ctrl_ps']
get_type = ['heartbeat', 'psap_status', 'swap_status']


def handle_request(request):
    log.info("<Cgw>:enter cgw handle_request function")
    global cgw_session_id
    body = ''
    typ = request.GET.get('type')
    if request.method == "POST" and typ not in post_type:
        return JsonResponse({'result_code': "1", 'message': 'illegal POST, type not in list'})
    elif request.method == "GET" and typ not in get_type:
        return JsonResponse({'result_code': "1", 'message': 'illegal GET, type not in list'})
    elif request.method not in ['POST', "GET"]:
        return JsonResponse({'result_code': "1", 'message': 'illegal request, not POST and not GET'})
    elif request.method == "POST":
        log.debug(f"<Cgw>:Post请求数据:{str(request.body)}")
        body = request.body

    if typ == 'auth':
        msg = Message.Message(body)
        res = authenticate.perform(msg)
        cgw_session_id = msg.get_session_id()
        #res["result_code"] = "0"
        result_code = res["result_code"]
        log.debug(f"<Cgw>:auth Post返回数据:{str(res)}")
        return JsonResponse(res)
    if typ == 'nextstep':
        msg = Message.Message(body)
        if cgw_session_id:
            msg.set_session_id(cgw_session_id)
        else:
            return JsonResponse({'result_code': "2", 'message': 'should request auth first'})
        res = next_step.perform(msg)
        #res["result_code"] = "0"
        result_code = res["result_code"]
        log.debug(f"<Cgw>:nextstep Post返回数据:{str(res)}")
        return JsonResponse(res)
    if typ == 'prepare':
        msg = Message.Message(body)
        if cgw_session_id:
            msg.set_session_id(cgw_session_id)
        else:
            return JsonResponse({'result_code': "2", 'message': 'should request auth first'})
        res = prepare.perform(msg)
        #res["result_code"] = "0"
        result_code = res["result_code"]
        log.debug(f"<Cgw>:prepare Post返回数据:{str(res)}")
        return JsonResponse(res)
    if typ == 'diagnosis':
        msg = Message.Message(body)
        if cgw_session_id:
            msg.set_session_id(cgw_session_id)
        else:
            return JsonResponse({'result_code': "2", 'message': 'should request auth first'})
        res = diagnosis.perform(msg)
        #res["result_code"] = "0"
        result_code = res["result_code"]
        log.debug(f"<Cgw>:diagnosis Post返回数据:{str(res)}")
        return JsonResponse(res)
    if typ == 'session_close':
        msg = Message.Message(body)
        if cgw_session_id:
            msg.set_session_id(cgw_session_id)
        else:
            return JsonResponse({'result_code': "2", 'message': 'should request auth first'})
        res = session_close.perform(msg)
        #res["result_code"] = "0"
        result_code = res["result_code"]
        log.debug(f"<Cgw>:session_close Post返回数据:{str(res)}")
        return JsonResponse(res)
    if typ == 'vehicle_info':
        msg = Message.Message(body)
        if cgw_session_id:
            msg.set_session_id(cgw_session_id)
        else:
            return JsonResponse({'result_code': "2", 'message': 'should request auth first'})
        res = vehicle_info.perform(msg)
        #res["result_code"] = "0"
        result_code = res["result_code"]
        log.info(f"<Cgw>:vehicle_info Post返回数据:{str(res)}")
        return JsonResponse(res)
    if typ == 'heartbeat':
        msg = Message.Message()
        log.info(msg)
        if cgw_session_id:
            msg.set_session_id(cgw_session_id)
        else:
            return JsonResponse({'result_code': "2", 'message': 'should request auth first'})
        res = heartbeat.perform(msg)
        #res["result_code"] = "0"
        result_code = res["result_code"]
        log.debug(f"<Cgw>:heartbeat Get返回数据:{str(res)}")
        return JsonResponse(res)
    if typ == 'door':
        msg = Message.Message(body)
        if cgw_session_id:
            msg.set_session_id(cgw_session_id)
        else:
            return JsonResponse({'result_code': "2", 'message': 'should request auth first'})
        res = door.perform(msg)
        #res["result_code"] = "0"
        result_code = res["result_code"]
        log.debug(f"<Cgw>:door Post返回数据:{str(res)}")
        return JsonResponse(res)
    if typ == 'sleep':
        msg = Message.Message(body)
        if cgw_session_id:
            msg.set_session_id(cgw_session_id)
        else:
            return JsonResponse({'result_code': "2", 'message': 'should request auth first'})
        res = sleep.perform(msg)
        #res["result_code"] = "0"
        result_code = res["result_code"]
        log.debug(f"<Cgw>:sleep Post返回数据:{str(res)}")
        return JsonResponse(res)
    if typ == 'ctrl_ps':
        msg = Message.Message(body)
        if cgw_session_id:
            msg.set_session_id(cgw_session_id)
        else:
            return JsonResponse({'result_code': "2", 'message': 'should request auth first'})
        res = ctrl_ps.perform(msg)
        #res["result_code"] = "0"
        result_code = res["result_code"]
        log.debug(f"<Cgw>:ctrl_ps Post返回数据:{str(res)}")
        return JsonResponse(res)
    if typ == 'psap_status':
        msg = Message.Message()
        if cgw_session_id:
            msg.set_session_id(cgw_session_id)
        else:
            return JsonResponse({'result_code': "2", 'message': 'should request auth first'})
        res = psap_status.perform(msg)
        #res["result_code"] = "0"
        result_code = res["result_code"]
        log.debug(f"<Cgw>:psap_status Get返回数据:{str(res)}")
        return JsonResponse(res)
    if typ == 'swap_status':
        msg = Message.Message()
        if cgw_session_id:
            msg.set_session_id(cgw_session_id)
        else:
            return JsonResponse({'result_code': "2", 'message': 'should request auth first'})
        res = swap_status.perform(msg)
        #res["result_code"] = "0"
        result_code = res["result_code"]
        log.debug(f"<Cgw>:swap_status Get返回数据:{str(res)}")
        return JsonResponse(res)
