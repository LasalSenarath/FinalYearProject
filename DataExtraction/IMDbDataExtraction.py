import json
from requests import get
from bs4 import BeautifulSoup
from pymongo import MongoClient
import re

client = MongoClient( 'mongodb://localhost:27017/' )
db = client.MovieSystemDB

url = 'https://www.imdb.com/title/tt5052448/reviews?ref_=tt_ql_3'

response = get( url )

html_soup = BeautifulSoup( response.content, 'lxml' )



movie_containers = html_soup.find_all( 'div', class_='lister-list' )

def get_movie_reviews():
    movie_title = html_soup.find_all( 'div', class_='parent' )[0].h3.a.text
    movie_Url = "https://www.imdb.com/" + html_soup.find_all( 'div', class_='parent' )[0].h3.a["href"]
    relesed_Year = html_soup.find_all( 'div', class_='parent' )[0].h3.span.text
    relesed_Year = re.sub( r"[\(\)\n\t ]", r"", relesed_Year )
    relesed_Year = re.sub( r".*(\d{4}).*", r"\1", relesed_Year )
    movie_container = html_soup.find( 'div', class_='lister-list' )
    user_reviews = movie_container.find_all( 'div', class_='imdb-user-review' )


    reviews=[]
    coll = db.get_collection( "IMDb_User_Review" )
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
            'title': title,
            'user_rating': user_rating,
            'review': review
        }
        reviews.append(data)

    movie_Deatils={
        'movie_title': movie_title,
        'movie_Url': movie_Url,
        'relesed_Year': relesed_Year,
        'user_reviews':reviews
    }

    coll.insert_one(movie_Deatils)

print("Entered...")

get_movie_reviews()
