# !/usr/bin/env Python2
# -*- coding: utf-8 -*-
# @Author   : 得灵
# @FILE     : room_controller.py
# @Time     : 2021/1/23 11:15
# @Software : PyCharm
# @Introduce: This is
import threading
import time

from base_controller import BaseController
import sys

sys.path.append("..")
from command_code import RequestCode, ReturnCode, ActionCode, action_code_to_handle, RoleType


class TimerThread(threading.Thread):
    """
    用于计时的线程
    """

    def __init__(self, func, args, name=''):
        threading.Thread.__init__(self)
        self.name = name
        self.func = func
        self.args = args

    def run(self):
        self.func(*self.args)

    pass


class RoomState:
    def __init__(self):
        pass

    WaitingJoin = 0
    WaitingBattle = 1
    Battle = 2
    End = 3


class Room:
    MAX_HP = 200

    def __init__(self):
        # 该房间存放了客户端的连接
        self.house_owner = None
        self.client_room = []
        self.state = RoomState.WaitingJoin

    def add_client(self, conn):
        if len(self.client_room) == 0:
            self.house_owner = conn
        self.client_room.append(conn)
        conn.room = self
        conn.hp = self.MAX_HP
        if len(self.client_room) >= 2:
            self.state = RoomState.WaitingBattle

    def remove_client(self, conn):
        conn.room = None
        self.client_room.remove(conn)
        if len(self.client_room) >= 2:
            self.state = RoomState.WaitingBattle
        else:
            self.state = RoomState.WaitingJoin

    def get_house_owner_data(self):
        return self.house_owner.get_user_data()

    def is_waiting_join(self):
        return self.state == RoomState.WaitingJoin

    def get_id(self):
        return self.house_owner.get_user_id()

    def get_room_data(self):
        res_data = ''
        for client in self.client_room:
            res_data += client.get_user_data()
            res_data += '|'

        if len(res_data) > 0:
            res_data = res_data[:-1:]
        return res_data

    def broadcast_message(self, conn, action_code, data):
        for client in self.client_room:
            if client != conn:
                client.send_in_loop(action_code, data)
                pass
        pass

    def quit_room(self, conn):
        """
        客户端在房间内断开连接时的处理
        :param conn:
        :return:
        """
        if conn == self.house_owner:
            RoomController.remove_room(self)
        else:
            self.client_room.remove(conn)

    def start_timer(self):
        TimerThread(self.run_timer, ()).start()
        pass

    def run_timer(self):
        time_count = 3
        time.sleep(1)
        while time_count:
            self.broadcast_message(None, ActionCode.SHOW_TIMER, str(time_count))
            time.sleep(1)
            time_count -= 1
        self.broadcast_message(None, ActionCode.START_PLAY, "r")

    def take_damage(self, conn, damage):
        is_die = False
        for client in self.client_room:
            if client != conn:
                if client.take_damage(damage):
                    is_die = True
        if not is_die:
            return None
        for client in self.client_room:
            if client.is_die():
                client.update_result(False)
                client.send_in_loop(ActionCode.GAME_OVER, str(ReturnCode.FAILURE))
            else:
                client.update_result(True)
                client.send_in_loop(ActionCode.GAME_OVER, str(ReturnCode.SUCCESS))
        self.close()


    def close(self):
        for client in self.client_room:
            client.room = None
        RoomController.remove_room(self)
        pass


class RoomController(BaseController):
    room_list = []

    def __init__(self):
        BaseController.__init__(self)
        self.request_code = RequestCode.ROOM

    def create_room(self, conn, data):
        new_room = Room()
        new_room.add_client(conn)
        RoomController.room_list.append(new_room)
        return str(ReturnCode.SUCCESS) + ',' + str(RoleType.BLUE)
        pass

    @classmethod
    def remove_room(cls, room):
        if len(cls.room_list) and room:
            cls.room_list.remove(room)

    @classmethod
    def get_room_by_id(cls, id):
        for room in cls.room_list:
            if room.get_id() == id:
                return room
        return None

    def list_room(self, conn, data):
        res_data = ''
        for room in self.room_list:
            if room.is_waiting_join():
                res_data += room.get_house_owner_data() + '|'
        if res_data == '':
            res_data += '0'
        else:
            res_data = res_data[:-1:]
        return res_data

    def join_room(self, conn, data):
        id = int(data)
        room = self.get_room_by_id(id)
        if not room:
            return str(ReturnCode.NOT_FOUND)
        elif not room.is_waiting_join():
            return str(ReturnCode.FAILURE)
        else:
            room.add_client(conn)
            room_data = room.get_room_data()
            room.broadcast_message(conn, ActionCode.UPDATE_ROOM, room_data)
            return str(ReturnCode.SUCCESS) + ',' + str(RoleType.RED) + '-' + room_data

    def quit_room(self, conn, data):
        # 房主退出
        room = conn.room
        if conn == room.house_owner:
            room.broadcast_message(conn, ActionCode.QUIT_ROOM, str(ReturnCode.SUCCESS))
            room.close()
            return str(ReturnCode.SUCCESS)
        else:
            room.broadcast_message(conn, ActionCode.UPDATE_ROOM, conn.room.get_room_data())
            room.remove_client(conn)
            return str(ReturnCode.SUCCESS)
