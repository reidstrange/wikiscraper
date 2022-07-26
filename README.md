# wikiscraper
## Wikipedia scraper microservice for CS361

This is is a microservice that provides a text summary and an image from wikipedia:

Receives:
A string containing a wikipedia search query

Returns:
A string representation of a JSON object containing a description and image from the wikipedia article about the user's search query.

## usage:

There are two external libraries required to run this microservice.  
They are listed in the provided requirements.txt file, and they can be installed as follows:

1. Open a terminal window
2. Navigate to the folder where you downloaded wikiscraper
3. Run the following command:
```
pip install -r requirements.txt
```
4. Then, you can run the microservice:
```
python3 wikiscraper.py
```


_This usage guide is based on the documentation for connecting to CloudAMQP:  https://www.cloudamqp.com/docs/python.html_

## making a call to wikiscraper in Python:

```
import pika, os

# The url passed in to os.environ.get is the url for an instance of rabbitMQ running on CloudAMQP
url = os.environ.get('CLOUDAMQP_URL', 'amqps://bzwlgfru:nSPek3rNzDaKr_OrsM0rmBUGDHf7HROz@beaver.rmq.cloudamqp.com/bzwlgfru')

# Set up connection to RabbitMQ
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
queryChannel = connection.channel()
queryChannel.queue_declare(queue='wikiscraperQuery') # This is the queue responsible for transmitting queries

# Send query string into the pipe
queryChannel.basic_publish(exchange='',
                      routing_key='wikiscraperQuery',
                      body='Query String') # Insert your query string or variable here.
                      
connection.close()
```


## receiving a response from wikiscraper in Python

```
import pika, os, json

# The url passed in to os.environ.get is the url for an instance of rabbitMQ running on CloudAMQP
url = os.environ.get('CLOUDAMQP_URL', 'amqps://bzwlgfru:nSPek3rNzDaKr_OrsM0rmBUGDHf7HROz@beaver.rmq.cloudamqp.com/bzwlgfru')

# Set up connection to RabbitMQ
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
responseChannel = connection.channel() # start a channel
responseChannel.queue_declare(queue='wikiscraperResponse') # This is the queue responsible for transmitting responses

# This function is called when the response is received,
# This is where you should process the response data.
def callback(ch, method, properties, body):
  response_dict = json.loads(str(body)) # response_dict holds the response data in a Python dictionary

# Listen for incoming responses from the pipe
responseChannel.basic_consume('wikiscraperResponse',
                      callback,
                      auto_ack=True)

print(' [*] Waiting for messages:')
responseChannel.start_consuming()
connection.close()
```





