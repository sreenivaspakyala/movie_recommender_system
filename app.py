import os

import streamlit as st
import pickle
import pandas as pd
import requests
import os
import bz2
import _pickle as cpickle
from dotenv import load_dotenv

load_dotenv('keys.env')

api_key = os.getenv('API_KEY')
image_path = os.getenv('IMAGE_PATH')



def get_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key={}&language=en-US'.format(movie_id,api_key))
    data = response.json()
    return image_path + data['poster_path']

def decompress_pickle(file):
     data = bz2.BZ2File(file, 'rb')
     data = cpickle.load(data)
     return data

movies_dict = pickle.load(open('movies_dict.pkl','rb'))
similarity = decompress_pickle('similarity.pbz2')

movies_df = pd.DataFrame(movies_dict)
movies_list = movies_df['title'].values

st.title('Movie Recommender System')

def recommend_movies(movie_name):
    movie_index = movies_df[movies_df['title'] == movie_name].index[0]
    movie_id = movies_df.iloc[movie_index].id
    distances = similarity[movie_index]
    movies_found = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    movie_posters = []
    for i in movies_found:
        movie_id = movies_df.iloc[i[0]].id
        recommended_movies.append(movies_df.iloc[i[0]].title)
        movie_posters.append(get_poster(movie_id))


    return recommended_movies,movie_posters

movie_typed = st.selectbox('Enter Movie Name',movies_list)

if st.button("Recommend Movies"):
    recommendations,posters = recommend_movies(movie_typed)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(recommendations[0])
        st.image(posters[0])

    with col2:
        st.text(recommendations[1])
        st.image(posters[1])

    with col3:
        st.text(recommendations[2])
        st.image(posters[2])

    with col4:
        st.text(recommendations[3])
        st.image(posters[3])

    with col5:
        st.text(recommendations[4])
        st.image(posters[4])

