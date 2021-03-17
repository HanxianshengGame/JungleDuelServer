# !/usr/bin/env Python2
# -*- coding: utf-8 -*-
# @Author   : 得灵
# @FILE     : 根据方法名调用对应方法.py
# @Time     : 2021/1/16 14:15
# @Software : PyCharm
# @Introduce: This is

from math import pi
from operator import methodcaller


class Circle(object):
    def __init__(self, radius):
        self.radius = radius

    def getArea(self):
        return round(pow(self.radius, 2) * pi, 2)


class Rectangle(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def get_area(self, sss):
        return self.width * self.height


if __name__ == '__main__':
    c1 = Circle(5.0)
    r1 = Rectangle(4.0, 5.0)

    # 第一个参数是函数字符串名字，后面是函数要求传入的参数，执行括号中传入对象
    methodcaller('get_area', 1)(r1)
