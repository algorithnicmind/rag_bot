from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from vector_store import get_vector_store
import os


_llm_instance = None

def get_llm():
    global _llm_instance
    if _llm_instance is not None:
        return _llm_instance

    openai_api_key = os.getenv("OPENAI_API_KEY")
    groq_api_key = os.getenv("GROQ_API_KEY")
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    
    if openai_api_key:
        from langchain_openai import ChatOpenAI
        _llm_instance = ChatOpenAI(model="gpt-4o-mini", temperature=0.3, api_key=openai_api_key)
    elif groq_api_key:
        from langchain_groq import ChatGroq
        # Using the reliable Llama 3.1 8B instant model
        _llm_instance = ChatGroq(model="llama-3.1-8b-instant", temperature=0.3, api_key=groq_api_key)
    elif gemini_api_key:
        from langchain_google_genai import ChatGoogleGenerativeAI
        _llm_instance = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.3, max_retries=2, google_api_key=gemini_api_key)
    else:
         raise ValueError("Missing API Keys in .env file. Provide OPENAI_API_KEY, GROQ_API_KEY, or GEMINI_API_KEY.")
    
    return _llm_instance


def generate_rag_response(query: str, user_id: int):
    # 1. Access the specific user's vector embeddings
    vectorstore = get_vector_store()
    
    # We only retrieve the chunks that belong to the current user!
    retriever = vectorstore.as_retriever(
        search_kwargs={
            "k": 5, # Find the top 5 most relevant paragraphs
            "filter": {"user_id": user_id} 
        }
    )

    # 2. Get the LLM based on provided API keys
    llm = get_llm()

    # 3. Create the prompt instruction for the LLM
    system_prompt = (
        "You are an elite, highly intelligent AI Research Assistant designed to serve users in a professional, "
        "production-grade environment. Your primary function is to directly synthesize and answer the user's "
        "queries rigorously based on the provided document contexts.\n\n"
        "### STRICT GUIDELINES ###\n"
        "1. GROUNDING: You MUST base your answer ENTIRELY on the provided Context. Do NOT invent, hallucinate, "
        "or inject external knowledge that is not directly supported by the text. If the Context does not contain "
        "sufficient information to answer fully, explicitly state: 'I cannot find the answer to this question in "
        "your uploaded documents.'\n"
        "2. COMPREHENSIVENESS: Provide highly detailed, analytical, and structured answers. Extract every relevant "
        "nuance from the Context.\n"
        "3. FORMATTING: Use Markdown extensively for readability. Utilize clear headings, bullet points, bold emphasis "
        "on key terms, and numbered lists where appropriate.\n"
        "4. TONE: Maintain a highly professional, objective, and expert tone. Avoid casual language or filler phrases.\n"
        "5. DIRECTNESS: Start your answer directly. Do not begin with phrases like 'Based on the context provided...' "
        "Just deliver the highly synthesized knowledge immediately.\n\n"
        "### CONTEXT ###\n"
        "{context}"
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])

    # 4. Create the Langchain RAG Chain
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)

    # 5. Execute the query
    response = rag_chain.invoke({"input": query})
    
    # Extract unique source filenames to show the user where we got the info
    sources = list(set([doc.metadata.get("filename", "Unknown") for doc in response.get("context", [])]))
    
    return {
        "answer": response["answer"],
        "sources": sources
    }
