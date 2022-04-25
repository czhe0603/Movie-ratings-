from bs4 import BeautifulSoup
import requests
import re
import sqlite3
import os
import json
from pylab import *
from matplotlib import pyplot as plt
import numpy as np
import csv


name = []
score = []
year = []
def put_info_into_lists():
    url = "https://stacker.com/stories/1587/100-best-movies-all-time"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    table = soup.find_all('h2', class_ = 'ct-slideshow__slide__text-container__caption')
    for item in table[1:]:
        reg_exp = '\((\d{4})\)'
        reg_exp2 = '(?:[A-Za-z:\'·]+\s)+'
        year.append(re.findall(reg_exp, item.text.strip())[0].strip())
        name.append(re.findall(reg_exp2, item.text.strip())[0].strip())
    table_score = soup.find_all('div', class_ = "ct-slideshow__slide__text-container__description")
    for item in table_score[1:]:
        reg_exp = 'Stacker score: (\S+)'
        score.append(float(re.findall(reg_exp, item.text.strip())[0])/10)
    name.reverse()
    score.reverse()
    year.reverse()
    
def setUpDatabase():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+'movies.db')
    cur = conn.cursor()
    return cur, conn

def setUpStackerTable(cur, conn):
    cur.execute('DROP TABLE IF EXISTS Stacker')
    cur.execute('CREATE TABLE IF NOT EXISTS Stacker(name TEXT, score NUMERIC(3,1), year INTEGER)')
    for i in range(25):
        cur.execute('INSERT OR IGNORE INTO Stacker(name, score, year) VALUES (?,?,?)', (name[i], score[i], year[i]))
    for j in range(25, 50):
        cur.execute('INSERT OR IGNORE INTO Stacker(name, score, year) VALUES (?,?,?)', (name[j], score[j], year[j]))
    for k in range(50, 75):
        cur.execute('INSERT OR IGNORE INTO Stacker(name, score, year) VALUES (?,?,?)', (name[k], score[k], year[k]))
    for g in range(75, 100):
        cur.execute('INSERT OR IGNORE INTO Stacker(name, score, year) VALUES (?,?,?)', (name[g], score[g], year[g]))   
    conn.commit()

name1 = []
score1 = []
year1 = []

def loop_for_five(new_url):
    url=new_url
    payload = {}
    headers= {}
    response = requests.request("GET", url, headers=headers, data = payload)
    new=json.loads(response.text)
    for i in new['results']:
        name1.append(i['title'])
        score1.append(str(i['vote_average']))
        regx_str="\d{4}"
        year1.append(re.findall(regx_str,i['release_date'])[0])

def put_api_1_into_lists():
    url_1 = "https://api.themoviedb.org/3/movie/top_rated?api_key=b43896c051c7b6aaa71f92ebe105fe08&language=en-US&page=1"
    url_2 = "https://api.themoviedb.org/3/movie/top_rated?api_key=b43896c051c7b6aaa71f92ebe105fe08&language=en-US&page=2"
    url_3 = "https://api.themoviedb.org/3/movie/top_rated?api_key=b43896c051c7b6aaa71f92ebe105fe08&language=en-US&page=3"
    url_4 = "https://api.themoviedb.org/3/movie/top_rated?api_key=b43896c051c7b6aaa71f92ebe105fe08&language=en-US&page=4"
    url_5 = "https://api.themoviedb.org/3/movie/top_rated?api_key=b43896c051c7b6aaa71f92ebe105fe08&language=en-US&page=5"
    url_6 = "https://api.themoviedb.org/3/movie/top_rated?api_key=b43896c051c7b6aaa71f92ebe105fe08&language=en-US&page=6"
    url_7 = "https://api.themoviedb.org/3/movie/top_rated?api_key=b43896c051c7b6aaa71f92ebe105fe08&language=en-US&page=7"
    url_8 = "https://api.themoviedb.org/3/movie/top_rated?api_key=b43896c051c7b6aaa71f92ebe105fe08&language=en-US&page=8"
    url_9 = "https://api.themoviedb.org/3/movie/top_rated?api_key=b43896c051c7b6aaa71f92ebe105fe08&language=en-US&page=9"
    url_10 = "https://api.themoviedb.org/3/movie/top_rated?api_key=b43896c051c7b6aaa71f92ebe105fe08&language=en-US&page=10"
    loop_for_five(url_1)
    loop_for_five(url_2)
    loop_for_five(url_3)
    loop_for_five(url_4)
    loop_for_five(url_5)
    loop_for_five(url_6)
    loop_for_five(url_7)
    loop_for_five(url_8)
    loop_for_five(url_9)
    loop_for_five(url_10)


def setUpTMDBTable(cur, conn):
    cur.execute('DROP TABLE IF EXISTS TMDB')
    cur.execute('CREATE TABLE IF NOT EXISTS TMDB(name TEXT, score NUMERIC(3,1), year INTEGER)')
    for i in range(25):
        cur.execute('INSERT OR IGNORE INTO TMDB(name, score, year) VALUES (?,?,?)', (name1[i], score1[i], year1[i]))
    for j in range(25, 50):
        cur.execute('INSERT OR IGNORE INTO TMDB(name, score, year) VALUES (?,?,?)', (name1[j], score1[j], year1[j]))
    for k in range(50, 75):
        cur.execute('INSERT OR IGNORE INTO TMDB(name, score, year) VALUES (?,?,?)', (name1[k], score1[k], year1[k]))
    for g in range(75, 100):
        cur.execute('INSERT OR IGNORE INTO TMDB(name, score, year) VALUES (?,?,?)', (name1[g], score1[g], year1[g]))  
    for i in range(100,125):
        cur.execute('INSERT OR IGNORE INTO TMDB(name, score, year) VALUES (?,?,?)', (name1[i], score1[i], year1[i]))
    for j in range(125, 150):
        cur.execute('INSERT OR IGNORE INTO TMDB(name, score, year) VALUES (?,?,?)', (name1[j], score1[j], year1[j]))
    for k in range(150, 175):
        cur.execute('INSERT OR IGNORE INTO TMDB(name, score, year) VALUES (?,?,?)', (name1[k], score1[k], year1[k]))
    for g in range(175, 200):
        cur.execute('INSERT OR IGNORE INTO TMDB(name, score, year) VALUES (?,?,?)', (name1[g], score1[g], year1[g])) 
    conn.commit()

name2 = []
score2 = []
year2 = []
def put_api_2_into_lists():
    url = "https://imdb-api.com/en/API/Top250Movies/k_91qzf1h3"
    payload = {}
    headers= {}
    response = requests.request("GET", url, headers=headers, data = payload)
    new=json.loads(response.text)
    regex_str="(.+) "
    for i in new['items']:
        name2.append(re.findall(regex_str,i['fullTitle'])[0])
        score2.append(i['imDbRating'])
        year2.append(i['year'])



def setUpIMDBTable(cur, conn):
    cur.execute('DROP TABLE IF EXISTS IMDB')
    cur.execute('CREATE TABLE IF NOT EXISTS IMDB(name TEXT, year INTEGER, score NUMERIC(3,1))')
    for i in range(25):
        cur.execute('INSERT OR IGNORE INTO IMDB(name, score, year) VALUES (?,?,?)', (name2[i], score2[i], year2[i]))
    for j in range(25, 50):
        cur.execute('INSERT OR IGNORE INTO IMDB(name, score, year) VALUES (?,?,?)', (name2[j], score2[j], year2[j]))
    for k in range(50, 75):
        cur.execute('INSERT OR IGNORE INTO IMDB(name, score, year) VALUES (?,?,?)', (name2[k], score2[k], year2[k]))
    for g in range(75, 100):
        cur.execute('INSERT OR IGNORE INTO IMDB(name, score, year) VALUES (?,?,?)', (name2[g], score2[g], year2[g]))  
    for i in range(100,125):
        cur.execute('INSERT OR IGNORE INTO IMDB(name, score, year) VALUES (?,?,?)', (name2[i], score2[i], year2[i]))
    for j in range(125, 150):
        cur.execute('INSERT OR IGNORE INTO IMDB(name, score, year) VALUES (?,?,?)', (name2[j], score2[j], year2[j]))
    for k in range(150, 175):
        cur.execute('INSERT OR IGNORE INTO IMDB(name, score, year) VALUES (?,?,?)', (name2[k], score2[k], year2[k]))
    for g in range(175, 200):
        cur.execute('INSERT OR IGNORE INTO IMDB(name, score, year) VALUES (?,?,?)', (name2[g], score2[g], year2[g])) 
    for k in range(200, 225):
        cur.execute('INSERT OR IGNORE INTO IMDB(name, score, year) VALUES (?,?,?)', (name2[k], score2[k], year2[k]))
    for g in range(225, 250):
        cur.execute('INSERT OR IGNORE INTO IMDB(name, score, year) VALUES (?,?,?)', (name2[g], score2[g], year2[g])) 
    conn.commit()

name3 = []
year3 = []
def put_api_3_into_lists():
    url = "https://imdb-api.com/en/API/MostPopularMovies/k_7ftqef3a"
    payload = {}
    headers= {}
    response = requests.request("GET", url, headers=headers, data = payload)
    new=json.loads(response.text)
    
    for i in new['items']:
        name3.append(i['title'])
        year3.append(i['year'])
         

def setUpPopTable(cur, conn):
    cur.execute('DROP TABLE IF EXISTS Pop')
    cur.execute('CREATE TABLE IF NOT EXISTS Pop(name TEXT, year INTEGER)')
    for i in range(25):
        cur.execute('INSERT OR IGNORE INTO Pop(name, year) VALUES (?,?)', (name3[i], year3[i]))
    for j in range(25, 50):
        cur.execute('INSERT OR IGNORE INTO Pop(name, year) VALUES (?,?)', (name3[j], year3[j]))
    for k in range(50, 75):
        cur.execute('INSERT OR IGNORE INTO Pop(name, year) VALUES (?,?)', (name3[k], year3[k]))
    for g in range(75, 100):
        cur.execute('INSERT OR IGNORE INTO Pop(name, year) VALUES (?,?)', (name3[g], year3[g]))  
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

def writeTable(cur, conn, file_name):
    cur.execute('SELECT * FROM Ave_Table')
    data = cur.fetchall()
    MyFile = open(file_name, 'w', newline = '')
    with MyFile:
        write = csv.writer(MyFile)
        header = ["Name", "Year", "Average_Score"]
        write.writerow(header)
        write.writerows(data)

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
  

    
def main():
    put_info_into_lists()
    cur,conn = setUpDatabase()
    setUpStackerTable(cur, conn)

    put_api_1_into_lists()
    setUpTMDBTable(cur, conn)

    put_api_2_into_lists()
    setUpIMDBTable(cur, conn)

    JoinTables(cur, conn)

    Average(cur, conn)

    linechart(cur, conn)
    bar_chart(cur, conn)

    put_api_3_into_lists()
    setUpPopTable(cur, conn)
    PopAndTop(cur, conn)

    writeTable(cur, conn, 'outfile.csv')




main()
    


