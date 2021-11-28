import psycopg2
from load import *
from queries import *
from visualizer import *
import pandas as pd
import PySimpleGUI as sg
import threading



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
        [sg.Button("Relação entre populaçao e número de restaurantes", font=("Helvetica", 15))],
        [sg.Button("Relação entre PIB e número de restaurantes", font=("Helvetica", 15))],
        [sg.Button("Estados com excesso ou escassez de restaurantes", font=("Helvetica", 15))],
        [sg.Button("Sugestões", font=("Helvetica", 15))],
        [sg.Button("Mapa", font=("Helvetica", 15))],
        [sg.Button("Info", font=("Helvetica", 15))],
        ]


    # Create the window
    window = sg.Window("Chipotle", layout)

    # Create an event loop
    while True:
        event, values = window.read()
        if event == "Distribuicao por Estado":
            plot_state_distribution(df)
        elif event == "Relação entre populaçao e número de restaurantes":
            plot_pop_rest_relation(df)
        elif event == "Relação entre PIB e número de restaurantes":
            plot_pop_rest_gdp(df)
        elif event == "Estados com excesso ou escassez de restaurantes":
            linear_regression(df, False)
        elif event == "Sugestões":
            linear_regression(df, True)
        elif event == "Mapa":
            map.showMap()
        elif event == "Info":
            info_layout = get_info_layout()
            w2 = sg.Window("Chipotle Info", info_layout)
            event, values = w2.read(timeout=100)
        elif event == sg.WIN_CLOSED:
            break

    window.close()

def get_info_layout():
    return [
        [sg.Text("Informações sobre as funcionalidades", font=("Helvetica", 18, 'bold'))],
        [sg.Text("Distribuição por Estado:", font=("Helvetica", 16, 'bold'))],
        [sg.Text("Gráfico com o número de restaurantes em cada estado", font=("Helvetica", 15))],
        [sg.Text("Relação entre populaçao e número de restaurantes:", font=("Helvetica", 16, 'bold'))],
        [sg.Text("Gráfico com regressão linear na relação entre o número de restaurantes e a população para cada estado", font=("Helvetica", 15))],
        [sg.Text("Relação entre PIB e número de restaurantes:", font=("Helvetica", 16, 'bold'))],
        [sg.Text("Gráfico com regressão linear na relação entre o número de restaurantes e o PIB para cada estado", font=("Helvetica", 15))],
        [sg.Text("Estados com excesso ou escassez de restaurantes:", font=("Helvetica", 16, 'bold'))],
        [sg.Text("Gráfico mostrando o número de restaurantes e o número de restaurantes esperados, calculado atráves de um regressão linear levando em conta a população e o PIB de cada estado. \nAcima da linha vemos os estados com excesso de restaurantes, e abaixo, os estados com escassez.", font=("Helvetica", 15))],
        [sg.Text("Sugestões:", font=("Helvetica", 16, 'bold'))],
        [sg.Text("Gráfico que mostra um ranking da diferença entre o número de restaurantes, e o número esperados. \n A sugestão seria focar em estados com escassez de restaurantes", font=("Helvetica", 15))],
        [sg.Text("Mapa:", font=("Helvetica", 16, 'bold'))],
        [sg.Text("Abre em um browser o mapa com todas as localizações dos restaurantes", font=("Helvetica", 15))],
    ]

if __name__ == "__main__":
    main()
