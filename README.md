# wikiscraper
## Wikipedia scraper microservice for CS361

This is is a microservice that provides a text summary and an image from wikipedia:

Receives:
A string containing a wikipedia search query

Returns:
A string representation of a JSON object containing a description and image from the wikipedia article about the user's search query.

## usage:

1. First, clone the github repository into the project folder where you'll be using the microservice.

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

## Add the following import statement at the top of the .py file where you'll be calling the microservice:
```
from wiki
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

![UML Sequence Diagram](https://drive.google.com/file/d/11hnpeV40RebEIpkCfKOpjZ-ncbuw8YOd/view?usp=sharing)




