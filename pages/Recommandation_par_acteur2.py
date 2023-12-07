import streamlit as st
import pandas as pd
import zipfile
import csv
from io import TextIOWrapper

# Chargement des données depuis le fichier CSV avec cache
@st.cache_data
def load_data():
# Chemin vers le fichier ZIP contenant le fichier CSV
    chemin_fichier_zip = r'.\Base_prete.zip'

# Nom du fichier CSV à l'intérieur du ZIP
    nom_fichier_csv = 'Base_prete.csv'

# Ouvrir le fichier ZIP en mode lecture
    with zipfile.ZipFile(chemin_fichier_zip, 'r') as zip_ref:
    # Extraire le fichier CSV en mémoire
        with zip_ref.open(nom_fichier_csv) as csv_file:
        # Lire le contenu CSV à l'aide de csv.reader
            df1 = pd.read_csv(TextIOWrapper(csv_file, 'utf-8'))
    return df1
   
def get_full_poster_url(poster_path):
    base_url = 'https://image.tmdb.org/t/p/w500/'
    return base_url + poster_path

# Interface Streamlit
st.title("Recommandations de films basées sur les acteurs")
actor_name = st.text_input("Entrez le nom d'un acteur :", "Brad Pitt")  # Valeur par défaut : "Brad Pitt"

# Filtrage des films en fonction du nom de l'acteur
df1 = load_data()  # Chargement des données
filtered_movies = df1[(df1['profession_1'] == 'actor') | 
                      (df1['profession_2'] == 'actor') |
                      (df1['profession_3'] == 'actor')]
filtered_movies = filtered_movies[filtered_movies['primaryName'] == actor_name]

# Affichage des films associés à l'acteur en colonnes de 4
if not filtered_movies.empty:
    st.write(f"Les films associés à l'acteur '{actor_name}' sont :")
    cols = st.columns(4)
    for index, movie in filtered_movies.iterrows():
        poster_url = get_full_poster_url(movie['poster_path'])
        with cols[int(index % 4)]:
            st.image(poster_url, caption=movie['originalTitle'], width=150)
else:
    st.write(f"Aucun film associé à l'acteur '{actor_name}' trouvé.")
