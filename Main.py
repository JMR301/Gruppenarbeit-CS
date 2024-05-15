import streamlit as st
import pandas as pd
import csv
import matplotlib.pyplot as plt


import sqlite3


def page_home():
    st.image("/Users/moritz/CsProjekt/InMatch-3.png", width=300)
    st.title("Willkommen zu InMatch!")
    st.text("Du bist genervt davon, die richtigen Influencer passend zu deiner Marketingaktion \n zu finden? Dann bist du genau richtig bei uns!\n"
            "Gehe auf die nächste Seite und passe die Filter so an, dass sie zu den Interessen \n für die Vermarktung deines Produkts passen!\n"
            "Wir liefern dir dann den Influencer, passend zu deiner Marketingaktion!")
    
def page_team():
    st.title("Über Uns")   
    st.text("Wir von InfluMatch sind ein Team von 7 Leuten, die gemeinsam dieses Programm \n gecoded haben, um dir zu helfen, den perfekten Influencer, passend zu deiner \n Marketingaktion zu finden! \n \n Eure Alessandra, Adrien Stella, Ali, Momo, Moritz und Jan!")


def page_tool():
    st.title("Das Tool")
    
    # Step 1. Load data file
    csv_datei_pfad = '/Users/moritz/CsProjekt/top_insta_influencers_dataCSV.csv'
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


    #df = pd.DataFrame(query1)

    # Data cleaning and type conversion for k, m

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

    print(df['Gesamte Likes'])
    #converting string to float
    #print(df['Durchschnittliche Likes'])

    Datenbank = pd.read_sql(query1, connection)
    Tablename = pd.read_sql(query5, connection)
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
            if key in ['Durchschnittliche Likes', 'Abonnenten', 'Influencerscore', 'BeitrÃ¤ge', 'Durschnittliche Likes neuer Posts', 'Engagement Rate', 'Gesamte Likes']:
                filtered_df = filtered_df[filtered_df[key].between(values[0],values[1])]
            else:

                print(filtered_df[filtered_df[key].isin(values)])
                filtered_df = filtered_df[filtered_df[key].isin(values)]
        
            



    #Hier startet die Visualisierung

    def millions(x):
        return f"{float(x / 1000000)}"



    df_sorted = filtered_df.sort_values(by="Abonnenten").iloc[:20]
    df_sorted['Abonnenten'] = df_sorted['Abonnenten'].apply(millions)
    df_sorted['Gesamte Likes'] = df_sorted['Gesamte Likes'].apply(millions)
    fig, ax = plt.subplots()
    ax.scatter(df_sorted['Abonnenten'], df_sorted['Gesamte Likes'])
    ax.set_xlabel('Abonnenten (mio)')
    ax.set_ylabel('Gesamte Likes (mio)')
    st.pyplot(fig)

    # Ergebnis anzeigen
    st.header('Filtered Recommendations')
    st.dataframe(filtered_df)






    # Step 5. close connection
    connection.close()

    print(filtered_df)

    #print("Spaltennamen:")

    #print(query1)
    #print(df)
    #print(df.columns.array)
    #print(first_three_entries)
    #print(selected_column)

    #warum funzt der commit nicht

def page_algo():

    # Step 1. Load data file
    csv_datei_pfad = '/Users/moritz/CsProjekt/top_insta_influencers_dataCSV.csv'
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

if __name__ == "__main__":
    main()

