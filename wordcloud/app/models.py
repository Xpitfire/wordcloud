"""
Definition of models.
"""
# -*- coding: utf-8 -*-
import feedparser
import urllib.request
from django.db import models
import sqlite3

databasepath = 'app/wordcloud.db';
feedsData = []

# build database structure
conn = sqlite3.connect(databasepath)
cur = conn.cursor()
cur.execute("CREATE TABLE if not exists search (id integer primary key autoincrement, keyword text)")
cur.execute("CREATE TABLE if not exists url (id integer primary key autoincrement, title text, link text, srcfrom text, search_id integer, FOREIGN KEY(search_id) REFERENCES search(id))")
cur.close()
conn.commit()

# DML operations
def getSearchId(kw):
    conn = sqlite3.connect(databasepath)
    cur = conn.cursor()
    searchid = -1
    id = cur.execute("SELECT id FROM search WHERE keyword = '%s'" % kw).fetchone()
    if id:
        searchid = id[0]
    cur.close()
    conn.commit()
    return searchid

def getResults(searchid):
    conn = sqlite3.connect(databasepath)
    cur = conn.cursor()
    data = cur.execute("SELECT title, link, srcfrom FROM url WHERE search_id = '%s'" % searchid).fetchall()
    result = []
    for i in data:
        result.append({'title': i[0], 'link': i[1], 'from': i[2]})
    cur.close()
    conn.commit()
    return result

def isAvailable(kw, cur):
    exists = True
    id = cur.execute("SELECT id FROM search WHERE keyword = '%s'" % kw).fetchone()
    if not id:
        print("New request")
        exists = False
    else:
        print("Found ID = " + str(id[0]))
    return exists

def insert(kw, linklist):
    conn = sqlite3.connect(databasepath)
    cur = conn.cursor()
    exists = isAvailable(kw, cur)
    if not exists and len(linklist) > 0:
        cur.execute("INSERT INTO search VALUES (NULL, ?)", (kw,))
        id = cur.execute("SELECT id FROM search WHERE keyword = '%s'" % kw)
        idval = str(id.fetchone()[0])
        print("Keyword Reference ID = " + idval)
        for i in linklist:
            title = i["title"]
            link = i["link"]
            srcfrom = i["from"]      
            cur.execute("INSERT INTO url VALUES (NULL, ?, ?, ?, ?)", (title, link, srcfrom, idval,))

    cur.close()
    conn.commit()

# keyword detection
def keywordExistsInString(kw, line):
    return kw in line

def getLinksForKeyword(kw):
    result = []
    searchid = getSearchId(kw)
    if (searchid == -1):
        for data in feedsData:
            for item in data.entries:
                if keywordExistsInString(kw.lower(), item.title.lower()):
                    result.append({'title': item.title, 'link': item.link, 'from': data.feed.title})
        insert(kw, result)
    else:
        result = getResults(searchid)
    return result


# load resource file
with open('app/rss.txt', 'r') as f:
    feeds = [line.strip() for line in f]
    for feed in feeds:
        feedsData.append(feedparser.parse(feed))