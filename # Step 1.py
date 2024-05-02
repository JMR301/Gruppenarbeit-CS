import sqlite3

# Verbindung zur SQLite-Datenbank herstellen
connection = sqlite3.connect('Influencer.db')
cursor = connection.cursor()

# Funktion zum Filtern nach Kategorien
def filter_by_category(category):
    cursor.execute("SELECT * FROM 'Influencer Database' WHERE Category=?", (category,))
    rows = cursor.fetchall()
    return rows
    
# Funktion zum Filtern nach einem Wertebereich
def filter_by_range(column, min_val, max_val):
    cursor.execute("SELECT * FROM 'Influencer Database' WHERE {} BETWEEN ? AND ?".format(column), (min_val, max_val))
    rows = cursor.fetchall()
    return rows

# Filterfunktionen für die restlichen Kategorien
def filter_by_posts(posts):
    cursor.execute("SELECT * FROM 'Influencer Database' WHERE posts=?", (posts,))
    rows = cursor.fetchall()
    return rows

def filter_by_followers(followers):
    cursor.execute("SELECT * FROM 'Influencer Database' WHERE followers=?", (followers,))
    rows = cursor.fetchall()
    return rows

def filter_by_avg_likes(avg_likes):
    cursor.execute("SELECT * FROM 'Influencer Database' WHERE avg_likes=?", (avg_likes,))
    rows = cursor.fetchall()
    return rows

def filter_by_60_day_eng_rate(rate):
    cursor.execute("SELECT * FROM 'Influencer Database' WHERE 60_day_eng_rate=?", (rate,))
    rows = cursor.fetchall()
    return rows

def filter_by_new_post_avg_like(average_like):
    cursor.execute("SELECT * FROM 'Influencer Database' WHERE new_post_avg_like=?", (average_like,))
    rows = cursor.fetchall()
    return rows

def filter_by_total_likes(total_likes):
    cursor.execute("SELECT * FROM 'Influencer Database' WHERE total_likes=?", (total_likes,))
    rows = cursor.fetchall()
    return rows

def filter_by_country(country):
    cursor.execute("SELECT * FROM 'Influencer Database' WHERE country=?", (country,))
    rows = cursor.fetchall()
    return rows