#!/usr/bin/python3
# -*- coding:utf-8 -*-

"""
车辆注册动态生成VIN码校验
"""

import string, random, time

# print ''.join(random.sample(string.ascii_uppercase + string.digits, 8) + random.sample(string.digits + 'X', 1) +
#               random.sample(string.ascii_uppercase + string.digits, 8))
#
# print string.ascii_uppercase

vin_test = 'SQETEST0'
timestamp = str(int(round(time.time() * 1000)))[5:]
# print timestamp

def check():
    # vin = ''.join(random.sample(('ABCDEFGHJKLMNPQRSTUVWXYZ') + string.digits, 8) + random.sample(string.digits + 'X', 1) +
    #           random.sample(('ABCDEFGHJKLMNPQRSTUVWXYZ') + string.digits, 8))
    vin = vin_test + '0' + timestamp
    # print vin
    jianquan = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 0, 'J': 1, 'K': 2, 'L': 3, 'M': 4,
                'N': 5, 'O': 0, 'P': 7, 'Q': 8, 'R': 9, 'S': 2, 'T': 3, 'U': 4, 'V': 5, 'W': 6, 'X': 7, 'Y': 8, 'Z': 9}
    pos = [8, 7, 6, 5, 4, 3, 2, 10, 0, 9, 8, 7, 6, 5, 4, 3, 2]
    num = 0
    for i in range(0, 17):
        if (vin[i] >= 'A') and (vin[i] <= 'Z'):
            num += (jianquan[vin[i]] * pos[i])
        elif (vin[i] >= '0') and (vin[i] <= '9'):
            num += (int(vin[i]) * pos[i])
    remainder = num % 11
    # print vin[8], remainder
    l = list(vin)
    if remainder == 10:
        l[8] = 'X'
    else:
        l[8] = str(remainder)
    new_vin = ''.join(l)
    # print new_vin
    if new_vin[8] != 'X':
        if remainder == int(new_vin[8]):
            print(new_vin, new_vin[8], remainder)
            return new_vin
    elif new_vin[8] == 'X':
        if remainder == 10:
            print(new_vin, new_vin[8], remainder)
            return new_vin
    # return num, remainder, vin[8]
    # return vin, vin[0]

if __name__ == '__main__':
    print(check())