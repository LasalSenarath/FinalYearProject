from requests import get
from bs4 import BeautifulSoup
from pymongo import MongoClient
import re

#Auto crwling IMDbPage
client = MongoClient( 'mongodb://localhost:27017/' )
db = client.MovieSystemDB
IMDb_Movie_Profile = db.get_collection( "IMDb_Movie_Profile" )
def FindUrl(string):
    url = re.sub( r".*(\d{7}).*", r"\1", string )
    return url

def select_MovieName(movieid):
    for movie in IMDb_Movie_Profile.find({'movie_id':movieid}):
        movieName=movie['movie_title']
        return movieName



def check_movie_id(getmovieid):
    setmovieid=int(getmovieid)
    aList = []
    for movie in IMDb_Movie_Profile.find():
        movieid= int(movie['movie_id'])
        aList.append(movieid)
    print( len(aList) )
    if setmovieid not in aList:
        return setmovieid
    else:
        return 0


def get_movie_basic_details(movieid):
    Id=movieid
    if check_movie_id(Id)!=0:
        url = "https://www.imdb.com/title/tt"+Id+"/"
        response = get( url )
        soup = BeautifulSoup( response.content, 'lxml' )
        movieName = soup.findAll( "div", {"class": "title_wrapper"} )[0].h1.text
        movieName = re.sub( r"\d+", " ", movieName )
        movieName = re.sub( r"[\(\)\n\t ]", " ", movieName ).strip()
        movieid = Id
        try:
            released_Year = soup.findAll( "div", {"class": "title_wrapper"} )[0].h1.find( 'span',{'id': 'titleYear'} ).a.text
        except:
            released_Year =""
        released_Year = re.sub( r"[\(\)\n\t ]", r"", released_Year )
        released_Year = re.sub( r".*(\d{4}).*", r"\1", released_Year )
        movieImDb = soup.findAll( "div", {"class": "ratingValue"} )[0].strong.find( 'span' ).text
        movieType1 = soup.findAll( "div", {"class": "subtext"} )[0].find_all( 'a' )[0].find( 'span' ).text
        try:
            movieType2 = soup.findAll( "div", {"class": "subtext"} )[0].find_all( 'a' )[1].find( 'span' ).text
        except:
            movieType2 =""
        try:
            movieType3 = soup.findAll( "div", {"class": "subtext"} )[0].find_all( 'a' )[2].find( 'span' ).text
        except:
            movieType3 =""
        movieType = [movieType1, movieType2, movieType3]
        movieSummery = soup.findAll( "div", {"class": "summary_text"} )[0].text
        movieSummery = re.sub( r"\s+", " ", movieSummery )
        movieDirector = soup.findAll( "div", {"class": "credit_summary_item"} )[0].find( 'span' ).a.text
        movieWriter = soup.findAll( "div", {"class": "credit_summary_item"} )[1].find( 'span' ).a.text
        try:
            movieStars1 = soup.findAll( "div", {"class": "credit_summary_item"} )[2].find_all( 'a' )[0].find( 'span' ).text
        except:
            movieStars1=""
        try:
            movieStars2 = soup.findAll( "div", {"class": "credit_summary_item"} )[2].find_all( 'a' )[1].find( 'span' ).text
        except:
            movieStars2=""
        try:
            movieStars3 = soup.findAll( "div", {"class": "credit_summary_item"} )[2].find_all( 'a' )[2].find( 'span' ).text
        except:
            movieStars3=""
        movieStars = [movieStars1, movieStars2, movieStars3]
        country = soup.find( "div", {"id": "titleDetails"} ).findAll( "div" )[1].find( 'a' ).text
        language = soup.find( "div", {"id": "titleDetails"} ).findAll( "div" )[2].find( 'a' ).text
        runtime = soup.find( 'time' )['datetime']
        runtime = re.sub( r"\D", "", runtime )
        runtime = re.sub( r"^\s+", "", runtime ).strip()
        try:
            metascore = soup.find( "div", {"class": "titleReviewBar"} ).find( "div", {"class": "metacriticScore score_favorable titleReviewBarSubItem"} ).find( 'span' ).text
        except:
            try:
                metascore = soup.find( "div", {"class": "titleReviewBar"} ).find( "div", {"class": "metacriticScore score_unfavorable titleReviewBarSubItem"} ).find( 'span' ).text
            except:
                try:
                    metascore = soup.find( "div", {"class": "titleReviewBar"} ).find( "div", {"class": "metacriticScore score_mixed titleReviewBarSubItem"} ).find( 'span' ).text
                except:
                    metascore=""
        try:
            popularity = soup.find( "div", {"class": "titleReviewBar"} ).findAll( "div", {"class": "titleReviewBarItem"} )[2].find( "span", {"class": "subText"} ).text
            popularity = re.sub( r"\(.*\)", " ", popularity )
            popularity = re.sub( r"\s+", "", popularity )
        except:
            popularity=""

        thumbnail = soup.find( "div", {"class": "poster"} ).find( 'img' )['src']
        thumbnail = re.sub( r"http.*/images/M/", "", thumbnail )
        try:
            video = soup.find( "div", {"class": "slate"} ).find( 'a' )['href']
            video = re.sub( r"\?.*", "", video )
            videoid = re.sub( r".*vi(\d+)", r"\1", video )
        except:
            videoid=""

        coll = db.get_collection( "IMDb_Movie_Profile" )
        movie_Details = {
            'movie_id': movieid,
            'movie_title': movieName,
            'released_Year': released_Year,
            'movieImDb': movieImDb,
            'movieType': movieType,
            'movieSummery': movieSummery,
            'movieDirector': movieDirector,
            'movieWriter': movieWriter,
            'movieStars': movieStars,
            'country': country,
            'language': language,
            'runtime': runtime,
            'popularity': popularity,
            'metascore': metascore,
            'thumbnail': thumbnail,
            'videoid':videoid
        }
        coll.insert_one( movie_Details )
        # print( "Entered..."+movieName )
        return movieName
    else:
        return select_MovieName( Id )
# print("Updated All Movie Details...")

# get_movie_basic_details("1340138")
