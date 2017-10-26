#!/usr/bin/python
# -*- coding: utf-8 -*-
#This sample of the code get number and other information about customer from maridb and put all data in specific field sqlite3db using python 2.7.5. 

import MySQLdb, gc
import sqlite3
import os, re
from sqlite3 import Error

def hasnumbers(inputstring): #check if string contain two number values
    return bool(re.search(r'\d \d', inputstring))

def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return None

def create_table():
    conn = create_connection(dbfilepath)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS numbers (id INTEGER PRIMARY KEY, conid VARCHAR(10), tel VARCHAR(20), name VARCHAR(255))")

def data_entry(tel, name):
    conn = create_connection(dbfilepath)
    c = conn.cursor()
    c.execute("INSERT INTO numbers(conid, tel, name) VALUES(?,?,?)", (conid, tel, name))
    conn.commit()

def store_data(dbfilepath):
    conn = create_connection(dbfilepath)
    c = conn.cursor()
    create_table()
    '''Get data from mysql utf8 data. The first row is contactid, the second one row is concatenated fields phone and mobile, the third row is else info data '''
    db = MySQLdb.connect(host="localhost", port=3306, user="root", passwd="", db="vtiger", charset="utf8", use_unicode=True)
    cursor = db.cursor()
    cursor.execute("select contactid as idis, concat(phone, ' ', mobile) as phones, concat(firstname, ' ', lastname, ' ', title) as info from vtiger_contactdetails;")
    data = cursor.fetchall()
    for row in data:
        if hasnumbers(row[1]): #if two numbers in the row
            for i in [s for s in row[1].split() if s.isdigit()]: #divide them
                data_entry(row[0], i, row[2])
        elif row[1] == ' ': #skip contacts that do not contain a number
            pass
        else:
            data_entry(row[0], row[1], row[2])
    cursor.close()
    gc.collect()
	
dbfilepath = 'call.db'
if os.path.isfile(dbfilepath) and os.path.getsize(dbfilepath) > 0: #file exist and not empty
    os.remove(dbfilepath)
    store_data(dbfilepath)
else:
    store_data(dbfilepath)
