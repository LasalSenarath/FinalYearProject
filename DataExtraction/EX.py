import re
import PreProcessing.emojiDictionary as emoji
# import PreProcessing.emoticonDictionary as emot
import PreProcessing.emoticonDirectory as emot
# import acronymDictionary as acrn
# import emoticonDirectory as emot
import pypyodbc
import json
from pymongo import MongoClient
import re
from nltk.tokenize import TweetTokenizer

import PreProcessing.acronymDictionary as acrn

if __name__ == "__main__":

    client = MongoClient( 'mongodb://localhost:27017/' )
    db = client.MovieSystemDB

    Twitter_User_Comments=db.get_collection("Twitter_User_Comments")

    for movie in Twitter_User_Comments.find():
        _id = movie['_id']
        Twitter_User_Comments.update_one( {'_id': _id}, {"$unset": {'PreprocessedComment':1}}, upsert=False )
        print( movie )