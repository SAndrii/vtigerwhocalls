#!/usr/bin/python
# -*- coding: utf-8 -*-

import re, sqlite3

def hasnumbers(inputstring): #check if string contain to number values
	return bool(re.search(r'\d \d', inputstring))

def create_table():
    c.execute("CREATE TABLE IF NOT EXISTS numbers (id INTEGER PRIMARY KEY, tel VARCHAR(20), name VARCHAR(255))")

def data_entry(tel, name):
    c.execute("INSERT INTO numbers(tel, name) VALUES(?,?)", (tel, name))
    conn.commit()

sps = [] #result list
conn = sqlite3.connect('calls.db')
c = conn.cursor()
with open('po3.csv', encoding='utf8') as f: 
        lines = f.readlines()
        for string in lines:
                if string[1] == ' ':
                        pass #skip all lines that begin with ' '
                else:
                        sep = ';'
                        r1,r2 = [], []
                        s = string.replace('\n', '').replace('"', '').split(sep)
                        if hasnumbers(s[0]): #if string with 2 number split them and add name value
                                r1.append(s[0].split(' ')[0])
                                r1.append(s[1])
                                r2.append(s[0].split(' ')[1])
                                r2.append(s[1])
                                sps.append(r1)
                                sps.append(r2)
                        else:
                                sps.append(s)
        f.close

create_table
for i in sps:
        data_entry(i[0], i[1])
c.close()
conn.close()
        
