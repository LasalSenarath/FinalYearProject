import json
from requests import get
from bs4 import BeautifulSoup
from pymongo import MongoClient
import re

client = MongoClient( 'mongodb://localhost:27017/' )
db = client.MovieSystemDB

url = 'https://www.imdb.com//title/tt5052448/?ref_=tt_urv'

response = get( url )

soup = BeautifulSoup( response.content, 'lxml' )


movieName = soup.findAll("div", {"class": "title_wrapper"})[0].h1.text
movieName = re.sub(r"\d+", " ", movieName)
movieName = re.sub( r"[\(\)\n\t ]", " ", movieName)
# print(movieName)

relesed_Year = soup.findAll("div", {"class": "title_wrapper"})[0].h1.find('span',{'id':'titleYear'}).a.text
relesed_Year = re.sub( r"[\(\)\n\t ]", r"", relesed_Year )
relesed_Year = re.sub( r".*(\d{4}).*", r"\1", relesed_Year )
# print(movieYear)

movieImDb = soup.findAll("div", {"class": "ratingValue"})[0].strong.find('span').text
# print(movieImDb)

movieType1 = soup.findAll("div", {"class": "subtext"})[0].find_all('a')[0].find('span').text
movieType2 = soup.findAll("div", {"class": "subtext"})[0].find_all('a')[1].find('span').text
movieType3 = soup.findAll("div", {"class": "subtext"})[0].find_all('a')[2].find('span').text

movieType=[movieType1,movieType2,movieType3]
# movieType=[movieType1,movieType2]

#movieReleaseData = soup.findAll("div", {"class": "subtext"})[0].find_all('a')[2].text
# movieReleaseData = soup.find("div", {"class": "titleDetails"}).findAll("div", {"class": "txt-block"})
# movieReleaseData=re.sub(r"\(.*\)", " ", movieReleaseData)
# movieReleaseData = re.sub( r"\s+", " ", movieReleaseData)
# print(movieType1)
# print(movieType2)
# print(movieType3)
# print(movieReleaseData)

movieSummery=soup.findAll("div", {"class": "summary_text"})[0].text
movieSummery = re.sub( r"\s+", " ", movieSummery )
# print(movieSummery)

movieDirector=soup.findAll("div", {"class": "credit_summary_item"})[0].find('span').a.text
# print(movieDirector)

movieWriter=soup.findAll("div", {"class": "credit_summary_item"})[1].find('span').a.text
# print(movieWriter)

movieStars1=soup.findAll("div", {"class": "credit_summary_item"})[2].find_all('a')[0].find('span').text
movieStars2=soup.findAll("div", {"class": "credit_summary_item"})[2].find_all('a')[1].find('span').text
movieStars3=soup.findAll("div", {"class": "credit_summary_item"})[2].find_all('a')[2].find('span').text

movieStars=[movieStars1,movieStars2,movieStars3]
# print(movieStars1)
# print(movieStars2)
# print(movieStars3)

country=soup.find("div", {"id": "titleDetails"}).findAll("div")[1].find('a').text
# print(country)

language=soup.find("div", {"id": "titleDetails"}).findAll("div")[2].find('a').text
# print(language)

# runtime=soup.find("div", {"id": "titleDetails"}).findAll("div")[12].time.text
# print(runtime)
# runtime = re.sub( r"\D", " ", runtime )
# print(runtime)

runtime=soup.find('time')['datetime']
runtime = re.sub( r"\D", " ", runtime )
runtime = re.sub( r"^\s+", "", runtime )
# print(runtime)


metascore=soup.find("div", {"class": "titleReviewBar"}).find("div", {"class": "metacriticScore score_favorable titleReviewBarSubItem"}).find('span').text
# print(metascore)

popularity=soup.find("div", {"class": "titleReviewBar"}).findAll("div", {"class": "titleReviewBarItem"})[2].find("span", {"class": "subText"}).text
popularity=re.sub(r"\(.*\)", " ", popularity)
popularity = re.sub( r"\s+", "", popularity)
# print(Popularity)


coll = db.get_collection( "IMDb_Movie_Details" )


movie_Deatils={
        'movie_title': movieName,
        'movie_Url': url,
        'relesed_Year': relesed_Year,
        'movieImDb':movieImDb,
        'movieType':movieType,
        'movieSummery':movieSummery,
        'movieDirector':movieDirector,
        'movieWriter':movieWriter,
        'movieStars':movieStars,
        'country':country,
        'language':language,
        'runtime':runtime,
        'popularity':popularity,
        'metascore':metascore
}

coll.insert_one(movie_Deatils)

print("Entered...")
