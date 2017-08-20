import numpy as np
import sqlite3
from collections import *
from matplotlib import pyplot as plt

def connect(name):
    conn = sqlite3.connect(name)
    cursor = conn.cursor()
    return cursor

if __name__ == '__main__':
    db = 'Raw_Movie.db'
    cursor = connect(db)
    sql = 'select time from VMovie'
    result = cursor.execute(sql)
    dates = result.fetchall()
    year = []
    for date in dates:
        year.append(date[0].split('-')[0])
    yearDict = Counter(year)
    od = OrderedDict(sorted(yearDict.items()))
    years = [int(x) for x in od.keys()]
    numbers = [int(y) for y in od.values()]
#    plt.pie(sizes, labels=labels,colors=('b', 'g', 'r', 'c', 'm', 'y', 'violet'), shadow=True, autopct='%1.1f %%', pctdistance=0.8)
    y_pos = np.arange(len(years))
    plt.bar(y_pos, numbers, align='center', alpha=0.5)
    plt.xticks(y_pos, years)
    plt.ylabel('counts')
    plt.title('VMovie counts in terms of year')
    plt.show()
