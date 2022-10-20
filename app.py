import streamlit as st
import pandas as pd
import numpy as np
import difflib

DATA_URL = 'data/movies.csv'
SCORES_URL = 'data/sim_scores.npy'

@st.cache(persist =True)
def get_simscores(SCORES_URL):
    similarity_matrix = np.load('data/sim_scores.npy')
    return similarity_matrix

@st.cache(persist =True)
def get_titles(DATA_URL):
    titles = pd.read_csv(DATA_URL, usecols = ['title'])['title'].tolist()
    return titles
def match_input_movie(inp_movie, titles_lst):
    closest_match = difflib.get_close_matches(inp_movie, titles_lst)[0]
    return closest_match

def get_ten_suggestions(mov_idx, sim_scores, idx_to_title):
    movie_movies_sim = list(enumerate(sim_scores[mov_idx]))
    sortd_sim = sorted(movie_movies_sim, key= lambda x: x[1], reverse= True)
    k = 1
    for i, _ in sortd_sim[1:]:
        if k < 11:
            title = idx_to_title[i]
            st.write(f"{k} . {title}")
            k+=1




if __name__ == "__main__":
    similarity_matrix = get_simscores(SCORES_URL)
    titles = get_titles(DATA_URL)

    title_to_idx = {v: k for k, v in enumerate(titles)}
    idx_to_title = {k: v for k, v in enumerate(titles)}

    st.header("Movie Recommender 🍿👀📽")

    st.subheader('How it works:')
    st.write('We recommend you 10 movies based on the last movie you have watched.')
    mov = st.text_input("Last Movie")
    if mov:
        cl_mov = match_input_movie(mov, titles)
        cl_mov_idx = title_to_idx[cl_mov]

        get_ten_suggestions(cl_mov_idx, similarity_matrix, idx_to_title)

