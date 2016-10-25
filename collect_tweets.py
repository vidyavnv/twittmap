import json
from TwitterSearch import *

from config import access_token, access_token_secret, \
                   consumer_secret, consumer_key, \
                   ES_INDEX, ES_TYPE
from settings import es, gmaps
from utils import get_category


try:
    tso = TwitterSearchOrder() # create a TwitterSearchOrder object
    tso.set_keywords(['sports'])
    tso.set_language('en') # we want to see German tweets only

    # it's about time to create a TwitterSearch object with our secret tokens
    ts = TwitterSearch(
        consumer_key = consumer_key,
        consumer_secret = consumer_secret,
        access_token = access_token,
        access_token_secret = access_token_secret
     )

     # this is where the fun actually starts :)
    count = 0
    
    for tweet in ts.search_tweets_iterable(tso):
        try:
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
        except Exception as e:
            continue

except TwitterSearchException as e: # take care of all those ugly errors if there are some
    print(e)