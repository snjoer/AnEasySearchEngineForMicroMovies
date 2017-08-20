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

def getRatingData():
    conn = connect()
    cursor = conn.cursor()
    # get sorted data from database
    data = cursor.execute("SELECT title, link , rating FROM RawData ORDER BY rating DESC limit 30;")
    retv = []
    results = data.fetchall()
    # parse and add data to return list
    for title, link, rating in results:
        retv.append([title, link, rating])
    return retv

def getLikeData():
    conn = connect()
    cursor = conn.cursor()
    # get sorted data from database
    data = cursor.execute("SELECT title, link , like FROM RawData ORDER BY like DESC limit 30;")
    retv = []
    results = data.fetchall()
    # parse and add data to return list
    for title, link, like in results:
        retv.append([title, link, like])                                                                                    
    return retv

def getPlayData():
    conn = connect()
    cursor = conn.cursor()
    #get sorted data from database
    data = cursor.execute("SELECT title, link , play FROM RawData ORDER BY play DESC limit 30;")
    retv = []
    results = data.fetchall()
    # parse and add data to return list
    for title, link, play in results:
        retv.append([title, link, play])                                                                                        
    return retv
