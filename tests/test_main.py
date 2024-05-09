import unittest
from unittest.mock import patch, AsyncMock
import asyncio
from main import subscribe_to_agg_trade_feed
from kafka_manager import KafkaManager, save_to_database

class TestMain(unittest.IsolatedAsyncioTestCase):
    @patch('main.websockets.connect')
    async def test_subscribe_to_agg_trade_feed(self, mock_connect):
        mock_connect.return_value.__aenter__.return_value = AsyncMock()
        mock_connect.return_value.__aenter__.return_value.recv.side_effect = [
            '{"E": 1620410933624, "a": 12345, "p": "0.1234", "q": "1.0", "f": 123456, "l": 123457, "T": 1620410933624, "m": true}',
            '{"E": 1620410934624, "a": 12346, "p": "0.1235", "q": "2.0", "f": 123457, "l": 123458, "T": 1620410934624, "m": false}'
        ]
        symbols = ['BTCUSDT']
        db_connection = None  # Mock the db connection for testing
        producer = None  # Mock the Kafka producer for testing
        await subscribe_to_agg_trade_feed(symbols[0], producer, db_connection)

if __name__ == '__main__':
    unittest.main()
