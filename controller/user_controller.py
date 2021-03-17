# !/usr/bin/env Python2
# -*- coding: utf-8 -*-
# @Author   : 得灵
# @FILE     : user_controller.py
# @Time     : 2021/1/21 22:16
# @Software : PyCharm
# @Introduce: This is
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from base_controller import BaseController
from command_code import RequestCode, ReturnCode
from model_dao.user import User, UserDAO
from model_dao.result import Result, ResultDAO


class UserController(BaseController):
    def __init__(self):
        BaseController.__init__(self)
        self.request_code = RequestCode.USER
        self.user_dao = User

    def login(self, conn, data):
        # 关于登录账号密码以 , 分割
        user_name, password = data.split(',')
        user = UserDAO.verify_user(conn.mysql_conn, user_name, password)

        if not user:
            return str(ReturnCode.FAILURE)
        else:
            res = ResultDAO.get_result_by_userid(conn.mysql_conn, user.id)
            conn.set_user_data(user, res)
            return '{0},{1},{2},{3}'.format(str(ReturnCode.SUCCESS), user.user_name,
            res.total_count, res.win_count)

    def register(self, conn, data):
        # 关于登录账号密码以 , 分割
        user_name, password = data.split(',')
        result = UserDAO.get_user_by_username(conn.mysql_conn, user_name)
        if result:
            return str(ReturnCode.FAILURE)
        UserDAO.add_user(conn.mysql_conn, user_name, password)
        return str(ReturnCode.SUCCESS)
