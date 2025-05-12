import streamlit as st
import requests

TMDB_API_KEY = "YOUR_TMDB_API_KEY"  # Replace with your real TMDb API key

BASE_URL = "https://api.themoviedb.org/3"


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


def show_movie_details(movie):
    st.markdown(f"### 🎬 {movie.get('title', 'N/A')} ({movie.get('release_date', 'N/A')[:4]})")
    st.text(f"⭐ Rating: {movie.get('vote_average', 'N/A')} / 10")
    st.markdown(f"📝 **Overview**: {movie.get('overview', 'N/A')}")
    poster_path = movie.get("poster_path")
    if poster_path:
        st.image(f"https://image.tmdb.org/t/p/w500{poster_path}", width=300)


# === Streamlit App UI ===
st.set_page_config(page_title="🎥 TMDb Actor Movie Search", layout="centered")
st.title("🎥 Search Movies by Actor (TMDb)")

actor_input = st.text_input("👤 Enter actor's name (e.g. Leonardo DiCaprio)")

if st.button("Search") and actor_input.strip():
    with st.spinner("Searching TMDb..."):
        actor = search_actor(actor_input)
        if not actor:
            st.error("❌ Actor not found.")
        else:
            st.success(f"Found: {actor['name']}")
            movies = get_filmography(actor["id"])
            if not movies:
                st.info("No movies found for this actor.")
            else:
                titles = [
                    f"{movie.get('title', 'N/A')} ({movie.get('release_date', '')[:4]})"
                    for movie in movies if movie.get('title')
                ]
                selected = st.selectbox("🎞️ Select a movie to view details:", titles)
                selected_movie = movies[titles.index(selected)]
                movie_details = get_movie_details(selected_movie["id"])

                st.markdown("---")
                show_movie_details(movie_details)
