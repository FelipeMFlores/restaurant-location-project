import pandas as pd
import psycopg2
from load import *
from queries import *

def reset(cursor):
    cursor.execute("DROP TABLE IF EXISTS public.chipotle")

def main():
    # To install postgis
    # CREATE EXTENSION postgis;
    # CREATE EXTENSION postgis_topology;

    #Establishing the connection
    conn = psycopg2.connect(
    database="pbd", user='postgres', password='Test123', host='127.0.0.1', port= '5433')
    conn.autocommit = True
    cursor = conn.cursor()

    reset(cursor)

    create_chipotle_table()
    prepare_chipotle_table(cursor)
    count_restaurants_per_state(cursor)
    
    conn.close()




if __name__=="__main__":
    main()