import re
import PreProcessing.emojiDictionary as emoji
import PreProcessing.emoticonDirectory as emot
import PreProcessing.acronymDictionary as acrn
from pymongo import MongoClient
from nltk.tokenize import word_tokenize, TweetTokenizer


client = MongoClient( 'mongodb://localhost:27017/' )
db = client.MovieSystemDB
#Preprpcessing FB post and extract url Id




def preprocesse_actor_post():
    Actor = db.get_collection( "Plot" )

    for user in Actor.find():
        _id = user['_id']
        postid = user['CommentId']
        message = user['Comment']

        # Remove white spacees
        whitespace_less_tweet = re.sub( '[\s]+', " ", message )
        # print( "whitespace_less_tweet:",whitespace_less_tweet )
        #  Remove new lines
        newline_less_tweet = re.sub( '\n', '', whitespace_less_tweet )
        # print( "newline_less_tweet:", newline_less_tweet )

        # Remove hash_tag
        hash_tag_less_tweet = re.sub( r'\S*#(?:\[[^\]]+\]|\S+)', '', newline_less_tweet )
        # hash_tag_less_tweet = re.sub(r'#([^\s]+)', r'\1)',whitespace_less_tweet)
        # print("hash_tag_less_tweet:",hash_tag_less_tweet)

        # Remove additional white spaces
        additional_white_less_tweet = re.sub( '[\s]+', ' ', hash_tag_less_tweet )
        # print("additional_white_less_tweet:", additional_white_less_tweet)

        # remove urls
        url_less_tweet = re.sub( r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '',
                                 additional_white_less_tweet )
        # print("url_less_tweet:",url_less_tweet)

        # Remove http
        http_less_tweet = re.sub( r"http\S+", "", url_less_tweet )
        # print("http_less_tweet:",http_less_tweet)

        # remove email
        email_less_tweet = re.sub( r'\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$', '', http_less_tweet )
        # print("email_less_tweet:",email_less_tweet)

        # remove repeated characters
        repeate_char_less_tweet = re.sub( r'(.)\1{3,}', r'\1\1', email_less_tweet, flags=re.DOTALL )
        # print("repeate_char_less_tweet:",repeate_char_less_tweet)

        filtered_sentence = []
        words = TweetTokenizer( strip_handles=True, reduce_len=True ).tokenize( repeate_char_less_tweet )
        # print("TweetTokenizerwords:",words)

        # replace emoticon
        for w in words:
            try:
                filtered_sentence.append( emot.select_emoticon( w ) )

            except:
                filtered_sentence.append( w )
        # print("filtered_sentence",filtered_sentence)

        # replace emoji
        filtered_replace_emoji = []
        # print(filtered_sentence)

        for w in filtered_sentence:
            try:
                filtered_replace_emoji.append( emoji.select_emoji( w ) )
            except:
                filtered_replace_emoji.append( w )
        # print( "filtered_replace_emoji", filtered_replace_emoji )

        # replace acronym
        filtered_replaced_acronym = []
        for w in filtered_replace_emoji:
            try:
                filtered_replaced_acronym.append( acrn.select_acronym( w.lower() ) )
            except:
                filtered_replaced_acronym.append( w )
        # print( "filtered_replaced_acronym", filtered_replaced_acronym )
        sen = ""
        for a in filtered_replaced_acronym:
            sen = sen + a + " "

        # remove non alphanueric characters(/\[]{})
        nonalphanumeric_less_tweet = re.sub( r'[^A-Za-z\s]+', '', sen )
        # print("nonalphanumeric_less_tweet",nonalphanumeric_less_tweet)
        stop_words = []
        word_tokens = (word_tokenize( nonalphanumeric_less_tweet ))
        # print( "word_tokens",word_tokens)
        with open( "E:\Project\MyProject\PreProcessing\stopwords.txt", encoding='utf-8', errors='ignore' )as f:
            lines = f.readlines()
        for line in lines:
            stop_words.append( line.strip() )

        # print(stop_words)
        filtered_sentence_stopword = []
        for w in word_tokens:
            if w not in stop_words:
                filtered_sentence_stopword.append( w )
        # print( "filtered_sentence_stopword", filtered_sentence_stopword )
        sentence = ""
        for a in filtered_sentence_stopword:
            sentence = sentence + a + " "
        # remove single characters
        remove_single = re.sub( r'\b[B-Zb-z]\b', '', sentence )
        preprocessed_final = ''.join( map( str, remove_single ) )
        user['PreprocessedPost'] = preprocessed_final
        Actor.update_one( {'_id': _id}, {"$set": user}, upsert=False )
print( "Preprocessed all!" )

preprocesse_actor_post()
