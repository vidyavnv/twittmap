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


class StreamListener(StreamListener):
    def on_data(self, data):
        tweet = json.loads(data)
        if tweet['lang'] == 'en' and tweet['user'].get('location') is not None:
            location = tweet['user'].get('location')
            tweet_id = str(tweet['id'])
            geocode_result = gmaps.geocode(location)
            raw_tweet = {
                'user': tweet['user']['screen_name'],
                'text': tweet['text'],
                'location': tweet['user']['location'],
                'coordinates': geocode_result, 
                'time': tweet['created_at']
            }
            es.index(index=ES_INDEX, doc_type=ES_TYPE, id=tweet_id, body=raw_tweet)
            return True

    def on_error(self, status):
        print status
        # sys.exit()


if __name__ == '__main__':
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = API(auth)

    listener = StreamListener()
    stream = Stream(api.auth, listener=listener)

    while True:
        stream.filter(track=['sports', 'music', 'hillary'])