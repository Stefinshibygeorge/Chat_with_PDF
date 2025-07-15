import os
import tempfile
from utils import load_and_split_pdf, build_astra_vectorstore, retrieve_context
from inference_client import get_response
from html_templates import render_chat_bubble
from res_prompt_style import build_prompt_with_memory 
from res_prompt_style import styles, wordlimit
from res_prompt_style import instruction_format 
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# --- Streamlit App Configuration ---
st.set_page_config(page_title="📄 Chat with PDF", layout="centered")

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>📄 Chat with PDF</h1>", unsafe_allow_html=True)
st.markdown("---")

# --- Session State Initialization ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

if "last_file" not in st.session_state:
    st.session_state.last_file = None

if "query_input" not in st.session_state:
    st.session_state.query_input = ""

if "new_message" not in st.session_state:
    st.session_state.new_message = False

if "settings_open" not in st.session_state:
    st.session_state.settings_open = False

if "response_type" not in st.session_state:
    st.session_state.response_type = styles[0]

if "word_limit" not in st.session_state:
    st.session_state.word_limit = wordlimit[2]

if "memory_limit" not in st.session_state:
    st.session_state.memory_limit = 5

if "strictness" not in st.session_state:
    st.session_state.strictness = 5

# ------------------------------------------------------ Upload PDF ------------------------------------------------------

uploaded_file = st.file_uploader("📁 Upload a PDF file", type=["pdf"])

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

# ----------------------------------------- Show Chat History Above Form --------------------------------------------------
if st.session_state.chat_history:
    st.markdown("### 💬 Chat")
    for q, a in st.session_state.chat_history:
        st.markdown(render_chat_bubble(q, a), unsafe_allow_html=True)

# ------------------------------------------------ Query Input Form -------------------------------------------------------
if uploaded_file:
    st.markdown("---")
    st.markdown("### 🛠 Customize Answer and Ask a Question")

    with st.form(key="query_form"):
        col1, col2, col3 = st.columns([8, 1, 1])

        with col1:
            query_input = st.text_input("", value=st.session_state.query_input, label_visibility="collapsed", placeholder="Ask a question...")

        with col2:
            submitted = st.form_submit_button("📤", use_container_width=True)

        with col3:
            settings_toggle = st.form_submit_button("⚙️", use_container_width=True)

        if settings_toggle:
            st.session_state.settings_open = not st.session_state.settings_open

        if st.session_state.settings_open:
            # Cache current values to avoid visual reset
            current_response_type = st.session_state.response_type
            current_word_limit = st.session_state.word_limit
            current_memory_limit = st.session_state.memory_limit
            current_strictness = st.session_state.strictness

            with st.expander("⚙️ Settings", expanded=True):
                st.session_state.response_type = st.radio("Response style", styles, index=styles.index(current_response_type))
                st.session_state.word_limit = st.slider("Word limit", wordlimit[0], wordlimit[1], current_word_limit, help="Maximum number of words in the response")
                st.session_state.memory_limit = st.slider("Memory (previous Q&A pairs to remember)", 1, 10, current_memory_limit)
                st.session_state.strictness = st.slider("📏 Strictness (how tightly to follow the PDF content)", 1, 10, current_strictness)

        if submitted and query_input.strip():
            query = query_input.strip()

            with st.spinner("🧠 Thinking..."):
                context, _ = retrieve_context(query, st.session_state.vectorstore, k=3)
                response_type = st.session_state.response_type
                memory_limit = st.session_state.memory_limit
                instruction = instruction_format[response_type]

                prompt = build_prompt_with_memory(context, query, instruction, st.session_state.chat_history, memory_limit=memory_limit)

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
        st.markdown("""
            <script>
                const chatBox = window.document;
                chatBox.onload = () => window.scrollTo(0, chatBox.body.scrollHeight);
            </script>
        """, unsafe_allow_html=True)

# ---------------------------------------------- Reset Chat and Exit ------------------------------------------

col1, col2 = st.columns(2)
with col1:
    if st.button("🔄 Reset Chat", use_container_width=True):
        st.session_state.chat_history = []
        st.session_state.vectorstore = None
        st.session_state.last_file = None
        st.session_state.query_input = ""
        st.session_state.settings_open = False
        st.rerun()

with col2:
    if st.button("❌ Exit App", use_container_width=True):
        st.write("👋 Exiting...")
        st.stop()
        os._exit(0)
