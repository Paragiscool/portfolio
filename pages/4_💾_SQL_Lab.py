import streamlit as st
import sqlite3
import pandas as pd
from utils import set_theme

# --- PAGE CONFIG ---
st.set_page_config(page_title="SQL Lab", page_icon="💾", layout="wide")

# --- APPLY THEME ---
set_theme()

def local_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass

local_css("assets/style.css")

st.title("Interactive SQL Playground")
st.markdown("""
**Prove your DB skills live.** 
This sandbox runs a real in-memory SQLite database.
""")

# --- SETUP DATABASE ---
# Create connection
conn = sqlite3.connect(":memory:")
c = conn.cursor()

# Create Table matching PROMPT: id, company, role, status, gpa_cutoff
c.execute('''
    CREATE TABLE internship_applications (
        id INTEGER PRIMARY KEY,
        company TEXT,
        role TEXT,
        status TEXT,
        gpa_cutoff REAL
    )
''')

# Seed Data
seed_data = [
    (1, "Google", "SDE Intern", "Interview", 9.0),
    (2, "Microsoft", "ML Intern", "Applied", 8.5),
    (3, "Amazon", "SDE Intern", "Applied", 8.0),
    (4, "Uber", "Backend Intern", "Rejected", 8.5),
    (5, "Atlassian", "SDE Intern", "Offer", 8.5),
    (6, "Sprinklr", "Product Engineer", "Applied", 8.0),
    (7, "Media.net", "SDE Intern", "Interview", 8.2),
]

c.executemany('INSERT INTO internship_applications VALUES (?,?,?,?,?)', seed_data)
conn.commit()

# --- INTERFACE ---
col1, col2 = st.columns([1, 2])

with col1:
    st.info("Available Table: `internship_applications`")
    st.code("""
CREATE TABLE internship_applications (
    id INTEGER PRIMARY KEY,
    company TEXT,
    role TEXT,
    status TEXT,
    gpa_cutoff REAL
)
    """, language="sql")
    
    st.write("**Goal:** Filter applications where GPA cutoff is less than 8.5.")

with col2:
    # Default query from PROMPT
    default_query = "SELECT * FROM internship_applications WHERE gpa_cutoff < 8.5"
    query = st.text_area("SQL Query", value=default_query, height=150)
    
    if st.button("Run Query", type="primary"):
        try:
            # Run query
            df = pd.read_sql_query(query, conn)
            st.success("Query Executed Successfully!")
            st.dataframe(df, use_container_width=True)
        except Exception as e:
            st.error(f"Syntax Error: {e}")

st.markdown("---")
