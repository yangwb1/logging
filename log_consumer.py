import pika
import json

def callback(ch, method, properties, body):
    log_message = json.loads(body)
    print(f"Received log: {log_message}")

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='logs', exchange_type='direct')
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange='logs', queue=queue_name, routing_key='log')
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    print('Waiting for logs. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == "__main__":
    main()
