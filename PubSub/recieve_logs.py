#!/usr/bin/env python
import pika

#Define connection to localhost and connect to channel
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

#Create a fanout exchange on the channel called logs
channel.exchange_declare(exchange='logs',exchange_type='fanout')

#create a queue on the exchange we defined on the channel
#exclusive=True tells it to delete the queue when the consumer connection is closed 
result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

#Bind the queue to the exchange (i.e. tell exchange to start send messages to our queue)
channel.queue_bind(exchange='logs', queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')

#Define callback to execute when message is recieved
def callback(ch, method, properties, body):
	print(" [x] %r" % body)

#Consume the messages sent to queue queue_name, and perform callback on message as recieved
channel.basic_consume(callback, queue=queue_name, no_ack=True)

channel.start_consuming()
