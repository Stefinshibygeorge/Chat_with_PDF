import os
import cassio
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import cassandra
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter



from config import (
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    ASTRA_DB_TABLE_NAME,
    ASTRA_DB_EMBEDDING_MODEL_NAME,
    ASTRA_DB_APPLICATION_TOKEN,
    ASTRA_DB_ID,
)


def load_and_split_pdf(pdf_path: str):
    
    print("Loading and splitting PDF...")
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, 
                                chunk_overlap=CHUNK_OVERLAP)
    splits = splitter.split_documents(docs)
    print(f"✅ Loaded and split PDF into {len(splits)} chunks")
    return splits


def build_astra_vectorstore(docs, 
                            filename="unknown.pdf"):
    
    print(f"📦 Building vector store for: {filename}")

    if not ASTRA_DB_APPLICATION_TOKEN or not ASTRA_DB_ID:
        raise ValueError("❌ ASTRA_DB_APPLICATION_TOKEN and ASTRA_DB_ID must be set.")

    # Init AstraDB connection
    cassio.init(
        token=ASTRA_DB_APPLICATION_TOKEN,
        database_id=ASTRA_DB_ID,
    )

    # Initialize the vector store
    vectorstore = cassandra.Cassandra(
        embedding=HuggingFaceEmbeddings(model_name=ASTRA_DB_EMBEDDING_MODEL_NAME),
        table_name=ASTRA_DB_TABLE_NAME,
    )

    # Check if this file is already indexed using metadata
    existing = vectorstore.similarity_search_with_score(
        query="check file",  # dummy query
        k=5,
        filter={"source": filename}
    )

    if existing:
        print(f"⚠️ Skipping re-indexing. File already exists in AstraDB: {filename}")
        return vectorstore

    # Add metadata to each doc
    for doc in docs:
        doc.metadata["source"] = filename

    vectorstore.add_documents(docs)
    print(f"✅ {len(docs)} chunks added to AstraDB with metadata source='{filename}'")

    return vectorstore




def retrieve_context(query: str, 
                     vectorstore, k=3):
    
    print(f"Retrieving context for query: {query}")
    
    if not vectorstore:
        raise ValueError("VectorStore is not initialized. Please build the vectorstore first.")
    
    retriever = vectorstore.as_retriever(search_kwargs={"k": k})
    docs = retriever.invoke(query)
    
    if not docs:
        print("No documents found for the query.")
        return ""
    else:
        print(f"✅ Context retrieved successfully with {len(docs)} documents")
        return "\n".join([doc.page_content for doc in docs]), docs


def build_prompt_with_memory(context, 
                             query, 
                             instruction,
                             history, 
                             strictness= 100,
                             memory_limit=5):
    
    """
    Construct a chat prompt including limited previous conversation memory.

    Parameters:
    - context (str): Extracted context from the PDF using vector search.
    - query (str): The latest user question.
    - instruction (str): How the assistant should respond (short, long, explain).
    - history (list): List of (question, answer) tuples from previous chat turns.
    - degree (int): Degree of adherence to provided context (percentage).
    - memory_limit (int): Number of previous Q&A pairs to include as memory.

    Returns:
    - List[Dict]: A prompt compatible with LLM chat-completion APIs.
    """
    messages = []
    
    # Include limited memory from past exchanges
    for prev_q, prev_a in history[-memory_limit:]:
        messages.append({"role": "user", "content": prev_q})
        messages.append({"role": "assistant", "content": prev_a})

    # Add instruction and current question
    messages.append({"role": "system", "content": "Use the context to answer.The degree to which you should stick onto the 'pdf and database provided ONLY' is {strictness} percent strict. {instruction}."})
    messages.append({"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"})

    return messages



