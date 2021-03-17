# !/usr/bin/env Python2
# -*- coding: utf-8 -*-
# @Author   : 得灵
# @FILE     : controller_manager.py
# @Time     : 2021/1/16 13:37
# @Software : PyCharm
# @Introduce: This is

from operator import methodcaller
import sys

sys.path.append("..")
from controller.default_controller import DefaultController
from controller.user_controller import UserController
from controller.room_controller import RoomController
from controller.game_controller import GameController
from command_code import RequestCode, action_code_to_handle



class ControllerManager:

    def __init__(self):
        # request_code : base_controller
        self.__code_to_controller = {}
        self.init()
        pass

    def init(self):
        # 这里要把controller全部注册管理  request : controller
        default_controller = DefaultController()
        self.__code_to_controller[default_controller.request_code] = default_controller
        self.__code_to_controller[RequestCode.USER] = UserController()
        self.__code_to_controller[RequestCode.ROOM] = RoomController()
        self.__code_to_controller[RequestCode.GAME] = GameController()
        pass

    def handle_request(self, conn, request_code, action_code, data):
        # 处理请求的步骤： 根据request_code 找到对应的 controller， 根据 action_code 找到对应的 处理方法
        controller = self.__code_to_controller[request_code]
        handle_method_name = action_code_to_handle[action_code].lower()
        return_val = methodcaller(handle_method_name, conn, data)(controller)
        return return_val
