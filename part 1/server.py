import pika

QUEUE_NAME = 'hello'

def callback(ch, method, properties, body):
    message = body.decode('utf-8')
    print(" [x] Received '" + message + " '")

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=False)
    print(" [*] Waiting for messages. To exit press CTRL+C")
    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

if __name__ == '__main__':
    main()