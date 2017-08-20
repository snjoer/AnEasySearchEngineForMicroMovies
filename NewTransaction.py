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

jieba.load_userdict('dict.txt')

channel_list = ['*', '动画', '励志', '剧情', '生活', '旅行', '音乐', '搞笑', '运动', '科幻', '爱情']
year_list = ['*', '2017', '2016', '2015', '2014', '2013', '2012', '2011']
duration = []

def connect():
    conn = sqlite3.connect('SearchEngineDB.db')
    conn.text_factory = str
    return conn

def getResult(query, rank, channel, year, duration):
    _list = jieba.lcut_for_search(query)
    _list = [x for x in _list if x != ' ']
    # sort input terms and construct a dictionary
    searchDict = Counter(_list)
    # get frequency list
    termVec = searchDict.values()
    # get term list
    terms = searchDict.keys()
    docIDs = {}
    docSqrtSum = {}
    conn = connect()
    cursor = conn.cursor()
    
    for i in xrange(len(terms)):
        term = terms[i]
        termID = hash(term)
        result = cursor.execute("select docID, NoH, SqrtSum \
                from InvertedIndex where wordID = '%s' \
                order by NoH DESC;" % termID)
        docs = result.fetchall()
        # for every doc, cal corresponding frequency for given position
        for doc in docs:
            docID, NoH, sqrtSum = doc
            try:
                docIDs[docID][i] = NoH
            except:
                docIDs[docID] = [0] * len(terms)
                docIDs[docID][i] = NoH
                docSqrtSum[docID] = sqrtSum
    rankDict = {}
    # calculate cosine similarity
    for k, v in docIDs.iteritems():
        rankDict[k] = sum(x * y for (x, y) in zip(termVec, v)) / \
                (math.sqrt(sum(x*x for x in termVec)) * docSqrtSum[k])
    # sort by cosine similarity
    sortedRankDict = sorted(rankDict.items(), key=operator.itemgetter(1), reverse=True)
    retv = []
    for docID, fre in sortedRankDict:
        # get info of given docID
        data = cursor.execute("select title, link, poster, author,\
                time, content, play , rating, like, comment, channel, duration from RawData where docID = %s;" % docID)
        result = data.fetchall()
        # dismiss vmovie whose duration is None
        if result[0][11] == None:
            continue
        # select by channel, year and duration
        if channel != 1:
            if channel_list[channel-1] != result[0][10]:
                continue
        if year != 0:
            if str(year) != result[0][4].split('-')[0]:
                continue
        if duration != 1:
            if duration == None:
                continue
            if duration == 2:
                if getMinute(result[0][11]) >= 5:
                    continue
                else:
                    pass
            if duration == 3:
                dur = getMinute(result[0][11])
                if dur < 5 or dur >= 10:
                    continue
                else:
                    pass
            if duration == 4:
                dur = getMinute(result[0][11])
                if dur < 10 or dur >= 30:
                    continue
                else:
                    pass
            if duration == 5:
                dur = getMinute(result[0][11])
                if dur < 30:
                    continue
        content = result[0][5]
        # cut content shorter to adapt poster
        if len(content) > 900:
            content = unicode(content[0:897] + '...', errors='ignore')
        # sort data
        if rank == 1:
            insertDataByDefault(result, content, retv)
        else:
            insertDataByAttribution(result, content, retv, 0, len(retv) - 1, rank + 4)
    return _list, retv

def insertDataByDefault(result, content, retv):
    retv.append([result[0][0], result[0][1], result[0][2], result[0][3],\
        result[0][4], content, result[0][6], result[0][7], result[0][8],\
        result[0][9], result[0][10], result[0][11]])
    return

def insertDataByAttribution(result, content, retv, fst, lst, rank):
    # trivial situation
    if retv == [] or result[0][rank] == None:
        insertDataByDefault(result, content, retv)
        return
    while fst <= lst:
        # get middle point
        mid = (fst + lst) // 2
        if mid == lst:
            # insert to after if less than
            if retv[mid][rank] != None  and float(retv[mid][rank]) >= \
                    float(result[0][rank]):
                retv.insert(mid+1, [result[0][0], result[0][1], result[0][2], result[0][3],\
                        result[0][4], content, result[0][6], result[0][7], result[0][8],\
                        result[0][9], result[0][10], result[0][11]])
            # else insert before
            else:
                retv.insert(mid, [result[0][0], result[0][1], result[0][2], result[0][3],\
                        result[0][4], content, result[0][6], result[0][7], result[0][8],\
                        result[0][9], result[0][10], result[0][11]])
            return
        # replace if equal to middle 
        if retv[mid][rank] != None and float(retv[mid][rank]) == \
                float(result[0][rank]):
            # not stable
            retv.insert(mid+1, [result[0][0], result[0][1], result[0][2], result[0][3],\
                    result[0][4], content, result[0][6], result[0][7], result[0][8],\
                    result[0][9], result[0][10], result[0][11]])
            return
        # if bigger than mid then lst becomes mid
        elif retv[mid][rank] == None or float(retv[mid][rank]) \
                < float(result[0][rank]):
            lst = mid - 1
        else:
            fst = mid + 1
    return

def getMinute(duration):
    arr = duration.split(':')
    if len(arr) == 2:
        return int(arr[0])
    else:
        return int(arr[0]) * 60 + int(arr[1])
