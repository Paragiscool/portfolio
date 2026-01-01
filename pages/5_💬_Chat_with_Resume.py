import streamlit as st
import utils
import time

# Page Config
st.set_page_config(page_title="Chat with Resume", page_icon="💬", layout="wide")

# 1. Apply Layout & Theme
utils.render_page_layout()

st.title("💬 Chat with Parag's Resume")
st.markdown("Ask questions about my Experience, Skills, or Projects directly to this AI assistant.")

# 2. API Key Handling
api_key = None

# Check Secrets first
try:
    if "openai" in st.secrets:
        api_key = st.secrets["openai"]["api_key"]
except Exception:
    pass

# Fallback to Sidebar Input
if not api_key:
    with st.sidebar:
        st.divider()
        api_key = st.text_input("🔑 OpenAI API Key", type="password", help="Enter your key to chat.")
        if not api_key:
            st.warning("Please enter an API Key to activate the chat.")

# 3. Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle User Input
if prompt := st.chat_input("Ask me anything... (e.g., 'What is his GPA?')"):
    # Add User Message to History
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking...")
        
        # Build & Run Chain
        chain = utils.build_rag_chain(api_key)
        
        # Check if chain is a Stub (Fallback)
        if isinstance(chain, utils.StubChain):
            response = chain.run(prompt)
            # Add a small delay for realism if it's a stub
            time.sleep(0.5)
        else:
            try:
                # Run the actual RAG chain
                res = chain.invoke(prompt)
                response = res['result']
            except Exception as e:
                response = f"❌ Error: {str(e)}"

        message_placeholder.markdown(response)
    
    # Add Assistant Message to History
    st.session_state.messages.append({"role": "assistant", "content": response})
