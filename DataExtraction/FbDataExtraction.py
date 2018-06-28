import facebook
from pymongo import MongoClient

token= 'EAACEdEose0cBAFZB06luZC5OC9cbHsFZAZBwjUpxHOfqsSeA9bHWhlNRnoAAuVk6OiZCO7AnWoYi4ggiwpLXNlRWDanFP2sY0S3h0fGhwKa1BkHBSSk4lOET35xZAW4amYrStllUuczPDCFZBIz8BY56ZC8wV9OZBCOmHTimphBlGqesBK5DGTf2wxeFziz0x9gQhUjnCxCOXdM83xV9w1FWz'
graph = facebook.GraphAPI(token, version='2.7')
client = MongoClient( 'mongodb://localhost:27017/' )
db = client.MovieSystemDB

def get_fb_user_details():
    # userID = graph.get_object("me?fields=name")['id']
    # userName = graph.get_object("me?fields=name")['name']
    # userAgeRange = graph.get_object("me?fields=age_range")['age_range']['min']
    # userGender = graph.get_object("me?fields=gender")['gender']
    # userHometown = graph.get_object("me?fields=hometown")['hometown']['name']
    # print(userID,userName,userAgeRange,userGender,userHometown)
        coll = db.get_collection("FB_User_Details")
        user_Deatils = {
            'userId': graph.get_object("me?fields=name")['id'],
            'userName': graph.get_object("me?fields=name")['name'],
            'userAgeRange': graph.get_object("me?fields=age_range")['age_range']['min'],
            'userGender': graph.get_object("me?fields=gender")['gender'],
            'userHometown':graph.get_object("me?fields=hometown")['hometown']['name']
        }
        coll.insert_one( user_Deatils )
print("downloaded")


get_fb_user_details()
