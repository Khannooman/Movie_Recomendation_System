import streamlit as st
import pandas as pd
import pickle
import requests
new_df = pickle.load(open('movies_dic.pkl', 'rb'))
similarity_score = pickle.load(open('similarity_score.pkl', 'rb'))

movies = pd.DataFrame(new_df)
st.title('Movie Recomendation System')

selected_movie_name = st.selectbox('Movies',
             (movies['title'].values))

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"

    headers = {
        "accept": "application/json",
        "Authorization":  "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzZGQ2Y2Y2NmM5NjY5MzhjOTRjNWY2MmY0N2Q5OWE4OCIsInN1YiI6IjY0ZGY0ZjZiMzcxMDk3MDExYzUzNzRlZiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.OyriFcX7l9Snl6Y-v95bva14sl464Zj0QuzoEXY5hYk"
    }
    response = requests.get(url, headers=headers)

    data = response.json()
    return  "https://image.tmdb.org/t/p/original" + data['poster_path']

def recomend(movie):
    similar_movies = []
    movie_poster = []
    movie_index = movies[movies["title"]==movie].index[0]
    distance = similarity_score[movie_index]
    similar = sorted(enumerate(distance), key = lambda x:x[1], reverse = True)[1:6]
    for i, j in similar:
        movie_id = movies.loc[i]['id']
        # featch poster
        try:
            poster_path = fetch_poster(movie_id=movie_id)
            movie_poster.append(poster_path)
        except:
            movie_poster.append('path_error')
        similar_movies.append(movies.loc[i]['title'])

    return similar_movies, movie_poster


if st.button('Recomend'):
    st.write(selected_movie_name)
    movie_to_recomend, poster = recomend(selected_movie_name)

    col1 , col2, col3, col4, col5 = st.columns(5)
    with col1:
        if poster[0] == "path_error":
            st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTQysrTNrGQQZFyJhxVLSl98UvbpYSLvOnt0A&usqp=CAU")
        else:
            print(poster[0])
            st.image(poster[0])
        st.subheader(movie_to_recomend[0])

    with col2:
        if poster[1] == "path_error":
            st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTQysrTNrGQQZFyJhxVLSl98UvbpYSLvOnt0A&usqp=CAU")
        else:
            st.image(poster[1])
        st.subheader(movie_to_recomend[1])

    with col3:
        if poster[2] == "path_error":
            st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTQysrTNrGQQZFyJhxVLSl98UvbpYSLvOnt0A&usqp=CAU")
        else:
            st.image(poster[2])
        st.subheader(movie_to_recomend[2])


    with col4:
        if poster[3] == "path_error":
            st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTQysrTNrGQQZFyJhxVLSl98UvbpYSLvOnt0A&usqp=CAU")
        else:
            st.image(poster[3])
        st.subheader(movie_to_recomend[3])

    with col5:
        if poster[4] == "path_error":
            st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTQysrTNrGQQZFyJhxVLSl98UvbpYSLvOnt0A&usqp=CAU")
        else:
            st.image(poster[4])
        st.subheader(movie_to_recomend[4])
    



