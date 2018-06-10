import json
from requests import get
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient( 'mongodb://localhost:27017/' )
db = client.MovieSystemDB

url = 'https://www.imdb.com/title/tt3501632/reviews?ref_=tt_ql_3'

response = get( url )

html_soup = BeautifulSoup( response.content, 'lxml' )

movie_containers = html_soup.find_all( 'div', class_='lister-list' )


def get_movie_reviews():
    movie_container = html_soup.find( 'div', class_='lister-list' )
    user_reviews = movie_container.find_all( 'div', class_='imdb-user-review' )

    coll = db.get_collection( "Thor" )
    id = 0
    for user_review in user_reviews:
        id += 1
        review_container = user_review.find( 'div', class_='review-container' )
        ratings_bar = review_container.find( 'div', class_='ipl-ratings-bar' )
        user_rating = "0"
        if ratings_bar:
            user_rating = int( ratings_bar.find( 'span', class_='rating-other-user-rating' ).find( 'span' ).get_text() )
        title = review_container.find( 'div', class_='title' ).text
        review = review_container.find( 'div', class_='text show-more__control' ).text
        data = {
            '_id': id,
            'title': title,
            'user_rating': user_rating,
            'review': review
        }
        coll.insert_one( data )
        print( title, user_rating )


get_movie_reviews()
