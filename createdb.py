import psycopg2
import os

print os.getcwd()

def connect_db(db_name):
    """Connects to a database and creates that database if it doesn't exist"""
    try:
        conn = psycopg2.connect('dbname=' + db_name)
    except:
        conn = psycopg2.connect('dbname=postgres')
        cursor = conn.cursor()
        cursor.execute('CREATE DATABASE ' + db_name)
        cursor.close()
        conn.close()
        try:
            conn = psycopg2.connect('dbname=' + db_name)
        except Exception, e:
            raise e
    return conn

    
# open the sql commands file
if __name__ == '__main__':
    conn = connect_db('tournament')
    with open('tournament.sql') as sql_file:
    # iterate over the lines
        for line in sql_file:
            if line.strip() and not line[:2] == '--':
                print(line[:-2])

