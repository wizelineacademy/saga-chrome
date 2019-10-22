from slackClient import SlackClient
from datetime import datetime
from urlextract import URLExtract
import tldextract
import json
import os
#Given a string, find all the URL domains in it
#Returns a list of strings with all the domains found
def getURLDomains(text):
    extractor = URLExtract()
    urls = extractor.find_urls(text)
    domains_list = []
    for url in urls:
        domain = tldextract.extract(url).domain
        domains_list.append(domain)
    return domains_list

#Given a file name and an object or dictionary write a JSON with that file name
def writeJSON(file_name, object_instance):
    f = open(file_name+".json", "w")
    f.write(json.dumps(object_instance))
    f.close()

#Given a slack key and an output file name, find all domains from URLs sended in all channels
#Writes a JSON that segments channels, grouped by day and then all the domains with a count of appearances
# that day in that channel
def getDomainsByChannel(key, jsonName):
    client = SlackClient(key)
    channels = client.getChannels(True)
    result = {}
    for channel in channels:
        result[channel["id"]] = {}
        result[channel["id"]]["name"] = channel["name"]
        result[channel["id"]]["domains"] = {}
        print("Getting " + channel["name"] + "(" + channel["id"] + ") channel's messages.", end="")
        messages = client.getChannelHistory(channel["id"])
        print(".",end="")
        for message in messages:
            date = datetime.utcfromtimestamp(float(message["ts"])).strftime('%Y-%m-%d %H:%M:%S')
            day = date.split(" ")[0]
            domains = result[channel["id"]]["domains"]
            newDomains = getURLDomains(message["text"])
            if len(newDomains) > 0:
                if day not in domains:
                    domains[day] = {}
                for domain in newDomains:
                    if domain not in domains[day]:
                        domains[day][domain] = 0
                    domains[day][domain] += 1
        print("DONE")
    writeJSON(jsonName, result)
    
today = str(datetime.now()).split()[0]
slack_api_key = os.environ.get("SLACK_API_KEY")
if slack_api_key:
    jsonName = "allChannels_"+today
    getDomainsByChannel(slack_api_key, jsonName)
else:
    print("Error: Be sure to set the api key in an environment variable called SLACK_API_KEY")