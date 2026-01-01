import streamlit as st
import pandas as pd
from datetime import datetime
import requests
import plotly.graph_objects as go

# --- PAGE CONFIG ---
st.set_page_config(page_title="Skills & Expertise", page_icon="🧠", layout="wide")

def local_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning(f"Style file {file_name} not found.")

local_css("assets/style.css")

st.title("🧠 Technical Skills & Impact")

# --- LIVE CODEFORCES STATS ---
def get_codeforces_stats():
    """Fetches live rating/rank from Codeforces API"""
    try:
        url = "https://codeforces.com/api/user.info?handles=paragpatle"
        r = requests.get(url, timeout=3)
        if r.status_code == 200:
            data = r.json()
            if data["status"] == "OK":
                user_info = data["result"][0]
                return {
                    "rating": user_info.get("rating", "N/A"),
                    "rank": user_info.get("rank", "Unrated"),
                    "maxRating": user_info.get("maxRating", "N/A")
                }
    except Exception:
        pass
    return None

cf_stats = get_codeforces_stats()

# --- METRICS ROW ---
st.markdown("### 🏆 Competitive Coding Stats (Live)")
col1, col2, col3 = st.columns(3)

if cf_stats:
    col1.metric("Current Rating", cf_stats["rating"], f"Rank: {cf_stats['rank'].title()}")
    col2.metric("Max Valid Rating", cf_stats["maxRating"], "Peak Performance")
    col3.metric("Problems Solved", "500+", "Est. Practice") # Placeholder as API doesn't give solved count easily
else:
    # Fallback
    col1.metric("Current Rating", "1400+", "Est.")
    col2.metric("Max Valid Rating", "1400+", "Peak")
    col3.metric("Problems Solved", "500+", "Practice")

st.markdown("---")

# --- SKILLS RADAR CHART ---
st.subheader("Interactive Skill Matrix")

# Default Skills (Expanded for SDE)
default_skills = {
    "Python": 90,
    "Data Structures & Algorithms": 90, # SDE Focus
    "SQL & DBMS": 85,          # Backend Focus
    "Competitive Programming": 90, # New Skill
    "TensorFlow": 75,
    "Genetic Algorithms": 85,
    "C++": 70
}

# Input Column (Sliders)
col_input, col_viz = st.columns([1, 2])

with col_input:
    st.markdown("### Adjust Levels")
    updated_skills = {}
    for skill, level in default_skills.items():
        updated_skills[skill] = st.slider(skill, 0, 100, level)

# Visualization Column
with col_viz:
    try:
        categories = list(updated_skills.keys())
        values = list(updated_skills.values())
        
        # Close the loop for radar chart
        categories = [*categories, categories[0]]
        values = [*values, values[0]]

        fig = go.Figure(
            data=[
                go.Scatterpolar(
                    r=values,
                    theta=categories,
                    fill='toself',
                    name='Parag Patle',
                    line_color='#00CC96',
                    fillcolor="rgba(0, 204, 150, 0.4)" # Matching Green Theme
                )
            ]
        )

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    gridcolor="rgba(255, 255, 255, 0.1)",
                    linecolor="rgba(255, 255, 255, 0.1)",
                    tickfont=dict(color="#A0A5B0")
                ),
                angularaxis=dict(
                    tickfont=dict(color="#FAFAFA", size=14),
                    gridcolor="rgba(255, 255, 255, 0.1)"
                ),
                bgcolor="rgba(0,0,0,0)"
            ),
            paper_bgcolor="rgba(0,0,0,0)", # Transparent for Glassmorphism
            font=dict(color="#FAFAFA"),
            showlegend=False,
            margin=dict(l=40, r=40, t=40, b=40)
        )

        st.plotly_chart(fig, use_container_width=True)

    except ImportError:
        st.error("Plotly is not installed. Showing raw data instead.")
        st.table(pd.DataFrame.from_dict(updated_skills, orient='index', columns=['Level']))
    except Exception as e:
        st.error(f"Error rendering chart: {e}")
