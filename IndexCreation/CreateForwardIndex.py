#!/usr/bin/env python
# -*- encoding:utf-8 -*-

import re
import sys
import csv
import jieba
import string
import sqlite3

reload(sys)
sys.setdefaultencoding('utf-8')

csv.field_size_limit(sys.maxsize)

# [[word_id, term, DF, Pointer], ...]
item_list = {}
# [[doc_id, word_id, NoH, [HL]], ...]
forward_index = {}

i = 0
jieba.load_userdict('dict.txt')
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
    select_sql = "select title, author, channel, content from VMovie;"
    data_table = rm_cursor.execute(select_sql)
    data = data_table.fetchall()
    rm_conn.close()
    for row in data:
        tt = row[0]
        at = row[1]
        ch = row[2]
        ct = row[3]
        if tt == None:
            tt = ''
        if at == None:
            at = ''
        if ch == None:
            ch = ''
        if ct == None:
            ct = ''
        doc_id = hash(tt)
        forward_index[doc_id] = []
        title = jieba.lcut_for_search(tt)
        author = jieba.lcut_for_search(at)
        genre = jieba.lcut_for_search(ch)
        content = jieba.lcut_for_search(ct)
        # add terms to _list
        _list = title + author + genre + content
        # analyze terms in _list
        for item in _list:
            # valid term (duplicate terms will be set as None)
            if item != None:
                re.sub(u"[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+", u'',item)
                item = ''.join(item.split())
                if item == '' or item in string.punctuation:
                    break
                word_id = hash(item)
                try:
                    item_list[word_id][1] += 1
                except KeyError:                                 
                    item_list[word_id] = [item, 1, word_id]                 
                forward_index[doc_id].append([word_id, 0, []])
                # find all item in _list
                while item != None:
                    # try to get its index
                    try:
                        idx = _list.index(item)
                    except ValueError:
                        break
                    # set to None
                    _list[idx] = None
                    # increase NoH according to related field
                    if item in title:
                        forward_index[doc_id][-1][1] += 4
                    elif item in author:
                        forward_index[doc_id][-1][1] += 3
                    elif item in genre:
                        forward_index[doc_id][-1][1] += 2
                    else:
                        forward_index[doc_id][-1][1] += 1
                    forward_index[doc_id][-1][2].append(idx)
        print i
        i += 1
    # write into database
    for key in item_list:
        se_cursor.execute("insert into ItemList values (?, ?, ?, ?)", \
                (key, item_list[key][0], item_list[key][1], item_list[key][2]))
    for key in forward_index:
        for item in forward_index[key]:
            se_cursor.execute("insert into InvertedIndex values (?, ?, ?, ?)",\
                (item[0], key, item[1], str(item[2])))
    se_conn.commit()
    se_conn.close()
