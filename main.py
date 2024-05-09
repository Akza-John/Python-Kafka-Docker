import asyncio
import json
import psycopg2
import websockets
from aiokafka import AIOKafkaProducer
from kafka_manager import KafkaManager, save_to_database
import os

# Database connection details
DATABASE_HOST = os.environ.get('DATABASE_HOST')
DATABASE_PORT = os.environ.get('DATABASE_PORT')
DATABASE_USER = os.environ.get('DATABASE_USER')
DATABASE_NAME = os.environ.get('DATABASE_NAME')

# Kafka connection details
# KAFKA_BOOTSTRAP_SERVERS = 'kafka:9092'


async def subscribe_to_agg_trade_feed(symbol, producer, db_connection):
    uri = f"wss://fstream.binance.com/ws/{symbol.lower()}@aggTrade"
    async with websockets.connect(uri) as websocket:
        async for message in websocket:
            trade_data = json.loads(message)
            save_to_database(symbol, trade_data, db_connection)
            await producer.send_message("trade_data", json.dumps(trade_data).encode())


async def main(symbols):

    kafka_manager = KafkaManager()
    await kafka_manager.start_producer()

    db_connection = psycopg2.connect(
        host=DATABASE_HOST,
        port=DATABASE_PORT,
        user=DATABASE_USER,
        database=DATABASE_NAME
    )

    tasks = [subscribe_to_agg_trade_feed(symbol, kafka_manager, db_connection) for symbol in symbols]
    await asyncio.gather(*tasks)

    await kafka_manager.producer.stop()
    db_connection.close()


if __name__ == "__main__":
    symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT']  # Add more symbols as needed
    asyncio.run(main(symbols))
