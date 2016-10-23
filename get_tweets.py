import sys
import json

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream, API

from config import access_token, access_token_secret, \
                   consumer_secret, consumer_key


class StreamListener(StreamListener):
    def on_data(self, data):
        print data
        # parse data based on 
        tweet = json.loads(data)
        if tweet.get('lang') == 'en' and tweet.get('coordinates') is not None:
                print tweet['coordinates']

    def on_error(self, status):
        print status
        sys.exit()


if __name__ == '__main__':
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = API(auth)

    listener = StreamListener()
    stream = Stream(api.auth, listener=listener)

    while True:
        stream.filter(track=['kevin hogan'])