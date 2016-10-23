import sys
import json

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

from config import access_token, access_token_secret, consumer_secret, consumer_key


class StdOutListener(StreamListener):
    def on_data(self, data):
        # print d##ata
        s = json.loads(data)
        if data:
            print s['geo']

    def on_error(self, status):
        print status
        sys.exit()


if __name__ == '__main__':
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    listener = StdOutListener()
    stream = Stream(auth, listener)

    stream.filter(track=['#clinton'])