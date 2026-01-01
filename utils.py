import streamlit as st
import requests
import pandas as pd
import numpy as np

# --- THEME SWITCHER LOGIC ---
def set_theme():
    """Calculates and injects CSS variables based on sidebar selection."""
    
    # Theme Descriptions
    themes = {
        "Glass (Default)": {
            "bg_color": "#0e1117",
            "text_color": "#FAFAFA",
            "card_bg": "rgba(255, 255, 255, 0.05)",
            "card_border": "rgba(255, 255, 255, 0.1)",
            "primary": "#00CC96",
            "font_body": "'Inter', sans-serif",
            "font_code": "'JetBrains Mono', monospace",
            # Glass has a special gradient background handled in CSS, so we just set vars
            "extra_css": """
                .stApp {
                    background: linear-gradient(315deg, #0f0c29 3%, #302b63 38%, #24243e 68%, #0f0c29 98%);
                    background-size: 400% 400%;
                    animation: gradient 15s ease infinite;
                }
                @keyframes gradient {
                    0% { background-position: 0% 50%; }
                    50% { background-position: 100% 50%; }
                    100% { background-position: 0% 50%; }
                }
            """
        },
        "Light": {
            "bg_color": "#ffffff",
            "text_color": "#111111",
            "card_bg": "rgba(0, 0, 0, 0.03)",
            "card_border": "#e0e0e0",
            "primary": "#007AFF",
            "font_body": "'Inter', sans-serif",
            "font_code": "'JetBrains Mono', monospace",
            "extra_css": ".stApp { background: #ffffff; }"
        },
        "Matrix": {
            "bg_color": "#0D0208",
            "text_color": "#00FF41",
            "card_bg": "rgba(0, 20, 0, 0.3)",
            "card_border": "#00FF41",
            "primary": "#00FF41",
            "font_body": "'Courier Prime', monospace",
            "font_code": "'Courier Prime', monospace",
            "extra_css": """
                .stApp { background: #0D0208; }
                /* Matrix Glow */
                h1, h2, h3, h4, h5, h6, p, label, div {
                    text-shadow: 0 0 5px rgba(0, 255, 65, 0.5);
                }
            """
        }
    }

    # Sidebar Selection
    with st.sidebar:
        st.markdown("### 🎨 Theme Settings")
        selected_theme = st.selectbox("Choose Interface", list(themes.keys()), index=0)

    # Get Theme Config
    config = themes[selected_theme]

    # Inject CSS Variables
    css = f"""
    <style>
        :root {{
            --bg-color: {config['bg_color']};
            --text_color: {config['text_color']};
            --card-bg: {config['card_bg']};
            --card-border: {config['card_border']};
            --primary-color: {config['primary']};
            --font-body: {config['font_body']};
            --font-code: {config['font_code']};
        }}
        {config['extra_css']}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


# --- CACHING LOGIC (Existing) ---
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
