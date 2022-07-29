import pika
import os
import json


def search_for(query_string):
    send_query(query_string)
    while 1:
        res = receive_response()
        if res:
            return res


def send_query(query_string):
    # Get URL for RabbitMQ instance running on CloudAMQP account
    url = os.environ.get(
        'CLOUDAMQP_URL', 'amqps://bzwlgfru:nSPek3rNzDaKr_OrsM0rmBUGDHf7HROz@beaver.rmq.cloudamqp.com/bzwlgfru')

    # Init connection
    params = pika.URLParameters(url)
    connection = pika.BlockingConnection(params)
    query_channel = connection.channel()  # start a channel
    query_queue = 'wikiscraperQuery'  # name of message queue for search queries

    # Send query
    query_channel.basic_publish(exchange='',
                                routing_key=query_queue,
                                body=query_string)

    print(
        f'Search query "{query_string}" sent to message queue {query_queue}...')
    connection.close()


def receive_response():
    # Get URL for RabbitMQ instance running on CloudAMQP account
    url = os.environ.get(
        'CLOUDAMQP_URL', 'amqps://bzwlgfru:nSPek3rNzDaKr_OrsM0rmBUGDHf7HROz@beaver.rmq.cloudamqp.com/bzwlgfru')

    # Set up connection to RabbitMQ
    params = pika.URLParameters(url)
    connection = pika.BlockingConnection(params)
    response_channel = connection.channel()  # start a channel
    response_queue = 'wikiscraperResponse'  # name of message queue for responses

    # Get one response message from RabbitMQ and return response body
    method_frame, header_frame, body = response_channel.basic_get(
        response_queue, auto_ack=True)
    response = json.loads(body) if body else None
    response_channel.queue_purge(response_queue)
    connection.close()
    return response
