import streamlit as st
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
import zipfile
import csv
from io import TextIOWrapper

# Chemin vers le fichier ZIP contenant le fichier CSV
chemin_fichier_zip = r'.\Base_prete.zip'

# Nom du fichier CSV à l'intérieur du ZIP
nom_fichier_csv = 'Base_prete.csv'

# Ouvrir le fichier ZIP en mode lecture
with zipfile.ZipFile(chemin_fichier_zip, 'r') as zip_ref:
    # Extraire le fichier CSV en mémoire
    with zip_ref.open(nom_fichier_csv) as csv_file:
        # Lire le contenu CSV à l'aide de csv.reader
        df2 = pd.read_csv(TextIOWrapper(csv_file, 'utf-8'))

#Recommandation pour 3 films

# Sélection des colonnes incluant des nombres
features2 = df2.select_dtypes(include=['number']).columns.tolist()

# Groupement des données par titre de film
grouped2 = df2.groupby('originalTitle')[features2].mean().reset_index()

# Normalisation
scaler2 = StandardScaler()
scaled_features2 = scaler2.fit_transform(grouped2[features2])

# KNN
k2 = 10  # Nombre de voisins
model2 = NearestNeighbors(n_neighbors=k2, metric='euclidean')
model2.fit(scaled_features2)

def movie_title2(num_recommendations=1):
    movies = []

    for _ in range(3):  # Repeat the process for three movies
        film = input("Entrée un film: ")
        movie_indices2 = grouped2[grouped2['originalTitle'] == film].index.values

        while len(movie_indices2) == 0:
            print("Le film spécifié n'est pas trouvé.")
            film = input("Enter the movie title again: ")
            movie_indices2 = grouped2[grouped2['originalTitle'] == film].index.values

        movies.append(film)
        
    movie_index2 = movie_indices2[0] 
    distances, indices = model2.kneighbors([scaled_features2[movie_index2]])
    recommended_movies2 = []
    for i in range(1, num_recommendations + 1):
        recommended_movies2.append(grouped2.iloc[indices[0][i]]['originalTitle'])
    return recommended_movies2
def recommend_movies2(film1, film2, film3, num_recommendations=1):
    movies = []
    movies.append(film1)
    movies.append(film2)
    movies.append(film3)
    movie_index2 = movie_indices2[0] 
    distances, indices = model2.kneighbors([scaled_features2[movie_index2]])
    recommended_movies2 = []
    for i in range(1, num_recommendations + 1):
        recommended_movies2.append(grouped2.iloc[indices[0][i]]['originalTitle'])
    return recommended_movies2
   
# Ajouter les URLs complètes des affiches dans le DataFrame
def get_full_poster_url(poster_path):
    base_url = 'https://image.tmdb.org/t/p/w500/'
    return base_url + poster_path

df2['poster_url'] = df2['poster_path'].apply(get_full_poster_url)
# Interface Streamlit
st.title("Système de recommandation de films")
#film_utilisateur = st.text_input("Entrez le nom d'un film :", "Inception")  # Valeur par défaut : "Inception"
movies = []

film1 = st.text_input("Entrée un premier film: ")
movie_indices2 = grouped2[grouped2['originalTitle'] == film1].index.values

while len(movie_indices2) == 0:
    print("Le film spécifié n'est pas trouvé.")
    film1 = input("Entrée un premier film: ")
    movie_indices2 = grouped2[grouped2['originalTitle'] == film1].index.values


film2 = st.text_input("Entrée un second film: ")
movie_indices2 = grouped2[grouped2['originalTitle'] == film2].index.values

while len(movie_indices2) == 0:
    print("Le film spécifié n'est pas trouvé.")
    film2 = input("Entrée un premier film: ")
    movie_indices2 = grouped2[grouped2['originalTitle'] == film2].index.values


film3 = st.text_input("Entrée un troisième film: ")
movie_indices2 = grouped2[grouped2['originalTitle'] == film3].index.values

while len(movie_indices2) == 0:
    print("Le film spécifié n'est pas trouvé.")
    film3 = input("Entrée un premier film: ")
    movie_indices2 = grouped2[grouped2['originalTitle'] == film3].index.values



if st.button("Obtenir la recommandation"):
    recommended_movies2 = recommend_movies2(film1, film2, film3)

    if recommended_movies2:
        st.write(f"Pour {film1, film2, film3}, le film recommandés est :")
        
        # Mise en page en ligne des images des affiches
        
        cols = st.columns(len(recommended_movies2))
        for i, movie_title in enumerate(recommended_movies2):
            poster_url = df2[df2['originalTitle'] == movie_title]['poster_url'].iloc[0]
            with cols[i]:
                st.image(poster_url, caption=movie_title, width=150)
    else:
        st.write("Le film spécifié n'a pas été trouvé.")