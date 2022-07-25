import wikipedia
import pika
import sys
import os
import json


def main():
    message_queue_url = os.environ.get(
        'CLOUDAMQP_URL', 'amqps://bzwlgfru:nSPek3rNzDaKr_OrsM0rmBUGDHf7HROz@beaver.rmq.cloudamqp.com/bzwlgfru')
    params = pika.URLParameters(message_queue_url)

    rabbit_mq_connection = pika.BlockingConnection(params)

    # initialize channel for queries
    queryChannel = rabbit_mq_connection.channel()
    queryChannel.queue_declare(queue='wikiscraperQuery')

    # initialize channel for responses
    responseChannel = rabbit_mq_connection.channel()
    responseChannel.queue_declare(queue='wikiscraperResponse')

    def send_response(ch, method, properties, body):

        # Get summary of wikipedia article
        searchResults = wikipedia.search(body)
        topResult = searchResults[0]
        description = wikipedia.summary(topResult)

        # Get image from wikipedia article
        page = wikipedia.page(topResult)
        img = page.images[2]

        # Create object and send as response
        response = {
            'description': description,
            'img': img
        }

        responseString = json.dumps(response)
        responseChannel.basic_publish(
            exchange='', routing_key='wikiscraperResponse', body=responseString)

    queryChannel.basic_consume(
        queue='wikiscraperQuery', on_message_callback=send_response, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    queryChannel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
