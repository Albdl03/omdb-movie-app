import streamlit as st
import requests

# === CONFIG ===
API_KEY = "thewdb"  # Replace with your personal OMDb API key

# === FUNCTION: Search by movie title ===
def search_by_title(title):
    url = "http://www.omdbapi.com/"
    params = {"s": title, "apikey": API_KEY}
    res = requests.get(url, params=params)
    data = res.json()
    return data.get("Search", []) if data.get("Response") == "True" else []

# === FUNCTION: Get full movie details by IMDb ID ===
def get_movie_details(imdb_id):
    url = "http://www.omdbapi.com/"
    params = {"i": imdb_id, "apikey": API_KEY}
    res = requests.get(url, params=params)
    return res.json()

# === FUNCTION: Search by actor (partial match) ===
def search_by_actor(actor_query):
    all_results = search_by_title(actor_query)
    filtered = []
    for movie in all_results:
        details = get_movie_details(movie["imdbID"])
        actors = details.get("Actors", "").lower()
        if actor_query.lower() in actors:
            filtered.append(details)
    return filtered

# === FUNCTION: Show selected movie details ===
def show_movie_details(movie):
    st.markdown(f"### 🎬 {movie.get('Title', 'N/A')} ({movie.get('Year', 'N/A')})")
    st.text(f"🎭 Genre: {movie.get('Genre', 'N/A')}")
    st.text(f"🎬 Director: {movie.get('Director', 'N/A')}")
    st.text(f"👥 Actors: {movie.get('Actors', 'N/A')}")
    st.text(f"⭐ IMDB Rating: {movie.get('imdbRating', 'N/A')}")
    st.markdown(f"📝 **Plot**: {movie.get('Plot', 'N/A')}")

# === Streamlit UI ===
st.set_page_config(page_title="🎥 OMDb Movie Explorer", layout="centered")
st.title("🎥 OMDb Movie Explorer")

# Search type selection
search_type = st.radio("Choose search type:", ["By Title", "By Actor"])

# Search query input
query = st.text_input("Enter search query (e.g. 'Inception' or 'DiCaprio')")

# Search button
if st.button("Search"):
    if not query.strip():
        st.warning("Please enter a search term.")
    else:
        if search_type == "By Title":
            results = search_by_title(query)
        else:
            results = search_by_actor(query)

        if not results:
            st.error("No results found.")
        else:
            titles = [f"{movie.get('Title', 'N/A')} ({movie.get('Year', 'N/A')})" for movie in results]
            selected = st.selectbox("Select a movie to view details:", titles)
            selected_index = titles.index(selected)
            selected_movie = results[selected_index]

            st.markdown("---")
            show_movie_details(selected_movie)
