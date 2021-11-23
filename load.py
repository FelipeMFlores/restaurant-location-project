import pandas as pd
from sqlalchemy import create_engine


def create_chipotle_table():
    # Create table from csv
    engine = create_engine("postgresql://postgres@localhost:5432/pbd", echo=False)
    df = pd.read_csv("chipotle/chipotle_stores.csv")
    df.to_sql("chipotle", con=engine, if_exists='replace')
    engine.dispose()


def prepare_chipotle_table(cursor):
    # Add the geometry column
    cursor.execute('ALTER TABLE public.chipotle ADD COLUMN geom geometry(Point, 4326)')
    cursor.execute('UPDATE public.chipotle SET geom = ST_SetSRID(ST_MakePoint(longitude, latitude), 4326)')


def create_us_census_table():
    engine = create_engine("postgresql://postgres@localhost:5432/pbd", echo=False)
    df = pd.read_csv("us-census/us-census.csv")
    df.to_sql("us_census", con=engine, if_exists='replace')
    engine.dispose()

def prepare_us_census_table(cursor):
    # drop every column except the ones we want
    columns_required = ('State', 'GDP2014', 'POPESTIMATE2014')
    
    cursor.execute('''SELECT *
        FROM information_schema.columns
        WHERE table_schema = 'public'
        AND table_name   = 'us_census' ''')

    columns_list = cursor.fetchall()
    for c in columns_list:
        if c[3] not in  columns_required :
            cursor.execute('ALTER TABLE public.us_census DROP COLUMN "' + c[3] + '"')
