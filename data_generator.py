import random
import time
from datetime import datetime
from confluent_kafka import Producer
import json

# Kafka configuration
KAFKA_BROKER = 'localhost:9092'
KAFKA_TOPIC = 'user_interactions'

# Data generation parameters
USER_COUNT = 1000
ITEM_COUNT = 100
INTERACTION_TYPES = ['click', 'view', 'purchase']

def generate_interaction():
    return {
        'user_id': f'user_{random.randint(1, USER_COUNT)}',
        'item_id': f'item_{random.randint(1, ITEM_COUNT)}',
        'interaction_type': random.choice(INTERACTION_TYPES),
        'timestamp': datetime.now().isoformat()
    }

def delivery_report(err, msg):
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

def produce_messages(producer, batch_size=100, interval=1):
    while True:
        batch = [generate_interaction() for _ in range(batch_size)]
        for interaction in batch:
            producer.produce(
                KAFKA_TOPIC,
                key=interaction['user_id'].encode('utf-8'),
                value=json.dumps(interaction).encode('utf-8'),
                on_delivery=delivery_report
            )
        producer.poll(0)  # Trigger any available delivery report callbacks
        print(f"Produced {batch_size} messages")
        time.sleep(interval)

if __name__ == "__main__":
    producer_conf = {
        'bootstrap.servers': KAFKA_BROKER,
        'client.id': 'python-producer'
    }
    producer = Producer(producer_conf)
    
    try:
        produce_messages(producer)
    except KeyboardInterrupt:
        print("Stopping producer...")
    finally:
        producer.flush()
