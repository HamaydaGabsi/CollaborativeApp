import pika


class Access:
    @staticmethod
    def requestAccess(name, user_name):

        queue_name = "Access"+name
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        numMsgs = channel.queue_declare(queue=queue_name).method.message_count
        if (numMsgs > 0):

            return False
        else:

            channel.basic_publish(
                exchange='', routing_key=queue_name, body=user_name)

            return True

    def releaseAccess(name):
        queue_name = "Access"+name
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.queue_declare(queue=queue_name)

        def callback(ch, method, properties, body):
            message = body.decode('utf-8')
            channel.stop_consuming()
        channel.basic_consume(
            queue=queue_name, on_message_callback=callback, auto_ack=True)
        channel.start_consuming()
        channel.close()
        connection.close()
