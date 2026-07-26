# test.py
import os
from langchain_ollama import ChatOllama

if "HTTP_PROXY" in os.environ: del os.environ["HTTP_PROXY"]
if "HTTPS_PROXY" in os.environ: del os.environ["HTTPS_PROXY"]
if "OLLAMA_HOST" in os.environ: del os.environ["OLLAMA_HOST"]
os.environ["NO_PROXY"] = "localhost"
OLLAMA_BASE_URL = "http://127.0.0.1:11434"

llm = ChatOllama(model="llama3.1:latest", base_url=OLLAMA_BASE_URL)
response = llm.invoke("hi")

print(f"🤖 Agent Response:\n{response.content}\n")