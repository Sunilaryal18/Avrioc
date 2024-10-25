from confluent_kafka import Consumer, KafkaError
from pymongo import MongoClient
import json
from collections import defaultdict

# Kafka configuration
KAFKA_BROKER = 'localhost:9092'
KAFKA_TOPIC = 'user_interactions'

# MongoDB configuration
MONGO_URI = 'mongodb://localhost:27017/'
DB_NAME = 'user_interactions_db'
COLLECTION_NAME = 'aggregations'

def process_message(message, aggregations):
    if message is None:
        return
    if message.error():
        if message.error().code() == KafkaError._PARTITION_EOF:
            print(f"Reached end of partition {message.topic()}/{message.partition()}")
        else:
            print(f"Error: {message.error()}")
        return

    try:
        interaction = json.loads(message.value().decode('utf-8'))
        user_id = interaction['user_id']
        item_id = interaction['item_id']

        # Update user interactions count
        aggregations['user_interactions'][user_id] += 1

        # Update item interactions count
        aggregations['item_interactions'][item_id] += 1
    except json.JSONDecodeError:
        print(f"Error decoding message: {message.value()}")
    except KeyError as e:
        print(f"Missing key in message: {e}")

def calculate_aggregations(aggregations):
    user_interactions = aggregations['user_interactions']
    item_interactions = aggregations['item_interactions']

    return {
        'avg_interactions_per_user': sum(user_interactions.values()) / len(user_interactions) if user_interactions else 0,
        'max_interactions_per_item': max(item_interactions.values()) if item_interactions else 0,
        'min_interactions_per_item': min(item_interactions.values()) if item_interactions else 0
    }

def update_mongodb(mongo_collection, aggregations):
    agg_results = calculate_aggregations(aggregations)
    mongo_collection.update_one({}, {'$set': agg_results}, upsert=True)
    print(f"Updated MongoDB with aggregations: {agg_results}")

def main():
    consumer_conf = {
        'bootstrap.servers': KAFKA_BROKER,
        'group.id': 'user_interactions_group',
        'auto.offset.reset': 'earliest'
    }

    consumer = Consumer(consumer_conf)
    consumer.subscribe([KAFKA_TOPIC])

    mongo_client = MongoClient(MONGO_URI)
    db = mongo_client[DB_NAME]
    collection = db[COLLECTION_NAME]

    aggregations = {
        'user_interactions': defaultdict(int),
        'item_interactions': defaultdict(int)
    }

    message_count = 0
    try:
        while True:
            message = consumer.poll(1.0)
            if message:
                process_message(message, aggregations)
                message_count += 1

                if message_count % 100 == 0:  # Update aggregations every 100 messages
                    update_mongodb(collection, aggregations)
    except KeyboardInterrupt:
        print("Stopping consumer...")
    finally:
        consumer.close()
        mongo_client.close()

if __name__ == "__main__":
    main()
