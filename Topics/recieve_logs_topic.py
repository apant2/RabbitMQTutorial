#!/usr/bin/env python
import pika 
import sys

#Define a connection to a localhost RMQ server, and open a channel using connection object
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

#Declare a topic exchange called topic_logs on the channel
channel.exchange_declare(exchange='topic_logs',
			 exchange_type='topic')

#Declare (i.e. create) an randomly neamed queue on the channel
#set exclusive=True to delete it when the connection here is closed
result = channel.queue_declare(exclusive=True)

queue_name = result.method.queue

#Create binding keys from system arguments
binding_keys = sys.argv[1:]
if not binding_keys:
	sys.stderr.write('Usage: %s [binding key]...\n' % sys.argv[0])
	sys.exit(1)

#For each of the binding keys, bind the key to our queue in the topic_logs exchange
#Tell the exchannge topic_logs to start sending messages with routing_key binding_key to the queue queue_name 
for binding_key in binding_keys:
	channel.queue_bind(exchange='topic_logs',
	 		   queue=queue_name, 
			   routing_key=binding_key)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
	print(" [x] %r:%r" % (method.routing_key, body))

#Start consuming messages sent to the queue queue_name
channel.basic_consume(callback,queue=queue_name,no_ack=True)

#Start consuming mesages from the channel
channel.start_consuming()
