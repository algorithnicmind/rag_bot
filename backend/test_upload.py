import os
from dotenv import load_dotenv
load_dotenv()

try:
    from langchain_google_genai import GoogleGenerativeAIEmbeddings
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001", 
        google_api_key=gemini_api_key
    )
    embeddings.embed_query("hello")
    print("Embedding works!")
except Exception as e:
    print("Embedding Error:", e)

try:
    from pinecone import Pinecone
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    print("Pinecone indexes:", pc.list_indexes().names())
except Exception as e:
    print("Pinecone Error:", e)
