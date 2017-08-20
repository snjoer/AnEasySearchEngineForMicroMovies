import sqlite3
import numpy as np
from collections import Counter
from matplotlib import pyplot as plt

def connect(name):
    conn = sqlite3.connect(name)
    cursor = conn.cursor()
    return cursor

def getMinute(duration):
    arr = duration.split(':')
    length = len(arr)
    if length == 2:
        return int(arr[0])
    else:
        return 60 * int(arr[0]) + int(arr[1])

if __name__ == '__main__':
    db = 'Raw_Movie.db'
    cursor = connect(db)
    sql = 'select duration, like from VMovie'
    result = cursor.execute(sql)
    data = result.fetchall()
    # [<5, 5-10, 10-30, >30]
    duration = [0, 0, 0, 0]
    counts = [0, 0, 0, 0]
    for dur, like in data:
        if dur == None or like == None:
            continue
        minutes = getMinute(dur)
        if minutes < 5:
            duration[0] += like
            counts[0] += 1
        elif minutes < 10:
            duration[1] += like
            counts[1] += 1
        elif minutes < 30:
            duration[2] += like
            counts[2] += 1
        else:
            duration[3] += like
            counts[3] += 1
    for i in xrange(len(duration)):
        duration[i] /= counts[i]
    x_axis = ['< 5 min', '5 - 10 min', '10 - 30 min', '> 30 min']
    explode = (0, 0.1, 0, 0)
    plt.pie(duration, explode=explode, labels=x_axis, colors=('c', 'm', 'y', 'violet'), shadow=True, autopct='%1.1f %%', pctdistance=0.8, startangle=90)
    plt.title('Likes with respect to Vmovie length')

    plt.show()
