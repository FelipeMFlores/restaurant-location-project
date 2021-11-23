

def count_restaurants_per_state(cursor):
    cursor.execute('''
    SELECT state, count, "GDP2014", "POPESTIMATE2014"
    FROM (SELECT state, COUNT (state) FROM chipotle GROUP BY state) as ch, us_census
    WHERE ch.state=us_census."State" ''')
    return cursor.fetchall()


def get_all_locations_as_multipoint(cursor):
    cursor.execute("""\
    SELECT ST_AsGeoJSON(ST_Multi(ST_Union(geom)))
    FROM chipotle""")
    return cursor.fetchall()[0][0]
