"""
功能：云端收集数据完成运营类的管理
需求来源：DLB流量信息
上报时机：
上报频率：实时通信
支持版本：NT2
应用方：AA
"""
import time
import random
import uuid
from nio_messages import pb2, pbjson
from nio_messages.data_unit import gen_adas_header, gen_flow_info
from nio_messages.nextev_msg import gen_nextev_message
from nio_messages.pb2.dlb_flow_warn_pb2 import DlbFlowWarn


def generate_message(vin, vid, sample_ts=None, protobuf_v=pb2.VERSION,
                     adas_header_data=None, dlb_flow_warn_data=None):
    """
    :param dlb_flow_warn_data:
    :param sample_ts:
    :param protobuf_v:
    :param vin: 车辆vin
    :param vid: 车辆vid,消息如果是给NMP发，则采用默认值None；消息如果是发给kafka的，需要填写正确的vid
    :param adas_header_data: adas header数据
    :return: 包含np事件事件的nextev_msg以及feature_status_update本身
    """
    if dlb_flow_warn_data is None:
        dlb_flow_warn_data = {}
    dlb_flow_warn_info = DlbFlowWarn()

    dlb_flow_warn_info.uuid = dlb_flow_warn_data.get('uuid', str(uuid.uuid1()))
    dlb_flow_warn_info.statid = dlb_flow_warn_data.get('statid', random.randint(0, 2147483647))
    dlb_flow_warn_info.adc_version = dlb_flow_warn_data.get('adc_version', 'BL061')
    dlb_flow_warn_info.utc_nano_timestamp = dlb_flow_warn_data.get('ptp_nano_timestamp', round(time.time()))
    dlb_flow_warn_info.vehicle_id = dlb_flow_warn_data.get('vehicle_id', vid)
    dlb_flow_warn_info.vehicle_type = dlb_flow_warn_data.get('vehicle_type', 'ES8')
    dlb_flow_warn_info.upload_info.MergeFrom(gen_flow_info(dlb_flow_warn_data.get('upload_info', None)))

    if sample_ts is None:
        sample_ts = round(time.time() * 1000)
    adas_header = gen_adas_header(adas_header_data, sample_ts)

    dlb_flow_warn_event = {'AdasHeader': adas_header, 'dlb_flow_warn': dlb_flow_warn_info}

    # type为DATA_REPORT  sub_type为FeatureStatusUpdate
    # header的params的key为AdasHeader
    # status的params的key为FeatureStatusUpdate

    nextev_msg = gen_nextev_message('dlb_flow_warn',
                                    dlb_flow_warn_event,
                                    sample_ts,
                                    version=protobuf_v,
                                    account_id=vid
                                    )
    dlb_flow_warn_obj = {
        'AdasHeader': pbjson.pb2dict(adas_header),
        'dlb_flow_warn': pbjson.pb2dict(dlb_flow_warn_info)
    }
    return nextev_msg, dlb_flow_warn_obj
