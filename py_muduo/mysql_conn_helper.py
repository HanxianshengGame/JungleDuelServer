# !/usr/bin/env Python2
# -*- coding: utf-8 -*-
# @Author   : 得灵
# @FILE     : mysql_conn_helper.py
# @Time     : 2021/1/16 19:04
# @Software : PyCharm
# @Introduce: This is
import MySQLdb


class ConnHelper:
    host = 'localhost'
    user_name = 'root'
    pass_word = '525907'
    database = 'jungle_duel'
    port = 3306
    charset = 'utf8'

    def __init__(self):
        self.__cursor = None
        pass

    @classmethod
    def connect(cls):
        mysql_conn = MySQLdb.connect(cls.host,
                                     cls.user_name,
                                     cls.pass_word,
                                     cls.database,
                                     cls.port,
                                     charset=cls.charset)
        return mysql_conn

    @classmethod
    def close_connection(cls, mysql_conn):
        if mysql_conn:
            mysql_conn.close()
