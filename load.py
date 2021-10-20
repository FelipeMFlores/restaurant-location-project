import pandas as pd
from sqlalchemy import create_engine
import psycopg2

# To install postgis
# CREATE EXTENSION postgis;
# CREATE EXTENSION postgis_topology;


#Establishing the connection
conn = psycopg2.connect(
   database="pbd", user='postgres', password='Test123', host='127.0.0.1', port= '5433'
)
cursor = conn.cursor()
cursor.execute("DROP TABLE IF EXISTS public.chipotle")
conn.commit()

# Create table from csv
engine = create_engine("postgresql://postgres@localhost:5433/pbd", echo=False)
df = pd.read_csv("chipotle/chipotle_stores.csv")
df.to_sql("chipotle", con=engine, if_exists='replace')
engine.dispose()

# Add the geometry column
cursor.execute('ALTER TABLE public.chipotle ADD COLUMN geom geometry(Point, 4326)')
cursor.execute('UPDATE public.chipotle SET geom = ST_SetSRID(ST_MakePoint(longitude, latitude), 4326)')

conn.commit()
conn.close()
