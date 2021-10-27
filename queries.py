

def count_restaurants_per_state(cursor):
    cursor.execute('SELECT state, COUNT (state) FROM chipotle GROUP BY state')
    return cursor.fetchall()