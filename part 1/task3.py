import pika
import threading
import tkinter as tk

class Task3:
    def __init__(self):
        self.queue_name1 = "task1"
        self.queue_name2 = "task2"
        self.connection1 = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel1 = self.connection1.channel()
        self.channel1.queue_declare(queue=self.queue_name1)
        self.connection2 = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel2 = self.connection2.channel()
        self.channel2.queue_declare(queue=self.queue_name2)
        self.window = tk.Tk()
        self.text1 = tk.Text(self.window, width=50, height=20)
        self.text2 = tk.Text(self.window, width=50, height=20)
        self.text1.pack(side=tk.LEFT)
        self.text2.pack(side=tk.RIGHT)
        
    def start(self):
        t1 = threading.Thread(target=self.receive_message1, args=())
        t1.start()
        t2 = threading.Thread(target=self.receive_message2, args=())
        t2.start()
        self.window.mainloop()
        
    def receive_message1(self):
        def callback(ch, method, properties, body):
            message = body.decode('utf-8')
            self.text1.delete(1.0, tk.END)
            self.text1.insert(tk.END, message + "\n")
        self.channel1.basic_consume(queue=self.queue_name1, on_message_callback=callback, auto_ack=True)
        self.channel1.start_consuming()
        
    def receive_message2(self):
        def callback(ch, method, properties, body):
            message = body.decode('utf-8')
            self.text2.delete(1.0, tk.END)
            self.text2.insert(tk.END, message + "\n")
        self.channel2.basic_consume(queue=self.queue_name2, on_message_callback=callback, auto_ack=True)
        self.channel2.start_consuming()
        
t3 = Task3()
t3.start()
