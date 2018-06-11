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

    filtered_sentence = []

    for movie in Twitter_User_Comments.find():
        _id = movie['_id']

        # print(movie)
        if "user_reviews" in movie:
            updated_user_review = []
            user_reviews=movie['user_reviews']

            for user_review in user_reviews:
                CommentId = user_review['CommentId']
                Comment = user_review['Comment']
                # print(CommentId,Comment)

                remove_hash_tag_tweet = re.sub(r'\S*#(?:\[[^\]]+\]|\S+)', '', Comment)
                # remove urls
                remove_url_tweet = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*','', remove_hash_tag_tweet)
                # print(remove_url_tweet)
                # remove email
                remove_email_tweet = re.sub(r'\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$', '', remove_url_tweet)
                # remove repeated characters
                repeate_char_less_tweet = re.sub(r'(.)\1{3,}', r'\1\1', remove_email_tweet, flags=re.DOTALL)

                # print(repeate_char_less_tweet)
                filtered_sentence = []
                words = TweetTokenizer(strip_handles=True, reduce_len=True).tokenize(repeate_char_less_tweet)
                # print("words")
                # print(words)
                # replace emoticon
                for w in words:
                    try:
                        filtered_sentence.append(emot.select_emoticon(w))

                    except:
                        filtered_sentence.append(w)
                # print(filtered_sentence)
                filtered_replace_emoji = []
                # replace emoji
                for w in filtered_sentence:
                    try:
                        filtered_replace_emoji.append(emoji.select_emoji(w))
                    except:
                        filtered_replace_emoji.append(w)
                # print(filtered_replace_emoji)
                filtered_replaced_acronym = []
                # replace acronym
                for w in filtered_replace_emoji:
                    try:
                        filtered_replaced_acronym.append(acrn.select_acronym(w.lower()))
                    except:
                        filtered_replaced_acronym.append(w)

                # print(filtered_replaced_acronym)
                sen = ""
                for a in filtered_replaced_acronym:
                    sen = sen + a + " "
                # remove non alphanumeric characters
                # print(sen)
                nonalphanumeric_less_tweet = re.sub(r'[^A-Za-z\s]+', '', sen)
                print(Comment,nonalphanumeric_less_tweet)
                # remove single characters
                # preprocessed_final = re.sub(r'\b[B-Zb-z]\b', '', nonalphanumeric_less_tweet)
                # print(nonalphanumeric_less_tweet)
                # print(id)
                user_review['PreprocessedComment'] = nonalphanumeric_less_tweet
                updated_user_review.append(user_review)

            movie['user_reviews'] = updated_user_review
            Twitter_User_Comments.update_one({'_id':_id},{"$set": movie}, upsert=False)
            # print(movie)
print("Preprocessed all!")