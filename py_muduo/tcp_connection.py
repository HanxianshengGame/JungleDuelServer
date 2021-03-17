# !/usr/bin/env Python2
# -*- coding: utf-8 -*-
# @Author   : 得灵
# @FILE     : tcp_connection.py
# @Time     : 2021/1/10 19:26
# @Software : PyCharm
# @Introduce: This is
from mysql_conn_helper import ConnHelper
from socket_message_handler import send_fixed_sz_data, MessageHandler, Flag
import sys

sys.path.append("..")
from model_dao.result import ResultDAO
from command_code import ActionCode


class TcpConnection:
    on_connection_callback = None
    on_message_callback = None
    on_close_callback = None

    def __init__(self, client_sock):
        self.__sock = client_sock
        self.__event_loop = None
        """
        IO socket 搭配epoll 一般是非阻塞+边缘触发ET
        """
        self.__sock.setblocking(False)
        self.__local_addr = client_sock.getsockname()
        self.__peer_addr = client_sock.getpeername()
        self.__msg_handler = MessageHandler()
        self.mysql_conn = ConnHelper.connect()

        self.user = None
        self.result = None
        self.room = None
        self.hp = 0
        pass

    def take_damage(self, damage):
        self.hp = max(self.hp - damage, 0)
        if self.hp <= 0:
            return True
        else:
            return False

    def update_result(self, is_victory):
        self.__update_result_to_db(is_victory)


    def __update_result_to_db(self, is_victory):
        self.result.total_count += 1
        if is_victory:
            self.result.win_count += 1
        ResultDAO.update_or_add_result(self.mysql_conn, self.result)
        pass

    def __update_result_to_client(self):
        self.send_in_loop((ActionCode.UPDATE_RESULT, '{0},{1}'.format(self.result.total_count, self.result.win_count)))
        pass


    def is_die(self):
        return self.hp <= 0

    def get_user_id(self):
        return self.user.id

    def set_user_data(self, user, result):
        self.user = user
        self.result = result
        pass

    def get_user_data(self):
        """
        :return: 用户名，总场数，胜利场数 字符串
        """
        return '{0},{1},{2},{3}'.format(self.user.id, self.user.user_name, self.result.total_count,
            self.result.win_count)

    def set_loop(self, event_loop):
        self.__event_loop = event_loop

    def recv_msg(self):
        while True:
            # 1. recv 如果本次接收时缓冲区无数据抛出异常，（errorno == 11）
            # 2. recv 如果本次接收时对端关闭返回None
            # 3. recv 如果接收的消息不足以解析，或者这边缓冲区仅有 4（11）+ 10，
            # 接收到存储到 msg_data 中，之后按1的处理，等待下次epollin的响应
            data = self.__sock.recv(Flag.BUFFER_SIZE)
            if not data:
                break
            self.__msg_handler.append_new_data(data)
            msgs = self.__msg_handler.decode_message_data()
            if len(msgs):
                return msgs, False
        return [], True

    def send_msg(self, msg):
        data = self.__msg_handler.encode_msg_data(msg)
        # send_fixed_sz_data(self.__sock, data)
        try:
            self.__sock.sendall(data)
        except BaseException as e:
            self.handle_close_callback()
            self.__event_loop.handle_conn_close(self.get_fd())


    def send_in_loop(self, msg):
        if self.__event_loop:
            self.__event_loop.run_in_loop(self.send_msg, msg)

    def close(self):
        if self.room:
            self.room.quit_room(self)
        ConnHelper.close_connection(self.mysql_conn)
        self.__sock.close()

    def get_peer_addr(self):
        return self.__peer_addr

    def get_fd(self):
        return self.__sock.fileno()

    def handle_message_callback(self):
        return TcpConnection.on_message_callback(self)

    def handle_connection_callback(self):
        TcpConnection.on_connection_callback(self)

    def handle_close_callback(self):
        TcpConnection.on_close_callback(self)
