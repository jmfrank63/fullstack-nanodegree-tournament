import psycopg2
from psycopg2.extensions import adapt, AsIs
import os

# constants
DB_NAME = "tournament"
TABLE_QUERIES = 'sql/tournament.sql'
APLAYERS_QUERIES = 'sql/register_aplayers.sql'
JPLAYERS_QUERIES = 'sql/register_jplayers.sql'
MAKE_UNEVEN = 'sql/uneven_aplayers.sql'


def create_db(db_name=DB_NAME):
    ''' Create a database deleting any previous versions
    Return a connection to the database
    '''
    # connect to standard database
    try:
        conn = psycopg2.connect("dbname=postgres")
    except Exception, exp:
        raise exp

    # create a cursor and end any transaction
    cursor = conn.cursor()
    cursor.execute('END')

    # drop the database if it exists
    # we have to use double quotes for this command to work
    cursor.execute("DROP DATABASE IF EXISTS %s", (AsIs('"' + db_name + '"'),))

    # end any open transactions and create the database
    cursor.execute('END')
    # we have to use double quotes for this command to work
    cursor.execute("CREATE DATABASE %s", (AsIs('"' + db_name + '"'),))

    # commit any pending queries and close connection to standard database
    conn.commit()
    conn.close()


def connect_db(db_name=DB_NAME):
    """Connects to a database and creates that database if it doesn't exist"""
    try:
        # no sql injection possible without connection to the database
        # so we can safely use string formating in the connection string
        conn = psycopg2.connect('dbname={}'.format(db_name))
    except Exception, exp:
        raise exp
    return conn


def parse_queries(filename):
    """Parse a file with sql queries and return a list of queries"""
    with open(filename) as sql_file:
        query_buffer = ''
        # iterate over the lines
        for line in sql_file:
            # read in lines; ignore comments and empty lines
            if not line[:2] == '--' and line.strip():
                query_buffer += line.strip('\r').strip('\n')

    return query_buffer.split(';')[:-1]


def execute_db(connection, queries):
    '''Fill a database with a table structure'''
    cursor = connection.cursor()
    for query in queries:
        cursor.execute(query)
    connection.commit()


# open the sql commands file
def init_tournament():
    # create a database deleting any previous versions and connect to it
    create_db(DB_NAME)
    conn = connect_db(DB_NAME)

    # create the table structure
    execute_db(conn, parse_queries(TABLE_QUERIES))

    # fill database with players
    execute_db(conn, parse_queries(APLAYERS_QUERIES))
    execute_db(conn, parse_queries(JPLAYERS_QUERIES))

    # make number of players uneven
    execute_db(conn, parse_queries(MAKE_UNEVEN))

    # close the connection
    conn.close()

if __name__ == '__main__':
    init_tournament()
