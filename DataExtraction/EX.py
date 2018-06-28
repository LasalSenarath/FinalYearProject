from requests import get
from bs4 import BeautifulSoup
from pymongo import MongoClient
import re



def get_movie_basic_details(movieid):
    Id=movieid
    url = "https://www.imdb.com/title/tt"+Id+"/"
    response = get( url )
    soup = BeautifulSoup( response.content, 'lxml' )
    movieName = soup.findAll( "div", {"class": "title_wrapper"} )[0].h1.text
    movieName = re.sub( r"\d+", " ", movieName )
    movieName = re.sub( r"[\(\)\n\t ]", " ", movieName ).strip()
    thumbnail = soup.find( "div", {"class": "poster"} ).find( 'img' )['src']
    thumbnail = re.sub( r"http.*/images/M/", "", thumbnail )
    video = soup.find( "div", {"class": "slate"} ).find( 'a' )['href']
    video1 = re.sub( r"\?.*", "", video )
    video2=re.sub( r".*vi(\d+)", r"\1", video1 )
    print(movieName)
    print(thumbnail)
    print(video2)
# print("Updated All Movie Details...")
get_movie_basic_details("1340138")

# https://www.imdb.com/title/tt2560140/videoplayer/vi1401073433