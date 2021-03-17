#!/usr/bin/env python27
# -*- coding: utf-8 -*-
# @Time    : 2021/1/13 10:03
# @Author  : handling
# @File    : task.py
# @Software: PyCharm


from controller_manager import ControllerManager


import sys
sys.path.append("..")
import logger

controller_manager = ControllerManager()


class Task:
    def __init__(self, conn, msg):
        self.__conn = conn
        self.__request_code = msg[0]
        self.__action_code = msg[1]
        self.__data = msg[2]

    def process(self):
        """
        该函数会交付给线程池处理
        :return:
        """
        # compute
        logger.simple_log(self.__conn.get_peer_addr(), '发来了请求: ',
            self.__request_code, ' ', self.__action_code,
            ' ', self.__data)
        response_data = controller_manager.handle_request(self.__conn, self.__request_code,
            self.__action_code,
            self.__data)

        logger.simple_log('回应 ', self.__conn.get_peer_addr(), '的请求: ',
            self.__action_code, ' ', response_data)

        # 根据数据判定是否需要回应
        if response_data:
            self.__conn.send_in_loop((self.__action_code, response_data))
