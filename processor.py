# processor_pure.py
import json
import time
from kafka import KafkaConsumer
import chromadb

TOPIC_NAME = 'crypto-ticks'

print("Initializing pure Python Kafka Consumer...")
try:
    # Set up a pure Python Kafka client (No Java required)
    consumer = KafkaConsumer(
        TOPIC_NAME,
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',  # Listen to fresh data flowing from this point onward - earliest or latest
        enable_auto_commit=True,
        value_deserializer=lambda x: json.loads(x.decode('utf-8')) # Decode JSON bytes directly
    )
   # consumer.seek_to_beginning()
except Exception as kafka_error:
    print(f"❌ Failed to connect to local Kafka Broker: {kafka_error}")
    print("Ensure you ran 'brew services start kafka' in a separate terminal window!")
    exit(1)

# Connect to a local folder-based persistent Chroma Vector Database
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="market_insights")

print("🚀 Pure Python Stream Processor is active! Listening for Kafka messages...")

try:
    for message in consumer:
        row = message.value
        print(f"📥 Received data from Kafka: {row}")
        
        # Structure raw integers into natural language paragraphs for RAG embeddings
        doc_text = f"Asset: {row['asset']} at timestamp: {row['timestamp']} is tracking at a price of ${row['price']:.2f}. The 24-hour exchange volume is ${row['volume_24h']:.2f} and the 24-hour value change rate is {row['change_24h']:.4f}%."
        
        # Create a unique database key combining timestamp and block index
        unique_id = f"{row['timestamp']}_{message.offset}"
        
        # Insert raw context directly into Chroma Vector Database
        collection.add(
            documents=[doc_text],
            metadatas=[{"asset": row['asset'], "time": row['timestamp']}],
            ids=[unique_id]
        )
        print(f"💾 Successfully indexed event {unique_id} into Chroma DB.\n")
        
except KeyboardInterrupt:
    print("\nStopping processor stream smoothly...")