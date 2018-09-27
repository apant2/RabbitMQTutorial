#!/usr/bin/env python
import pika
import sys

#Define a connection, and connect to the RabbitMQ channel on the connection's host
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

#Declare a direct exchange called direct_logs on the channel
channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

#Read severity from the message
severity = sys.argv[1] if len(sys.argv) > 2 else 'info'
message = ' '.join(sys.argv[2:]) or 'Hello World'

#Publish to the direct logs_exchange, and give the routing_key the value severity to the body
channel.basic_publish(exchange='direct_logs', routing_key=severity, body=message)

print(" [x] Sent %r:%r" % (severity, message))
connection.close()
