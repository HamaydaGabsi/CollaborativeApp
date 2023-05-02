import pika

class Task2:
    def __init__(self):
        self.queue_name = "task2"
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name)
        
    def send_message(self, message):
        self.channel.basic_publish(exchange='', routing_key=self.queue_name, body=message)

t2= Task2()
t2.send_message("this is task 3")