from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import tweepy
from time import gmtime, strftime
import time
import json
from pymongo import MongoClient
import re


client = MongoClient( 'mongodb://localhost:27017/' )
db = client.MovieSystemDB

def get_tweeter_reviews():
    consumer_key = "xNYeah4Jyhij8W12DfjyEPqOa"
    consumer_secret = "ipNtVWFx9hxtspfQInu9S2JQ7jJJfXz94mGjnXkrYHXnTGXnFN"
    access_token = "2700948805-xJZdpaq5YbDKCbYPUTX9umlBebOkawsVVUsSnNI"
    access_token_secret = "nEek40Ry1s8D170TO8fPxb9NcHXMraWnKrTo7RYP3tWuR"
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    twitter_api = tweepy.API(auth)
    search_results = tweepy.Cursor(twitter_api.search, q="#plot -filter:retweets‏", lang="en",result_type="mixed").items(1000)
    coll = db.get_collection( "Plot" )
    reviews=[]
    for result in search_results:
        movie_Deatils = {
                'UserId': result.user.id,
                'CreatedAt': result.created_at,
                'CommentId': result.id,
                'Comment': json.dumps( result.text ).replace( "\"", "" ).replace( "'", "" )
        }
        coll.insert_one( movie_Deatils )
    print("downloaded")


get_tweeter_reviews()