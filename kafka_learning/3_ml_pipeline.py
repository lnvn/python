from kafka import KafkaProducer, KafkaConsumer
import json
import time
import random

# Simulate raw sensor data producer
def produce_sensor_data():
    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092', 'localhost:9093'],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    print("=== Sensor Data Producer ===")
    for i in range(10):
        data = {
            'sensor_id': random.choice(['sensor-1', 'sensor-2', 'sensor-3']),
            'temperature': round(20 + random.uniform(-5, 15), 2),
            'humidity': round(random.uniform(30, 80), 2),
            'timestamp': time.time()
        }
        producer.send('raw-sensor-data', value=data)
        print(f"Sent sensor data: {data}")
        time.sleep(0.5)

    producer.flush()
    producer.close()


# Simulate data transformer (consumes raw data, produces cleaned data)
def transform_sensor_data():
    consumer = KafkaConsumer(
        'raw-sensor-data',
        bootstrap_servers=['localhost:9092', 'localhost:9093'],
        auto_offset_reset='earliest',
        group_id='transformer-group',
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        max_poll_records=5
    )

    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092', 'localhost:9093'],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    print("\n=== Data Transformer (consuming & transforming) ===")
    count = 0
    for message in consumer:
        raw_data = message.value

        # Simple transformation: add a status field
        transformed = {
            **raw_data,
            'status': 'high' if raw_data['temperature'] > 30 else 'normal',
            'processed_at': time.time()
        }

        producer.send('processed-sensor-data', value=transformed)
        print(f"Transformed: {transformed}")

        count += 1
        if count >= 10:  # Stop after processing 10 messages
            break

    consumer.close()
    producer.close()


# Simulate consumer (reads final processed data)
def consume_processed_data():
    consumer = KafkaConsumer(
        'processed-sensor-data',
        bootstrap_servers=['localhost:9092', 'localhost:9093'],
        auto_offset_reset='earliest',
        group_id='ml-model-group',
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        max_poll_records=10
    )

    print("\n=== ML Model Consumer ===")
    for message in consumer:
        data = message.value
        print(f"Model input: {data}")
        # Here you'd feed this to your ML model

    consumer.close()


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage: python 3_ml_pipeline.py [producer|transformer|consumer]")
        sys.exit(1)

    role = sys.argv[1]

    if role == 'producer':
        produce_sensor_data()
    elif role == 'transformer':
        transform_sensor_data()
    elif role == 'consumer':
        consume_processed_data()
    else:
        print(f"Unknown role: {role}")
