import pandas as pd
import sqlite3

class InfluencerFilter:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.load_all_data()

    def load_all_data(self):
        query = "SELECT * FROM 'Influencer Database'"
        self.df = pd.read_sql_query(query, self.connection)

    def filter_by_category(self, category):
        return self.df[self.df['Category'] == category]

    def filter_by_range(self, column, min_val, max_val):
        return self.df[(self.df[column] >= min_val) & (self.df[column] <= max_val)]

    def filter_by_posts(self, posts):
        return self.df[self.df['posts'] == posts]

    def filter_by_followers(self, followers):
        return self.df[self.df['followers'] == followers]

    def filter_by_avg_likes(self, avg_likes):
        return self.df[self.df['avg_likes'] == avg_likes]

    def filter_by_60_day_eng_rate(self, rate):
        return self.df[self.df['60_day_eng_rate'] == rate]

    def filter_by_new_post_avg_like(self, average_like):
        return self.df[self.df['new_post_avg_like'] == average_like]

    def filter_by_total_likes(self, total_likes):
        return self.df[self.df['total_likes'] == total_likes]

    def filter_by_country(self, country):
        return self.df[self.df['country'] == country]
