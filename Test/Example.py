import re
import DataExtraction.IMDbBasicDetailsExtraction as DEI
from pymongo import MongoClient
import time


client = MongoClient( 'mongodb://localhost:27017/' )
db = client.MovieSystemDB

#call auto update movie collection
def FindUrl(string):
    # url = re.sub(r".*(\d{7}).*", "https://www.imdb.com/title/tt"+r"\1/", string)
    url = re.sub( r".*(\d{7}).*", r"\1", string )
    return url


def update_movie_profile():
    FB_User_Details = db.get_collection( "FB_User_Details" )
    for user in FB_User_Details.find():
        _id = user['_id']
        if "posts" in user:
            updated_post = []
            posts = user['posts']
            for post in posts:
                postid = post['id']
                message = post['message']
                urlid= FindUrl(message)
                DEI.get_movie_basic_details( urlid )
                # time.sleep( 60 )

update_movie_profile()

# DEI.get_movie_basic_details("1825683")
# https://www.imdb.com/videoplayer/