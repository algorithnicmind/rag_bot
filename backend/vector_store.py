import os
import time
import logging
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

index_name = "rag-bot-index-v3"

# --- Rate Limit Configuration ---
BATCH_SIZE = 5            # Number of chunks to embed per API call
DELAY_BETWEEN_BATCHES = 2 # Seconds to wait between batches
MAX_RETRIES = 5           # Max retries on rate-limit (429) errors
INITIAL_BACKOFF = 2       # Initial backoff delay in seconds


def get_vector_store():
    pinecone_api_key = os.getenv("PINECONE_API_KEY")
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    
    if not pinecone_api_key or not gemini_api_key:
        raise ValueError("Missing API Keys in .env file.")

    # Initialize Pinecone
    pc = Pinecone(api_key=pinecone_api_key)

    # Set up Gemini Embeddings
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001", 
        google_api_key=gemini_api_key
    )
    
    # Check if index exists, if not, create it
    if index_name not in pc.list_indexes().names():
        pc.create_index(
            name=index_name,
            dimension=3072, # gemini-embedding-001 produces 3072-dim vectors
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )
    
    return PineconeVectorStore.from_existing_index(index_name, embeddings)


def _add_texts_with_retry(vectorstore, texts: list, metadatas: list):
    """Add a small batch of texts to Pinecone with retry logic for rate limits."""
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            vectorstore.add_texts(texts=texts, metadatas=metadatas)
            return  # Success — exit
        except Exception as e:
            error_msg = str(e)
            # Check if it's a rate-limit error (429)
            if "429" in error_msg or "quota" in error_msg.lower() or "rate" in error_msg.lower():
                backoff = INITIAL_BACKOFF * (2 ** (attempt - 1))  # Exponential backoff
                logger.warning(
                    f"Rate limit hit (attempt {attempt}/{MAX_RETRIES}). "
                    f"Waiting {backoff}s before retrying..."
                )
                time.sleep(backoff)
            else:
                # Not a rate-limit error — re-raise immediately
                raise
    # If we exhausted all retries
    raise RuntimeError(
        f"Failed to embed text after {MAX_RETRIES} retries due to API rate limits. "
        "Please wait a few minutes and try again, or upgrade your Gemini API plan."
    )


def process_and_store_text(text: str, user_id: int, filename: str):
    """Chunks text and uploads it to Pinecone with user_id metadata, 
    using batched requests to avoid hitting Gemini API rate limits."""
    if not text.strip():
        return
        
    # 1. Chunk the text
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    chunks = text_splitter.split_text(text)
    
    logger.info(f"Processing '{filename}': {len(chunks)} chunks (batch size: {BATCH_SIZE})")
    
    # 2. Add metadata
    # We include user_id so users can only search their OWN documents!
    metadatas = [{"user_id": user_id, "filename": filename, "chunk_index": i} for i in range(len(chunks))]
    
    # 3. Store in Pinecone — in small batches to respect rate limits
    vectorstore = get_vector_store()
    
    total_batches = (len(chunks) + BATCH_SIZE - 1) // BATCH_SIZE
    
    for i in range(0, len(chunks), BATCH_SIZE):
        batch_num = (i // BATCH_SIZE) + 1
        batch_texts = chunks[i : i + BATCH_SIZE]
        batch_metas = metadatas[i : i + BATCH_SIZE]
        
        logger.info(f"  Embedding batch {batch_num}/{total_batches} ({len(batch_texts)} chunks)...")
        _add_texts_with_retry(vectorstore, batch_texts, batch_metas)
        
        # Pause between batches to stay under rate limits
        if i + BATCH_SIZE < len(chunks):
            time.sleep(DELAY_BETWEEN_BATCHES)
