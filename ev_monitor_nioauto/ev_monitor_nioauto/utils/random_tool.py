# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : random_tool.py
# @Author : qiangwei.zhang
# @CreateTime : 2021/6/16 10:27 上午
# @Description :
from dateutil import parser
import random
import string
import time
import json
import base64
from datetime import datetime, timedelta, date
from utils.logger import logger


def random_string(n=13):
    if n <= 0:
        return ""
    str_list = []
    for i in range(n):
        str_list.append(str(random.sample(string.ascii_letters, 1)[0]))
    return "".join(str_list)


def random_str(n=13):
    if n <= 0:
        return ""
    str_list = []
    for i in range(n):
        str_list.append(str(random.sample(string.ascii_letters + string.digits, 1)[0]))
    return "".join(str_list)


def random_int(n=13):
    if n <= 0:
        return ""
    str_list = []
    for i in range(n):
        str_list.append(str(random.sample(string.digits, 1)[0]))
    return "".join(str_list)


def random_code(prefix="03UP"):
    # code = "03UPE01000011C85A00FTY45"
    return prefix + "".join(random.sample(string.ascii_uppercase + string.digits, 20))


def int_time_10():
    return int(time.time())


def int_time_13():
    return int(time.time() * 1000)


def format_time():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())


def int_time_to_format_time(int_time=time.time(), format="%Y-%m-%d %H:%M:%S"):
    return time.strftime(format, time.localtime(int(int_time)))


def formatt(ts):
    t = parser.parse(ts)
    return t


def format_time_to_int_10(date_time, format="%Y-%m-%d %H:%M:%S", offset_sec=0):
    time_array = datetime.strptime(date_time, format)
    time_stamp = int(datetime.timestamp(time_array))
    # time_array = time.strptime(date_time, format)
    # time_stamp = int(time.mktime(time_array))
    if offset_sec < 0:
        time_stamp = time_stamp - abs(offset_sec)
    else:
        time_stamp = time_stamp + offset_sec
    return time_stamp


def format_time_to_int_13(date_time, format="%Y-%m-%d %H:%M:%S"):
    time_array = time.strptime(date_time, format)
    time_stamp = int(time.mktime(time_array) * 1000)
    return time_stamp


def format_date():
    return time.strftime('%Y-%m-%d', time.localtime())


def format_date_n_day_ago(n=1):
    return datetime.strftime(datetime.now() - timedelta(n), '%Y-%m-%d')


def format_date_n_hours_ago(format_time=None, n=1):
    if format_time:
        time_str_new = datetime.strptime(format_time, '%Y-%m-%d %H:%M:%S')
    else:
        time_str_new = datetime.now()
    return datetime.strftime(time_str_new - timedelta(hours=n), '%Y-%m-%d %H:%M:00')


def time_sleep(n):
    while n > 0:
        time.sleep(1)
        n = n - 1
        logger.debug(f"等待中>>>剩余等待时间{n}秒")


def generate_random_nio_code():
    # 电池nio_code生成格式
    # [8位零件号(数字字母)]V[两位版本号(字母)]D[5位制造日期(数字，儒略日期格式)][6位供应商代码(数字字母)]S[6位供应商信息(数字字母)]N[5位序列号(数字)]
    # 8位零件号一般使用P开头, 按照虚拟电池包创建要求，在'P0085553', 'P0073713', 'P0000084'三个值中选择
    # nio_code为36位字符串，nio_encoding为去掉nio_code的4个标识码(V D S N)后的32位字符串
    # 按照虚拟电池包创建要求，后五位改为Dtest方便过滤
    component_no = random.choice(['P0085553', 'P0073713', 'P0000084'])
    version = ''.join(random.choices(string.ascii_uppercase, k=2))
    product_date = ''.join(random.choices(string.digits, k=5))
    supplier = ''.join(random.choices(string.digits + string.ascii_uppercase, k=6))
    supplier_info = ''.join(random.choices(string.digits + string.ascii_uppercase, k=6))
    # sn = ''.join(random.choices(string.digits, k=5))
    sn = 'Dtest'
    nio_code = f'{component_no}V{version}D{product_date}{supplier}S{supplier_info}N{sn}'
    nio_encoding = f'{component_no}{version}{product_date}{supplier}{supplier_info}{sn}'
    return nio_code, nio_encoding


def generate_random_gbt_code(supplier, product_type, count=1):
    # 电池国标码生成格式
    # https://git.nevint.com/greatwall/battery-trace/blob/master/docs/GBT%E5%9B%BD%E6%A0%87%E8%A7%A3%E6%9E%90.png
    # [3位供应商代码][1位产品类型代码][1位电池类型代码][2位规格代码][7位追溯信息代码][3位生产日期代码][7位序列号]
    # 共24位字符串
    # 供应商代码:
    # 03U - 正力蔚来
    # 001 - CATL
    # 071 - XPT
    # 产品类型代码:
    # P: 电池
    # M: 模组
    # C: 单体
    # 电池类型A-G，Z为其他，具体指代参考上述文档
    # 规格代码： 01, 03
    battery_type_option = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'Z']
    year_option = ['7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
    month_option = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C']
    day_option = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L',
                  'M', 'N', 'P', 'R', 'S', 'T', 'V', 'W', 'X', 'Y']
    battery_type = random.choice(battery_type_option)
    spec = random.choice(["01", "03"])
    trace = ''.join(random.choices(string.digits, k=7))
    today = date.today()
    year = today.year
    month = today.month
    day = today.day
    if year < 2017:
        year = 2017
    produce_date = f'{year_option[year - 2017]}{month_option[month - 1]}{day_option[day % 31]}'
    if count < 2:
        result = f'{supplier}{product_type}{battery_type}{spec}{trace}{produce_date}' \
                 f'{"".join(random.choices(string.digits + string.ascii_uppercase, k=7))}'
    else:
        result = []
        for _ in range(count):
            result.append(f'{supplier}{product_type}{battery_type}{spec}{trace}{produce_date}'
                          f'{"".join(random.choices(string.digits + string.ascii_uppercase, k=7))}')
    return result


def generate_battery_pack(is_internal=True, logistic_des=None):
    supplier = random.choice(['03U', '001', '071'])  # 03U - 正力蔚来, 001 - CATL, 071 - XPT
    nio_code, nio_encoding = generate_random_nio_code()
    gbt_code = generate_random_gbt_code(supplier, 'P')
    print(f'gbt: {gbt_code}, nio_code: {nio_code}')
    if is_internal:
        code = f'[>16{nio_code}{gbt_code}'
    else:
        code = f'[&gt;16{nio_code}{gbt_code}'
    pack_model_id = 'BAC0701701'
    model_id = 'NCM_100Ah_21.9V_2P6S'
    cell_model_id = 'S5E891'
    order_no = '2510000560'
    if not logistic_des:
        logistic_des = random.choice([101, 102, 103])  # 101 - 生产库, 102 - 售后库, 103 - 换电库
    if is_internal:
        battery_data = {'code': code, 'modelId': pack_model_id, 'orderNo': order_no,
                        'logisticDes': logistic_des, 'moduleList': []}
    else:
        battery_data = {'code': code, 'model_id': pack_model_id, 'order_no': order_no,
                        'logistic_des': logistic_des, 'module_list': []}
    model_list = generate_random_gbt_code(supplier, 'M', count=32)
    for model_code in model_list:
        if is_internal:
            model_info = {'code': model_code, 'modelId': model_id, 'cellModelId': cell_model_id, 'cellList': []}
        else:
            model_info = {'code': model_code, 'model_id': model_id, 'cell_model_id': cell_model_id, 'cell_list': []}
        cell_list = generate_random_gbt_code(supplier, 'C', count=12)
        for cell_code in cell_list:
            if is_internal:
                model_info['cellList'].append(cell_code)
            else:
                model_info['cell_list'].append(cell_code)
        if is_internal:
            battery_data['moduleList'].append(model_info)
        else:
            battery_data['module_list'].append(model_info)
    result = {'gbt_code': gbt_code, 'logistic_des': logistic_des, 'order_no': order_no,
              'nio_code': nio_code, 'nio_encoding': nio_encoding}
    if is_internal:
        result['battery_data'] = [battery_data]
    else:
        base64_result = json.dumps(battery_data)
        base64_result = base64.b64encode(base64_result.encode("ascii"))
        result['battery_data'] = base64_result.decode("ascii")
    return result


def generate_battery_pack_with_virtual_module(repetition_model=False, repetition_same_mode_cell=False, repetition_diff_mode_cell=False):
    supplier = '001'  # CATL
    nio_code, nio_encoding = generate_random_nio_code()
    gbt_code = generate_random_gbt_code(supplier, 'P')
    print(f'gbt: {gbt_code}, nio_code: {nio_code}')
    code = f'[&gt;16{nio_code}{gbt_code}'
    pack_model_id = 'BAC1002003'
    model_id = 'NCM_280Ah_29.84V_1P8S'
    cell_model_id = 'CE2H0'
    order_no = '2510000560'
    battery_data = {'code': code, 'model_id': pack_model_id, 'order_no': order_no, 'module_list': []}
    model_list = generate_random_gbt_code(supplier, 'M', count=12)
    if repetition_model:
        model_list[0] = model_list[-1]
        logger.debug(f"包内单体重复。定位:电池包:{battery_data['code'][-13:]}模组:{model_list[0]}重复")
    for model_code in model_list:
        model_info = {'code': model_code + 'C', 'model_id': model_id, 'cell_model_id': cell_model_id, 'cell_list': []}
        cell_list = generate_random_gbt_code(supplier, 'C', count=8)
        if repetition_same_mode_cell:
            cell_list[0] = cell_list[-1]
            logger.debug(f"包内单体重复。定位:电池包:{battery_data['code'][-13:]}模组:{model_info['code']}中单体{cell_list[0]}重复")
        for cell_code in cell_list:
            model_info['cell_list'].append({'code': cell_code, 'cell_model_id': cell_model_id})
        battery_data['module_list'].append(model_info)
    if repetition_diff_mode_cell:
        battery_data['module_list'][0]["cell_list"][0] = battery_data['module_list'][-1]['cell_list'][-1]
        logger.debug(
            f"包内单体重复。定位:电池包:{battery_data['code'][-13:]}模组:{battery_data['module_list'][0]['code']}中单体{battery_data['module_list'][-1]['cell_list'][-1]}和模组:{battery_data['module_list'][-1]['code']}中单体重复")
    _result = {'gbt_code': gbt_code, 'order_no': order_no, 'nio_code': nio_code, 'nio_encoding': nio_encoding}
    base64_result = json.dumps(battery_data)
    base64_result = base64.b64encode(base64_result.encode("ascii"))
    _result['battery_data'] = base64_result.decode("ascii")
    return _result


def generate_battery_add_info():
    doc_id = ''.join(random.choices(string.digits, k=12))
    p_code = f"001PF000000000B11{''.join(random.choices(string.digits + string.ascii_uppercase, k=7))}"
    cus_code = ''.join(random.choices(string.digits, k=5))
    battery_add_info = {'doc_id': doc_id, 'data_list': [
        {'p_code': p_code, 'cus_code': cus_code, 'measure_name_list': [
            {'measure_name': 'DTDXDYV001', 'test_date': '2020-09-11 03:23:33', 'actual': '3.310'},
            {'measure_name': 'DTDXDYV002', 'test_date': '', 'actual': '3.298'}]
         }]}
    result = json.dumps(battery_add_info)
    result = base64.b64encode(result.encode("ascii"))
    return {'p_code': p_code, 'battery_add_info': result.decode("ascii")}


def fixed_length_range_strings(max_num=1000, n=3):
    str_zero = "0" * n
    num_list = []
    for i in range(max_num):
        num_list.append(str_zero[0:n - len(str(i))] + str(i))
    return num_list


def random_cn_string(n=13):
    if n <= 0:
        return ""
    Chinese_list = ["中", "文", "字", "符", "随", "机", "美", "快", "暹", "曀", "曒", "蔚", "来", "汽", "车"]
    str_list = []
    for i in range(n):
        str_list.append(str(random.sample(Chinese_list, 1)[0]))
    return "".join(str_list)


if __name__ == '__main__':
    # ts = "2022-06-09 05:12:25"
    # ts_int = 1654722745
    # print(format_time_to_int_10(ts))
    print(int(datetime.timestamp(datetime.strptime("2022-06-09 05:12:25", "%Y-%m-%d %H:%M:%S"))))

