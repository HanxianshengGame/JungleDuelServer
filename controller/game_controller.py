#!/usr/bin/env python27
# -*- coding: utf-8 -*-
# @Time    : 2021/1/25 11:00
# @Author  : handling
# @File    : game_controller.py
# @Software: PyCharm
from base_controller import BaseController
import sys

sys.path.append("..")
from command_code import RequestCode, ReturnCode, ActionCode, action_code_to_handle


class GameController(BaseController):
    def __init__(self):
        BaseController.__init__(self)
        self.request_code = RequestCode.GAME
        pass

    def start_game(self, conn, data):
        room = conn.room
        if room.house_owner == conn:
            room.broadcast_message(conn, ActionCode.START_GAME, str(ReturnCode.SUCCESS))
            room.start_timer()
            return str(ReturnCode.SUCCESS)
        else:
            return str(ReturnCode.FAILURE)

    def move(self, conn, data):
        room = conn.room
        if room:
            room.broadcast_message(conn, ActionCode.MOVE, data)
        return None

    def shoot(self, conn, data):
        room = conn.room
        if room:
            room.broadcast_message(conn, ActionCode.SHOOT, data)
        return None

    def attack(self, conn, data):
        damage = int(data)
        room = conn.room
        if room:
            room.take_damage(conn, damage)
        return None

    def quit_battle(self, conn, data):
        room = conn.room
        if room:
            room.broadcast_message(None, ActionCode.QUIT_BATTLE, 'r')
            room.close()
        return None

