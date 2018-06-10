import re

import acronymDictionary as acrn
import emoticonDirectory as emot
import pypyodbc
from nltk.tokenize import TweetTokenizer

from PreProcessing import emojiDictionary as emoji

# import negationWordDictionary as negation
# from nltk.corpus import stopwords
#from Preprocessing.TwitterDataProcessingWithStopWord import DataProcessWithStopWord

if __name__ == "__main__":
    con = pypyodbc.connect(Trusted_Connection='yes', driver='{SQL Server}', server='DESKTOP-M6FNGC5',
                           database='MovieSystemDB', Uid='sa', Pwd='1234')
    cursor = con.cursor()
    cursor.execute("SELECT CommentId,Comment FROM Actor WHERE Id=4")

    filtered_sentence = []
    for row in cursor.fetchall():
        print(row[1])
        print(row[0])
        tweet=str(row[1])
        id=str(row[0])

        print("Tweets:")
        print(tweet)
        # remove email
        email_less_tweet= re.sub(r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?", '', tweet)
        print("Email Remove")
        print(email_less_tweet)

        # remove urls
        url_less_tweet = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*','', email_less_tweet)
        print("Remove urls")
        print(url_less_tweet)



        filtered_sentence = []
        tw = url_less_tweet.split()
        words = TweetTokenizer(strip_handles=True, reduce_len=True).tokenize(url_less_tweet)

        # replace emoticon
        for w in tw:
            try:
                filtered_sentence.append(emot.select_emoticon(w))

            except:
                filtered_sentence.append(w)


        filtered_replace_emoji = []
        # replace emoji
        for w in filtered_sentence:
            try:
                filtered_replace_emoji.append(emoji.select_emoji(w))
            except:
                filtered_replace_emoji.append(w)

        print('emoji relace')
        print(filtered_replace_emoji)

        filtered_replaced_acronym = []
        # replace acronym
        for w in filtered_replace_emoji:
            try:
                filtered_replaced_acronym.append(acrn.select_acronym(w.lower()))
            except:
                filtered_replaced_acronym.append(w)

        sen = ""
        for a in filtered_replaced_acronym:
            sen = sen + a + " "


        #Remove punctuation
        outPunctuation = re.sub(r'[^a-zA-Z0-9\s]', ' ', sen)
        print("Remove Punctuation")
        print(outPunctuation)


        # remove only #tag and url both
        hash_tag_less_tweet = re.sub('(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)', '', outPunctuation)
        print("Remove only has tag and url")
        print(hash_tag_less_tweet)

       #Remove stop words
        # pattern = re.compile(r'\b(' + r'|'.join(stopwords.words('english')) + r')\b\s*')
        # RemoveHastext = pattern.sub('', hash_tag_less_tweet)
        # print("Remove stop words")
        # print(RemoveHastext)

        # remove single characters(f f f)
        preprocessed_final = re.sub(r'\b[B-Zb-z]\b', '', hash_tag_less_tweet)
        print("Remove single charcter")
        print(preprocessed_final)


        # # print(preprocessed_final)
        # cursor.execute("UPDATE UserTwitterData SET Comment ='" + str(preprocessed_final) + "' WHERE Id =" + str(id))
        # cursor.execute("UPDATE UserTwitterData SET IsPreprossed='TRUE' WHERE Id =" + str(id))
        # cursor.commit()
        # print("Comment Updated!")
    cursor.close()
