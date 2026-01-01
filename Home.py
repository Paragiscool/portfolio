import streamlit as st
import os
import requests
import utils  # Import new utils module

# Page Config
st.set_page_config(
    page_title="Parag Patle | Physical AI Engineer",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- APPLY NEW THEME & LAYOUT ---
utils.render_page_layout()

# --- Sidebar Animation Logic ---
def load_lottieurl(url: str):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

with st.sidebar:
    st.markdown("### ⚙️ Engine Room")
    lottie_url = "https://assets5.lottiefiles.com/packages/lf20_fcfjwiyb.json" 
    
    try:
        from streamlit_lottie import st_lottie
        lottie_json = load_lottieurl(lottie_url)
        if lottie_json:
            st_lottie(lottie_json, height=200, key="coding_anim")
    except ImportError:
        pass

    st.divider()
    
    # Resume Download
    resume_path = os.path.join("assets", "resume.pdf")
    if os.path.exists(resume_path):
        with open(resume_path, "rb") as f:
            st.download_button(
                label="📄 Download Full Resume",
                data=f,
                file_name="Parag_Patle_Resume.pdf",
                mime="application/pdf",
                use_container_width=True
            )

# --- Main Layout ---
col1, col2 = st.columns([1, 2], gap="large")

with col1:
    # Profile Image Logic (JPG -> PNG -> Placeholder)
    profile_path_jpg = os.path.join("assets", "profile.jpg")
    profile_path_png = os.path.join("assets", "profile.png")
    
    if os.path.exists(profile_path_jpg):
        st.image(profile_path_jpg, width=280)
    elif os.path.exists(profile_path_png):
        st.image(profile_path_png, width=280)
    else:
        st.markdown(
            """
            <div style='background-color: rgba(255,255,255,0.1); height: 280px; width: 280px; 
            border-radius: 15px; display: flex; align-items: center; justify-content: center; border: 1px solid rgba(255,255,255,0.2);'>
                <span style='color: #888; font-size: 50px;'>👤</span>
            </div>
            """, unsafe_allow_html=True
        )

with col2:
    # Gradient Title using HTML
    st.markdown(
        """
        <h1 style='background: linear-gradient(to right, #00c6ff, #0072ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
        Parag Patle
        </h1>
        """, unsafe_allow_html=True
    )
    st.subheader("Physical AI Engineer — Ocean Engineering × AI")
    
    # Status Badge
    st.markdown(
        """
        <div style='background: rgba(0, 255, 65, 0.1); border: 1px solid #00FF41; color: #00FF41; 
        padding: 5px 15px; border-radius: 20px; display: inline-block; font-size: 0.8rem; margin-bottom: 20px;'>
        🟢 Actively Looking for SDE/ML Internships (Summer 2025)
        </div>
        """, unsafe_allow_html=True
    )
    
    st.markdown("---")
    
    st.markdown(
        """
        **Dual Degree Scholar (B.Tech + M.Tech) at IIT Kharagpur.**
        
        I bridge the gap between **Complex Physical Systems** and **Artificial Intelligence**. 
        My work focuses on optimizing stochastic environments—from hydrodynamic simulation 
        to vehicle routing logistics—using Genetic Algorithms and Reinforcement Learning.
        
        * **GATE CSE Aspirant:** Strong foundations in OS, DBMS, and Algorithms.
        * **Backend Engineering:** Proficient in SQL, System Design, and API integration.
        * **Codeforces Max Rating:** 1400+ (Specialist).
        """
    )
    
    st.markdown("### Connect")
    
    # Social Badges
    c_gh, c_li, c_cf = st.columns(3)
    
    with c_gh:
        st.link_button("GitHub", "https://github.com/Paragiscool", use_container_width=True)
    with c_li:
        st.link_button("LinkedIn", "https://www.linkedin.com/in/parag-patle-6a0387256/", use_container_width=True)
    with c_cf:
        st.link_button("Codeforces", "https://codeforces.com/profile/paragpatle", use_container_width=True)
