import psycopg2
import os

print os.getcwd()

with open('tournament.sql') as sql_file:
    for line in sql_file.readlines:
        print line


    
