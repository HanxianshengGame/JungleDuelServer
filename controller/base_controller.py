# !/usr/bin/env Python2
# -*- coding: utf-8 -*-
# @Author   : 得灵
# @FILE     : base_controller.py
# @Time     : 2021/1/21 22:15
# @Software : PyCharm
# @Introduce: This is

from command_code import RequestCode
class BaseController:

    def __init__(self):
        self.request_code = RequestCode.NONE
        pass

    def default_handle(self, data):
        return ''
