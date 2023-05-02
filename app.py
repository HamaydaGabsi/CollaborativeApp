import pika
import threading
import tkinter as tk
from Paragraph import Paragraph
from User import User


class TextEditorGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.user = User()
        # User label
        self.user_label = tk.Label(self.window, text='User: '+self.user.name)
        self.user_label.pack(side='top', pady=5)

        # connections
        connection_params = pika.ConnectionParameters(host='localhost')
        self.paragraphs = [
            Paragraph("paragraph1", connection_params,self.user.name),
            Paragraph("paragraph2", connection_params,self.user.name),
            Paragraph("paragraph3", connection_params,self.user.name),
        ]

    def start(self):
        print("started threads")
        for paragraph in self.paragraphs:
            t = threading.Thread(target=paragraph.receive_message, args=())
            t.start()
        self.window.mainloop()


if __name__ == '__main__':

    app = TextEditorGUI()
    app.start()
