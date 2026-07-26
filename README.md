# Crypto Kafka RAG Project

A demo project that streams live cryptocurrency price data from CoinGecko into Kafka, indexes it into a local Chroma vector store, and answers user questions using a RAG-style application powered by Ollama.

## Project Structure

- `producer.py` - fetches Bitcoin market data from CoinGecko and publishes it to the Kafka topic `crypto-ticks`.
- `processor.py` - consumes Kafka messages from `crypto-ticks`, transforms them into text, and indexes them into a local Chroma database.
- `agent.py` - queries the Chroma vector store for relevant context and sends it to an Ollama model for question answering.
- `test.py` - simple Ollama connection test.
- `chroma_db/` - local persistent Chroma database folder.
- `requirement.txt` - Python dependencies.

## Prerequisites

- macOS
- Python 3.9+ (this workspace uses a `venv`)
- Kafka broker running locally on `localhost:9092`
- Ollama running locally on `127.0.0.1:11434`
- Internet access for CoinGecko API calls

## Setup

1. Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirement.txt
```

3. Start Kafka locally and ensure the broker is available on `localhost:9092`.

4. Start Ollama locally and verify it is listening on `127.0.0.1:11434`.

## Running the Project

### 1. Start the Kafka consumer/processor

This process reads incoming Kafka messages from `crypto-ticks` and stores them in Chroma.

```bash
python processor.py
```

### 2. Start the Kafka producer

This process polls CoinGecko and sends Bitcoin updates into Kafka.

```bash
python producer.py
```

### 3. Query the RAG agent

Once data is indexed, you can run the agent:

```bash
python agent.py
```

Enter your question when prompted.

### 4. Validate Ollama connectivity

You can test the Ollama connection directly with:

```bash
python test.py
```

If successful, it will print a short model response.

## Notes

- `processor.py` uses `auto_offset_reset='earliest'` so a new consumer group can read all stored topic messages from the beginning.
- `agent.py` clears proxy-related environment variables and forces Ollama to use `127.0.0.1` to avoid IPv6/localhost resolution issues.
- The Chroma collection name is `market_insights`.

## Troubleshooting

- If Kafka cannot connect:
  - Ensure Kafka is running locally.
  - Verify `localhost:9092` is reachable.

- If Ollama cannot connect:
  - Confirm Ollama is running on `127.0.0.1:11434`.
  - Use `curl http://127.0.0.1:11434/api/tags` to test.

- If the agent returns empty context:
  - Make sure `processor.py` has consumed Kafka messages and written them to `chroma_db`.

## Dependency Notes

The project depends on:

- `kafka-python-ng`
- `chromadb`
- `langchain`
- `langchain-ollama`
- `langchain_core`
- `langchain_community`
- `requests`
- `Flask`
- `faiss-cpu`
- `pypdf`

If you want cleaner dependency management, consider using `pip freeze > requirements.txt` after installing all packages.

## GitHub Repository

This project is intended for the repository:
https://github.com/rajeshgmv/crypto-kaka-rag.git
