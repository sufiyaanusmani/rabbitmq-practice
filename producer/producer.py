import pika
import time

# Use explicit non-guest credentials
credentials = pika.PlainCredentials('myuser', 'mypass')
params = pika.ConnectionParameters(host='rabbitmq', credentials=credentials)

# Retry loop to wait for RabbitMQ and handle transient auth/ready issues
for i in range(10):
    try:
        connection = pika.BlockingConnection(params)
        break
    except pika.exceptions.AMQPConnectionError as e:
        print(f"RabbitMQ not ready or auth failed ({type(e).__name__}): {e}. Retrying in 2 seconds...", flush=True)
        time.sleep(2)
else:
    raise Exception("Cannot connect to RabbitMQ after several attempts.")

channel = connection.channel()

channel.queue_declare(queue='test_queue', durable=True)

for i in range(5):
    message = f"Hello RabbitMQ! Message {i+1}"
    channel.basic_publish(
        exchange='',
        routing_key='test_queue',
        body=message,
        properties=pika.BasicProperties(delivery_mode=2)  # Persistent message
    )
    print(f"[x] Sent '{message}'", flush=True)

connection.close()
