try:
    import json
except ImportError:
    import simplejson as json
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import tweepy
from time import gmtime, strftime
import time
import pypyodbc
import pyodbc

if __name__ == "__main__":
    consumer_key = "mWFMS61zK1W5gmlwPF1ucDKAC"
    consumer_secret = "t6RqsxPsoXzWJmxUKnpCipiEMpJrdoH70POuIK4zcqso6mV3ht"
    access_token = "2700948805-62HrSd4H6sfrAWcSURCGYpbDk3fTbAxFtDLGFXG"
    access_token_secret = "76LScw7XXexlBiG4341cROiK2RpvbVR8vSGCsBHTnBDzU"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    twitter_api = tweepy.API(auth)
    search_results = tweepy.Cursor(twitter_api.search, q="#ThorRagnarok-filter:retweets‏", lang="en",result_type="mixed").items(1000)

    #print(search_results)

    con = pypyodbc.connect(Trusted_Connection='yes', driver='{SQL Server}', server='DESKTOP-M6FNGC5', database='MovieSystemDB',Uid = 'sa',Pwd = '1234')
   #print(con)
cursor = con.cursor()
   #print(cursor)

   #print(row)


for result in search_results:
    cursor.execute('INSERT INTO ThorRagnarok(UserId,CreatedAt,CommentId,Comment) VALUES (?,?,?,?)',(result.user.id, result.created_at, result.id,json.dumps(result.text).replace("\"", "").replace("'", "")))
    cursor.commit()

print("downloaded")


