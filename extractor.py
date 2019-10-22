# pip install extruct
import extruct
import requests
from w3lib.html import get_base_url
import json

#Given a url obtain metadata in JSON format from the website using extruct library 
#If writedata==True write a JSON file with the data
#Returns a dictionary with the metadata form the url
def extractJSON(url, write_data=False):
    r = requests.get(url)
    base_url = get_base_url(r.text, r.url)
    data = extruct.extract(r.text, base_url=base_url)["json-ld"]
    if len(data) > 0:
        if write_data:
            with open('last_data.json', 'w') as outfile:
                json.dump(data[0], outfile)
        return data[0]
    return []

#Given a url obtain only the keywords
#Returns a list with the keywords found in the url
def getKeywords(url):
    data = extractJSON(url, True)
    return data["keywords"]

url = 'https://medium.com/@felipegaiacharly/live-reloading-and-lazy-loading-for-micro-frontends-using-ara-framework-707ccb0f1960'
keywords = getKeywords(url)
print(keywords)
