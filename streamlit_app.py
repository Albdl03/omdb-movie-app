import streamlit as st
import requests

API_KEY = "thewdb"


def search_movies(title_filter=None, actor_filter=None, year_filter=None, max_pages=5):
    query = title_filter if title_filter else (actor_filter if actor_filter else "a")
    movies = []

    for page in range(1, max_pages + 1):
        url = "http://www.omdbapi.com/"
        params = {"s": query, "apikey": API_KEY, "page": page}
        res = requests.get(url, params=params)
        data = res.json()

        if data.get("Response") != "True":
            break  # Stop if no more results

        for movie in data.get("Search", []):
            imdb_id = movie.get("imdbID")
            details = get_movie_details(imdb_id)

            # Actor filter
            if actor_filter:
                actors = details.get("Actors", "").lower()
                if actor_filter.lower() not in actors:
                    continue

            # Title filter (re-check if needed)
            if title_filter:
                if title_filter.lower() not in details.get("Title", "").lower():
                    continue

            # Year filter
            if year_filter:
                if year_filter != details.get("Year"):
                    continue

            movies.append(details)

    return movies


def get_movie_details(imdb_id):
    url = "http://www.omdbapi.com/"
    params = {"i": imdb_id, "apikey": API_KEY}
    res = requests.get(url, params=params)
    return res.json()


def show_movie_details(movie):
    st.markdown(f"### 🎬 {movie.get('Title', 'N/A')} ({movie.get('Year', 'N/A')})")
    st.text(f"🎭 Genre: {movie.get('Genre', 'N/A')}")
    st.text(f"🎬 Director: {movie.get('Director', 'N/A')}")
    st.text(f"👥 Actors: {movie.get('Actors', 'N/A')}")
    st.text(f"⭐ IMDB Rating: {movie.get('imdbRating', 'N/A')}")
    st.markdown(f"📝 **Plot**: {movie.get('Plot', 'N/A')}")


# === Streamlit App ===
st.set_page_config(page_title="🎥 OMDb Movie Explorer", layout="centered")
st.title("🎥 OMDb Movie Explorer")

st.markdown("Search by **title**, **actor**, and/or **year**. You can leave any field empty.")

# Input fields (none are required)
title_input = st.text_input("🎬 Title (optional)")
actor_input = st.text_input("👤 Actor (optional, partial name allowed)")
year_input = st.text_input("📅 Year (optional, e.g. 1999)")

# Search button
if st.button("Search"):
    if not (title_input.strip() or actor_input.strip() or year_input.strip()):
        st.warning("Please enter at least one search criteria (title, actor, or year).")
    else:
        results = search_movies(
            title_filter=title_input.strip(),
            actor_filter=actor_input.strip(),
            year_filter=year_input.strip()
        )

        if not results:
            st.error("No matching results found.")
        else:
            titles = [f"{movie.get('Title', 'N/A')} ({movie.get('Year', 'N/A')})" for movie in results]
            selected = st.selectbox("Select a movie to view details:", titles)
            selected_movie = results[titles.index(selected)]

            st.markdown("---")
            show_movie_details(selected_movie)
