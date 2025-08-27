# RabbitMQ Practice (Producer/Consumer with Python + Docker)

## Overview

This is a minimal RabbitMQ demo that shows a Python producer publishing messages to a queue and a Python consumer receiving and acknowledging them. The stack is fully containerized with Docker Compose and includes the RabbitMQ Management UI.

Components:
- Producer: `producer/producer.py` (publishes 5 messages to `test_queue`)
- Consumer: `consumer/consumer.py` (consumes and ack's messages)
- Broker: RabbitMQ (management plugin enabled)

## Tech Stack

- Python 3.11 (Slim images)
- Pika 1.3
- RabbitMQ 3 (management)
- Docker Compose

## Prerequisites

- Docker Desktop (with Compose)

## Quick Start

1) From the project root, build and start the stack:

```bash
docker compose up --build -d
```

2) Check logs (producer should send 5 messages, consumer should receive them):

```bash
docker compose logs -n 200 producer
docker compose logs -n 200 consumer
```

3) Open RabbitMQ Management UI:

- URL: http://localhost:15672
- Username: `myuser`
- Password: `mypass`
- Go to Queues → `test_queue` to view messages and consumers.

## Useful Commands

- Recreate the stack and apply credential changes (destroys broker data):

```bash
docker compose down -v
docker compose up --build -d
```

- Follow logs live:

```bash
docker compose logs -f consumer
docker compose logs -f rabbitmq
```

- List containers:

```bash
docker compose ps
```

## Troubleshooting

- "AMQPConnectionError" at startup: normal while RabbitMQ initializes; the apps retry until the broker becomes healthy.
- No messages consumed: ensure the consumer is running and the queue name matches `test_queue` in both producer and consumer.
- Changed credentials but login fails: run `docker compose down -v` once to recreate the RabbitMQ data volume and then `docker compose up --build -d`.

## License

This project is licensed under the MIT License. See `LICENSE` for details.