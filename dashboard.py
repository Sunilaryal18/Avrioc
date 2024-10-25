from flask import Flask, render_template, jsonify
from pymongo import MongoClient
import json

app = Flask(__name__)

# MongoDB configuration
MONGO_URI = 'mongodb://localhost:27017/'
DB_NAME = 'user_interactions_db'
COLLECTION_NAME = 'aggregations'

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/data')
def get_data():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    
    # Get the latest aggregation
    latest_agg = collection.find_one(sort=[('_id', -1)])
    
    if latest_agg:
        # Remove the _id field as it's not JSON serializable
        latest_agg.pop('_id', None)
        return jsonify(latest_agg)
    else:
        return jsonify({})

if __name__ == '__main__':
    app.run(debug=True)
