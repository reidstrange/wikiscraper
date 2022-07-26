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

# Usage:
_This usage guide is based on the documentation for connecting to CloudAMQP:  https://www.cloudamqp.com/docs/python.html_

## 1)  Add this setup code at the top of the .py file where you'll be using the microservice

```
import pika, os

# The url passed in to os.environ.get is the url for an instance of rabbitMQ running on CloudAMQP
url = os.environ.get('CLOUDAMQP_URL', 'amqps://bzwlgfru:nSPek3rNzDaKr_OrsM0rmBUGDHf7HROz@beaver.rmq.cloudamqp.com/bzwlgfru')

# Set up connection to RabbitMQ
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)

# Set up message queue channel for queries
queryChannel = connection.channel()
queryChannel.queue_declare(queue='wikiscraperQuery') # This is the queue responsible for transmitting queries

# Set up message queue channel for responses
responseChannel = connection.channel() # start a channel
responseChannel.queue_declare(queue='wikiscraperResponse') # This is the queue responsible for transmitting responses

# Listen for incoming responses from the pipe
responseChannel.basic_consume('wikiscraperResponse',
                      response_callback,
                      auto_ack=True)
                      
responseChannel.start_consuming()
```

## 2)  Send a search query to the microservice:

```
queryChannel.basic_publish(exchange='',
                          routing_key='wikiscraperQuery',
                          body='Query String') # Insert your query string or variable here.
```


## 3)  Process the response from the microservice using the callback function 
```
def response_callback(ch, method, properties, body):
    # response is a dictionary containing the results from the wikiscraper microservice
    response = json.loads(str(body))
    # ------------------------------
    # Process the response data here
    # ------------------------------
```





