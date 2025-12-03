import pika
import json
import time

connection = pika.BlockingConnection(
    pika.ConnectionParameters("localhost")
)
channel = connection.channel()

channel.queue_declare(queue="orders", durable=True)

def process_order(order):
    print(f"Processing order: {order}")
    time.sleep(3)  # simulate long task
    print("✓ Order processed")

def callback(ch, method, properties, body):
    order = json.loads(body)
    process_order(order)
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)

channel.basic_consume(
    queue="orders",
    on_message_callback=callback
)

print("Worker started. Waiting for orders...")
channel.start_consuming()
