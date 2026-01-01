import streamlit as st
import requests
import pandas as pd
import numpy as np

# CACHING: This decorator tells Streamlit to run this function ONLY ONCE
# every 1 hour (3600 seconds), preventing slow page loads.
@st.cache_data(ttl=3600)
def fetch_codeforces_stats(handle):
    """Fetches live user rating from Codeforces API."""
    url = f"https://codeforces.com/api/user.info?handles={handle}"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        if data["status"] == "OK":
            user = data["result"][0]
            return {
                "rating": user.get("rating", "N/A"),
                "rank": user.get("rank", "N/A"),
                "max_rating": user.get("maxRating", "N/A")
            }
    except Exception as e:
        return None
    return None

# CACHING: Prevents generating new random coordinates on every click
@st.cache_data
def generate_vrp_data(num_points=12, seed=42):
    """Generates reproducible random coordinates for VRP map."""
    rs = np.random.RandomState(seed)
    # Center near Mumbai
    center_lat, center_lon = 19.0760, 72.8777
    lats = center_lat + (rs.rand(num_points) - 0.5) * 0.1
    lons = center_lon + (rs.rand(num_points) - 0.5) * 0.1
    
    return pd.DataFrame({
        'lat': lats,
        'lon': lons,
        'id': range(1, num_points + 1)
    })
