# Machine Learning en version streamlit exploitable
import streamlit as st
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
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
        df1 = pd.read_csv(TextIOWrapper(csv_file, 'utf-8'))


# Sélection des colonnes incluant des nombres
features = df1.select_dtypes(include=['number']).columns.tolist()

# Groupement des données par titre de film
grouped = df1.groupby('originalTitle')[features].mean().reset_index()

# Normalisation
scaler = StandardScaler()
scaled_features = scaler.fit_transform(grouped[features])

# KNN
k = 10  # Nombre de voisins
model = NearestNeighbors(n_neighbors=k, metric='euclidean')
model.fit(scaled_features)

# Fonction de recommandation des films
def recommend_movies(movie_title, num_recommendations=5):
    movie_indices = grouped[grouped['originalTitle'] == movie_title].index.values
    if len(movie_indices) == 0:
        print("Le film spécifié n'est pas trouvé.")
        return []
    
    movie_index = movie_indices[0] 
    distances, indices = model.kneighbors([scaled_features[movie_index]])
    recommended_movies = []
    for i in range(1, num_recommendations + 1):
        recommended_movies.append(grouped.iloc[indices[0][i]]['originalTitle'])
    return recommended_movies

# Ajouter les URLs complètes des affiches dans le DataFrame
def get_full_poster_url(poster_path):
    base_url = 'https://image.tmdb.org/t/p/w500/'
    return base_url + poster_path

df1['poster_url'] = df1['poster_path'].apply(get_full_poster_url)

# Interface Streamlit
st.title("Système de recommandation de films")
film_utilisateur = st.text_input("Entrez le nom d'un film :", "Inception")  # Valeur par défaut : "Inception"

if st.button("Obtenir les recommandations"):
    recommended_movies = recommend_movies(film_utilisateur)

    if recommended_movies:
        st.write(f"Pour '{film_utilisateur}', les films recommandés sont :")
        
        # Mise en page en ligne des images des affiches
        
        cols = st.columns(len(recommended_movies))
        for i, movie_title in enumerate(recommended_movies):
            poster_url = df1[df1['originalTitle'] == movie_title]['poster_url'].iloc[0]
            with cols[i]:
                st.image(poster_url, caption=movie_title, width=150)
    else:
        st.write("Le film spécifié n'a pas été trouvé.")
