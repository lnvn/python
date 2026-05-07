from kafka import KafkaProducer
from kafka.errors import KafkaError
import json
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RobustProducer:
    def __init__(self, bootstrap_servers=['localhost:9092', 'localhost:9093']):
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            acks='all',  # Wait for all replicas to acknowledge
            retries=3,   # Retry failed sends
            max_in_flight_requests_per_connection=1,  # Ensure ordering
        )

    def send_with_callback(self, topic, message):
        """Send message with success/failure callbacks"""

        def on_success(record_metadata):
            logger.info(
                f"Message sent to topic={record_metadata.topic}, "
                f"partition={record_metadata.partition}, "
                f"offset={record_metadata.offset}"
            )

        def on_error(exc):
            logger.error(f"Failed to send message: {exc}")

        future = self.producer.send(topic, value=message)
        future.add_callback(on_success).add_errback(on_error)

    def send_sync(self, topic, message, timeout=10):
        """Send message and wait for confirmation"""
        try:
            future = self.producer.send(topic, value=message)
            record_metadata = future.get(timeout=timeout)
            logger.info(f"Message confirmed at offset {record_metadata.offset}")
            return True
        except KafkaError as e:
            logger.error(f"Failed to send: {e}")
            return False

    def close(self):
        self.producer.flush()
        self.producer.close()


if __name__ == '__main__':
    producer = RobustProducer()

    print("Sending messages with error handling...\n")

    for i in range(5):
        message = {
            'id': i,
            'data': f'Important data {i}',
            'timestamp': time.time()
        }

        success = producer.send_sync('events', message)
        if not success:
            logger.warning(f"Retrying message {i}...")

        time.sleep(0.5)

    producer.close()
    print("\nAll messages sent and confirmed")
