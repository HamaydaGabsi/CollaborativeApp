import pika
import threading
import tkinter as tk
from Access import Access

class Paragraph:
    def __init__(self, name, connection_params, user_name):
        self.name = name
        self.user_name = user_name
        self.old_text = ""
        self.Exchange_Name = "TextAreaExchange" + self.name
        self.User_Exchange_Name = "UserExchange" + self.name
        connection = pika.BlockingConnection(connection_params)
        self.channel = connection.channel()
        self.channel.exchange_declare(
            exchange=self.Exchange_Name, exchange_type='fanout')
        connection2 = pika.BlockingConnection(connection_params)
        self.channel2 = connection2.channel()
        self.channel2.exchange_declare(
            exchange=self.User_Exchange_Name, exchange_type='fanout')
        self.text = tk.Text(height=10)
        self.text.pack(side='top', padx=20, pady=5)
        self.text.configure(state='disabled')
        self.label = tk.Label(text=name)
        self.editLabel = tk.Label(text="No one is editing")
        self.label.pack(side='top', pady=5)
        self.editLabel.pack(side='top', pady=5)
        self.button = tk.Button(
            text='Edit', command=lambda: self.toggle_edit())
        self.button.pack(side='top', pady=5)
        self.callback_lock = threading.Lock()
    def receive_editor(self):
        print(f"listening for editor on {self.name}")

        def callback(ch, method, properties, body):
            message = body.decode('utf-8')
            print(f"received {message}")
            self.editLabel.configure(text=message)

        result = self.channel2.queue_declare(queue='')
        queue_name = result.method.queue
        self.channel2.queue_bind(
            exchange=self.User_Exchange_Name, queue=queue_name, routing_key='')
        self.channel2.basic_consume(
            queue=queue_name, on_message_callback=callback, auto_ack=True)
        self.channel2.start_consuming()

    def receive_message(self):
        print(f"listening on {self.name}")

        def callback(ch, method, properties, body):
            message = body.decode('utf-8')
            print(f"received {message}")
            with self.callback_lock:
                self.text.configure(state='normal')
                self.text.delete('1.0', tk.END)
                self.text.insert(tk.END, message)
                self.text.configure(state='disabled')
        result = self.channel.queue_declare(queue='')
        queue_name = result.method.queue
        self.channel.queue_bind(
            exchange=self.Exchange_Name, queue=queue_name, routing_key='')
        self.channel.basic_consume(
            queue=queue_name, on_message_callback=callback, auto_ack=True)
        self.channel.start_consuming()

    def toggle_edit(self):
        state = str(self.text['state'])

        if state == 'normal':
            if self.old_text != self.text.get("1.0", tk.END):
                self.channel.basic_publish(
                    exchange=self.Exchange_Name, routing_key='', body=self.text.get("1.0", tk.END))
                
            Access.releaseAccess(self.name)
            self.channel2.basic_publish(
                    exchange=self.User_Exchange_Name, routing_key='', body="No one is editing")
            self.text.configure(state='disabled')
            self.button.configure(text='Edit')
        else:
            print('state disabled')
            if Access.requestAccess(self.name, self.user_name):
                self.channel2.basic_publish(
                    exchange=self.User_Exchange_Name, routing_key='', body=self.user_name+" is editing")
                self.text.configure(state='normal')
                self.button.configure(text='Save')
                self.old_text = self.text.get("1.0", tk.END)
                print("sent request")
                print(self.old_text)
