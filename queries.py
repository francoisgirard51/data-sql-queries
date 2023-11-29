# pylint: disable=C0103, missing-docstring

def detailed_movies(database):
    query = """
        SELECT movies.title, movies.genres, directors.name
        FROM movies
        INNER JOIN directors ON movies.director_id = directors.id
    """
    database.execute(query)
    return database.fetchall()

def late_released_movies(database):
    '''Return the list of all movies released after their director's death.'''
    query = "SELECT movies.title " \
            "FROM movies " \
            "INNER JOIN directors ON movies.director_id = directors.id " \
            "WHERE movies.start_year > directors.death_year"
    database.execute(query)
    return [row[0] for row in database.fetchall()]

def stats_on(database, genre_name):
    query = """
        SELECT ?, COUNT(*), AVG(movies.minutes)
        FROM movies
        WHERE movies.genres = ?
    """
    database.execute(query, (genre_name, genre_name))
    result = database.fetchone()
    return {
        'genre': result[0],
        'number_of_movies': result[1],
        'avg_length': round(result[2], 2) if result[2] else None
    }

def top_five_directors_for(database, genre_name):
    query = """
        SELECT directors.name, COUNT(movies.id)
        FROM movies
        INNER JOIN directors ON movies.director_id = directors.id
        WHERE movies.genres = ?
        GROUP BY directors.name
        ORDER BY COUNT(movies.id) DESC, directors.name
        LIMIT 5
    """
    database.execute(query, (genre_name,))
    return database.fetchall()

def movie_duration_buckets(database):
    query = """
        SELECT CASE
                   WHEN movies.minutes IS NULL THEN 0
                   ELSE ((movies.minutes / 30) + 1) * 30
               END AS duration_bucket,
               COUNT(*)
        FROM movies
        GROUP BY duration_bucket
        ORDER BY duration_bucket
    """
    database.execute(query)
    results = database.fetchall()

    filtered_results = [result for result in results if result[0] <= 1020 and result[0] != 0]
    return filtered_results

def top_five_youngest_newly_directors(database):
    query = """
        SELECT directors.name, MIN(movies.start_year - directors.birth_year) AS age
        FROM directors
        INNER JOIN movies ON directors.id = movies.director_id
        GROUP BY directors.name
        HAVING age IS NOT NULL
        ORDER BY age, directors.name
        LIMIT 5
    """
    database.execute(query)
    return database.fetchall()

def never_watched_movies(database):
    query = """
        SELECT movies.title
        FROM movies
        INNER JOIN directors ON movies.director_id = directors.id
        WHERE movies.start_year > directors.death_year
    """
    database.execute(query)
    return [row[0] for row in database.fetchall()]
