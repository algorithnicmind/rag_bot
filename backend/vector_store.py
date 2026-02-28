import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv

load_dotenv()

index_name = "rag-bot-index-v2"

def get_vector_store():
    pinecone_api_key = os.getenv("PINECONE_API_KEY")
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    
    if not pinecone_api_key or not gemini_api_key:
        raise ValueError("Missing API Keys in .env file.")

    # Initialize Pinecone
    pc = Pinecone(api_key=pinecone_api_key)

    # Set up Gemini Embeddings
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001", 
        google_api_key=gemini_api_key
    )
    
    # Check if index exists, if not, create it
    if index_name not in pc.list_indexes().names():
        pc.create_index(
            name=index_name,
            dimension=768, # Gemini embeddings dimension is 768
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )
    
    return PineconeVectorStore.from_existing_index(index_name, embeddings)

def process_and_store_text(text: str, user_id: int, filename: str):
    """Chunks text and uploads it to Pinecone with user_id metadata."""
    if not text.strip():
        return
        
    # 1. Chunk the text
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    chunks = text_splitter.split_text(text)
    
    # 2. Add metadata
    # We include user_id so users can only search their OWN documents!
    metadatas = [{"user_id": user_id, "filename": filename, "chunk_index": i} for i in range(len(chunks))]
    
    # 3. Store in Pinecone
    vectorstore = get_vector_store()
    vectorstore.add_texts(texts=chunks, metadatas=metadatas)
