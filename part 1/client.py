import pika

QUEUE_NAME = 'hello'

def send_message(message):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=False)
    channel.basic_publish(exchange='', routing_key=QUEUE_NAME, body=message)
    print(" [x] Sent '" + message + " '")
    connection.close()

send_message("first message")