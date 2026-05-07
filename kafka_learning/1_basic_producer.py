from kafka import KafkaProducer
import json
import time
import random

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092', 'localhost:9093'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

print("Random Producer started (Ctrl+C to stop)...")
print("Sending random events to 'events' topic\n")

message_count = 0

try:
    while True:
        # Generate random message
        message = {
            'id': message_count,
            'event_type': random.choice(['click', 'view', 'purchase', 'login', 'logout']),
            'user_id': f'user_{random.randint(1, 100)}',
            'value': round(random.uniform(10, 1000), 2),
            'timestamp': time.time()
        }

        future = producer.send('test', value=message)
        # future = producer.send('events', value=message)
        record_metadata = future.get(timeout=10)

        message_count += 1
        print(f"Message #{message_count}:")
        print(f"  Event: {message['event_type']} by {message['user_id']}")
        print(f"  Partition: {record_metadata.partition} | Offset: {record_metadata.offset}")
        print()

        # Random interval (0.5 to 2 seconds)
        sleep_time = random.uniform(0.5, 2)
        time.sleep(sleep_time)

except KeyboardInterrupt:
    print(f"\n\nProducer stopped after sending {message_count} messages")
finally:
    producer.flush()
    producer.close()
    print("Producer closed")
