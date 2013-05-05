import requests
import time
from datetime import datetime, timedelta
import tweepy
import ujson as json

api = tweepy.API()
extended = set()
interval = 10
since_id = 0

def search(since_id):
    return api.search(
        '#angelhacksf',
        since_id=since_id,
        rpp=20,
    )

def mk_message(tweet):
    return json.dumps({
        'id': tweet.id,
        'channel': 'badass',
        'text': tweet.text,
        'eventid': time.mktime(tweet.created_at.timetuple()),
    })

def publish(tweets):
    for tweet in tweets:
        msg = mk_message(tweet)
        requests.post(
            'http://sandbox.netcat.io/publish?channel=badass',
            data=msg
        )

while True:
    tweets = search(since_id)
    tweets = [t for t in tweets if t.id not in extended]
    since_id = tweets[0].id if tweets else 0

    publish(tweets)

    removals = []
    for tweet_id in extended:
        if t.created_at < (datetime.utcnow()-timedelta(hours=2)):
            removals.append(tweet_id)
    [extended.remove(t) for t in removals]

    for tweet in tweets:
        extended.add(tweet.id)

    time.sleep(interval)

