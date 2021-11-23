from typing import List
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import webbrowser
import folium
from folium.plugins import MarkerCluster


def plot_state_distribution(state_count: List):
    df_state_count = pd.DataFrame(
        state_count, columns=['Name', 'Restaurants', 'GDP', 'Population']).sort_values(by=['Restaurants'])
    plt.figure(figsize=(10, 6))
    plt.title("Number of Chipotle Stores by State")
    sns.barplot(x='Name', y='Restaurants', data=df_state_count)
    plt.xticks(rotation=90)
    plt.show()

def plot_pop_rest_relation(state_table: List):
    df = pd.DataFrame(
        state_table, columns=['Name', 'Restaurants', 'GDP', 'Population'])
    plt.figure(figsize=(10, 6))
    plt.title("Population vs Restaurants")
    sns.regplot(x='Restaurants', y='Population', data=df)
    plt.xticks(rotation=90)
    plt.show()

def plot_pop_rest_gdp(state_table: List):
    df = pd.DataFrame(
        state_table, columns=['Name', 'Restaurants', 'GDP', 'Population'])
    plt.figure(figsize=(10, 6))
    plt.title("Population vs GDP")
    sns.regplot(x='Restaurants', y='GDP', data=df)
    plt.xticks(rotation=90)
    plt.show()

class Map:
    def __init__(self, geoJSON):
        m = folium.Map(
            location=[37.0902, -95.7129],
            zoom_start=5
        )
        marker_cluster = MarkerCluster().add_to(m)
        folium.GeoJson(geoJSON, name="geojson").add_to(marker_cluster)
        self.map = marker_cluster

    def showMap(self):
        # Save map in a file and open on browser
        self.map.save("map.html")
        webbrowser.open('file://' + os.path.realpath('map.html'))
