import os
import MySQLdb

if __name__ == "__main__":
    file_object = open('thefile.txt', 'w')
    file_object.write("nihao")
    file_object.close( )
