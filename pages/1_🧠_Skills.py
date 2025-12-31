import streamlit as st
import pandas as pd
from datetime import datetime

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

# --- METRICS ROW ---
col1, col2, col3 = st.columns(3)

# Calculate years of study (2022 start)
current_year = datetime.now().year
years_study = current_year - 2022

col1.metric("Years of Study (IIT KGP)", f"{years_study}+", "Dual Degree")
col2.metric("Internships Completed", "1", "Data Science @ Encryptix")
col3.metric("VRP Optimization Impact", "28%", "Distance Reduction")

st.markdown("---")

# --- SKILLS RADAR CHART ---
st.subheader("Interactive Skill Matrix")

# Default Skills (Expanded for SDE)
default_skills = {
    "Python": 90,
    "Data Structures & Algorithms": 90, # SDE Focus
    "SQL & DBMS": 85,          # Backend Focus
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
        import plotly.graph_objects as go
        
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
                    fillcolor="rgba(0, 204, 150, 0.4)"
                )
            ]
        )

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    gridcolor="#41424C",
                    linecolor="#41424C",
                    tickfont=dict(color="#A0A5B0")
                ),
                angularaxis=dict(
                    tickfont=dict(color="#FAFAFA", size=14),
                    gridcolor="#41424C"
                ),
                bgcolor="#0e1117"
            ),
            paper_bgcolor="#0e1117",
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
