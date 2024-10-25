from confluent_kafka import Producer, Consumer
import json
from pymongo import MongoClient

def test_kafka():
    # Test producer
    producer_conf = {'bootstrap.servers': 'localhost:9092'}
    producer = Producer(producer_conf)
    producer.produce('user_interactions', json.dumps({'test': 'message'}).encode('utf-8'))
    producer.flush()
    print("Message sent to Kafka")

    # Test consumer
    consumer_conf = {
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'test-group',
        'auto.offset.reset': 'earliest'
    }
    consumer = Consumer(consumer_conf)
    consumer.subscribe(['user_interactions'])
    
    msg = consumer.poll(1.0)
    if msg is None:
        print("No message received")
    elif msg.error():
        print(f"Consumer error: {msg.error()}")
    else:
        print(f"Received message: {msg.value().decode('utf-8')}")
    
    consumer.close()

def test_mongodb():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['test_db']
    collection = db['test_collection']
    
    # Insert a document
    result = collection.insert_one({'test': 'document'})
    print(f"Inserted document with id: {result.inserted_id}")
    
    # Retrieve the document
    doc = collection.find_one({'test': 'document'})
    print(f"Retrieved document: {doc}")

if __name__ == "__main__":
    print("Testing Kafka...")
    test_kafka()
    print("\nTesting MongoDB...")
    test_mongodb()
