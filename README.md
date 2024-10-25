# Avrioc: Real-time User Interaction Analytics

Avrioc is a real-time data processing and visualization system for user interaction logs. It uses Kafka for data streaming, MongoDB for storage, and a Flask-based dashboard for visualization.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Running the System](#running-the-system)
5. [Viewing the Dashboard](#viewing-the-dashboard)
6. [Troubleshooting](#troubleshooting)

## Prerequisites

- Python 3.8+
- Kafka
- MongoDB
- pip (Python package manager)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/sunilaryal1/avrioc.git
   cd avrioc
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install confluent-kafka pymongo flask
   ```

## Configuration

1. Kafka:
   - Ensure Kafka is installed and running on `localhost:9092`
   - Create a topic named `user_interactions`

2. MongoDB:
   - Ensure MongoDB is installed and running on `localhost:27017`
   - The system will automatically create a database named `user_interactions_db`

3. Update configuration in scripts if your Kafka or MongoDB is running on different hosts/ports.

## Running the System

1. Ensure all required services are running:
   - Kafka (on `localhost:9092`)
   - MongoDB (on `localhost:27017`)
   - Zookeeper (required for Kafka)

2. Run the entire system using the `run_avrioc.py` script:
   ```
   python run_avrioc.py
   ```
   This script will start all components of the Avrioc system:
   - Data Generator
   - Consumer and Aggregator
   - Dashboard Server

   You'll see output from each component in the console.

Alternatively, you can run each component separately:

3. Start the data generator:
   ```
   python data_generator.py
   ```
   This will start producing random user interaction data to Kafka.

4. Start the consumer and aggregator:
   ```
   python consumer_aggregator.py
   ```
   This will consume data from Kafka, aggregate it, and store results in MongoDB.

5. Start the dashboard server:
   ```
   python dashboard.py
   ```
   This will start the Flask server for the dashboard.

## Viewing the Dashboard

1. Open a web browser and go to `http://localhost:5000`
2. You should see a bar chart displaying the latest aggregation metrics:
   - Average interactions per user
   - Maximum interactions per item
   - Minimum interactions per item
3. The dashboard auto-refreshes every 5 seconds.

## Troubleshooting

If you encounter issues:

1. Ensure all prerequisites are correctly installed and running:
   - Kafka
   - MongoDB
   - Zookeeper
2. Check if Kafka and MongoDB are accessible on the configured hosts and ports.
3. Verify that the `user_interactions` topic exists in Kafka.
4. Check the console output of each script for error messages.
5. For dashboard issues, check the browser's developer console for JavaScript errors.
6. If using `run_avrioc.py`, make sure all required Python packages are installed.

If problems persist, please open an issue on the GitHub repository with detailed information about the error and your environment.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
