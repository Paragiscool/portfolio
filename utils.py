import os
import logging
import math
import streamlit as st  # Added Streamlit import
import pandas as pd
import numpy as np
import requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def _sigmoid(x):
    """Helper function for demonstration purposes."""
    return 1 / (1 + math.exp(-x))

# --- THEME LOGIC ---

THEMES = {
    "glass": """
        <style>
        .stApp {
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            background-size: 400% 400%;
            animation: gradient 15s ease infinite;
            color: #ffffff;
        }
        @keyframes gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        div[data-testid="metric-container"], .css-1r6slb0, .stSidebar {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: #ffffff;
        }
        h1, h2, h3 { color: #ffffff !important; }
        /* Custom Scrollbar */
        ::-webkit-scrollbar { width: 8px; background: rgba(0,0,0,0.2); }
        ::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.2); border-radius: 4px; }
        </style>
    """,
    "light": """
        <style>
        .stApp { background: #ffffff; color: #333333; }
        div[data-testid="metric-container"] {
            background: #f0f2f6; border: 1px solid #d1d5db; color: #333333; box-shadow: none;
        }
        .stSidebar { background: #f8f9fa; border-right: 1px solid #e5e7eb; }
        h1, h2, h3 { color: #111827 !important; }
        </style>
    """,
    "matrix": """
        <style>
        .stApp { background-color: #0D0208; color: #00FF41; font-family: 'Courier New', Courier, monospace; }
        div[data-testid="metric-container"], .stSidebar {
            background: #000000; border: 1px solid #00FF41; box-shadow: 0 0 10px #00FF41; color: #00FF41;
        }
        h1, h2, h3, p, label, .stMarkdown, .stButton>button {
            color: #00FF41 !important; font-family: 'Courier New', Courier, monospace !important;
            text-shadow: 0 0 5px #003B00;
        }
        .stButton>button { background-color: #00FF41; color: #000000; border: none; }
        </style>
    """
}

def get_theme_css(theme_name: str) -> str:
    """Returns the CSS string for the requested theme."""
    normalized_name = theme_name.lower().strip()
    if normalized_name in THEMES:
        return THEMES[normalized_name]
    logger.warning(f"Theme '{theme_name}' not found. Defaulting to 'glass'.")
    return THEMES["glass"]

def render_page_layout():
    """Renders the standard page layout with theme switcher."""
    # Theme Switcher in Sidebar
    theme = st.sidebar.selectbox(
        "🎨 Theme", 
        ["Glass", "Light", "Matrix"], 
        index=0, 
        key="theme_selector"
    )
    
    # Inject CSS
    css = get_theme_css(theme)
    st.markdown(css, unsafe_allow_html=True)

# Alias for backward compatibility
set_theme = render_page_layout

# --- RAG LOGIC ---

class StubChain:
    """Fallback object returned when RAG cannot be initialized."""
    def __init__(self, message: str):
        self.message = message

    def run(self, query: str) -> str:
        return f"⚠️ System Notice: {self.message}"
    
    def invoke(self, input_data):
        return {"result": self.run(str(input_data))}

def build_rag_chain(api_key: str | None = None) -> object:
    """Initializes a RAG chain for the resume."""
    try:
        from langchain_community.document_loaders import PyPDFLoader
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        from langchain_openai import OpenAIEmbeddings, ChatOpenAI
        from langchain_community.vectorstores import FAISS
        from langchain.chains import RetrievalQA
    except ImportError:
        return StubChain("Required libraries not installed.")

    pdf_path = os.path.join("assets", "resume.pdf")
    if not os.path.exists(pdf_path):
        return StubChain("Resume file not found in assets/resume.pdf.")

    final_api_key = api_key or os.environ.get("OPENAI_API_KEY")
    if not final_api_key:
        return StubChain("OpenAI API Key is missing.")

    try:
        loader = PyPDFLoader(pdf_path)
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        chunks = text_splitter.split_documents(documents)
        
        embeddings = OpenAIEmbeddings(openai_api_key=final_api_key)
        vectorstore = FAISS.from_documents(chunks, embeddings)
        
        llm = ChatOpenAI(temperature=0, openai_api_key=final_api_key, model_name="gpt-3.5-turbo")
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm, chain_type="stuff", retriever=vectorstore.as_retriever()
        )
        return qa_chain
    except Exception as e:
        return StubChain(f"Internal RAG Error: {str(e)}")

# --- STATS HELPERS (Existing) ---
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
