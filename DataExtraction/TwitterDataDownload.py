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
    consumer_key = "GUtsa3GvtI2peP9df5qU6Ak4N"
    consumer_secret = "5u8in2ZuK1aFzp2nFxYZeh4T0O1mMlcvb9OWdvyUxdfmDiyeM4"
    access_token = "2700948805-rI67xpX23ecGoGVma5c3YFDfcwEoxUIEp6qsydL"
    access_token_secret = "0svmiaKrpiispQAplgVfk1dX7uKB6SzNhf6rLixcEtDFX"
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    twitter_api = tweepy.API(auth)
    search_results = tweepy.Cursor(twitter_api.search, q="#GetOut-filter:retweets‏", lang="en",result_type="mixed").items(1000)

    coll = db.get_collection( "Twitter_User_Comments" )
    reviews=[]
    for result in search_results:
        data = {
            'UserId': result.user.id,
            'CreatedAt': result.created_at,
            'CommentId': result.id,
            'Comment': json.dumps( result.text ).replace( "\"", "" ).replace( "'", "" )
        }
        reviews.append( data )

    movie_Deatils = {
        'movie_title': "Get Out",
        'hashtag': "#GetOut",
        'user_reviews': reviews
    }

    coll.insert_one( movie_Deatils )


print("downloaded")


get_tweeter_reviews()