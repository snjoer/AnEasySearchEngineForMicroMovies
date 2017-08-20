#!/usr/bin/env python
# -*- encoding:utf-8 -*-

import re
import sys
import csv
import math
import string
import sqlite3

reload(sys)
sys.setdefaultencoding('utf-8')

i = 0
def connect(data_base):
    conn = sqlite3.connect(data_base)
    conn.text_factory = str
    return conn

if __name__ == '__main__':
    conn = connect('SearchEngineDB.db')
    cursor = conn.cursor()
    sql = "select * from DocSqrtSum"
    result = cursor.execute(sql)
    data = result.fetchall()
    i = 0
    for docID, value in data:
        sql = 'update InvertedIndex set SqrtSum = %s where docID = %s' % (value, docID)
        cursor.execute(sql)
        print i
        i += 1
    conn.commit()
    conn.close()
