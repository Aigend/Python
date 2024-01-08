#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:靳文龙
# @time: 2020/4/12 10:19


"""字典列表"""
alien_1 = {"color":"red1","age":1}
alien_2 = {"color":"red2","age":2}
alien_3 = {"color":"red3","age":3}
alien_4 = {"color":"red4","age":4}
alien_5 = {"color":"red5","age":5}
aliens = [alien_1,alien_2,alien_3,alien_4,alien_5]
for alien in aliens:
    print(alien)

"""在字典中存储列表"""
favite_languages = {
    "jen":["python","java"],
    "sarahc":["java","C"],
    "skafj":["C++","java"],
    "phil":["ruby","ksgvksb;"],
    "jsk":["axxa","C#","java","python"]
}
