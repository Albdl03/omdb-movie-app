import streamlit as st
import requests

# === Configuration ===
TMDB_API_KEY = "7d86c51be1bfe3761bfe7cbecf1f62fb"  # Replace with your actual TMDb API key
BASE_URL = "https://api.themoviedb.org/3"


# === API Functions ===
def search_actor(actor_name):
    url = f"{BASE_URL}/search/person"
    params = {"api_key": TMDB_API_KEY, "query": actor_name}
    res = requests.get(url, params=params)
    results = res.json().get("results", [])
    return results[0] if results else None


def get_filmography(person_id):
    url = f"{BASE_URL}/person/{person_id}/movie_credits"
    params = {"api_key": TMDB_API_KEY}
    res = requests.get(url, params=params)
    data = res.json()
    return sorted(data.get("cast", []), key=lambda x: x.get("release_date", ""), reverse=True)


def get_movie_details(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}"
    params = {"api_key": TMDB_API_KEY}
    res = requests.get(url, params=params)
    return res.json()


def search_combined(actor_name=None, title=None, year=None):
    results = []

    # If actor is provided, search filmography
    if actor_name:
        actor = search_actor(actor_name)
        if not actor:
            return []
        all_movies = get_filmography(actor["id"])
    else:
        # No actor: search by title and/or year
        url = f"{BASE_URL}/search/movie"
        params = {
            "api_key": TMDB_API_KEY,
            "query": title or "a",  # fallback query
        }
        if year:
            params["year"] = year
        res = requests.get(url, params=params)
        all_movies = res.json().get("results", [])

    # Filter results
    if title:
        all_movies = [
            m for m in all_movies
            if title.lower() in m.get("title", "").lower()
        ]

    if year:
        all_movies = [
            m for m in all_movies
            if m.get("release_date", "").startswith(year)
        ]

    return all_movies


def show_movie_details(movie):
    st.markdown(f"### 🎬 {movie.get('title', 'N/A')} ({movie.get('release_date', '')[:4]})")
    st.text(f"⭐ Rating: {movie.get('vote_average', 'N/A')} / 10")
    st.markdown(f"📝 **Overview**: {movie.get('overview', 'N/A')}")
    poster_path = movie.get("poster_path")
    if poster_path:
        st.image(f"https://image.tmdb.org/t/p/w500{poster_path}", width=300)


# === Streamlit App ===
st.set_page_config(page_title="🎥 TMDb Movie Explorer", layout="centered")
st.title("🎥 Movie Explorer – Search by Actor, Title & Year")

st.markdown("Use one or more filters below:")

actor_input = st.text_input("👤 Actor (optional)")
title_input = st.text_input("🎬 Title (optional)")
year_input = st.text_input("📅 Year (optional, e.g. 2010)")

if st.button("Search Movies"):
    if not (actor_input or title_input or year_input):
        st.warning("Please enter at least one filter.")
    else:
        with st.spinner("Searching TMDb..."):
            movies = search_combined(
                actor_name=actor_input.strip() or None,
                title=title_input.strip() or None,
                year=year_input.strip() or None
            )

        if not movies:
            st.error("No matching results found.")
        else:
            st.markdown("---")
            st.subheader("🎞️ Top 3 Results")

            top_movies = movies[:3]

            for movie in top_movies:
                details = get_movie_details(movie["id"])
                show_movie_details(details)
                st.markdown("---")
