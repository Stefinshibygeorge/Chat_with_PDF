# 📄 Chat with PDF (Streamlit + LLM + AstraDB)

A conversational PDF assistant built using LangChain, LLaMA, AstraDB, and Streamlit. Upload any PDF and ask natural questions — it retrieves relevant content and answers intelligently, with memory and customizable styles.

---

## 🚀 Features

- 📁 Upload any PDF
- 🔍 Context-aware question answering
- 🧠 Conversational memory (adjustable)
- ✍️ Custom answer styles: Short, Long, Explain
- 🎛️ Word limit control
- 📜 Clean WhatsApp-style chat interface
- 🛠 Built with LangChain + HuggingFace + AstraDB + Streamlit

---

## 🧰 Tech Stack

- **Frontend**: Streamlit
- **LLM**: LLaMA 3 (via HuggingFace Inference Client)
- **Embeddings**: MiniLM (`all-MiniLM-L6-v2`)
- **Vector DB**: AstraDB (DataStax)
- **Memory**: Custom Q&A history injection
- **Styling**: External CSS + HTML templates

---

## 📦 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/Stefinshibygeorge/chat-with-pdf.git
cd chat-with-pdf
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up environment variables

Create a `.env` file with:

```env
HF_TOKEN= <your_huggingface_api_key>
HF_PROVIDER= <fireworks-ai>
ASTRA_DB_ID= <your_astra_db_id>
ASTRA_DB_APPLICATION_TOKEN= <your_astra_token>
```

### 4. Run the app

```bash
streamlit run app.py
```

---

## 📁 Project Structure

```
chat-with-pdf/
├── app.py                  # Streamlit app
├── inference_client.py     # LLM request logic
├── utils.py                # PDF loading, vector DB setup
├── main.py                 # test run, without UI
├── html_templates.py       # Chat bubble HTML renderer
├── style.css               # Chat UI styling
├── config.py               # Global config variables
├── requirements.txt
└── .env                    # Environment secrets
```

---


## 🛡 License

MIT License
