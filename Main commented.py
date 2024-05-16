#Import der benötigten Bibliotheken
import streamlit as st #Bibliothek zum Aufbau einer Web-App
import pandas as pd #Bibliothek zur Datenmanipulation und -analyse
import csv #Zum Einlesen der CSV Datei
import matplotlib.pyplot as plt #Visualisierung


import sqlite3

#Definition von Funktionen, welche verschiedene Seiten in Streamlit erstellen
#Formatierung der Landing-Page
def page_home():
    st.image("/Users/moritz/CsProjekt/InMatch-3.png", width=300)
    st.title("Willkommen bei InMatch!")
    st.text("Du bist genervt davon, die richtigen Influencer passend zu deiner Marketingaktion\nzu finden? Dann bist du genau richtig bei uns!\n"
            "Gehe auf die nächste Seite und passe die Filter so an, dass sie zu den Interessen\nfür die Vermarktung deines Produkts passen!\n"
            "Wir liefern dir dann den Influencer, passend zu deiner Marketingaktion!")

#Formatierung Über uns Seite    
def page_team():
    st.title("Über Uns")   
    st.text("Wir von InfluMatch sind ein Team von 7 Leuten, die gemeinsam dieses Programm\ngecoded haben, um dir zu helfen, den perfekten Influencer, passend zu deiner\nMarketingaktion zu finden!\n \nEure Alessandra, Adrien Stella, Ali, Momo, Moritz und Jan!")

#Formatierung Hauptseite
def page_tool():
    st.title("Das Tool")
    
    # Schritt 1. Datei laden
    csv_datei_pfad = '/Users/moritz/CsProjekt/top_insta_influencers_dataCSV.csv'
    df = pd.read_csv(csv_datei_pfad, encoding= 'latin1', sep=';')


    # Schritt 2. Datenbereinigung
    df.columns = df.columns.str.strip()

    # Schritt 3. Erstelle/Verbindung zu SQLite database C
    connection = sqlite3.connect('Influencer.db')

    # Schritt 4. Lade Datei in SQLite
    df.to_sql('Influencer Database',connection,if_exists='replace')

    print(len(df.columns))

    #Wiedergabe aller Daten aus Tabelle Influencer Database
    query1 = "SELECT * FROM 'Influencer Database'"

    # Details zur Tabelle aufrufen aus Übersichtszwecken
    query4 = "PRAGMA table_info('Influencer Database')"

    #Tabellennamen abfragen
    query5 = "SELECT name FROM sqlite_master WHERE type='table';"
    namen = pd.read_sql(query4, connection)


    #df = pd.DataFrame(query1)

    # Datenbereinigung und Konvertierung der Datentypen für k, m
    def clean_numeric(x):
        if isinstance(x, str):
            return float(x.replace("k", "0").replace("m", "00000").replace("b", "00000000").replace('.', ''))
        return x


   # Umwandlung der Spalten in Dataframes und bereinigt die Spaltenwerte
    df['BeitrÃ¤ge'] = df['BeitrÃ¤ge'].apply(clean_numeric)
    df['Abonnenten'] = df['Abonnenten'].apply(clean_numeric)
    df['Durchschnittliche Likes'] = df['Durchschnittliche Likes'].apply(clean_numeric)
    df['Engagement Rate'] = df['Engagement Rate'].str.rstrip('%').astype('float') / 100
    df['Durchschnittliche Likes neuer Posts'] = df['Durchschnittliche Likes neuer Posts'].apply(clean_numeric)
    df['Gesamte Likes'] = df['Gesamte Likes'].apply(clean_numeric)

    print(df['Gesamte Likes'])
    #Konvertierung float to string
    #print(df['Durchschnittliche Likes'])


    #SQL Abfrage wird gegen Datenbank ausgeführt und in ein DF geladen
    Datenbank = pd.read_sql(query1, connection)
    Tablename = pd.read_sql(query5, connection)
    #Streamlit-App
    st.header ('Finde die passenden Influencer:')



    # Hier ist der neue Filter


    #Benutzereingaben für Filteroptionen
    selected_options = {} #Leeres Dictionary erstellen
    for option in df.columns.array: #Schleife iteriert über alle Spaltennamen
        if option in ['Durchschnittliche Likes', 'Abonnenten', 'Influencerscore', 'BeitrÃ¤ge', 'Durschnittliche Likes neuer Posts', 'Engagement Rate', 'Gesamte Likes']:
            min_val, max_val = df[option].min(), df[option].max()
            # Überprüfen Sie, ob die Werte numerisch sind, bevor sie an den Slider übergeben werden
            if pd.api.types.is_numeric_dtype(df[option]):
                selected_options[option] = st.slider(f'Wähle {option}', min_value=min_val, max_value=max_val, value=(min_val, max_val)) #Übergabe in Slider
            else:
                st.warning(f"The '{option}' column contains non-numeric data and cannot be used with a slider.")
                selected_options[option] = []
        #elif: 
        else:
            selected_options[option] = st.multiselect(f'Wähle {option}', df[option].unique()) # Für Spalten die nicht in der obigen Auswahl sind Verwendung von Multiselect
    
    # Filterung des DF auf Basis der ausgewählten Optionen des Users
    filtered_df = df.copy() #Kopie des DF, sodass der ursprüngliche DF unverändert bleibt
    for key, values in selected_options.items(): #Schleife iteriert über Schlüssel-Wert-Paare im Dictionary selected_options
        if values:
            if key in ['Durchschnittliche Likes', 'Abonnenten', 'Influencerscore', 'BeitrÃ¤ge', 'Durschnittliche Likes neuer Posts', 'Engagement Rate', 'Gesamte Likes']:
                filtered_df = filtered_df[filtered_df[key].between(values[0],values[1])] #between-Methode filtert den DF so, dass nur Zeilen behalten werden zwischen Werten 0 und 1
            else:
                #Zeilen werdenbbehalten bei nicht-numerischen Spalten, deren Wert in der Spalte key in der Liste values enthalten ist
                print(filtered_df[filtered_df[key].isin(values)])
                filtered_df = filtered_df[filtered_df[key].isin(values)]

    # filtered_df enthält alle nach den Filterkriterien basierenden Zeilen  
            



    #Hier startet die Visualisierung

    def millions(x):
        return f"{float(x / 1000000)}"



    df_sorted = filtered_df.sort_values(by="Abonnenten").iloc[:20] #sortieren nach Abonennten & Auswahl der ersten 20 Einträge
    df_sorted['Abonnenten'] = df_sorted['Abonnenten'].apply(millions)
    df_sorted['Gesamte Likes'] = df_sorted['Gesamte Likes'].apply(millions) #Konvertierung der Werte in den genannten Spalten in Millionen
    
    fig, ax = plt.subplots() #Erstellung des Streudiagramms und einer neuen Achse
    ax.scatter(df_sorted['Abonnenten'], df_sorted['Gesamte Likes'])
    ax.set_xlabel('Abonnenten (mio)') #Benennung der Achsen
    ax.set_ylabel('Gesamte Likes (mio)')
    st.pyplot(fig) #Anzeigen des Diagrammes in Streamlit

    # Ergebnis anzeigen
    st.header('Alle Ergebnisse:')
    st.dataframe(filtered_df)






    # Schritt 5. Verbindung zur Datenbank schließen
    connection.close()

    print(filtered_df)



# Kodierung des Algorithmus
def page_algo():

    # Step 1. Laden der Daten
    csv_datei_pfad = '/Users/moritz/CsProjekt/top_insta_influencers_dataCSV.csv'
    df = pd.read_csv(csv_datei_pfad, encoding= 'latin1', sep=';')

    # Step 2. Datenbereinigung
    df.columns = df.columns.str.strip()  # Bereinigung der Spalten
    df['Score'] = 0  # Initialisieren eines scoring system für Influencer

    # Datenbereinigung und Typkonvertierung
    def clean_numeric(x):
        if isinstance(x, str):
            return float(x.replace("k", "0").replace("m", "00000").replace("b", "00000000").replace('.', ''))
        return x

    df['BeitrÃ¤ge'] = df['BeitrÃ¤ge'].apply(clean_numeric)
    df['Abonnenten'] = df['Abonnenten'].apply(clean_numeric)
    df['Durchschnittliche Likes'] = df['Durchschnittliche Likes'].apply(clean_numeric)
    df['Engagement Rate'] = df['Engagement Rate'].str.rstrip('%').astype('float') / 100
    df['Durchschnittliche Likes neuer Posts'] = df['Durchschnittliche Likes neuer Posts'].apply(clean_numeric)
    df['Gesamte Likes'] = df['Gesamte Likes'].apply(clean_numeric)

    # Step 3. Erstellen/Verbinden einer SQLite-Datenbank
    connection = sqlite3.connect('Influencer.db')
    df.to_sql('influencer_database', connection, if_exists='replace', index=False) #Speicherung des DF in einer Tabelle

    # Step 4. Streamlit-App für Filterung und Scoring
    st.header('Finde dein perfektes Match!')

    selected_options = {}
    for option in ['Abonnenten', 'Durchschnittliche Likes', 'BeitrÃ¤ge', 'Durchschnittliche Likes neuer Posts', 'Engagement Rate', 'Gesamte Likes']:
        if pd.api.types.is_numeric_dtype(df[option]):
            min_val, max_val = df[option].dropna().min(), df[option].dropna().max()
            selected_options[option] = st.slider(f'Wähle {option}', min_value=min_val, max_value=max_val, value=(min_val, max_val)) #Speichern der Auswahl des Benutzers im Dictionary

    # Filter anwenden und Punkte zuweisen
    filtered_df = df.copy() #Kopie DF
    #Für jede ausgewählte Option wird überprüft, ob der Wert in der Spalte innerhalb des ausgewählten Bereiches liegt
    # Wenn ja, dann wird 1 zum temp_score hinzugefügt
    # Danach wird temp_score zum Gesamtscore score addiert
    for key, values in selected_options.items():
        filtered_df['temp_score'] = filtered_df.apply(lambda row: 1 if values[0] <= row[key] <= values[1] else 0, axis=1)
        filtered_df['Score'] += filtered_df['temp_score']

    # Step 5. Top Influencer anzeigen
    #DF filtern um die Influencer mit dem höchsten Score zu finden
    top_influencer = filtered_df[filtered_df['Score'] == filtered_df['Score'].max()]
    st.header('Dein ideales Match:')
    st.dataframe(top_influencer[['Account', 'Score']])

    # Step 6. Close connection
    connection.close()

# Erstellung eines Side-Bar Menüs in Streamlit für jede Seite in Streamlit
def main():
    st.sidebar.title("Willkommen bei InMatch")
    page = st.sidebar.radio("Besuche:", ["Home", "Über Uns", "Das Tool", "Der Algorithmus"])

    if page == "Home":
        page_home()
    if page == "Über Uns":
        page_team()
    if page == "Das Tool":
        page_tool()
    elif page == "Der Algorithmus":
        page_algo()

#Koordination der Navigation zur korrekten Ausführung
if __name__ == "__main__":
    main()

