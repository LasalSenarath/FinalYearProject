import re
import PreProcessing.emojiDictionary as emoji
# import PreProcessing.emoticonDictionary as emot
import PreProcessing.emoticonDirectory as emot
import PreProcessing.acronymDictionary as acrn
from pymongo import MongoClient
from nltk.tokenize import word_tokenize, TweetTokenizer

if __name__ == "__main__":

    client = MongoClient( 'mongodb://localhost:27017/' )
    db = client.MovieSystemDB
    FB_User_Details = db.get_collection( "FB_User_Details" )
    # row = FB_User_Details.find({"_id":"5b2e5dac93a31608485eed55"})
    for row in FB_User_Details.find():
        if row['userid']=="16":
            print(row['name'])
            updated_user_posts = []
            data={
                "message": "The Dark Knight 🤩😍 Best superhero movie I have ever watched (<3). Known as all-time great. Considered by 'film critics' to be one of the best films of the 2000s and one of the best superhero films ever. It became the highest-grossing film of 2008 and is the 32nd-highest-grossing film of all time. Only superhero movie rated under top 10 movies in 2008. And it's the \"Only superhero movie rated under IMDB to 100\". In Dark Knight Christian Bale act as the Batman and Heath Ledger as the Joker. Heath Ledger's performance was widely praised and ultimately won him a posthumous Academy Award. Heath Ledger named as best Joker cast of all time(in the movies).Won 2 Oscars. https://www.imdb.com/title/tt0468569/ #TheDarkKnight #TheBestSuperHeroMovie",
                "updated_time": "2018-02-05T18:02:18+0000",
                "id": "2025873594337041_2037175796540154"
            }
            updated_user_posts.append( data )
            data ={
                "message": "The Last Samurai <3 An American military advisor arrived to Japan for destroy the samurai warriors, then the turned up the tables, he joined with samurai and fought against the American invasion. Its based on true story about end of samurai warriors. Great acting by Tom Cruise and the Hans Zimmer's magical music (<3) made the movie more interesting. Soundtracks were utterly beautiful. <3 <3 http://www.imdb.com/title/tt0325710/ #TheLastSamurai",
                "updated_time": "2018-02-03T06:31:22+0000",
                "id": "2025873594337041_2035235213400879"
            }
            updated_user_posts.append( data )
            data ={
                "message": "Gravity <3 Dr. Ryan Stone and her shuttle crew faced chaotic experience in the middle of space operation, made her the only survivor of the crew... One of the best Sci-fi movie in the 21st century. It includes awesome soundtracks as well. <3 http://www.imdb.com/title/tt1454468/ #Gravity #SciFi",
                "updated_time": "2018-01-14T18:46:47+0000",
                "id": "2025873594337041_2026370887620645"
            }
            updated_user_posts.append( data )
            data ={
                "message": "Interstellar... <3 Another classic Sci-Fi movie from hollywood. Group of astronauts travel through wormhole to ensure the existence of the humanity. Great movie with strong story lineup. Also one of greatest and awesome sound direction from Great Hans Zimmer <3. It soundtracks were utterly amazing. http://www.imdb.com/title/tt0816692/ #Interstellar #SciFi #HansZimmer",
                "updated_time": "2018-01-31T18:51:06+0000",
                "id": "2025873594337041_2029204780670589"
            }
            updated_user_posts.append( data )
            data ={
                "message": "The Martian.Team of astronauts landed on Mars for the scientific experiments, due to fierce storm, team blast off from the planet Mars and one of astronaut (Mark Watney) left behind(presumed dead). Will he able survive until the rescue team arrive? Yet another masterpiece of Sci-Fi genres. <3 http://www.imdb.com/title/tt3659388/ #TheMartian #SciFi",
                "updated_time": "2018-01-19T07:25:06+0000",
                "id": "2025873594337041_2027590664165334"
            }
            updated_user_posts.append( data )
            data ={
                "message": "The Good, Bad and Ugly... Screened in 1966. The Final volume of dollars trilogy. One of the highest rated movie of all time(All three movies consistently rated as it is). Highly recommended to watch :D http://www.imdb.com/title/tt0060196/ #GoodBadAndUgly #DollarsTrilogy",
                "updated_time": "2018-01-14T07:44:13+0000",
                "id": "2025873594337041_2026133304311070"
            }
            updated_user_posts.append( data )
            data ={
                "message": "The Foreigner...Never contend with a man who has nothing to lose. Old aged man loses his only daughter due bomb attack. Will he able to take the revenge? It's a great action movie in the summer...  http://www.imdb.com/title/tt1615160/ #NeverPushAGoodManTooFar #TheForeigner",
                "updated_time": "2018-01-16T20:18:42+0000",
                "id": "2025873594337041_2027269437530790"
            }
            updated_user_posts.append( data )

            data ={
                "message": "Assassin's Creed... 😶😶 Inspired by Assassin's Creed game series. Describes the beginning of the brotherhood, and relationship with eternal enemies (templars). There are lots of disappointments about this movie. The story differs from the original one(game version), actions are also not great. Main character is not about the ones we know about( :/ ). Assassin's Creed you are deserve better... 😥😣 http://www.imdb.com/title/tt2094766/ #AssassinsCreed",
                "updated_time": "2018-01-31T18:50:13+0000",
                "id": "2025873594337041_2032280750362992"
            }

            updated_user_posts.append( data )


            row['posts'] = updated_user_posts
            FB_User_Details.update_one( {'userid': "16"}, {"$set": row}, upsert=False )

print( "updated..." )
