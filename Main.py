import streamlit as st
import pandas as pd
import csv


import sqlite3
from Filter import InfluencerFilter
# Step 1. Load data file
csv_datei_pfad = '/Users/janreeg/HSG/Informatik/Gruppenarbeit CS/top_insta_influencers_dataCSV.csv'
df = pd.read_csv(csv_datei_pfad, sep=';')


# Step 2. Data Clean Up
df.columns = df.columns.str.strip()
# Step 3. Create/connect to a SQLite database
connection = sqlite3.connect('Influencer.db')
# Step 4. Load data file to SQLite
df.to_sql('Influencer Database',connection,if_exists='replace')



query1 = "SELECT * FROM 'Influencer Database'"









query4 = "PRAGMA table_info(Influencer Database)"

#Tabellennamen abfragen
query5 = "SELECT name FROM sqlite_master WHERE type='table';"

Tablename = pd.read_sql(query5, connection)
Datenbank = pd.read_sql(query1, connection)
#df = pd.DataFrame(query1 )

 #Dropdown-Optionen für Filterung
options = {
    'avg_likes': 'average Likes',
    'followers': 'followers',
    'Category': 'Category',
    'country': 'ountry'
            }

 #Streamlit-App
st.header ('Filter Recommendations')




# Hier ist der neue Filter
#warum geht das nicht

 #Benutzereingaben für Filteroptionen
selected_options = {}
for key, value in options.items():
    selected_options[key] = st.multiselect(f'Select {value}', df[key].unique())

 #Filterung des DataFrame basierend auf den Benutzereingaben
filtered_df = df.copy()
for key, values in selected_options.items():
    if values:
        filtered_df = filtered_df[filtered_df[key].isin(values)]

# Ergebnis anzeigen
st.header('Filtered Recommendations')
st.dataframe(filtered_df)






# Step 5. close connection
connection.close()



#print("Spaltennamen:")

print(query1)
print(df)
#print(first_three_entries)
#print(selected_column)

#warum funzt der commit nicht