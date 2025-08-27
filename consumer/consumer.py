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

def callback(ch, method, properties, body):
    print(f"[x] Received: {body.decode()}", flush=True)
    time.sleep(1)  # Simulate work
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='test_queue', on_message_callback=callback)

print("[*] Waiting for messages...", flush=True)
channel.start_consuming()
