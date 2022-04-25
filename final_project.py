
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
    cur.execute('CREATE TABLE IF NOT EXISTS Stacker(name TEXT, score NUMERIC(3,1), year INTEGER)')
    cur.execute('SELECT COUNT(name) FROM Stacker')
    
    max_num = int(cur.fetchone()[0])
    
    if max_num < 100:
        for i in range(max_num, max_num + 25):
           cur.execute('INSERT OR IGNORE INTO Stacker(name, score, year) VALUES (?,?,?)', (name[i], score[i], year[i]))
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
    
    cur.execute('CREATE TABLE IF NOT EXISTS TMDB(name TEXT, score NUMERIC(3,1), year INTEGER)')
    cur.execute('SELECT COUNT(name) FROM TMDB')
    max_num = int(cur.fetchone()[0])
    
    if max_num < 200:
        for i in range(max_num, max_num + 25):
           cur.execute('INSERT OR IGNORE INTO TMDB(name, score, year) VALUES (?,?,?)', (name1[i], score1[i], year1[i]))
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
    
    cur.execute('CREATE TABLE IF NOT EXISTS IMDB(name TEXT, year INTEGER, score NUMERIC(3,1))')
    cur.execute('SELECT COUNT(name) FROM IMDB')
    max_num = int(cur.fetchone()[0])
    
    if max_num < 250:
        for i in range(max_num, max_num + 25):
           cur.execute('INSERT OR IGNORE INTO IMDB(name, score, year) VALUES (?,?,?)', (name2[i], score2[i], year2[i]))
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
    
    cur.execute('CREATE TABLE IF NOT EXISTS Pop(name TEXT, year INTEGER)')
    cur.execute('SELECT COUNT(name) FROM Pop')
    max_num = int(cur.fetchone()[0])
    
    if max_num < 100:
        for i in range(max_num, max_num + 25):
           cur.execute('INSERT OR IGNORE INTO Pop(name, year) VALUES (?,?)', (name3[i], year3[i]))
    conn.commit()
  
def main():
    put_info_into_lists()
    cur,conn = setUpDatabase()
    setUpStackerTable(cur, conn)

    put_api_1_into_lists()
    setUpTMDBTable(cur, conn)

    put_api_2_into_lists()
    setUpIMDBTable(cur, conn)

    put_api_3_into_lists()
    setUpPopTable(cur, conn)
    
main()
    


