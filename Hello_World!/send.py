#!/usr/bin/env python
import pika

#Define code for the producer that sends a single message

#Define a connection to channel on host localhost, then connect to the channel
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()


#Create the queue hello on the channel
channel.queue_declare(queue='hello')

#Publish to default channel on queue hello. i
#Message has body HelloWorld
channel.basic_publish(exchange='',
			routing_key='hello',
			body='Hello World')

print("[x] Sent 'Hello World'")

#Flush and close connection
connection.close();
