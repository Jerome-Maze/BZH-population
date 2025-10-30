import requests
import pandas as pd

# URL du tableau
url = "https://france.comersis.com/listes-des-villes-de-bretagne-105.html"

# Lire les tables HTML avec pandas
tables = pd.read_html(url)

# Généralement, le premier tableau est celui qu'on veut
df = tables[0]

# Vérifier les colonnes
print(df.head())

# Sauvegarder en CSV
df.to_csv("bretagne_communes.csv", index=False)