import sys
import json
from datetime import datetime

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream, API

from config import access_token, access_token_secret, \
                   consumer_secret, consumer_key, \
                   ES_INDEX, ES_TYPE
from settings import es, gmaps
from utils import get_category


class StreamListener(StreamListener):
    def __init__(self):
        self.count = 0
        self.limit = 150

    def on_data(self, data):
        if self.count < self.limit:
            tweet = json.loads(data)
            if tweet['lang'] == 'en' and tweet['user'].get('location') is not None:
                location = tweet['user'].get('location')
                tweet_id = str(tweet['id'])
                geocode_result = gmaps.geocode(location)
                print geocode_result
                tweet_text = tweet['text'].lower().encode('ascii', 'ignore').decode('ascii')
                raw_tweet = {
                    'user': tweet['user']['screen_name'],
                    'text': tweet_text,
                    'location': tweet['user']['location'],
                    'coordinates': geocode_result, 
                    'time': tweet['created_at'],
                    'category': get_category(tweet_text)
                }
                es.index(index=ES_INDEX, doc_type=ES_TYPE, id=tweet_id, body=raw_tweet)
            self.count += 1
        else:
            stream.disconnect()


    def on_error(self, status):
        print status
        # sys.exit()


if __name__ == '__main__':
    while True:
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        listener = StreamListener()
        stream = Stream(auth, listener)

        stream.filter(track=['sports', 'politics', 'business', ])