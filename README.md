# Python-Kafka-Docker

**Code Implementation**

**main.py**
This script connects to the Binance WebSocket API to subscribe to aggregated trade feeds for specified symbols. It then saves the trade data to a Cockroach database and sends it to a Kafka topic using a Kafka producer.

**Kafka_manager.py**
This module contains a class KafkaManager which manages the Kafka producer. It provides methods to start the producer and send messages to Kafka topics.

**test_main.py**
This script contains unit tests for the subscribe_to_agg_trade_feed function in main.py. It mocks the WebSocket connection and tests the function's behavior.

**docker-compose.yml**
This YAML file defines a Docker Compose configuration for running the application along with CockroachDB and Apache Kafka services.

**Dockerfile**
This Dockerfile sets up the environment for running the Python application, including installing dependencies, running tests, and setting the command to execute the application.


**Point to be noted : While running the code kindly update bootstrap_Servers = machine-ip-address in kafka_manager.py line 13.**
