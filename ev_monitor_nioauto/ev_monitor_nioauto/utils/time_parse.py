import calendar
import time
from datetime import datetime


def timestamp_to_utc_strtime(timestamp, adjust=False):
    """将 13 位整数的毫秒时间戳转化成 utc 时间 (字符串格式，含毫秒)
    :param timestamp: 13 位整数的毫秒时间戳 (1456402864242)
    :param adjust: 为True时，如果毫秒位都为0，字符串时间将只保留到秒级
    :return: 返回字符串格式 {str}'2016-02-25 12:21:04.242000'
    """
    utc_str_time = datetime.utcfromtimestamp(int(timestamp) / 1000.0).strftime('%Y-%m-%d %H:%M:%S.%f')
    if adjust and utc_str_time[-6:] == '000000':
        utc_str_time = utc_str_time[:-7]
    utc_str_time = utc_str_time if utc_str_time[-7:] != '.000000' else utc_str_time[:-7]
    return utc_str_time


def utc_strtime_to_timestamp(utc_timestr):
    """将 utc 时间 (字符串格式) 转为 13 位的时间戳
    :param utc_timestr: {str}'2016-02-25 20:21:04.242'
    :return: 1456431664242
    """
    # 先将字符串的格式转为 datetime 格式
    utc_datetime = datetime.strptime(utc_timestr, "%Y-%m-%d %H:%M:%S.%f")
    # 再将 datetime 格式的时间转为时间戳
    timestamp = int(calendar.timegm(utc_datetime.timetuple()) * 1000.0 + utc_datetime.microsecond / 1000.0)

    return timestamp


def now_time_sec():
    """
    当前10位秒级别时间
    :return: str  eg:1456402864
    """
    return str(int(time.time()))


def time_sec_to_strtime(time_sec):
    """
    传入秒级别时间str(10位)
    :param time_sec:
    :return: {str}'2016-02-25 20:21:04'
    """
    return datetime.utcfromtimestamp(int(time_sec)).strftime('%Y-%m-%d %H:%M:%S')


def now_utc_strtime(format='%Y-%m-%d %H:%M:%S', offset_sec=0):
    """

    :param format:
    :param offset_sec: 当前时间推后的秒数
    :return: {str}'2016-02-25 20:21:04' 我们mysql保存的秒时间格式
    """
    if offset_sec < 0:
        return datetime.utcfromtimestamp(int(time.time()) - abs(offset_sec)).strftime(format)
    else:
        return datetime.utcfromtimestamp(int(time.time()) + offset_sec).strftime(format)


def now_shanghai_strtime(format='%Y-%m-%d %H:%M:%S', offset_sec=0):
    """

    :param format:
    :param offset_sec: 当前时间推后的秒数
    :return: {str}'2016-02-25 20:21:04' 我们mysql保存的秒时间格式
    """
    if offset_sec < 0:
        return datetime.utcfromtimestamp(int(time.time()) - abs(offset_sec) + (8 * 60 * 60)).strftime(format)
    else:
        return datetime.utcfromtimestamp(int(time.time()) + offset_sec + (8 * 60 * 60)).strftime(format)


def utc_to_local(format='%Y-%m-%d-%H', timestamp=None, offset_hour=0):
    """
    
    :param format: 
    :param offset_hour: 
    :return: 
    """
    if timestamp is None:
        timestamp = int(time.time())
    return datetime.utcfromtimestamp(timestamp + offset_hour * 3600).strftime(format)


def bj_strtime_to_timestamp(bj_datetime):
    """将北京时间 (datetime(2019,10,15,3,21,7)) 转为 10 位的UTC时间戳
    :return: 1571109667
    """
    # 再将 datetime 格式的时间转为时间戳
    timestamp = int(calendar.timegm(bj_datetime.timetuple())) - 8 * 3600

    return timestamp


def time_format(time_str=None, in_format="%Y-%m-%d %H:%M:%S.%f", out_format="%b %-d, %Y %-I:%-M:%-S %p", offset_sec=0):
    """
    :param time_str: 时间字符串，如果不输入则默认为当前时间
    :param in_format: 输入时间的时间格式
    :param out_format: 输出时间的时间格式
    :param offset_sec: 当前时间推后的秒数
    :return: 转换后的时间
    """
    if not time_str:
        return datetime.utcfromtimestamp(int(time.time())).strftime(out_format)
    if time_str.isdigit():
        return datetime.utcfromtimestamp(time_str + offset_sec).strftime(out_format)
    utc_datetime = datetime.strptime(time_str, in_format)
    timestamp = int(calendar.timegm(utc_datetime.timetuple()) * 1000.0 + utc_datetime.microsecond / 1000.0)
    return datetime.utcfromtimestamp(int(timestamp / 1000) + offset_sec).strftime(out_format)


if __name__ == '__main__':
    print(time_format())
