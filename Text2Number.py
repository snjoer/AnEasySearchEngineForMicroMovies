#!/usr/bin/env python
# -*- encoding:utf-8 -*-

import sys
import math
import jieba
import sqlite3
import operator
from collections import Counter

reload(sys)
sys.setdefaultencoding('utf-8')


def connect():
    conn = sqlite3.connect('SearchEngineDB.db')
    conn.text_factory = str
    return conn

def text2number(_type):
    conn = connect()
    cursor = conn.cursor()
    sql = 'select docID, %s from RawData;' % _type
    result = cursor.execute(sql)
    data = result.fetchall()
    i = 0
    for docID, num in data:
        if num != None and ',' in num:
            num = num.replace(',', '')
            sql = "update RawData set play = %s where docID = %s" % (num, docID)
            cursor.execute(sql)
        print i
        i += 1
    conn.commit()
    conn.close()

text2number('like')
text2number('comment')
