import streamlit as st
import json

# --- PAGE CONFIG ---
st.set_page_config(page_title="Career Timeline", page_icon="🎓", layout="wide")

def local_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning(f"Style file {file_name} not found.")

local_css("assets/style.css")

st.title("🎓 Journey So Far")

# --- DATA ---
events = [
    {
        "start_date": {"year": "2022"},
        "text": {
            "headline": "Attended IIT Kharagpur",
            "text": "<p>Started Dual Degree (B.Tech + M.Tech) in Ocean Engineering & Naval Architecture.</p>"
        }
    },
    {
        "start_date": {"year": "2024", "month": "05"},
        "end_date": {"year": "2024", "month": "06"},
        "text": {
            "headline": "Data Science Intern @ Encryptix",
            "text": "<p>Build fraud detection models. Gained expertise in imbalanced datasets.</p>"
        }
    },
    {
        "start_date": {"year": "2024", "month": "05"},
        "text": {
            "headline": "Solved Lunar Lander",
            "text": "<p>Applied Deep Q-Networks (DQN) to solve OpenAI Gym environment.</p>"
        }
    },
    {
        "start_date": {"year": "2025"},
        "text": {
            "headline": "Physical AI Engineer",
            "text": "<p>Developing VRP optimization using Genetic Algorithms (~28% reduction).</p>"
        }
    },
    {
        "start_date": {"year": "2025", "month": "05"},
        "text": {
            "headline": "🟢 Available for Summer Internship",
            "text": "<p>Actively looking for SDE / ML roles. Ready to join immediately.</p>"
        }
    }
]

# --- RENDER ---
try:
    from streamlit_timeline import timeline
    
    st.info("Swipe to explore the timeline ↔️")
    timeline(json.dumps({"events": events}), height=400)

except ImportError:
    st.warning("Timeline library not found. Showing simplified view.")
    
    # Fallback Vertical Timeline
    for event in events:
        start = event["start_date"]["year"]
        head = event["text"]["headline"]
        body = event["text"]["text"]
        
        # Highlight the "Available" node
        border_color = "#00CC96"
        if "Available" in head:
            border_color = "#FF4B4B" # Red for alert or just emphasize with a different style

        st.markdown(f"""
        <div style="border-left: 3px solid {border_color}; padding-left: 20px; margin-bottom: 25px;">
            <p style="color: #A0A5B0; margin: 0; font-size: 0.9em;">{start}</p>
            <h3 style="margin: 5px 0;">{head}</h3>
            <div style="color: #FAFAFA;">{body}</div>
        </div>
        """, unsafe_allow_html=True)
