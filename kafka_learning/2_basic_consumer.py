from kafka import KafkaConsumer
import json
from datetime import datetime

consumer = KafkaConsumer(
    'events',
    bootstrap_servers=['localhost:9092', 'localhost:9093'],
    auto_offset_reset='earliest',  # Start from the beginning if no offset exists
    group_id='my-group',  # Consumer group for tracking offsets
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

print("Listening for messages on 'events' topic...")
print("Press Ctrl+C to stop\n")

count = 0
try:
    for message in consumer:
        count += 1
        timestamp_ms = message.timestamp
        timestamp_dt = datetime.fromtimestamp(timestamp_ms / 1000)

        print(f"Message #{count}:")
        print(f"  Value: {message.value}")
        print(f"  Topic: {message.topic}")
        print(f"  Partition: {message.partition}")
        print(f"  Offset: {message.offset}")
        print(f"  Timestamp: {timestamp_dt} ({timestamp_ms}ms)")
        print(f"  Key: {message.key}")
        print(f"  Headers: {message.headers}")
        print()

except KeyboardInterrupt:
    print(f"\nConsumer stopped after receiving {count} messages")
finally:
    consumer.close()
