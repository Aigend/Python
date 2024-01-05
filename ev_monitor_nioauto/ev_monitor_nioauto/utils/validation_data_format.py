# -*- coding: utf-8 -*-
# @Project : ev_monitor_nioauto
# @File : data_type_verify.py
# @Author : qiangwei.zhang
# @time: 2021/07/29
# @api: GET_/api/XXX 【必填】
# @showdoc:
# @Description :脚本描述
import re
from utils.logger import logger

EMAIL_RE = r"[\w!#$%&'*+/=?^_`{|}~-]+(?:\.[\w!#$%&'*+/=?^_`{|}~-]+)*@(?:[\w](?:[\w-]*[\w])?\.)+[\w](?:[\w-]*[\w])?"
NIO_EMAIL_RE = r"^[a-z0-9\.]+@nio\.(com|io)$"
ALL_regex = "(?=^\\+(9[0123458]|96[0-8]|97[0-7]|99[234568]|8[1246]|85[02356]|88[06]|7|6[1234567]|68[012356789]|69[012]|5|4[013456789]|42[013]|3[01234569]|37[0-8]|38[01235679]|2[023467]|21[12368]|25[0-8]|29[01789]|1))(^\\+\\d{2,15}$)"
FAKE_MOBILE_PREFIX = "9876"
CN_FAKE_MOBILE_PREFIX = "\\+869876"


def validation_email_format(email):
    ex_email = re.compile(EMAIL_RE)
    result = ex_email.match(email)
    if result:
        logger.debug(f"【{email}】邮箱格式正确的")
    else:
        logger.debug(f"【{email}】邮箱格式不正确")
    return result


def validation_nio_email_format(email):
    ex_email = re.compile(NIO_EMAIL_RE)
    result = ex_email.match(email)
    if result:
        logger.debug(f"【{email}】是NIO邮箱")
    else:
        logger.debug(f"【{email}】不是NIO邮箱")
    return result


def validation_fake_mobile(mobile):
    fake_mobile = re.compile(FAKE_MOBILE_PREFIX)
    result = fake_mobile.match(mobile)
    if result:
        logger.debug(f"【{mobile}】是NIO定义的假手机号")
    else:
        logger.debug(f"【{mobile}】不是NIO定义的假手机号")
    return result


def validation_cn_fake_mobile(mobile):
    cn_fake_mobile = re.compile(CN_FAKE_MOBILE_PREFIX)
    result = cn_fake_mobile.match(mobile)
    if result:
        logger.debug(f"【{mobile}】是NIO定义的假手机号")
    else:
        logger.debug(f"【{mobile}】不是NIO定义的假手机号")
    return result


def validation_e164_mobile(mobile):
    e164_mobile = re.compile(ALL_regex)
    result = e164_mobile.match(mobile)
    if result:
        logger.debug(f"【{mobile}】是符合E.164规范的手机号")
    else:
        logger.debug(f"【{mobile}】不是符合E.164规范的手机号")
    return result


if __name__ == '__main__':
    for email in ["123344@qq.com", "xx.xx.o@nio.com", "xx.xx.o@nio.io", "12132112"]:
        print(validation_nio_email_format(email))
        print(validation_email_format(email))
    for mobile in ["+8698761021234", "98761021234", "+8617610551933", "17610551933", "wess1234", "+86 17610551933"]:
        # print(validation_e164_mobile(mobile))
        print(validation_fake_mobile(mobile))
