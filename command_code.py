# !/usr/bin/env Python2
# -*- coding: utf-8 -*-
# @Author   : 得灵
# @FILE     : command_code.py
# @Time     : 2021/1/16 18:05
# @Software : PyCharm
# @Introduce: This is


# 掌握着消息托付的 controller
class RequestCode:
    def __init__(self):
        pass

    NONE = 0
    USER = 1
    ROOM = 2
    GAME = 3


# 掌握着方法名
class ActionCode:


    def __init__(self):
        pass

    NONE = 0
    LOGIN = 1
    REGISTER = 2
    LIST_ROOM = 3
    CREATE_ROOM = 4
    JOIN_ROOM = 5
    UPDATE_ROOM = 6
    QUIT_ROOM = 7
    START_GAME = 8
    SHOW_TIMER = 9
    START_PLAY = 10
    MOVE = 11
    SHOOT = 12
    ATTACK = 13
    GAME_OVER = 14
    UPDATE_RESULT = 15
    QUIT_BATTLE = 16
    pass


class ReturnCode:
    def __init__(self):
        pass

    SUCCESS = 0
    FAILURE = 1
    NOT_FOUND = 2

class RoleType:
    def __init__(self):
        pass

    BLUE = 0
    RED = 1


action_code_to_handle = {ActionCode.NONE: 'NONE',
                         ActionCode.LOGIN: 'LOGIN',
                         ActionCode.REGISTER: 'REGISTER',
                         ActionCode.LIST_ROOM: 'LIST_ROOM',
                         ActionCode.CREATE_ROOM: 'CREATE_ROOM',
                         ActionCode.JOIN_ROOM: 'JOIN_ROOM'}
