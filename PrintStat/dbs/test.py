'''
Created on 2012-11-21

@author: daimin
'''
import os
import sqlite3

PS = [
      "BEIXING-GZ","BEIXING-GZ002",
      "BEIXING-GZ003","BEIXING-GZ006"
      "BEIXING-GZ003","BEIXING-GZ006"
      "BEIXING-GZ003","BEIXING-GZ006"
      "BEIXING-GZ003","BEIXING-GZ006"
      "BEIXING-GZ003","BEIXING-GZ006"
      "BEIXING-GZ003","BEIXING-GZ006"
      "BEIXING-GZ003","BEIXING-GZ006"
      "BEIXING-GZ003","BEIXING-GZ006"
      "BEIXING-GZ003","BEIXING-GZ006"
      "BEIXING-GZ003","BEIXING-GZ006"
      "BEIXING-GZ003","BEIXING-GZ006"
      "BEIXING-GZ003","BEIXING-GZ006"
      "BEIXING-GZ003","BEIXING-GZ006"
    ]


if __name__ == "__main__":
    """
    cx = sqlite3.connect("../data/printstat.db")
    cu = cx.cursor() 
    
    #cu.execute("insert into catalog values(0, 0, 'name1')") 
    #cu.execute("insert into catalog values(1, 0, 'hello')") 
    #cx.commit()
    cu.execute("select * from catalog") 
    print cu.fetchall() 
    cu.close()
    cx.close()
    """
    for i in range(0,100):
        print "%2d" %(i)
    