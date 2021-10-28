import psycopg2
from load import *
from queries import *
from visualizer import *



def reset(cursor):
    cursor.execute("DROP TABLE IF EXISTS public.chipotle")


def main():
    # To install postgis
    # CREATE EXTENSION postgis;
    # CREATE EXTENSION postgis_topology;

    # Establishing the connection
    conn = psycopg2.connect(
        database="pbd", user='postgres', password='Test123', host='127.0.0.1', port='5432')
    conn.autocommit = True
    cursor = conn.cursor()

    reset(cursor)

    create_chipotle_table()
    prepare_chipotle_table(cursor)
    result = count_restaurants_per_state(cursor)

    # here we are just using plot, in the future we want to use a GUI library
    plot_state_distribution(result)

    # Show all locations on map in the browser
    result = get_all_locations_as_multipoint(cursor)
    map = Map(result)
    map.showMap()

    conn.close()


if __name__ == "__main__":
    main()
