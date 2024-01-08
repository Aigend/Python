#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:靳文龙
# @time: 2020/4/12 18:08
with open("pi_million_digits.txt") as file_object:
    lines = file_object.readline().strip()
    pi_string = ""
    for line in lines:
        pi_string += line
print(pi_string)

#写入I love programmmer到programmmer.txt
with open("programmmer.txt","w") as file_write_object:
    file_write_object.write("I love programmmer")
    file_write_object.write("\tI love xiao xiao\n")
    file_write_object.write("I love programmmer\n")
    file_write_object.write("I love xiao xiao\n")

with open("programmmer.txt","a") as file_write_object:
    file_write_object.write("xiao xiao is an angle\n")
    file_write_object.write("I love xiao xiao\n")

"""这里想删除alien.txt文件，但未生效，需要再研究下"""
# with open("alien.txt","w") as file_onlyread_object:
#     pass
# file_onlyread_object = open("alien.txt")
# del file_onlyread_object