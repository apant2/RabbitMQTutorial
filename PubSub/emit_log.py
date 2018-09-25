#!/usr/bin/env python
import pika
import sys

#Define a connection to localhost rabbitmq instance, and connect to the channel
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

#Declare the name of the exchange to send messages on this channel to 
#Exchange type is defined as fanout (i.e. broadcast all messages it gets to all queues it knows)
channel.exchange_declare(exchange='logs',exchange_type='fanout')

message = ' '.join(sys.argv[1:]) or "info: Hello World!"

#Publish message to a new queue in the logs exchange
channel.basic_publish(exchange='logs',routing_key='',body=message)
print(" [x] sent %r" % message)
connection.close()
