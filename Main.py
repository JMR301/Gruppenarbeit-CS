import streamlit as st
import pandas as pd
import csv
import sqlite3

# Step 1. Load data file
csv_datei_pfad = '/Users/janreeg/HSG/Informatik/Gruppenarbeit CS/top_insta_influencers_dataCSV.csv'
df = pd.read_csv(csv_datei_pfad)


# Step 2. Data Clean Up
df.columns = df.columns.str.strip()
# Step 3. Create/connect to a SQLite database
connection = sqlite3.connect('Influencer.db')
# Step 4. Load data file to SQLite
df. to_sql('Influencer Database',connection,if_exists='replace')

query = "SELECT * FROM 'Influencer Database' LIMIT 3"

# Daten aus der Datenbank lesen
first_three_entries = pd.read_sql(query, connection)

# Step 5. close connection
connection.close()

print(first_three_entries)