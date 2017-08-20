#!/usr/bin/env python
# -*- encoding:utf-8 -*-

import re
import sys
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
#with open('vmovie.csv', 'r') as f:
#    reader = csv.reader(f)
    rm_conn = connect('Raw_Movie.db')
    rm_cursor = rm_conn.cursor()
    se_conn = connect('SearchEngineDB.db')
    se_cursor = se_conn.cursor()
    select_sql = "select title, author, time, channel, poster, link, content, rating, like, comment, duration, play  from VMovie;"
    data_table = rm_cursor.execute(select_sql)
    data = data_table.fetchall()
    rm_conn.close()
    for row in data:
        title = row[0]
        doc_id = hash(title)
        se_cursor.execute("insert into RawData values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", \
                (doc_id, row[0], row[1], row[2], row[3], row[4],\
                row[5], row[6], row[7], row[8], row[9], row[10], row[11]))
        print i
        i += 1
    se_conn.commit()
    se_conn.close()
