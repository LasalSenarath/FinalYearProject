import PreProcessing.emojiDictionary as emoji
# import PreProcessing.emoticonDictionary as emot
import PreProcessing.emoticonDirectory as emot
import PreProcessing.acronymDictionary as acrn
from pymongo import MongoClient
from nltk.tokenize import word_tokenize,TweetTokenizer
import ClassifiyMovie.WSD_MovieClassifier as WSD



if __name__ == "__main__":
    client = MongoClient( 'mongodb://localhost:27017/' )
    db = client.MovieSystemDB
    Twitter_User_Comments = db.get_collection( "Twitter_User_Comments" )
    for movie in Twitter_User_Comments.find():
        _id = movie['_id']
        if "user_reviews" in movie:
            updated_user_review = []
            user_reviews = movie['user_reviews']

            for user_review in user_reviews:
                CommentId = user_review['CommentId']
                PreprocessedComment = user_review['PreprocessedComment']
                result = WSD.AccessNewClassifier(PreprocessedComment)
                # print(PreprocessedComment+" "+result)
                user_review['validity'] = result
                updated_user_review.append( user_review )
            movie['user_reviews'] = updated_user_review
            Twitter_User_Comments.update_one( {'_id': _id}, {"$set": movie}, upsert=False )
