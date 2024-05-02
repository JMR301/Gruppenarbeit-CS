import sqlite3

class InfluencerFilter:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def filter_by_category(self, category):
        self.cursor.execute("SELECT * FROM 'Influencer Database' WHERE Category=?", (category,))
        rows = self.cursor.fetchall()
        return rows

    def filter_by_range(self, column, min_val, max_val):
        self.cursor.execute("SELECT * FROM 'Influencer Database' WHERE {} BETWEEN ? AND ?".format(column), (min_val, max_val))
        rows = self.cursor.fetchall()
        return rows

    def filter_by_posts(self, posts):
        self.cursor.execute("SELECT * FROM 'Influencer Database' WHERE posts=?", (posts,))
        rows = self.cursor.fetchall()
        return rows

    def filter_by_followers(self, followers):
        self.cursor.execute("SELECT * FROM 'Influencer Database' WHERE followers=?", (followers,))
        rows = self.cursor.fetchall()
        return rows

    def filter_by_avg_likes(self, avg_likes):
        self.cursor.execute("SELECT * FROM 'Influencer Database' WHERE avg_likes=?", (avg_likes,))
        rows = self.cursor.fetchall()
        return rows

    def filter_by_60_day_eng_rate(self, rate):
        self.cursor.execute("SELECT * FROM 'Influencer Database' WHERE 60_day_eng_rate=?", (rate,))
        rows = self.cursor.fetchall()
        return rows

    def filter_by_new_post_avg_like(self, average_like):
        self.cursor.execute("SELECT * FROM 'Influencer Database' WHERE new_post_avg_like=?", (average_like,))
        rows = self.cursor.fetchall()
        return rows

    def filter_by_total_likes(self, total_likes):
        self.cursor.execute("SELECT * FROM 'Influencer Database' WHERE total_likes=?", (total_likes,))
        rows = self.cursor.fetchall()
        return rows

    def filter_by_country(self, country):
        self.cursor.execute("SELECT * FROM 'Influencer Database' WHERE country=?", (country,))
        rows = self.cursor.fetchall()
        return rows
