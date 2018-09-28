#!/usr/bin/env python
import pika
import sys

#Creatie connection object, and open channel to the conneciton
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

#Declare a topic exchange on the channel called topic_logs
channel.exchange_declare(exchange='topic_logs',
			 exchange_type='topic')

routing_key = sys.argv[1] if len(sys.argv) > 2 else 'anonymous.info'
message = ' '.join(sys.argv[2:]) or 'Hello World!'

#Publish to the exchange the message with the defined routing_key
channel.basic_publish(exchange='topic_logs',
		      routing_key=routing_key,
		      body=message)

print(" [x] Sent %r:%r" % (routing_key, message))

#Close the connection
connection.close()
