
import os

#model which will be used for inference
MODEL_NAME = "meta-llama/Llama-3.1-8B-Instruct"



# HF Provider (for huggingface_hub InferenceClient)
HF_TOKEN = os.getenv("HF_TOKEN")
HF_PROVIDER = "fireworks-ai"

#Astra DB Configurations
ASTRA_DB_APPLICATION_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_DB_ID = os.getenv("ASTRA_DB_ID")
ASTRA_DB_TABLE_NAME = "qa_mini_demo"
ASTRA_DB_EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"



# Other configs (optional)
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
TOP_K = 3