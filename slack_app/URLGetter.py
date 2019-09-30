from slackClient import SlackClient
from datetime import datetime
from urlextract import URLExtract
import tldextract
import json

def getURLDomains(text):
    extractor = URLExtract()
    urls = extractor.find_urls(text)
    domains_list = []
    for url in urls:
        domain = tldextract.extract(url).domain
        domains_list.append(domain)
    return domains_list

def writeJSON(file_name, object_instance):
    f = open(file_name+".json", "w")
    f.write(json.dumps(object_instance))
    f.close()

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
slack_api_key = API_KEY_HERE
jsonName = "allChannels_"+today

getDomainsByChannel(slack_api_key, jsonName)