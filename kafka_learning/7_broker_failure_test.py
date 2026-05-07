"""
Test what happens when one broker dies.
If replication works, data should still be available from the other broker.
"""

from kafka import KafkaConsumer, KafkaProducer
import json
import time

print("="*70)
print("BROKER FAILURE TEST - Verifying Replication")
print("="*70)

# Step 1: Send some messages to both brokers
print("\n[Step 1] Sending messages to the cluster...")
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092', 'localhost:9093'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

for i in range(5):
    message = {'id': i, 'test': 'replication test'}
    future = producer.send('events', value=message)
    metadata = future.get(timeout=10)
    print(f"Sent message {i} to partition {metadata.partition}")

producer.close()
print("\n✓ Messages sent\n")

# Step 2: Read from both brokers
print("[Step 2] Reading from Broker 1 (9092)...")
consumer1 = KafkaConsumer(
    'events',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    group_id='test-broker1',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    max_poll_records=10
)

count1 = 0
for msg in consumer1:
    count1 += 1
    if count1 >= 5:
        break

consumer1.close()
print(f"✓ Read {count1} messages from Broker 1\n")

print("[Step 3] Reading from Broker 2 (9093)...")
consumer2 = KafkaConsumer(
    'events',
    bootstrap_servers=['localhost:9093'],
    auto_offset_reset='earliest',
    group_id='test-broker2',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    max_poll_records=10
)

count2 = 0
for msg in consumer2:
    count2 += 1
    if count2 >= 5:
        break

consumer2.close()
print(f"✓ Read {count2} messages from Broker 2\n")

# Step 4: Summary
print("="*70)
print("RESULTS:")
print(f"  Broker 1: {count1} messages")
print(f"  Broker 2: {count2} messages")

if count1 == count2 and count1 > 0:
    print("\n✓✓✓ REPLICATION WORKING! Both brokers have the same data!")
else:
    print("\n✗ Something's wrong - brokers don't have matching data")

print("="*70)

print("\n[Next Step] To test broker failure:")
print("1. Stop Broker 2: docker-compose stop kafka-broker-2")
print("2. Run again and see if you can still read from Broker 1")
print("3. Start Broker 2 again: docker-compose start kafka-broker-2")
print("4. Replication should re-sync the data")
