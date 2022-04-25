from bs4 import BeautifulSoup
import requests
import re
import sqlite3
import os
import json
from pylab import *
from matplotlib import pyplot as plt
import numpy as np
from wordcloud import WordCloud
import csv

def setUpDatabase():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+'movies.db')
    cur = conn.cursor()
    return cur, conn

def JoinTables(cur, conn):
    cur.execute('DROP TABLE IF EXISTS All_Table')
    cur.execute('SELECT Stacker.name, Stacker.score, Stacker.year, IMDB.score FROM Stacker JOIN IMDB ON Stacker.name = IMDB.name')
    a_list = cur.fetchall()
    cur.execute('SELECT Stacker.name, Stacker.score, Stacker.year, TMDB.score FROM Stacker JOIN TMDB ON TMDB.name = Stacker.name')
    b_list = cur.fetchall()
    cur.execute('CREATE TABLE IF NOT EXISTS All_Table(name TEXT, year INTEGER, score1 NUMERIC(3,1), score2 NUMERIC(3,1), score3 NUMERIC(3,1))')
    
    for i in a_list:
        for j in b_list:
            if i[0] == j[0]:
                cur.execute('INSERT OR IGNORE INTO All_Table(name, year, score1, score2, score3) VALUES (?,?,?,?,?)', (i[0], i[2], i[1], i[3], j[3]))
    conn.commit()



def Average(cur, conn):
    cur.execute('DROP TABLE IF EXISTS Ave_Table')
    cur.execute(
        """
        SELECT (score1 + score2 + score3) / 3
        FROM All_Table
        """
    )
    a_list = cur.fetchall()
    cur.execute('CREATE TABLE IF NOT EXISTS Ave_Table(name TEXT, year INTEGER, average_score NUMERIC(3,1))')
    cur.execute('SELECT name, year FROM All_Table')
    b_list = cur.fetchall()
    for i in range(28):
        cur.execute('INSERT OR IGNORE INTO Ave_Table VALUES (?,?,?)', (b_list[i][0], b_list[i][1], a_list[i][0]))
    
    conn.commit()

def PopAndTop(cur, conn):
    cur.execute('SELECT Pop.name, Pop.year FROM Pop JOIN IMDB ON Pop.name = IMDB.name')
    pop_list = cur.fetchall()

    label = ["In the Most Popular Movies List", "Not in the Most Popular Movies List"]

    temp = [len(pop_list), 250 - len(pop_list)]
    fig = plt.figure(figsize = (10, 7))
    explode = (0.1, 0)
    plt.pie(temp, explode = explode, labels = label, autopct = '%1.1f%%')
    plt.title('Most Popular Moives in Top 250 Moives')
    plt.show()

def writeTable(cur, conn, file_name):
    cur.execute('SELECT * FROM Ave_Table')
    data = cur.fetchall()
    MyFile = open(file_name, 'w', newline = '')
    with MyFile:
        write = csv.writer(MyFile)
        header = ["Name", "Year", "Average_Score"]
        write.writerow(header)
        write.writerows(data)


def Ave(lst):
    return sum(lst) / len(lst)

def linechart(cur, conn):
     cur.execute('SELECT average_score FROM Ave_Table WHERE year >= 1925 AND year < 1950')
     a_list = cur.fetchall()
     cur.execute('SELECT average_score FROM Ave_Table WHERE year >= 1950 AND year < 1975')
     b_list = cur.fetchall()
     cur.execute('SELECT average_score FROM Ave_Table WHERE year >= 1975 AND year < 2000')
     c_list = cur.fetchall()
     cur.execute('SELECT average_score FROM Ave_Table WHERE year >= 2000 AND year < 2025')
     d_list = cur.fetchall()
     conn.commit()
     ave_list = []
     ave_list.append(Ave(a_list))
     ave_list.append(Ave(b_list))
     ave_list.append(Ave(c_list))
     ave_list.append(Ave(d_list))

    
     year = ['1925-1950', '1950-1975', '1975-2000', '2000-2025']
     
     plot(year, ave_list)

     xlabel('Years')
     ylabel('Scores')
     title('Average Score of Moives in 4 Periods')
  
     grid(True)
     show()

     temp = [len(a_list), len(b_list), len(c_list), len(d_list)]
     fig = plt.figure(figsize = (10, 7))
     explode = (0, 0, 0, 0.1)
     plt.pie(temp, explode = explode, labels = year, autopct = '%1.1f%%')
     plt.title('Distribution of Moives in 4 Periods')
     plt.show()

def bar_chart(cur,conn):
    cur.execute('SELECT year,average_score FROM Ave_Table')
    b_list = cur.fetchall()
    y=[]
    for movie in b_list:
        y.append(movie[1])
    x=[movie[0] for movie in b_list]
    plt.bar(x,y)
    plt.ylabel("Scores")
    plt.xlabel("Years")
    plt.ylim(8,10)
    plt.title("Average score/Years for Movies")
    plt.show()
   
    
def word_cloud(cur, conn):
    d = {}
    cur.execute('SELECT name FROM Ave_Table')
    name = cur.fetchall()
    cur.execute('SELECT average_score FROM Ave_Table')
    avg = cur.fetchall()
    for i in range(28):
        d[name[i][0]] = avg[i][0]
    wordcloud = WordCloud()
    wordcloud.generate_from_frequencies(frequencies=d)
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()

def main():
    cur,conn = setUpDatabase()
    JoinTables(cur, conn)

    Average(cur, conn)
    writeTable(cur, conn, 'outfile.csv')

    linechart(cur, conn)
    bar_chart(cur, conn)
    word_cloud(cur, conn)

    PopAndTop(cur, conn)

main()