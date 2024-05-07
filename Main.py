import streamlit as st
import pandas as pd
import csv


import sqlite3
from Filter import InfluencerFilter
# Step 1. Load data file
csv_datei_pfad = '/Users/janreeg/HSG/Informatik/Gruppenarbeit CS/top_insta_influencers_dataCSV.csv'
df = pd.read_csv(csv_datei_pfad, encoding= 'latin1', sep=';')


# Step 2. Data Clean Up
df.columns = df.columns.str.strip()
# Step 3. Create/connect to a SQLite database
connection = sqlite3.connect('Influencer.db')
# Step 4. Load data file to SQLite
df.to_sql('Influencer Database',connection,if_exists='replace')

print(len(df.columns))

query1 = "SELECT * FROM 'Influencer Database'"




query4 = "PRAGMA table_info('Influencer Database')"

#Tabellennamen abfragen
query5 = "SELECT name FROM sqlite_master WHERE type='table';"
namen = pd.read_sql(query4, connection)
Tablename = pd.read_sql(query5, connection)
Datenbank = pd.read_sql(query1, connection)
#df = pd.DataFrame(query1 )




 #Streamlit-App
st.header ('Filter Recommendations')



# Hier ist der neue Filter


#Benutzereingaben für Filteroptionen
selected_options = {}
for option in df.columns.array:
    if option in ['Durchschnittliche Likes', 'Abonnenten', 'Influencerscore', 'BeitrÃ¤ge', 'Durschnittliche Likes neuer Posts', 'Engagement Rate', 'Gesamte Likes']:
        min_val, max_val = df[option].min(), df[option].max()
        # Überprüfen Sie, ob die Werte numerisch sind, bevor sie an den Slider übergeben werden
        if pd.api.types.is_numeric_dtype(df[option]):
            selected_options[option] = st.slider(f'Select {option}', min_value=min_val, max_value=max_val, value=(min_val, max_val))
        else:
            st.warning(f"The '{option}' column contains non-numeric data and cannot be used with a slider.")
            selected_options[option] = []
    #elif: 
    else:
        selected_options[option] = st.multiselect(f'Select {option}', df[option].unique())
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
print(df.columns.array)
#print(first_three_entries)
#print(selected_column)

#warum funzt der commit nicht