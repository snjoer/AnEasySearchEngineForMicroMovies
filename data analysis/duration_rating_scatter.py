import sqlite3
from collections import Counter
from matplotlib import pyplot as plt
from pylab import *
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

xmajorLocator = MultipleLocator(10)
xmajorFormatter = FormatStrFormatter('%1.1f')
xminorLocator = MultipleLocator(2)

ymajorLocator = MultipleLocator(1)
ymajorFormatter = FormatStrFormatter('%1.1f')
yminorLocator = MultipleLocator(0.2)

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
    sql = 'select duration, rating from VMovie'
    result = cursor.execute(sql)
    data = result.fetchall()
    minute = []
    rate = []
    for dur, rating in data:
        if dur == None or rating == None:
            continue
        minutes = getMinute(dur)
        minute.append(minutes)
        rate.append(rating)
    ax = subplot(111)
    plt.scatter(minute, rate, s=10)
    
    ax.xaxis.set_major_locator(xmajorLocator)
    ax.xaxis.set_major_formatter(xmajorFormatter)

    ax.yaxis.set_major_locator(ymajorLocator)
    ax.yaxis.set_major_formatter(ymajorFormatter)

    ax.xaxis.set_minor_locator(xminorLocator)
    ax.yaxis.set_minor_locator(yminorLocator)
    
    ax.xaxis.grid(True, which='major')
    ax.yaxis.grid(True, which='minor')

    plt.xlabel('Vmovie Length')
    plt.ylabel('Rating')
    plt.title('Rating with respect to Vmovie length')

    plt.show()
