'''
Created on 2012-11-21

@author: daimin
'''
import os
import sqlite3

if __name__ == "__main__":
    cx = sqlite3.connect("../data/printstat.db")
    cu = cx.cursor() 
    #cu.execute("""create table catalog ( id integer primary key, pid integer, name varchar(10) UNIQUE )""")
    #cu.execute("insert into catalog values(0, 0, 'name1')") 
    #cu.execute("insert into catalog values(1, 0, 'hello')") 
    #cx.commit()
    cu.execute("select * from catalog") 
    print cu.fetchall() 
    cu.close()
    cx.close()