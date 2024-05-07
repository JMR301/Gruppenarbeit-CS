import sqlite3
import pandas as pd

# Charger les données du fichier CSV
csv_path = 'top_insta_influencers_dataCSV.csv'
df = pd.read_csv(csv_path, delimiter=';', skipinitialspace=True)

# Afficher les premières lignes pour identifier la structure
print("Aperçu des données du fichier CSV :")
print(df.head())

# Création de la base de données SQLite dans le répertoire courant
db_path = 'marques_influenceurs.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
print(df.columns)
# Création de la table "influenceurs"
cursor.execute('''
    CREATE TABLE IF NOT EXISTS influenceurs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Rang INTEGER,
        Account TEXT,
        Influencerscore INTEGER,
        Beiträge TEXT,
        Abonnenten TEXT,
        'Durschnittliche Likes' TEXT,
        'Engagement Rate' REAL,
        'Durchschnittliche Likes neuer Posts' TEXT,
        'Gesamte Likes' TEXT,
        'Land' TEXT,
        'Kategorie' TEXT,
        brand_partners TEXT DEFAULT ''
    )
''')

# Insérer les données dans la table "influenceurs"
for _, row in df.iterrows():
    cursor.execute('''
        INSERT INTO influenceurs (
            Rang, Account, Influencerscore, Beiträge, Abonnenten, 'Durschnittliche Likes', 'Engagement Rate', 'Durchschnittliche Likes neuer Posts', 'Gesamte Likes', 'Land', 'Kategorie', brand_partners
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, '')
    ''', (
        row['Rang'], row['Account'], row['Influencerscore'], row['Beiträge'], row['Abonnenten'],
        row['Durschnittliche Likes'], row['Engagement Rate'], row['Durchschnittliche Likes neuer Posts'], row['Gesamte Likes'], row['Land'], row['Kategorie']
    ))

# Sauvegarder les modifications
conn.commit()
conn.close()

print("La base de données SQLite 'marques_influenceurs.db' a été créée et la table 'influenceurs' a été remplie avec succès.")