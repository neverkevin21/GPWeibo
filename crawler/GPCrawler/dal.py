#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
import settings


def get_insert_sql(table, keys):
    sql = 'INSERT INTO %s (%s) VALUES (%s)' % (
        table, ', '.join(keys), ', '.join(['%s'] * len(keys))
        )
    return sql


class MySQLDal(object):

    def __init__(self):
        self.mysql_db = MySQLdb.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DATABASE_NAME,
            user=settings.MYSQL_USER_NAME,
            passwd=settings.MYSQL_PASS_WORD,
            charset="utf8"
            )

    def insert(self, table, info):
        cursor = self.mysql_db.cursor()
        info.pop('contents')
        sql = get_insert_sql(table, info.keys())
        result = cursor.execute(sql, info.values())
        return result
