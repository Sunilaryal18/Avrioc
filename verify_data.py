from pymongo import MongoClient

MONGO_URI = 'mongodb://localhost:27017/'
DB_NAME = 'user_interactions_db'
COLLECTION_NAME = 'aggregations'

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# Get the latest document
latest_doc = collection.find_one(sort=[('_id', -1)])

if latest_doc:
    print("Latest document:")
    print(latest_doc)
else:
    print("No documents found in the collection.")

# Count total documents
doc_count = collection.count_documents({})
print(f"Total documents in collection: {doc_count}")

client.close()
