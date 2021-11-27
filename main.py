import psycopg2
from load import *
from queries import *
from visualizer import *
import pandas as pd
import PySimpleGUI as sg



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

    df = pd.DataFrame(
        result, columns=['Estado', 'Restaurantes', 'PIB', 'Populacao'])

    result = get_all_locations_as_multipoint(cursor)
    map = Map(result)
    # map.showMap()

    mainloop_ui(df, map)

    conn.close()

def mainloop_ui(df, map):
    layout = [[sg.Text("Dados sobre as localizações do restaurante Chipotle", font=("Helvetica", 18))], 
        [sg.Button("Distribuicao por Estado", font=("Helvetica", 15))],
        [sg.Button("Relação entre populaçao e numero de restaurantes", font=("Helvetica", 15))],
        [sg.Button("Relação entre PIB e numero de restaurantes", font=("Helvetica", 15))],
        [sg.Button("Estados com excesso ou escassez de restaurantes", font=("Helvetica", 15))],
        [sg.Button("Mapa", font=("Helvetica", 15))],
        ]

    # Create the window
    window = sg.Window("Chipotle", layout)

    # Create an event loop
    while True:
        event, values = window.read()
        if event == "Distribuicao por Estado":
            plot_state_distribution(df)
        elif event == "Relação entre populaçao e numero de restaurantes":
            plot_pop_rest_relation(df)
        elif event == "Relação entre PIB e numero de restaurantes":
            plot_pop_rest_gdp(df)
        elif event == "Estados com excesso ou escassez de restaurantes":
            linear_regression(df)
        elif event == "Mapa":
            map.showMap()
        elif event == sg.WIN_CLOSED:
            break

    window.close()

if __name__ == "__main__":
    main()
