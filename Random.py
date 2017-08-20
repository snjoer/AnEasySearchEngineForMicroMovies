#!/usr/bin/env python
# -*- encoding:utf-8 -*-

import sys
import jieba
import sqlite3
from collections import Counter

reload(sys)
sys.setdefaultencoding('utf-8')

jieba.load_userdict('dict.txt')

def connect():
    conn = sqlite3.connect('SearchEngineDB.db')
    conn.text_factory = str
    return conn

def getRandomData():
    conn = connect()
    cursor = conn.cursor()
    data = cursor.execute("SELECT title, link, poster, author,\
            time, content, play , rating, like, comment, channel, duration \
            FROM RawData ORDER BY RANDOM() limit 10;")
    retv = []
    results = data.fetchall()
    for result in results:
        content = result[5]
        if result[11] == None:
            continue
        if len(content) > 900:
            content = unicode(content[0:897] + '...', errors='ignore')
        retv.append([result[0], result[1], result[2], result[3],\
                result[4], content, result[6], result[7], result[8], \
                result[9], result[10], result[11]])
    return retv
