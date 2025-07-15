import streamlit as st
import tempfile
import os
from dotenv import load_dotenv
from utils import load_and_split_pdf, build_astra_vectorstore, retrieve_context
from inference_client import get_response
from html_templates import render_chat_bubble

load_dotenv()
st.set_page_config(page_title="📄 Chat with PDF", layout="centered")

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


st.markdown("<h1 style='text-align: center;'>📄 Chat with PDF</h1>", unsafe_allow_html=True)
st.markdown("---")



# --- Session State ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

if "last_file" not in st.session_state:
    st.session_state.last_file = None

if "query_input" not in st.session_state:
    st.session_state.query_input = ""
    
    
    

# --- Upload PDF ---
uploaded_file = st.file_uploader("📁 Upload a PDF file", type=["pdf"])

if "new_message" not in st.session_state:
    st.session_state.new_message = False
if uploaded_file:
    if uploaded_file.name != st.session_state.last_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.read())
            pdf_path = tmp.name

        st.info("⏳ Processing and indexing your PDF...")
        docs = load_and_split_pdf(pdf_path)
        vs = build_astra_vectorstore(docs, filename=uploaded_file.name)
        st.session_state.vectorstore = vs
        st.session_state.chat_history = []
        st.session_state.last_file = uploaded_file.name
        st.success("✅ PDF is ready for chat!")

    

    # --- Show Chat History Above Form ---
    if st.session_state.chat_history:
        st.markdown("### 💬 Chat")
        for q, a in st.session_state.chat_history:
            st.markdown(render_chat_bubble(q, a), unsafe_allow_html=True)




    st.markdown("---")
    st.markdown("### 🛠 Customize Answer and Ask a Question")
    
    with st.form(key="query_form"):
        col1, col2 = st.columns([1, 2])
        
        with col1:
            response_type = st.radio("Response style", ["Short", "Long", "Explain"], horizontal=True, key="response_type")
        with col2:
            word_limit = st.slider("Word limit", 50, 5000, 200, step=50, key="word_limit")


        query_input = st.text_input("Your question", value=st.session_state.query_input)
        submitted = st.form_submit_button("📤 Submit")

        if submitted and query_input.strip():
            query = query_input.strip()
            
            with st.spinner("🧠 Thinking..."):
                context, _ = retrieve_context(query, st.session_state.vectorstore, k=3)

                instruction = {
                    "Short": f"Give a short, direct answer in under {word_limit} words.",
                    "Long": f"Provide a thorough, detailed explanation within {word_limit} words.",
                    "Explain": f"Explain it clearly like teaching a beginner. Use under {word_limit} words."
                }[response_type]

                prompt = [
                    {"role": "system", "content": f"Use the context to answer. {instruction}"},
                    {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"}
                ]

                loading_area = st.empty()
                loading_area.info("⏳ Generating response...")
                answer = get_response(prompt)
                loading_area.empty()

            st.session_state.chat_history.append((query, answer))
            st.session_state.query_input = ""
            st.session_state.new_message = True
            st.rerun()
            
    if st.session_state.new_message:
        st.session_state.new_message = False
        st.markdown("<script>window.scrollTo(0, document.body.scrollHeight);</script>", unsafe_allow_html=True)


col1, col2 = st.columns(2)

with col1:
    if st.button("🔄 Reset Chat", use_container_width=True):
        st.session_state.chat_history = []
        st.session_state.vectorstore = None
        st.session_state.last_file = None
        st.session_state.query_input = ""
        st.rerun()

with col2:
    if st.button("❌ Exit App", use_container_width=True):
        st.write("👋 Exiting...")
        st.stop()
        os._exit(0)
