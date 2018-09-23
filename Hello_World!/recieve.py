#!/usr/bin/env python
import pika

#create connection to channel on localhost and connect
connection=pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

#Create queue hello if it doesn't exist 
channel.queue_declare(queue='hello')

#define callback
def callback(ch, method, properties, body):
	print("[x] Recieved %r" % body)

#consume from hello queue
#Execute callback method when message recieved
channel.basic_consume(callback,
		      queue='hello',no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')

#Start a never ending loop that...
#waits for data and runs callbacks when needed
channel.start_consuming()
