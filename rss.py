import feedparser
import json
import os
import datetime
import time
from dateutil.parser import parse
def rss(url, last_modified=None):# store the etag and modified
    if(last_modified == None):
        feed_update = feedparser.parse(url)
    else:
        feed_update = feedparser.parse(url, modified = last_modified)
    
    filename = 'savedata.json'
    with open(filename, 'r') as f:
        savefile = json.load(f)
        last_post_date = savefile['savedata']["rss.py"]["modified"]
    
    if (( duplicateCheck(last_post_date, feed_update["entries"][0]["published"]))): #("2023-01-29 23:09:25.052002", "2023-01-30 23:09:25.052002") )):
        filename = 'savedata.json'
        with open(filename, 'r') as f:
            data = json.load(f)
            data['savedata']["rss.py"]["modified"] = feed_update["entries"][0]["published"]
        os.remove(filename)
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        #print(feed_update["entries"][0])
        text = feed_update["entries"][0]["summary"]
        text = text.replace("\t", "")
        text = text.replace("\n \n\n\n", "\n\n")
        title = feed_update["entries"][0]["title"]
        link = feed_update["entries"][0]["link"]
        pubdate = feed_update["entries"][0]["published"]
        print()
        print("New post in RSS feed: " + title + " " + pubdate)
        print(repr(text))
        return (True, text, title, link, pubdate)
    else:
        return (False, None, None, None)


def heliohostrss():
    filename = 'savedata.json'
    with open(filename, 'r') as f:
        data = json.load(f)
    return rss("https://www.helionet.org/index/rss/1-news.xml/", data['savedata']["rss.py"]["modified"])

def duplicateCheck(oldtime, newtime):
    oldtime = oldtime.replace("+0000", "")
    oldtime = oldtime.replace("GMT", "")
    oldtime = parse(oldtime.split(".", 1)[0])
    oldtime = (time.mktime(oldtime.timetuple()))

    newtime = newtime.replace("+0000", "")
    newtime = newtime.replace("GMT", "")
    newtime = parse(newtime.split(".", 1)[0])
    newtime = (time.mktime(newtime.timetuple()))

    if (str(oldtime) < (str(newtime))):
        return True
    else:
        return False

if __name__ == "__main__":
    exit("Don't Run This File as a Standalone File! Import it into another file to use it")
