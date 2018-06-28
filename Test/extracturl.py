import re
from pymongo import MongoClient
client = MongoClient( 'mongodb://localhost:27017/' )
db = client.MovieSystemDB
IMDb_Movie_Profile = db.get_collection( "IMDb_Movie_Profile" )


def FindURL(text):
    new = re.sub(r".*(\d{7}).*", "https://www.imdb.com/title/tt"+r"\1/", text)
    # https://www.imdb.com/title/tt1028532/
    # print(new)
    return new

# print(FindURL("https://m.imdb.com/title/tt0892769/?ref=m_nv_sr_2"))


def check_movie_id(getmovieid):
    setmovieid=int(getmovieid)
    aList = []
    for movie in IMDb_Movie_Profile.find():
        movieid= int(movie['movie_id'])
        movie_title=movie['movie_title']
        aList.append(movieid)
        aList.append(movie_title)
    # print(len(aList))
    if setmovieid not in aList:
        return setmovieid
    else:
        return 0

print(check_movie_id(2395427))