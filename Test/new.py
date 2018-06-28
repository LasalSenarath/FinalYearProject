import PreProcessing.TestPreprocessing as TP
import DataExtraction.IMDbBasicDetailsExtraction as IMD
import Classify.SClassification as SCL


def MyTest(fbpost):
    result=[]
    # print("FB post:"+fbpost)
    movieid=TP.preprocesse_fb_post(fbpost)
    result.append(movieid[0])
    # print("Preprocessed Post:"+movieid[0])
    movie=IMD.get_movie_basic_details(movieid[1])
    result.append( movie )
    label=SCL.classifiedLabel(movieid[0])
    result.append( label )
    # print(label)
    return result
# text="Nice plot #ddffh #ffdhfgj https://www.imdb.com/title/tt2084970/"

# MyTest(text)







