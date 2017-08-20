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
    sql = 'select duration from VMovie'
    result = cursor.execute(sql)
    data = result.fetchall()
    # [<5, 5-10, 10-30, >30]
    duration = [0, 0, 0, 0]
    for dur in data:
        if dur[0] == None:
            continue
        minutes = getMinute(dur[0])
        if minutes < 5:
            duration[0] += 1
        elif minutes < 10:
            duration[1] += 1
        elif minutes < 30:
            duration[2] += 1
        else:
            duration[3] += 1
    print duration
    x_axis = ['< 5 min', '5 - 10 min', '10 - 30 min', '> 30 min']
    y_pos = np.arange(len(x_axis))
    plt.barh(y_pos, duration, align="center", alpha=0.5)
    plt.title('Views with respect to Vmovie length')
    plt.yticks(y_pos, x_axis)
    plt.xlabel('Views')
    plt.ylabel('Vmovie Length')

    plt.show()
