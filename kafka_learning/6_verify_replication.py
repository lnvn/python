from kafka import KafkaConsumer
import json

def read_from_broker(broker_address, group_id):
    """Read messages from a specific broker"""
    consumer = KafkaConsumer(
        'events',
        bootstrap_servers=[broker_address],
        auto_offset_reset='earliest',
        group_id=group_id,
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        max_poll_records=100
    )

    print(f"\n{'='*60}")
    print(f"Reading from broker: {broker_address}")
    print(f"Consumer group: {group_id}")
    print(f"{'='*60}\n")

    count = 0
    for message in consumer:
        count += 1
        print(f"Message #{count}:")
        print(f"  Value: {message.value}")
        print(f"  Partition: {message.partition}")
        print(f"  Offset: {message.offset}\n")

        if count >= 5:  # Read first 5 messages
            break

    consumer.close()
    print(f"Total messages read: {count}\n")


if __name__ == '__main__':
    # Read from Broker 1
    read_from_broker('localhost:9092', 'verify-broker1-group')

    # Read from Broker 2
    read_from_broker('localhost:9093', 'verify-broker2-group')

    print("\n" + "="*60)
    print("If both brokers show the SAME messages,")
    print("replication is working! ✓")
    print("="*60)
