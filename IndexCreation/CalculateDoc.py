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
    sql = "select distinct(docID) from InvertedIndex;"
    data_table = cursor.execute(sql)
    data = data_table.fetchall()
    i = 0
    for docID in data:
        sql = "select NoH from InvertedIndex where docID = %s" % docID[0]
        NoHs = cursor.execute(sql) 
        NoHs = NoHs.fetchall()
        NoHList = []
        for NoH in NoHs:
            NoHList.append(NoH[0])
        value = math.sqrt(sum(x * x for x in NoHList))
        cursor.execute("insert into DocSqrtSum values (?, ?)",\
                (docID[0], value))
        print i
        i += 1
    conn.commit()
    conn.close()
