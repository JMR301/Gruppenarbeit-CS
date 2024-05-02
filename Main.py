import streamlit as st
import pandas as pd
import csv
import sqlite3

# Step 1. Load data file
csv_datei_pfad = '/Users/janreeg/HSG/Informatik/Gruppenarbeit CS/top_insta_influencers_dataCSV.csv'
df = pd.read_csv(csv_datei_pfad, sep=';')


# Step 2. Data Clean Up
df.columns = df.columns.str.strip()
# Step 3. Create/connect to a SQLite database
connection = sqlite3.connect('Influencer.db')
# Step 4. Load data file to SQLite
df. to_sql('Influencer Database',connection,if_exists='replace')

query1 = "SELECT * FROM 'Influencer Database'"

# SQL-Abfrage, um eine einzelne Spalte abzufragen
#query2 = "SELECT Category FROM 'Influencer Database'"

# Daten aus der Datenbank lesen
#selected_column = pd.read_sql(query2 , connection)

# Daten aus der Datenbank lesen
first_three_entries = pd.read_sql(query1, connection)


# Daten aus der Datenbank lesen
#df = pd.read_sql(query3, connection)

query4 = "PRAGMA table_info(Influencer Database)"

#Tabellennamen abfragen
query5 = "SELECT name FROM sqlite_master WHERE type='table';"

Tablename = pd.read_sql(query5, connection)

# Step 5. close connection
connection.close()



#print("Spaltennamen:")

print(Tablename)
#print(first_three_entries)
#print(selected_column)