from kafka import KafkaProducer
import json
import time
import sys

def test_acks(acks_value):
    """Test producer with different acks settings"""

    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092', 'localhost:9093'],
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
        acks=acks_value
    )

    print(f"\n{'='*60}")
    print(f"Testing with acks={acks_value}")
    print(f"{'='*60}\n")

    for i in range(3):
        message = {'id': i, 'test': f'Message with acks={acks_value}'}

        try:
            start_time = time.time()
            future = producer.send('test-acks', value=message)

            # Try to get metadata (only works if acks > 0)
            record_metadata = future.get(timeout=10)

            elapsed = time.time() - start_time

            print(f"Message {i} sent successfully in {elapsed:.4f}s")
            print(f"  Topic: {record_metadata.topic}")
            print(f"  Partition: {record_metadata.partition}")
            print(f"  Offset: {record_metadata.offset}")
            print()

        except Exception as e:
            print(f"Message {i} - Error or no metadata: {e}\n")

        time.sleep(0.5)

    producer.flush()
    producer.close()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python 5_acks_comparison.py [0|1|all]")
        print("\nExamples:")
        print("  python 5_acks_comparison.py 0    # Fire & forget")
        print("  python 5_acks_comparison.py 1    # Leader acknowledges")
        print("  python 5_acks_comparison.py all  # All replicas acknowledge")
        sys.exit(1)

    acks = sys.argv[1]

    # Convert string "0" or "1" to int, keep "all" as string
    if acks in ('0', '1'):
        acks = int(acks)

    test_acks(acks)
