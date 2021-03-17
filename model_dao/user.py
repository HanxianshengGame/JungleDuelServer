# !/usr/bin/env Python2
# -*- coding: utf-8 -*-
# @Author   : 得灵
# @FILE     : user.py
# @Time     : 2021/1/17 20:14
# @Software : PyCharm
# @Introduce: This is
import logger


class User:
    def __init__(self, id, user_name, pass_word):
        self.id = id
        self.user_name = user_name
        self.pass_word = pass_word


class UserDAO:
    def __init__(self):
        pass

    @staticmethod
    def verify_user(mysql_conn, user_name, pass_word):
        cursor = mysql_conn.cursor()
        sql = "select *from user where username = '{0}' and password = '{1}'".format(user_name, pass_word)
        try:
            cursor.execute(sql)
            result = cursor.fetchone()
            if result:
                if cursor:
                    cursor.close()
                # id,username,password
                return User(result[0], result[1], result[2])

        except Exception as e:
            logger.simple_log(user_name, pass_word, 'error: unable to fecth data', e.message)
        if cursor:
            cursor.close()
        return None

    @staticmethod
    def get_user_by_username(mysql_conn, user_name):
        cursor = mysql_conn.cursor()
        sql = "select *from user where username = '{0}'".format(user_name)
        try:
            cursor.execute(sql)
            result = cursor.fetchone()
            if result:
                if cursor:
                    cursor.close()
                # id,username,password
                return True
        except Exception as e:
            logger.simple_log('get_user_by_username', user_name, 'error: unable to fecth data', e.message)
        finally:
            if cursor:
                cursor.close()
        return False

    @staticmethod
    def add_user(mysql_conn, user_name, pass_word):
        cursor = mysql_conn.cursor()
        sql = "insert into user set username = '{0}', password = '{1}'".format(user_name, pass_word)
        print user_name, pass_word
        try:
            cursor.execute(sql)
            mysql_conn.commit()
        except Exception as e:
            logger.simple_log('add_user throw exception', user_name, e.message)
            mysql_conn.rollback()
        finally:
            if cursor:
                cursor.close()
