#!/usr/bin/env python27
# -*- coding: utf-8 -*-
# @Time    : 2021/1/22 17:23
# @Author  : handling
# @File    : result.py
# @Software: PyCharm

# 描述战绩信息
import logger


class Result:
    def __init__(self, id, user_id, total_count, win_count):
        self.id = id
        self.user_id = user_id
        self.total_count = total_count
        self.win_count = win_count
        pass


class ResultDAO:
    def __init__(self):
        pass

    @staticmethod
    def get_result_by_userid(mysql_conn, user_id):
        cursor = mysql_conn.cursor()
        sql = "select *from result where userid = {0}".format(user_id)
        try:
            cursor.execute(sql)
            result = cursor.fetchone()
            if result:
                if cursor:
                    cursor.close()
                # id,user_id, total_count, win_count
                return Result(result[0], result[1], result[2], result[2])
        except Exception as e:
            logger.simple_log('get_result_by_userid', user_id, 'error: unable to fecth data',e.message)
        finally:
            if cursor:
                cursor.close()
        return Result(-1, user_id, 0, 0)

    @staticmethod
    def update_or_add_result(mysql_conn, res):
        cursor = mysql_conn.cursor()
        try:
            if res.id <= -1:
                sql = "insert into result set totalcount='{0}', wincount='{1}', userid='{2}'".format(
                    res.total_count, res.win_count, res.user_id)
            else:
                sql = "update result set totalcount='{0}', wincount='{1}' where userid='{2}'".format(
                    res.total_count, res.win_count, res.user_id)
            cursor.execute(sql)
            mysql_conn.commit()
            if res.id <= -1:
                tmp_res = ResultDAO.get_result_by_userid(mysql_conn, res.user_id)
                res.id = tmp_res.id
        except Exception as e:
            logger.simple_log('update_or_add_result', res.id, 'error: unable to fecth data',e.message)
            mysql_conn.rollback()
        finally:
            if cursor:
                cursor.close()
