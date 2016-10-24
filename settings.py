import googlemaps
from elasticsearch import Elasticsearch

from config import ES_PORT, ES_HOST, GMAP_KEY

es = Elasticsearch([{'host': ES_HOST, 'port': ES_PORT}])

gmaps = googlemaps.Client(key=GMAP_KEY)
