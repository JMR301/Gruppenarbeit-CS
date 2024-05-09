import sqlite3
import streamlit as st
import numpy as np
import pandas as pd



# Step 1. Load data file
csv_datei_pfad = '/Users/janreeg/HSG/Informatik/Gruppenarbeit CS/top_insta_influencers_dataCSV.csv'
df = pd.read_csv(csv_datei_pfad, encoding= 'latin1', sep=';')

# Step 2. Data Clean Up
df.columns = df.columns.str.strip()  # Clean up column names
df['Score'] = 0  # Initialize a scoring system for influencers

# Data cleaning and type conversion
def clean_numeric(x):
    if isinstance(x, str):
        return float(x.replace('k', '000').replace('m', '000000').replace('b', '000000000'))
    return x

df['BeitrÃ¤ge'] = df['BeitrÃ¤ge'].apply(clean_numeric)
df['Abonnenten'] = df['Abonnenten'].apply(clean_numeric)
df['Durchschnittliche Likes'] = df['Durchschnittliche Likes'].apply(clean_numeric)
df['Engagement Rate'] = df['Engagement Rate'].str.rstrip('%').astype('float') / 100
df['Durchschnittliche Likes neuer Posts'] = df['Durchschnittliche Likes neuer Posts'].apply(clean_numeric)
df['Gesamte Likes'] = df['Gesamte Likes'].apply(clean_numeric)

# Step 3. Create/connect to a SQLite database
connection = sqlite3.connect('Influencer.db')
df.to_sql('influencer_database', connection, if_exists='replace', index=False)

# Step 4. Streamlit-App for Filtering and Scoring
st.header('Filter Recommendations')

selected_options = {}
for option in ['Abonnenten', 'Durchschnittliche Likes', 'BeitrÃ¤ge', 'Durchschnittliche Likes neuer Posts', 'Engagement Rate', 'Gesamte Likes']:
    if pd.api.types.is_numeric_dtype(df[option]):
        min_val, max_val = df[option].dropna().min(), df[option].dropna().max()
        selected_options[option] = st.slider(f'Select {option}', min_value=min_val, max_value=max_val, value=(min_val, max_val))

# Apply filters and allocate points
filtered_df = df.copy()
for key, values in selected_options.items():
    filtered_df['temp_score'] = filtered_df.apply(lambda row: 1 if values[0] <= row[key] <= values[1] else 0, axis=1)
    filtered_df['Score'] += filtered_df['temp_score']

# Step 5. Display top influencer
top_influencer = filtered_df[filtered_df['Score'] == filtered_df['Score'].max()]
st.header('Top Influencer Based on Selected Filters')
st.dataframe(top_influencer[['Account', 'Score']])

# Step 6. Close connection
connection.close()