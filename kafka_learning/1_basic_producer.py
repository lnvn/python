from kafka import KafkaProducer
import json
import time

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

print("Sending messages to 'events' topic...\n")

for i in range(5):
    message = {
        'id': i,
        'event': f'User action {i}',
        'timestamp': time.time()
    }

    future = producer.send('events', value=message)
    record_metadata = future.get(timeout=10)

    print(f"Message {i}:")
    print(f"  Value: {message}")
    print(f"  Topic: {record_metadata.topic}")
    print(f"  Partition: {record_metadata.partition}")
    print(f"  Offset: {record_metadata.offset}")
    print(f"  Timestamp: {record_metadata.timestamp}")
    print()

    time.sleep(1)

producer.flush()
producer.close()
print("Producer closed")
