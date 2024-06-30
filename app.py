import streamlit as st
import pickle
import requests


# Load the movies DataFrame and similarity matrix
movies_df = pickle.load(open('movies.pkl', 'rb'))  # Keep the original DataFrame
movies = movies_df['title'].values
similarity = pickle.load(open('similarity.pkl', 'rb'))


def fetch_poster(movie_id):
    response=requests.get('https://api.themoviedb.org/3/movie/{}?'
                 'api_key=6ac1f677c4ded438cebac69d1495a77a&language=en-US'.format(movie_id))

    data=response.json()
    return "https://image.tmdb.org/t/p/w500/"+ data['poster_path']


def recommend(movie):
    # Get the index of the movie
    movie_index = movies_df[movies_df['title'] == movie].index[0]

    # Get the similarity scores for the movie
    distances = similarity[movie_index]

    # Get the indices of the top 5 similar movies
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]


    recommended_movies = []
    recommended_movies_poster=[]


    # Get the titles of the top 5 similar movies
    for i in movies_list:
        movie_id= movies_df.iloc[i[0]]['movie_id']

        recommended_movies.append(movies_df.iloc[i[0]]['title'])


        # fetch poster from API
        recommended_movies_poster.append(fetch_poster(movie_id))


    return recommended_movies,recommended_movies_poster


st.title('Movie Recommender System')

Movie_selected = st.selectbox(
    "Select a movie to get recommendations:",
    movies)

if st.button("RECOMMEND"):
    names,posters = recommend(Movie_selected)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])