import streamlit as st
import pandas as pd
# Import the function from your new utils file
from utils import fetch_codeforces_stats, set_theme
import plotly.graph_objects as go

# --- PAGE CONFIG ---
st.set_page_config(page_title="Skills & Expertise", page_icon="🧠", layout="wide")

# --- APPLY THEME ---
set_theme()

def local_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning(f"Style file {file_name} not found.")

local_css("assets/style.css")

st.title("🧠 Technical Skills & Impact")

# --- LIVE CODEFORCES STATS ---
st.markdown("## ⚡ Live Competitive Stats")

# Fetch data using the Cached function
stats = fetch_codeforces_stats("paragpatle")

if stats:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Current Rating", stats['rating'])
    with col2:
        st.metric("Rank", stats['rank'].title())
    with col3:
        st.metric("Max Rating", stats['max_rating'])
else:
    st.warning("Could not fetch live Codeforces data.")

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
