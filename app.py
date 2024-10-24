import streamlit as st
st.set_page_config(layout="wide")
st.text('started1')
from loader import load_data, load_model
from mood_recommendations import recommend_by_mood
from similar_movies import find_similar_movies
from user_input_recommendations import handle_user_input
import pandas as pd
import json
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer


st.text('started2')
# Set a base URL for the posters
BASE_URL = "https://image.tmdb.org/t/p/w500"  # Use a consistent base URL for all sections

# Paths to your data and model
data_path = 'data/df_movies.csv'
model_path = 'models/all-MiniLM-L6-v2'
embeddings_path = 'data/movies_embeddings.pkl'
top_10_similar_path = 'data/top_10_similar_movies.json'

@st.cache_data
def get_data(path):
    return load_data(path)

@st.cache_resource
def get_model(path):
    return load_model(path)

@st.cache_data
def load_top_10_similar(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return {key: (np.array(value[0]), np.array(value[1])) for key, value in data.items()}

@st.cache_data
def load_movie_embeddings(file_path):
    with open(file_path, 'rb') as f:
        embeddings = pickle.load(f)
    return embeddings

# Load the data and resources
df = get_data(data_path)
model = get_model(model_path)
top_10_similar = load_top_10_similar(top_10_similar_path)
movie_embeddings = load_movie_embeddings(embeddings_path)

st.title('Movies Recommendation Engine')

st.divider()
# Mood-based recommendations
st.header('(1/3) Recommend Movies Based on Mood')
moods = ['dramatic', 'tense', 'melancholy', 'inspirational', 'romantic',
       'sad', 'exciting', 'whimsical', 'epic', 'dark', 'uplifting',
       'chilling', 'joyful']

user_mood = st.selectbox("Select your mood", moods)
mood_recomms = recommend_by_mood(df, user_mood)
movie_titles = mood_recomms['tmdb_original_title']
poster_paths = mood_recomms['poster_path']

# Generate HTML for mood-based recommendations
images_html = (
    '<style>'
    'div.scrollmenu {'
    '    overflow: auto;'
    '    white-space: nowrap;'
    '    width: 100%;'
    '}'
    'div.movie-block {'
    '    display: inline-block;'
    '    text-align: center;'
    '    margin: 10px;'
    '    width: 200px;'
    '}'
    'img {'
    '    width: 100%;'
    '    height: auto;'
    '}'
    '</style>'
    '<div class="scrollmenu">'
)

images_html += "".join(
    f'<div class="movie-block">'
    f'<img src="{BASE_URL + path}" alt="Movie poster">'
    f'<div style="margin-top: 5px;">{title}</div>'
    f'</div>'
    for path, title in zip(poster_paths, movie_titles)
)

images_html += '</div>'
st.markdown(images_html, unsafe_allow_html=True)

st.divider()

# Similar movies
st.header('(2/3) Recommend Similar Movies')
all_titles = df['tmdb_original_title'].unique()
user_selected_movie = st.selectbox("Show me movies similar to:", all_titles)
similar_movies = find_similar_movies(user_selected_movie, df, top_10_similar, top_n=10)
similar_movie_titles = [movie[0] for movie in similar_movies]
similar_movie_poster_paths = [movie[1] for movie in similar_movies]

# Generate HTML for similar movies
similar_movies_images_html = (
    '<style>'
    'div.scrollmenu {'
    '    overflow: auto;'
    '    white-space: nowrap;'
    '    width: 100%;'
    '}'
    'div.movie-block {'
    '    display: inline-block;'
    '    text-align: center;'
    '    margin: 10px;'
    '    width: 200px;'
    '}'
    'img {'
    '    width: 100%;'
    '    height: auto;'
    '}'
    '</style>'
    '<div class="scrollmenu">'
)

similar_movies_images_html += "".join(
    f'<div class="movie-block">'
    f'<img src="{BASE_URL + path}" alt="Movie poster">'
    f'<div style="margin-top: 5px;">{title}</div>'
    f'</div>'
    for path, title in zip(similar_movie_poster_paths, similar_movie_titles)
)

similar_movies_images_html += '</div>'
st.markdown(similar_movies_images_html, unsafe_allow_html=True)

st.divider()

# User input based recommendations
st.header('(3/3) Find Movies Based on Your Input')
user_input = st.text_area("Enter the kind of movie you like to watch:", height=100)

if st.button('Show Recommendations'):
    result = handle_user_input(user_input, df, model, movie_embeddings)
    input_based_movie_titles = result['tmdb_original_title'].tolist()
    input_based_poster_paths = result['poster_path'].tolist()

    # Generate HTML for input-based recommendations
    input_based_recommendations_html = (
        '<style>'
        'div.scrollmenu {'
        '    overflow: auto;'
        '    white-space: nowrap;'
        '    width: 100%;'
        '}'
        'div.movie-block {'
        '    display: inline-block;'
        '    text-align: center;'
        '    margin: 10px;'
        '    width: 200px;'
        '}'
        'img {'
        '    width: 100%;'
        '    height: auto;'
        '}'
        '</style>'
        '<div class="scrollmenu">'
    )

    input_based_recommendations_html += "".join(
        f'<div class="movie-block">'
        f'<img src="{BASE_URL + path}" alt="Movie poster">'
        f'<div style="margin-top: 5px;">{title}</div>'
        f'</div>'
        for path, title in zip(input_based_poster_paths, input_based_movie_titles)
    )

    input_based_recommendations_html += '</div>'
    st.markdown(input_based_recommendations_html, unsafe_allow_html=True)
