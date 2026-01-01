import streamlit as st
import os
from utils import set_theme
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.schema import HumanMessage, AIMessage

# --- APPLY THEME ---
set_theme()

st.title("💬 Chat with My Resume")
st.markdown("""
<div class="glass-card" style="padding: 15px; margin-bottom: 20px;">
    🤖 <b>AI Recruiter Assistant</b><br>
    Ask questions about my experience, skills, or projects. The AI answers strictly based on my attached resume.
</div>
""", unsafe_allow_html=True)

# --- SIDEBAR: API KEY ---
with st.sidebar:
    st.divider()
    api_key = st.text_input("OpenAI API Key", type="password", help="Enter your key to chat.")
    if not api_key:
        st.warning("Please enter an OpenAI API Key to proceed.")
        st.stop()
    os.environ["OPENAI_API_KEY"] = api_key

# --- RAG PIPELINE ---
@st.cache_resource
def initialize_vector_store():
    """Ingests resume pdf and creates FAISS index."""
    resume_path = "assets/resume.pdf"
    
    if not os.path.exists(resume_path):
        st.error("Resume file not found in assets/resume.pdf")
        return None

    # 1. Load PDF
    loader = PyPDFLoader(resume_path)
    docs = loader.load()

    # 2. Split Text
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(docs)

    # 3. Create Embeddings & Vector Store
    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.from_documents(chunks, embeddings)
    
    return vector_store

# Initialize QA Chain
if api_key:
    vector_store = initialize_vector_store()
    
    if vector_store:
        llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vector_store.as_retriever(),
            return_source_documents=True
        )

        # --- CHAT INTERFACE ---
        if "messages" not in st.session_state:
            st.session_state.messages = [{"role": "assistant", "content": "Hello! I've read Parag's resume. Ask me anything!"}]

        # Display History
        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])

        # User Input
        if prompt := st.chat_input("Ex: What databases does Parag know?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = qa_chain.invoke({"query": prompt})
                    answer = response["result"]
                    st.write(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
