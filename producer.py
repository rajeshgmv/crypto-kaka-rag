# producer.py
import time
import json
import requests
from kafka import KafkaProducer

BOOTSTRAP_SERVERS = "localhost:9092"
TOPIC_NAME = "crypto-ticks"
# Initialize Kafka Producer
try:
    producer = KafkaProducer(
        bootstrap_servers=[BOOTSTRAP_SERVERS],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
except Exception as kafka_error:
    print(f"❌ Failed to connect to local Kafka Broker: {kafka_error}")
    print("Ensure you ran 'brew services start kafka' in a separate terminal!")
    exit(1)

DEMO_API_KEY = "CG-Pyx4XaEEfknCuNLFnVTwV2GG"

url = "https://api.coingecko.com/api/v3/simple/price"

params = {
    "ids": "bitcoin",
    "vs_currencies": "usd",
    "include_24hr_vol": "true",
    "include_24hr_change": "true",
}

headers = {
    "x-cg-demo-api-key": DEMO_API_KEY
}


while True:
    try:
        # requests.get automatically appends the parameters securely to the URL
        response = requests.get(url, params=params, headers=headers)
        
        if response.status_code == 200:
            data = response.json()['bitcoin']
            
            payload = {
                "asset": "BTC",
                "price": float(data["usd"]),
                "volume_24h": float(data["usd_24h_vol"]),
                "change_24h": float(data["usd_24h_change"]),
                "timestamp": int(time.time())
            }
            
            producer.send(TOPIC_NAME, payload)
            print(f"🚀 Sent to Kafka: {payload}")
        else:
            print(f"⚠️ API Error: Status {response.status_code}. Raw response: {response.text[:100]}")
            
    except requests.exceptions.JSONDecodeError:
        print("❌ Received non-JSON response from API endpoint.")
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        
    # 15 seconds keeps you safe under free demo tier rate limits
    time.sleep(20)