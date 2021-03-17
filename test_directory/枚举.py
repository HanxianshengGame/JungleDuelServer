# !/usr/bin/env Python2
# -*- coding: utf-8 -*-
# @Author   : 得灵
# @FILE     : 枚举.py
# @Time     : 2021/1/16 17:57
# @Software : PyCharm
# @Introduce: This is
import struct

from enum import Enum


class Color(Enum):
    # 为序列值指定value值
    red = 1
    green = 2
    blue = 3

    # 调用枚举成员的 3 种方式


print Color.red


class RequestCode(Enum):
    NONE = 0


class ActionCode(Enum):
    NONE = 0
    pass


print ActionCode.NONE == 0


# print(Color.red)
# print(Color(1))
# # 调取枚举成员中的 value 和 name
# # 遍历枚举类中所有成员的 2 种方式
# for color in Color:
#     print(color)

def int_to_bytes(convert_val):
    format_str = '<i'
    s = struct.Struct(format_str)
    return s.pack(convert_val)


print int_to_bytes(ActionCode.NONE)

print 'ss' + None
