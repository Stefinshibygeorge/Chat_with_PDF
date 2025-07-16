def load_and_split_pdf(pdf_path: str):
    
    print("Loading and splitting PDF...")
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, 
                                chunk_overlap=CHUNK_OVERLAP)
    splits = splitter.split_documents(docs)
    print(f"✅ Loaded and split PDF into {len(splits)} chunks")
    return splits