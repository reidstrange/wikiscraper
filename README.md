# wikiscraper
## Wikipedia scraper microservice for CS361

This is is a microservice that provides a text summary and an image from wikipedia:

Receives:
A string containing a wikipedia search query

Returns:
A string representation of a JSON object containing a description and image from the wikipedia article about the user's search query.

## usage:

1. Open a terminal window

2. Navigate to the project folder where you want to use the wikiscraper microservice

3. Run the following command to clone wikiscraper into your project:
```
git submodule add https://github.com/reidstrange/wikiscraper
```

4. Install the necessary dependencies by running:
```
pip install -r wikiscraper/requirements.txt
```

5. Open another terminal window and run the following from your project folder.
(This process must be left running as long as you need the wikiscraper microservice)
```
python3 wikiscraper/wikiscraper.py
```

6. To call the microservice from your app's .py files, just add this import statement:
```
from wikiscraper.wikiscraper_tools import search_for
```

Now, you can search wikipedia by calling search_for and passing in a string.
search_for will return a dictionary containing a description and a list of images
from the wikipedia article you searched for.  You'll have to index into the images list
in order to access the individual image URLs.
Example:
```
# Gets a wikiscraper search result
results = search_for('nasa')

# Prints a summary of the wikipedia article
print(results.description)

# Prints a list of image urls
print(results.images)
```

![UML Sequence Diagram](https://drive.google.com/file/d/11hnpeV40RebEIpkCfKOpjZ-ncbuw8YOd/view?usp=sharing)




