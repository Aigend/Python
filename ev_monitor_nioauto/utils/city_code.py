#!/usr/bin/env python
# coding=utf-8

def city_code(area_code):
    """
    地区码转换为城市码
    :param area_code: 地区码
    :return: 城市码
    """
    direct_city = ['11', '12', '31', '50']
    if area_code:
        return f"{area_code[:2]}0000" if area_code[:2] in direct_city else f"{area_code[:4]}00"
    else:
        return None