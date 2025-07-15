import os
from huggingface_hub import InferenceClient
from config import MODEL_NAME, HF_PROVIDER,HF_TOKEN  


def get_response(messages, model=MODEL_NAME):
    
    client = InferenceClient(
        provider=HF_PROVIDER, 
        api_key=HF_TOKEN
    )
    
    completion = client.chat.completions.create(
        model=model,
        messages=messages
    )
    return completion.choices[0].message.content

