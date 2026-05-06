# Kafka + Python Cheatsheet

## Starting Kafka
```bash
docker-compose up -d      # Start in background
docker-compose logs -f    # View logs
docker-compose down       # Stop everything
```

## Producer (Sending Messages)

```python
from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Send a message
producer.send('my-topic', value={'key': 'value'})
producer.flush()  # Wait for all sends to complete
producer.close()
```

## Consumer (Receiving Messages)

```python
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'my-topic',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',  # Start from beginning
    group_id='my-group',            # Consumer group name
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

for message in consumer:
    print(message.value)
```

## Important Parameters

### Producer
| Parameter | Purpose |
|-----------|---------|
| `acks='all'` | Wait for all replicas (slower, safer) |
| `retries=3` | Retry failed sends |
| `value_serializer` | Convert Python objects to bytes |

### Consumer
| Parameter | Purpose |
|-----------|---------|
| `auto_offset_reset='earliest'` | Start from beginning if no saved offset |
| `group_id='name'` | Consumer group (track progress together) |
| `value_deserializer` | Convert bytes back to Python objects |
| `max_poll_records=100` | Batch size (control memory usage) |

## Error Handling

```python
from kafka.errors import KafkaError

try:
    future = producer.send('topic', value=data)
    future.get(timeout=10)  # Wait for confirmation
except KafkaError as e:
    print(f"Failed: {e}")
```

## Check Kafka Health

```bash
# From inside docker container
docker-compose exec kafka kafka-topics --list --bootstrap-server localhost:9092

# List all topics
docker-compose exec kafka kafka-topics --list --bootstrap-server localhost:9092

# Describe a topic
docker-compose exec kafka kafka-topics --describe --topic events --bootstrap-server localhost:9092

# Check consumer group offsets
docker-compose exec kafka kafka-consumer-groups \
  --bootstrap-server localhost:9092 \
  --group my-group \
  --describe
```

## Data Serialization

### JSON (simple, human-readable)
```python
value_serializer=lambda v: json.dumps(v).encode('utf-8')
value_deserializer=lambda m: json.loads(m.decode('utf-8'))
```

### String (lightweight)
```python
value_serializer=lambda v: str(v).encode('utf-8')
value_deserializer=lambda m: m.decode('utf-8')
```

### Bytes (flexible)
```python
value_serializer=lambda v: v  # Already bytes
```

## Common Patterns

### Request-Reply Pattern
```python
# Producer sends request to 'requests' topic with reply_to field
producer.send('requests', value={'request_id': '123', 'reply_to': 'responses'})

# Consumer processes and sends reply
consumer.subscribe(['requests'])
for msg in consumer:
    response = process(msg.value)
    producer.send(msg.value['reply_to'], value=response)
```

### Broadcast Pattern
```python
# Multiple consumers with SAME group_id read from same topic
# Each consumer in group gets different partitions
consumer = KafkaConsumer('my-topic', group_id='shared-group')
```

### Fan-out Pattern
```python
# Multiple consumers with DIFFERENT group_id read ALL messages
consumer1 = KafkaConsumer('my-topic', group_id='group1')
consumer2 = KafkaConsumer('my-topic', group_id='group2')
# Both get all messages, independently
```

## Debugging

```python
# Enable verbose logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Check producer metrics
print(producer.metrics())

# Check message offset
for message in consumer:
    print(f"Offset: {message.offset}")
    print(f"Partition: {message.partition}")
    print(f"Timestamp: {message.timestamp}")
```

## Performance Tips

1. **Batch messages**: Send in groups, not one-by-one
2. **Increase `linger_ms`**: Wait for more messages to batch
3. **Use partitions**: Spread load across multiple partitions
4. **Consumer scaling**: One consumer per partition (max)
5. **Async sends**: Use callbacks instead of blocking on every send
