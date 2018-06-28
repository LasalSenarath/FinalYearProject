from requests import get
from bs4 import BeautifulSoup
import re

def get_you_tub_trailler(movie_name,year):

    url=""
    print(url)
    response = get( url )
    soup = BeautifulSoup( response.content, 'lxml' )
    videos = soup.findAll( "div", {"class": "g"} )[0]
    videos = soup.findAll( "div", {"class": "g"} )[0].find( 'a' )['href']
    print(videos)

get_you_tub_trailler("Tomb Raider","2018")