import streamlit as st
import pandas as pd
import zipfile
import csv
from io import TextIOWrapper

# Chemin vers le fichier ZIP contenant le fichier CSV
chemin_fichier_zip = r'./Base_prete.zip'

# Nom du fichier CSV à l'intérieur du ZIP
nom_fichier_csv = 'Base_prete.csv'

# Ouvrir le fichier ZIP en mode lecture
with zipfile.ZipFile(chemin_fichier_zip, 'r') as zip_ref:
    # Extraire le fichier CSV en mémoire
    with zip_ref.open(nom_fichier_csv) as csv_file:
        # Lire le contenu CSV à l'aide de csv.reader
        df = pd.read_csv(TextIOWrapper(csv_file, 'utf-8'))


# Fonction pour obtenir l'URL complète de l'affiche
def get_full_poster_url(poster_path):
    base_url = 'https://image.tmdb.org/t/p/w500/'
    return base_url + poster_path

df['poster_url'] = df['poster_path'].apply(get_full_poster_url)

# Liste des genres
genres = ['Drama', 'Comedy', 'Action', 'Documentary', 'Horror', 'Crime', 'Sci-Fi', 'Biography',
          'Adventure', 'Thriller', 'Romance', 'Fantasy', 'Family', 'Animation', 'Musical',
          'Western', 'Mystery', 'History', 'Music', 'War', 'Sport', 'Reality-TV', 'News']

top_movies_by_genre = {}

# Extraire les meilleurs films par genre
for genre in genres:
    genre_data = df[df[genre] == 1]
    grouped_genre_data = genre_data.groupby('originalTitle').first().reset_index()
    top_movies_genre = grouped_genre_data.sort_values(by='vote_count', ascending=False).head(5)
    top_movies_by_genre[genre] = top_movies_genre

# Interface Streamlit
st.title("Les 5 meilleurs films par genre")

# Affichage des films par genre
for genre, top_movies in top_movies_by_genre.items():
    st.header(f"Genre: {genre}")
    
    # Calcul du nombre de colonnes
    num_columns = min(5, len(top_movies))  # On prend soit 5 soit le nombre de films disponibles
    
    # Création des colonnes pour les affiches
    cols = st.columns(num_columns)
    for i in range(num_columns):
        if i < len(top_movies):
            movie = top_movies.iloc[i]
            poster_url = movie['poster_url']
            
            with cols[i]:
                st.image(poster_url, caption=movie['originalTitle'], width=150)
