import facebook
import requests
from pymongo import MongoClient
from datetime import datetime
import bson
connection = MongoClient('mongodb://localhost:27017/')
client = MongoClient()
db = client.user
token= 'EAACEdEose0cBAD76yFZAELUKdJZAvX8TVYuBBjgVj257rgCZCZBip0WohnNtSF9vZCsjJpV4l5IzfEeTxvqi8UajQhRMXnUutcbhUzz5m7jeM6x1QToPaEdWhQq6BQuHDgHedeDNNZAZAYQ7VCo7bFzJU8cw70K23i3YoZBhQPvCh3OHnSs38REndOI8QzWRMS0ZD'
graph = facebook.GraphAPI(token, version='2.7')
# userName = graph.get_object("me?fields=name")
# userEmail = graph.get_object("me?fields=email")
# userAgeRange = graph.get_object("me?fields=age_range")
# userBirthday = graph.get_object("me?fields=birthday")
# userGender = graph.get_object("me?fields=gender")
# userHometown = graph.get_object("me?fields=hometown")
db.users.insert(
    {
        'user':{
            'userName': graph.get_object("me?fields=name"),
            'userEmail': graph.get_object("me?fields=email"),
            'userAgeRange': graph.get_object("me?fields=age_range"),
            'userBirthday': graph.get_object("me?fields=birthday"),
            'userGender': graph.get_object("me?fields=gender"),
            'userHometown': graph.get_object("me?fields=hometown")
        }
    }
)