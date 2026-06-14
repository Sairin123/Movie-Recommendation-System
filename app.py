import streamlit as st
import pickle
import requests


# def fetch_poster(movie_id):
#     url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US"

#     try:
#         response = requests.get(url, timeout=10)
#         response.raise_for_status()   # check HTTP errors

#         data = response.json()
#         poster_path = data.get('poster_path')

#         if poster_path:
#             return "https://image.tmdb.org/t/p/w500/" + poster_path
#         else:
#             return "https://via.placeholder.com/500x750?text=No+Image"

#     except requests.exceptions.RequestException as e:
#         print("Error fetching poster:", e)
#         return "https://via.placeholder.com/500x750?text=No+Image"

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Image"
    except Exception as e:
        print(f"Error fetching poster for {movie_id}: {e}")
        return "https://via.placeholder.com/500x750?text=No+Image"


movies = pickle.load(open("movies_list.pkl", 'rb'))
similarity = pickle.load(open("similarity.pkl", 'rb'))
movies_list=movies['title'].values

st.header("Movie Recommender System")

import os
import zipfile
import streamlit.components.v1 as components

# Fix for Streamlit Cloud deployment: Use absolute path relative to this file
parent_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(parent_dir, "frontend", "public")

# If the frontend directory does not exist, try to extract it from frontend.zip
if not os.path.exists(build_dir):
    zip_path = os.path.join(parent_dir, "frontend.zip")
    if os.path.exists(zip_path):
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(parent_dir)
        except Exception as e:
            print(f"Error extracting frontend.zip: {e}")
    else:
        print("frontend.zip not found to extract.")

imageCarouselComponent = components.declare_component("image-carousel-component", path=build_dir)


imageUrls = [
    fetch_poster(1632),
    fetch_poster(299536),
    fetch_poster(17455),
    fetch_poster(2830),
    fetch_poster(429422),
    fetch_poster(9722),
    fetch_poster(13972),
    fetch_poster(240),
    fetch_poster(155),
    fetch_poster(598),
    fetch_poster(914),
    fetch_poster(255709),
    fetch_poster(572154)
   
    ]


imageCarouselComponent(imageUrls=imageUrls, height=200)
selectvalue=st.selectbox("Select movie from dropdown", movies_list)

# def recommend(movie):
#     index=movies[movies['title']==movie].index[0]
#     distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector:vector[1])
#     recommend_movie=[]
#     recommend_poster=[]
#     for i in distance[1:6]:
#         movies_id=movies.iloc[i[0]].id
#         recommend_movie.append(movies.iloc[i[0]].title)
#         recommend_poster.append(fetch_poster(movies_id))
#     return recommend_movie, recommend_poster

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    # similarity[index] now contains only the indices of top recommendations
    movie_indices = similarity[index]
    recommend_movie = []
    recommend_poster = []
    for i in movie_indices[1:9]: # Top 8 recommendations
        movies_id = movies.iloc[i].id
        recommend_movie.append(movies.iloc[i].title)
        recommend_poster.append(fetch_poster(movies_id))
    return recommend_movie, recommend_poster




if st.button("Show Recommend"):
    movie_name, movie_poster = recommend(selectvalue)
    col1,col2,col3,col4,col5,col6,col7,col8=st.columns(8)
    with col1:
        st.text(movie_name[0])
        st.image(movie_poster[0])
    with col2:
        st.text(movie_name[1])
        st.image(movie_poster[1])
    with col3:
        st.text(movie_name[2])
        st.image(movie_poster[2])
    with col4:
        st.text(movie_name[3])
        st.image(movie_poster[3])
    with col5:
        st.text(movie_name[4])
        st.image(movie_poster[4])
    with col6:
        st.text(movie_name[5])
        st.image(movie_poster[5])
    with col7:
        st.text(movie_name[6])
        st.image(movie_poster[6])
    with col8:
        st.text(movie_name[7])
        st.image(movie_poster[7])