import streamlit as st
# ---------------------------------------------word_limits----------------------------------------------------
maxwordlimit = 5000
minwordlimit = 0
defaultwordlimit = 2500
# ---------------------------------------------styles----------------------------------------------------
styles = ["Short", "Long", "Explain"]
defaultstyle = "Long"
# ---------------------------------------------instruction_format---------------------------------------------
instruction_format = {
    "Short": f"Give a short, direct answer in under {maxwordlimit} words.",
    "Long": f"Provide a thorough, detailed explanation within {maxwordlimit} words.",
    "Explain": f"Explain it clearly like teaching a beginner. Use under {maxwordlimit} words."
}   

def init_state():
    defaults = {
        "chat_history": [],
        "vectorstore": None,
        "last_file": None,
        "query_input": "",
        "new_message": False,
        "settings_open": False,
        "response_type": styles[1],
        "word_limit": maxwordlimit // 2,
        "memory_limit": 5,
        "strictness": 7,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
