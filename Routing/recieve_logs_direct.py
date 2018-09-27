#!/usr/bin/env python
import pika
import sys

#Define connection object, and open channel via connection
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

#create an exchange called direct_logs on the channel of type direct
channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

#create a queue (with a random name) on the channel i
#set exclusive=True to make sure it is deleted when this worker stops 
result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

severities = sys.argv[1:]
if not severities:
	sys.stderr.write("Usage: %s [info] [warning] [error]\n" % sys.argv[0])
	sys.exit(1)


for severity in severities:
	#bind the queue to the exchange direct_logs, and give it the routing_key severity (i.e. listen to all messages with the routing_key severity on this queue)
	#binding means that we want exchange to start listening to messages sent to this queue with the noted routing_key
	channel.queue_bind(exchange='direct_logs', queue=queue_name, routing_key=severity)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
	print(" [x] %r:%r" % (method.routing_key, body))

#Start consuming messages from the channel on the queue
channel.basic_consume(callback, queue=queue_name, no_ack=True)

channel.start_consuming()
