# agent.py
import os
import chromadb
from langchain_ollama import ChatOllama

def query_rag_agent(user_question):
    if "HTTP_PROXY" in os.environ: del os.environ["HTTP_PROXY"]
    if "HTTPS_PROXY" in os.environ: del os.environ["HTTPS_PROXY"]
    if "OLLAMA_HOST" in os.environ: del os.environ["OLLAMA_HOST"]
    os.environ["NO_PROXY"] = "localhost"
    OLLAMA_BASE_URL = "http://127.0.0.1:11434"
    
    # Connect to the local vector storage folder updated by the processor
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    collection = chroma_client.get_or_create_collection(name="market_insights")
    
    # Query Chroma for the top 5 closest market updates
    results = collection.query(
        query_texts=[user_question],
        n_results=5
    )
    
    # Safe checks to ensure we actually retrieved historical matches
    if not results or not results.get('documents') or not results['documents'][0]:
        retrieved_context = "No recent data streamed from Kafka yet."
    else:
        # Join the top returned documents for the single query
        retrieved_context = "\n".join(results['documents'][0])
    
    # Formulate system context prompt (using a unique variable name to prevent Typer library conflict)
    rag_prompt = f"""You are a financial advisor assistant. Use the following real-time data snippets to answer the user question accurately.
    
    Context Data:
    {retrieved_context}
    
    Question: {user_question}
    Answer:"""
    
    print("\n--- System Context Fed To Agent ---")
    print(retrieved_context)
    print("-----------------------------------\n")
    
    # Connect directly to the active Ollama background engine
    try:
        llm = ChatOllama(model="llama3.1:latest", base_url=OLLAMA_BASE_URL)
        response = llm.invoke(rag_prompt)
        # LangChain ChatOllama returns a dynamic object; extract .content for clean string text
        print(f"🤖 Agent Response:\n{response.content}\n")
    except Exception as e:
        print(f"❌ Failed to reach the local LLM engine: {e}")

if __name__ == "__main__":
    question = input("Enter your question: ")
    query_rag_agent(question)
