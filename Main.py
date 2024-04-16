import streamlit as st
import pandas as pd

# Lade die CSV-Datei
csv_datei_pfad = 'beispiel.csv'
df = pd.read_csv(csv_datei_pfad)

# Zeige die Daten in der Tabelle an
st.write(df)