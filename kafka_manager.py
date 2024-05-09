from aiokafka import AIOKafkaProducer
import psycopg2

import os

# Database connection details
DATABASE_HOST = os.environ.get('DATABASE_HOST')
DATABASE_PORT = os.environ.get('DATABASE_PORT')
DATABASE_USER = os.environ.get('DATABASE_USER')
DATABASE_NAME = os.environ.get('DATABASE_NAME')

class KafkaManager:
    def __init__(self, bootstrap_servers='172.18.16.1:9092'): #ip address of machine
        self.bootstrap_servers = bootstrap_servers
        self.producer = None

    async def start_producer(self):
        self.producer = AIOKafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            value_serializer=lambda v: v
        )
        await self.producer.start()

    async def send_message(self, topic, message):
        if self.producer:
            await self.producer.send_and_wait(topic, message)
def table_exists(conn, table_name):
    """Check if a table exists in the database."""
    query = """
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_name = %s
        );
    """
    with conn.cursor() as cursor:
        cursor.execute(query, (table_name,))
        return cursor.fetchone()[0]

def create_table(conn):
    """Create a new table in the database."""
    create_table_query = """
        CREATE TABLE trades (
                          symbol VARCHAR(50),
                           event_time VARCHAR(50),
                           trade_id VARCHAR(50),
                           price VARCHAR(50),
                           quantity VARCHAR(50),
                           first_trade_id VARCHAR(50),
                           last_trade_id VARCHAR(50),
                           timestamp VARCHAR(50),
                           is_buyer_maker VARCHAR(50)
                           );
    """
    with conn.cursor() as cursor:
        cursor.execute(create_table_query)
    conn.commit()

def save_to_database(symbol, trade_data, db_connection):
    conn = psycopg2.connect(
        host=DATABASE_HOST,
        port=DATABASE_PORT,
        user=DATABASE_USER,
        database=DATABASE_NAME
    )
    cursor = conn.cursor()
    table_name = "trades"

    # Check if the table exists
    if not table_exists(conn, table_name):
        # If the table does not exist, create it
        create_table(conn)

    insert_query = """
        INSERT INTO trades (symbol, event_time, trade_id, price, quantity, first_trade_id, last_trade_id, Timestamp, is_buyer_maker)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(insert_query, (
        symbol,
        str(trade_data['E']),
        str(trade_data['a']),
        str(trade_data['p']),
        str(trade_data['q']),
        str(trade_data['f']),
        str(trade_data['l']),
        str(trade_data['T']),
        str(trade_data['m'])
    ))
    conn.commit()
    cursor.close()
    conn.close()
