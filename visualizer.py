from typing import List
import matplotlib.pyplot as plt
from pandas.core.frame import DataFrame
import seaborn as sns
import os
import webbrowser
import folium
from folium.plugins import MarkerCluster
from sklearn.linear_model import LinearRegression
import numpy as np


def plot_state_distribution(df):
    df = df.sort_values(by=['Restaurantes'])
    plt.figure(figsize=(10, 6))
    plt.title("Numero de Restaurantes por Estado")
    sns.barplot(x='Estado', y='Restaurantes', data=df)
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()

def plot_pop_rest_relation(df):
    plt.figure(figsize=(10, 6))
    plt.title("Populacao vs Restaurantes")
    sns.regplot(x='Restaurantes', y='Populacao', data=df)
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()

def plot_pop_rest_gdp(df):
    plt.figure(figsize=(10, 6))
    plt.title("Populacao vs PIB")
    sns.regplot(x='Restaurantes', y='PIB', data=df)
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()

def linear_regression(df):
    X=df[['PIB','Populacao']]
    y=df['Restaurantes']
    model=LinearRegression()
    model.fit(X,y)
    y_pred=model.predict(X)
    y_pred=np.round(y_pred,0)
    df['Restaurantes Esperados']=y_pred
    df["Restaurantes Esperados"]=df["Restaurantes Esperados"].astype('int')

    plot_predictions(df)

def plot_predictions(df: DataFrame):
    plt.figure(figsize=(10,8))
    plt.title("Estados com excesso ou escasez (Regressao Linear com PIB e Populacao)")
    plot=sns.scatterplot(x='Restaurantes Esperados',y='Restaurantes',data=df)
    for i in range(0, df.shape[0]):
        plot.text(df["Restaurantes Esperados"][i], df.Restaurantes[i], df.Estado[i], alpha=0.8, fontsize=8 )
    plt.plot([-50,500],[-50,500],'r--')
    plt.xlim(-10,max(df["Restaurantes Esperados"])+20)
    plt.ylim(-10,max(df.Restaurantes)+20)
    plt.tight_layout()
    plt.show()

    df['Diferenca']=df["Restaurantes Esperados"]-df.Restaurantes
    plt.figure(figsize=(4,8))
    plt.title("Numero de restaurantes em excesso/escasez por Estado")
    sns.barplot(data=df.sort_values(by='Diferenca', ascending=False),
            x='Diferenca',y='Estado', orient='h')
    plt.tight_layout()
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
