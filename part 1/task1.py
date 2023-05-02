import pika

class Task1:
    def __init__(self):
        self.queue_name = "task1"
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name)
        
    def send_message(self, message):
        self.channel.basic_publish(exchange='', routing_key=self.queue_name, body=message)

t1= Task1()
t1.send_message("hellooo world")