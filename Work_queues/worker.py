#!/usr/bin/env python
import pika
import time

#Connect to localhost channel
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

#Create new queue on the channel that is durable
#Remember that manual messsage acknowledgements are turned on by default
#Define the channel as durable, i.e. that RabbitMQ will never lose queue if it quits/crashes
channel.queue_declare(queue='task_queue', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')

#Define callback that simulates heavy process with time.sleep
def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    time.sleep(body.count(b'.'))
    print(" [x] Done")
    #send a basic acknowledgement at end of callback
    ch.basic_ack(delivery_tag = method.delivery_tag)

#Tell rabbitMQ channel not to give more than one message to worker at a time
#(i.e. dont give message until worker has acknowledges previous message).
channel.basic_qos(prefetch_count=1)

channel.basic_consume(callback,
                      queue='task_queue')

channel.start_consuming()
