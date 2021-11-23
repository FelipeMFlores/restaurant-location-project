import psycopg2
from load import *
from queries import *
from visualizer import *



def reset(cursor):
    cursor.execute("DROP TABLE IF EXISTS public.chipotle")
    cursor.execute("DROP TABLE IF EXISTS public.us_census")


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

    # https://www.kaggle.com/lislejoem/us_energy_census_gdp_10-14
    create_us_census_table()
    prepare_us_census_table(cursor)

    result = count_restaurants_per_state(cursor)

    # here we are just using plot, in the future we want to use a GUI library
    plot_state_distribution(result)
    plot_pop_rest_relation(result)
    plot_pop_rest_gdp(result)

    plot_pop_rest_relation

    # Show all locations on map in the browser
    result = get_all_locations_as_multipoint(cursor)
    map = Map(result)
    map.showMap()

    conn.close()


if __name__ == "__main__":
    main()
