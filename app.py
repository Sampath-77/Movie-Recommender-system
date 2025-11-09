import streamlit as st
import pickle
import pandas as pd
import requests
import time
import base64
import io

# --- Page Configuration ---
# This should be the first Streamlit command in your script
st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed" # Changed to collapsed as sidebar is removed
)

# --- Constants ---
API_KEY = "TMDB_YOUR-API_KEY"
BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"
FALLBACK_POSTER = "https://via.placeholder.com/300x450/2b2b2b/ffffff?text=No+Poster"

# --- Data and Function Definitions ---

# Function to encode image to Base64
def get_image_as_base64(path):
    """Reads an image file and returns its Base64 encoded string."""
    try:
        with open(path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        st.warning(f"Background image '{path}' not found. Using a default fallback.", icon="⚠️")
        return None

# Function to fetch movie poster from TMDB API
def fetch_poster(movie_id):
    """Fetches a movie poster URL from TMDB API given a movie ID."""
    url = f'{BASE_URL}/movie/{movie_id}?api_key={API_KEY}&language=en-US'
    retries = 3
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # Raise an exception for bad status codes
            data = response.json()
            if data.get('poster_path'):
                return f"{IMAGE_BASE_URL}{data['poster_path']}"
            else:
                # Return a placeholder if no poster is found
                return FALLBACK_POSTER
        except requests.exceptions.RequestException as e:
            time.sleep(1) # Wait before retrying
    # Return a placeholder if all retries fail
    return FALLBACK_POSTER


# Function to get movie recommendations
def recommend(movie):
    """Returns a list of recommended movies and their posters."""
    try:
        movie_index = movies[movies['title'] == movie].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

        recommended_movies = []
        recommended_movies_posters = []
        for i in movies_list:
            movie_id = movies.iloc[i[0]].movie_id
            recommended_movies.append(movies.iloc[i[0]].title)
            recommended_movies_posters.append(fetch_poster(movie_id))
        return recommended_movies, recommended_movies_posters
    except IndexError:
        return [], []
    except Exception as e:
        st.error(f"An error occurred during recommendation: {e}")
        return [], []


# --- Load Data ---
# Load the movie dictionary and similarity matrix from pickle files.
# Ensure these files are in the same directory as your app.py.
try:
    movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
    movies = pd.DataFrame(movie_dict)
    similarity = pickle.load(open('similarity.pkl', 'rb'))
except FileNotFoundError:
    st.error("Model files (movie_dict.pkl, similarity.pkl) not found. Please ensure they are in the correct directory.", icon="🚨")
    st.stop()


# --- Set Background Image ---
DEFAULT_BG_IMAGE = "MARICINEMA_BACKGROUND.jpg"
FALLBACK_BG_URL = "https://assets.nflxext.com/ffe/siteui/vlv3/51e5354A-096B-4160-8AB3-233B8A7E0799/67272782-7235-4424-8509-91a5459ec78a/IN-en-20230320-popsignuptwoweeks-perspective_alpha_website_large.jpg"

# Try to use the default local image
base64_img = get_image_as_base64(DEFAULT_BG_IMAGE)
if base64_img:
    # Use the local file if found
    bg_image_css = f"data:image/jpg;base64,{base64_img}"
else:
    # If local image fails, use the fallback URL
    bg_image_css = FALLBACK_BG_URL


# --- Custom Styling (CSS) ---
st.markdown(f"""
<style>
    /* --- General Body and Font --- */
    .stApp {{
        background-image: linear-gradient(to top, rgba(0, 0, 0, 1) 0, rgba(0, 0, 0, 0.6) 60%, rgba(0, 0, 0, 1) 100%), url('{bg_image_css}');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    /* --- Hide Streamlit Header/Footer --- */
    header, footer {{
        visibility: hidden;
    }}
    /* --- Custom Button Styles --- */
    .stButton > button {{
        background-color: #E50914;
        color: white;
        border-radius: 5px;
        padding: 0.75rem 1.5rem;
        font-weight: bold;
        border: none;
        font-size: 1.25rem;
    }}
    .stButton > button:hover {{
        background-color: #F6121D;
        color: white;
    }}
    /* --- Custom SelectBox --- */
    .stSelectbox > div > div {{
        background-color: rgba(70, 70, 70, 0.7);
        border: 1px solid #8c8c8c;
        border-radius: 5px;
    }}
    /* --- Horizontal Line Separator --- */
    hr {{
        height: 8px;
        background-color: #222;
        border: none;
        margin: 2rem 0;
    }}
</style>
""", unsafe_allow_html=True)


# --- Header Section ---
col1, col2, col3 = st.columns([2, 5, 2])
with col1:
    st.image("MARICINEMA.png", width=200)


# --- Recommender Section ---
st.markdown("<br><br><br>", unsafe_allow_html=True)
with st.container():
    st.markdown("<h1 style='text-align: center; font-size: 3.5rem; font-weight: 900;'>Movie Recommender System</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2rem; margin: 1rem 0;'>Select a movie you like, and we'll recommend five similar ones.</p>", unsafe_allow_html=True)

    form_cols = st.columns([1, 2.5, 1])
    with form_cols[1]:
        selected_movie_name = st.selectbox(
            'Select a movie from the dropdown:',
            movies['title'].values,
            label_visibility="collapsed"
        )
        
        button_container = st.columns([1, 1.5, 1])
        with button_container[1]:
            if st.button('Recommend Movies', use_container_width=True):
                names, posters = recommend(selected_movie_name)
                # Store recommendations in session state to persist them
                st.session_state.names = names
                st.session_state.posters = posters

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)


# --- Display Recommendations Section ---
if 'names' in st.session_state and st.session_state.names:
    with st.container():
        st.markdown("<h2 style='font-size: 2rem; font-weight: bold; margin-bottom: 1.5rem;'>Recommended For You</h2>", unsafe_allow_html=True)
        
        # Create 5 columns for the 5 recommendations
        recommendation_cols = st.columns(5)
        for i, col in enumerate(recommendation_cols):
            with col:
                st.markdown(f"<h5 style='text-align: center; height: 3rem;'>{st.session_state.names[i]}</h5>", unsafe_allow_html=True)
                st.image(st.session_state.posters[i])
else:
    # A placeholder message before any recommendations are generated
    st.markdown("<div style='text-align: center; font-size: 1.2rem; color: #8c8c8c;'>Your recommendations will appear here...</div>", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

