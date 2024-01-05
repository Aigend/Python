"""
功能：设置上报文件和消息的白名单
上报时机：
上报频率：实时通信
支持版本：NT2
应用方：AA
"""
import time
import uuid
from nio_messages import pb2, pbjson
from nio_messages.data_unit import gen_adas_header, gen_upload_info
from nio_messages.nextev_msg import gen_nextev_message
from nio_messages.pb2.dlb_upload_switch_pb2 import DlbUploadSwitch


def generate_message(vin, vid, sample_ts=None, protobuf_v=pb2.VERSION,
                     adas_header_data=None, dlb_upload_switch_data=None):
    """
    :param event_type:
    :param dlb_upload_switch_data:
    :param sample_ts:
    :param protobuf_v:
    :param vin: 车辆vin
    :param vid: 车辆vid,消息如果是给NMP发，则采用默认值None；消息如果是发给kafka的，需要填写正确的vid
    :param adas_header_data: adas header数据
    :return: 包含np事件事件的nextev_msg以及feature_status_update本身
    """
    if dlb_upload_switch_data is None:
        dlb_upload_switch_data = {}
    dlb_upload_switch_info = DlbUploadSwitch()

    dlb_upload_switch_info.uuid = dlb_upload_switch_data.get('uuid', str(uuid.uuid1()))
    dlb_upload_switch_info.adc_version = dlb_upload_switch_data.get('adc_version', 'BL061')
    dlb_upload_switch_info.utc_nano_timestamp = dlb_upload_switch_data.get('utc_nano_timestamp', round(time.time()))
    dlb_upload_switch_info.vehicle_id = dlb_upload_switch_data.get('vehicle_id', vid)
    dlb_upload_switch_info.vehicle_type = dlb_upload_switch_data.get('vehicle_type', 'ET7')
    dlb_upload_switch_info.file_whitelist = dlb_upload_switch_data.get('file_whitelist', 'adc_log_1')
    dlb_upload_switch_info.message_whitelist = dlb_upload_switch_data.get('message_whitelist', 'cdm_app_upload, dlb_flow_warn')

    if sample_ts is None:
        sample_ts = round(time.time() * 1000)
    adas_header = gen_adas_header(adas_header_data, sample_ts)

    dlb_upload_switch_event = {'AdasHeader': adas_header, 'dlb_upload_switch': dlb_upload_switch_info}

    # type为DATA_REPORT  sub_type为FeatureStatusUpdate
    # header的params的key为AdasHeader
    # status的params的key为FeatureStatusUpdate

    nextev_msg = gen_nextev_message('dlb_upload_switch',
                                    dlb_upload_switch_event,
                                    sample_ts,
                                    version=protobuf_v,
                                    account_id=vid
                                    )
    dlb_upload_switch_obj = {
        'AdasHeader': pbjson.pb2dict(adas_header),
        'dlb_upload_switch': pbjson.pb2dict(dlb_upload_switch_info)
    }
    return nextev_msg, dlb_upload_switch_obj
