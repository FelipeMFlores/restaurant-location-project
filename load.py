import pandas as pd
from sqlalchemy import create_engine


def create_chipotle_table():
    # Create table from csv
    engine = create_engine("postgresql://postgres@localhost:5433/pbd", echo=False)
    df = pd.read_csv("chipotle/chipotle_stores.csv")
    df.to_sql("chipotle", con=engine, if_exists='replace')
    engine.dispose()


def prepare_chipotle_table(cursor):
    # Add the geometry column
    cursor.execute('ALTER TABLE public.chipotle ADD COLUMN geom geometry(Point, 4326)')
    cursor.execute('UPDATE public.chipotle SET geom = ST_SetSRID(ST_MakePoint(longitude, latitude), 4326)')
