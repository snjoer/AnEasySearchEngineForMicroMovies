# -*- encoding:utf-8 -*-

import sys
import sqlite3
reload(sys)
sys.setdefaultencoding('utf-8')

def connect():
    conn = sqlite3.connect('SearchEngineDB.db')
    conn.text_factory = str 
    return conn

conn = connect()
cursor = conn.cursor()
with open(sys.argv[1], 'r') as f:
    lines = f.readlines()
    for line in lines:
        key = hash(unicode(''.join(line.split())))
        print ''.join(line.split())
        cursor.execute('delete from InvertedIndex where wordID = ' \
                        + str(key))
        cursor.execute('delete from ItemList where wordID = ' \
                        + str(key))
        conn.commit()
    conn.close()
