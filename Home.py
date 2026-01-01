import streamlit as st
import os

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Parag Patle | Physical AI Engineer",
    page_icon="🌊",
    layout="wide",
)

# --- ASSETS & STYLES ---
def local_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning(f"Style file {file_name} not found.")

local_css("assets/style.css")

# --- SIDEBAR LOTTIE ---
try:
    from streamlit_lottie import st_lottie
    import requests

    def load_lottieurl(url):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()

    # Toggle for Lottie
    show_lottie = st.sidebar.checkbox("Show Animation", value=True)
    
    if show_lottie:
        # Tech/AI related Lottie
        lottie_url = "https://assets5.lottiefiles.com/packages/lf20_V9t630.json" 
        lottie_json = load_lottieurl(lottie_url)
        if lottie_json:
            with st.sidebar:
                st_lottie(lottie_json, height=200)
except ImportError:
    st.sidebar.info("Lottie animation disabled (libs missing).")
except Exception as e:
    st.sidebar.warning(f"Lottie error: {e}")

# --- HERO SECTION ---
# Status Badge
st.markdown(
    """
    <div style="
        background-color: rgba(0, 204, 150, 0.1); 
        border: 1px solid #00CC96; 
        border-radius: 50px; 
        padding: 10px 25px; 
        text-align: center; 
        margin-bottom: 25px; 
        box-shadow: 0 0 10px rgba(0, 204, 150, 0.3);
        animation: pulse 2s infinite;
    ">
        <h4 style="margin: 0; color: #00CC96; font-size: 1.1rem;">
            🟢 Actively Looking for SDE/ML Internships (Summer 2025)
        </h4>
    </div>
    <style>
        @keyframes pulse {
            0% { box-shadow: 0 0 0 0 rgba(0, 204, 150, 0.4); }
            70% { box-shadow: 0 0 0 10px rgba(0, 204, 150, 0); }
            100% { box-shadow: 0 0 0 0 rgba(0, 204, 150, 0); }
        }
    </style>
    """, 
    unsafe_allow_html=True
)

col1, col2 = st.columns([1, 2], gap="medium")

with col1:
    # Try multiple formats for profile image
    profile_path = "assets/profile.jpg"
    if not os.path.exists(profile_path):
        profile_path = "assets/profile.png"

    if os.path.exists(profile_path):
        st.image(profile_path, width=280)
    else:
        # Fallback placeholder
        st.info("Profile image not found (assets/profile.png/jpg). Using placeholder.")
        st.markdown('<div style="background-color:#333; height:250px; width:250px; border-radius:50%; display:flex; align-items:center; justify-content:center; border: 4px solid #00CC96;"><span>No Image</span></div>', unsafe_allow_html=True)

with col2:
    st.markdown('<h1 class="text-gradient" style="font-size: 3.5rem; margin-bottom: 0;">Parag Patle</h1>', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #00CC96; margin-top: 0;">Physical AI Engineer — SDE & ML</h3>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Recruiter-Focused Bio
    bio_text = """
    **Bridging Ocean Engineering with Computer Science.** 
    
    Aspiring SDE with strong foundations in **Machine Learning**, **Database Management**, and **physical system modeling**.
    
    GATE CSE Aspirant with strong foundations in Operating Systems, DBMS, and Algorithms. Proficient in SQL and Backend Logic.
    
    *   **Focus**: Building scalable AI systems that solve real-world engineering problems.
    """
    st.write(bio_text)
    
    # Social Badges & CTA
    st.markdown("""
    <div style="display: flex; gap: 15px; margin-top: 25px; align-items: center;">
        <a href="assets/resume.pdf" download target="_blank">
            <button style="background-color: #00CC96; color: #0e1117; font-weight: bold; border: none; padding: 12px 25px; border-radius: 5px; cursor: pointer; font-size: 1rem;">
                📄 Download Resume
            </button>
        </a>
        <a href="https://www.linkedin.com/in/parag-patle-6a0387256/" target="_blank" style="text-decoration:none;">
            <button style="background-color: #0A66C2; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer;">LinkedIn</button>
        </a>
        <a href="https://github.com/Paragiscool" target="_blank" style="text-decoration:none;">
            <button style="background-color: #24292e; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer;">GitHub</button>
        </a>
        <a href="https://codeforces.com/profile/paragpatle" target="_blank" style="text-decoration:none;">
             <button style="background-color: #F39C12; color: #0e1117; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-weight: bold;">Codeforces</button>
        </a>
        <a href="mailto:email@example.com" style="text-decoration:none;">
            <button style="background-color: #D44638; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer;">Email</button>
        </a>
    </div>
    """, unsafe_allow_html=True)

st.markdown("### 💻 Core Tech Stack")
c1, c2, c3, c4, c5 = st.columns(5)
with c1: st.info("**Python**")
with c2: st.info("**C++**")
with c3: st.info("**SQL**")
with c4: st.info("**TensorFlow**")
with c5: st.info("**Docker**")
