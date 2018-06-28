import Classify.SClassification as scl
from pymongo import MongoClient


client = MongoClient( 'mongodb://localhost:27017/' )
db = client.MovieSystemDB
#Preprpcessing FB post and extract url Id



def preprocesse_fb_post():
    FB_User_Details = db.get_collection( "FB_User_Details" )
    for user in FB_User_Details.find():
        _id = user['_id']
        if "posts" in user:
            updated_post = []
            posts = user['posts']
            for post in posts:
                label = scl.classifiedLabel(post['PreprocessedPost'])
                # label = ''.join( map( str, PreprocessedPost ) )
                post['Label'] = label
                updated_post.append( post )
            user['posts'] = updated_post
            FB_User_Details.update_one( {'_id': _id}, {"$set": user}, upsert=False )
print( "Preprocessed all!" )

preprocesse_fb_post()
