#!/usr/bin/env python
# -*- encoding:utf-8 -*-

import json
import redis
import sqlite3

def connectSqlite():
    conn = sqlite3.connect('Raw_Movie.db')
    conn.text_factory = str 
    return conn

if __name__ == '__main__':
    r = redis.Redis(host='localhost', port=6379)
    conn = connectSqlite()
    cursor = conn.cursor()
    while True:
        try:
            source, data = r.blpop(['XinLink:items'],\
                    timeout=1)
        except:
            break
        item = json.loads(data)
        cursor.execute('insert into VMovie values (?,?,?,?,?,?,?,?,?,?,?,?)',
            (item['title'], item['author'], item['time']\
            ,item['channel'], item['poster'], item['link']\
            ,item['content'], item['rating'], item['like']\
            ,item['comment'], item['duration'], item['play']))
        conn.commit()
    conn.close()
