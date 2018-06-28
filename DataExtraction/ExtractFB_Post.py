import facebook
import re
from pymongo import MongoClient

token= 'EAACEdEose0cBAC69WKyJHNy7OSlTeIbvRZAnx6geIq8WqWTc5Gtj8FtDjuIt949S34HeEtgv0SlyTu2Uzhv6gPxJchPZCWXdX7A4512NYsIh0aSwJgpeAVvAnpJI1EhuftlKvjxrjIfIP8vkwZCGImK5UK9VmeUUty8SmeVZCOUAcnImuAcA4kqFQnpTCIfwbuF1FwLnZCzm1fpXJzWxm'
graph = facebook.GraphAPI(token, version='2.7')
client = MongoClient( 'mongodb://localhost:27017/' )
db = client.MovieSystemDB

def FindUrl(string):
    # findall() has been used
    # with valid conditions for urls in string
    url = re.findall( 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]| [! * \(\), ] | (?: % [0 - 9a - fA - F][0 - 9 a - fA - F]))+', string)
    return url

def get_fb_user_post_details():
    for post in graph.get_object( "2025873594337041/feed" )['data']:
        # print(post['message'])
        if FindUrl(post['message']):
            url=', '.join( map( str, FindUrl(post['message'] )) )
            print(url)#url
            # print( post['message'] )
            # print(post['updated_time'])#
            date = post['updated_time'].split( 'T' )[0]
            print(date)
            # Remove white spacees
            whitespace_less_post = re.sub( '[\s]+', " ", post['message'])
            # print( "whitespace_less_tweet:",whitespace_less_tweet )
            #  Remove new lines
            newline_less_post = re.sub( '\n', '', whitespace_less_post )
            # print( "newline_less_tweet:", newline_less_tweet )

            # Remove hash_tag
            hash_tag_less_post = re.sub( r'\S*#(?:\[[^\]]+\]|\S+)', '', newline_less_post )
            # hash_tag_less_tweet = re.sub(r'#([^\s]+)', r'\1)',whitespace_less_tweet)
            # print("hash_tag_less_tweet:",hash_tag_less_tweet)

            # Remove additional white spaces
            additional_white_less_post = re.sub( '[\s]+', ' ', hash_tag_less_post )
            # print("additional_white_less_tweet:", additional_white_less_tweet)

            # remove urls
            url_less_post = re.sub( r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '',
                                     additional_white_less_post )
            # print("url_less_tweet:",url_less_tweet)

            # Remove http
            http_less_post = re.sub( r"http\S+", "", url_less_post )
            print(http_less_post)
            print("=============")

        coll = db.get_collection( "FB_User_Posts" )


        posts_Deatils = {
                    'movie_Url': url,
                    'date': date,
                    'post': http_less_post
        }

        coll.insert_one( posts_Deatils )

print("downloaded")

get_fb_user_post_details()
