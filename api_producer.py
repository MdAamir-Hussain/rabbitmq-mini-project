from flask import Flask, request, jsonify
import pika
import json

app = Flask(__name__)

def get_channel():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters("localhost")
    )
    return connection, connection.channel()

@app.route('/order', methods=['POST'])
def create_order():
    data = request.json

    connection, channel = get_channel()
    channel.queue_declare(queue='orders', durable=True)

    message = json.dumps(data)
    channel.basic_publish(
        exchange='',
        routing_key='orders',
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2  # make messages persistent
        )
    )

    connection.close()
    return jsonify({"status": "Order sent", "order": data}), 201

if __name__ == "__main__":
    app.run(port=5000)
