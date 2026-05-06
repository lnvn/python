# Kafka + Python Learning Guide

## Prerequisites
- Docker and Docker Compose installed
- Python 3.7+

## Step 1: Install Dependencies
```bash
pip install kafka-python
```

## Step 2: Start Kafka (locally with Docker)
```bash
docker-compose up -d
```

Wait ~10 seconds for Kafka to be ready. Check with:
```bash
docker-compose logs kafka | grep "started"
```

## Step 3: Learn Kafka Concepts

### What is a Topic?
- Like a "channel" or "queue" in your message broker
- Topics have **partitions** (for parallel processing)
- Messages in a partition are ordered

### What is a Consumer Group?
- Multiple consumers can read from the same topic
- Each consumer in a group reads different partitions
- Offsets track where each group has read up to

### What is a Producer?
- Application that sends messages to a topic
- Serializes data (we use JSON in examples)

---

## Run the Examples

### Example 1: Basic Producer → Consumer

**Terminal 1 (Consumer - starts listening first)**
```bash
python 2_basic_consumer.py
```

**Terminal 2 (Producer - sends 5 messages)**
```bash
python 1_basic_producer.py
```

You'll see the consumer receive the messages in real-time.

### Example 2: ML Pipeline (Multi-stage)

This simulates a real data pipeline: Raw Data → Transform → ML Model

**Terminal 1 (Start consumer listening)**
```bash
python 3_ml_pipeline.py consumer
```

**Terminal 2 (Start transformer)**
```bash
python 3_ml_pipeline.py transformer
```

**Terminal 3 (Send raw sensor data)**
```bash
python 3_ml_pipeline.py producer
```

You'll see data flow through the pipeline: sensor → transformer → model consumer

---

## Key Concepts Explained

| Concept | What it does |
|---------|-------------|
| **Topic** | Channel for messages (e.g., 'events', 'raw-sensor-data') |
| **Partition** | Sub-channel for parallelism (topic has multiple partitions) |
| **Offset** | Position in partition (message number) |
| **Consumer Group** | Set of consumers reading the same topic together |
| **Producer** | Sends messages to topics |
| **Broker** | Kafka server (can have many for high availability) |

## Kafka Advantages for ML Infrastructure

1. **Decoupling**: Data producers don't need to know about consumers
2. **Replay**: Can re-read old messages (retraining scenarios)
3. **Scalability**: Handle high-volume data streams
4. **Persistence**: Data survives crashes
5. **Parallelism**: Partitions enable parallel processing

## Common Patterns

### 1. **Event Streaming**
```
App → Kafka → Analytics Engine
```

### 2. **Data Pipeline**
```
Data Source → Transform → ML Model → Predictions
```

### 3. **Log Aggregation**
```
Multiple Services → Kafka → Centralized Logging
```

## Cleanup

Stop Kafka when done:
```bash
docker-compose down
```

## Next Steps

1. Try modifying the examples (add more transformations)
2. Experiment with different serialization formats (Avro, Protobuf)
3. Learn about Kafka Streams (higher-level processing)
4. Explore consumer group rebalancing
5. Set up error handling and retries
