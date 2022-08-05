import wikipedia
import pika
import sys
import os
import json


def main():
    # Get URL for RabbitMQ instance running on CloudAMQP account
    message_queue_url = os.environ.get(
        'CLOUDAMQP_URL', 'amqps://bzwlgfru:nSPek3rNzDaKr_OrsM0rmBUGDHf7HROz@beaver.rmq.cloudamqp.com/bzwlgfru')

    # Set queue names
    query_queue = 'wikiscraperQuery'
    response_queue = 'wikiscraperResponse'

    # Set up connection to RabbitMQ and declare queues
    params = pika.URLParameters(message_queue_url)
    rabbit_mq_connection = pika.BlockingConnection(params)
    rabbit_mq_channel = rabbit_mq_connection.channel()
    rabbit_mq_channel.queue_declare(queue=query_queue)
    rabbit_mq_channel.queue_declare(queue=response_queue)

    def send_response(ch, method, properties, body):

        # Get top wikipedia search result
        search_results = wikipedia.search(body)
        top_result = search_results[0]

        # Get summary of wikipedia article
        # or top disambiguation result
        try:
            description = wikipedia.summary(
                top_result, auto_suggest=False, redirect=False)
        except wikipedia.exceptions.DisambiguationError as err:
            top_result = err.options[0]
            description = wikipedia.summary(
                top_result)

        # Get image from wikipedia article
        try:
            page = wikipedia.page(
                title=top_result, auto_suggest=False, redirect=False)
            images = list(filter(lambda x: x[-3:] == 'jpg', page.images))
        except:
            images = []

        # Create JSON object and send as response
        response = {
            'description': description,
            'images': images
        }
        response_string = json.dumps(response)
        rabbit_mq_channel.basic_publish(
            exchange='', routing_key=response_queue, body=response_string)

    rabbit_mq_channel.basic_consume(
        queue=query_queue, on_message_callback=send_response, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    rabbit_mq_channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
