import nltk
import random
from nltk.corpus import movie_reviews
import _pickle
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import LinearSVC, NuSVC, SVC
from nltk.classify import ClassifierI
from statistics import mode
import operator
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier

# Ind_day_sense = "day_sense.txt"
# Ind_movie_sense = "movie_sense.txt"
from nltk.tokenize import sent_tokenize, word_tokenize, PunktSentenceTokenizer

class NewClassifier( ClassifierI ):
    def __init__(self, *classifiers):
        self._classifiers = classifiers
    def classify(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify( features )
            # print(v)
            votes.append( v )
        return mode( votes )

def word_feats_extrnl(words):
    return dict( [(word, True) for word in nltk.bigrams( word_tokenize( words ) )] )


def find_features(words):
    return dict( [(word, True) for word in nltk.bigrams( word_tokenize( words ) )] )


with open( "E:/Project/MyProject/Classify/Actor.txt", encoding='utf-8', errors='ignore' )as f:
    actor_content = f.read()

with open( "E:/Project/MyProject/Classify/Plot.txt", encoding='utf-8', errors='ignore' )as f:
    plot_content = f.read()

with open( "E:/Project/MyProject/Classify/Theme.txt", encoding='utf-8', errors='ignore' )as f:
    theme_content = f.read()


actorfeats = []
plotfeats = []
themefeats = []

for s in sent_tokenize( str( actor_content ) ):
    actorfeats.append( (word_feats_extrnl( s.lower() ), 'actor') )

for s in sent_tokenize( str( plot_content ) ):
    plotfeats.append( (word_feats_extrnl( s.lower() ), 'plot') )

for s in sent_tokenize( str( theme_content ) ):
    themefeats.append( (word_feats_extrnl( s.lower() ), 'theme') )

len_of_actor = int( len( actorfeats ) * 3 / 4 )
len_of_plot = int( len( plotfeats ) * 3 / 4 )
len_of_theme = int( len( themefeats ) * 3 / 4 )

training_set = actorfeats[:len_of_actor] + plotfeats[:len_of_plot]+ themefeats[:len_of_theme]
testing_set = actorfeats[len_of_actor:] + plotfeats[len_of_plot:]+ themefeats[len_of_theme:]

NB_classifier = nltk.NaiveBayesClassifier.train( testing_set )
print( "NB accuracy", (nltk.classify.accuracy( NB_classifier, testing_set )) * 100 )

print( "NB accuracy", (nltk.classify.accuracy( NB_classifier, testing_set )) * 100 )
LSV_classifier = SklearnClassifier( LinearSVC() )
LSV_classifier.train( training_set )
print( "LSV accuracy", (nltk.classify.accuracy( LSV_classifier, testing_set )) * 100 )

LR_classifier = SklearnClassifier( LogisticRegression() )
LR_classifier.train( training_set )
print( "LR accuracy", (nltk.classify.accuracy( LR_classifier, testing_set )) * 100 )

RF_classifier=SklearnClassifier(RandomForestClassifier())
RF_classifier.train(training_set)
print("RF accuracy",(nltk.classify.accuracy(RF_classifier,testing_set))*100)


DT_classifier=SklearnClassifier(DecisionTreeClassifier())
DT_classifier.train(training_set)
print("DT accuracy",(nltk.classify.accuracy(DT_classifier,testing_set))*100)

# KN_classifier=SklearnClassifier(KNeighborsClassifier())
# KN_classifier.train(training_set)
# print("KN accuracy",(nltk.classify.accuracy(KN_classifier,testing_set))*100)

new_classifier0 = NewClassifier( NB_classifier,LSV_classifier,LR_classifier )
new_classifier1 = NewClassifier( NB_classifier,LSV_classifier,RF_classifier )
new_classifier2 = NewClassifier( NB_classifier,LSV_classifier,DT_classifier )
new_classifier3 = NewClassifier( NB_classifier,LR_classifier,DT_classifier )
new_classifier4 = NewClassifier( NB_classifier,LR_classifier,RF_classifier )
new_classifier5 = NewClassifier( LR_classifier,RF_classifier,DT_classifier )
new_classifier6 = NewClassifier( LSV_classifier,RF_classifier,DT_classifier )
new_classifier7 = NewClassifier( LSV_classifier,LR_classifier,DT_classifier )
new_classifier8 = NewClassifier( LSV_classifier,LR_classifier,RF_classifier )
new_classifier9 = NewClassifier( NB_classifier,RF_classifier,DT_classifier )


# print( "New classifier accuracy0", ((nltk.classify.accuracy( new_classifier0, training_set )) * 100) )
# print( "New classifier accuracy1", ((nltk.classify.accuracy( new_classifier1, training_set )) * 100) )
# # print( "New classifier accuracy2", ((nltk.classify.accuracy( new_classifier2, testing_set )) * 100) )
# # print( "New classifier accuracy3", ((nltk.classify.accuracy( new_classifier3, testing_set )) * 100) )
# print( "New classifier accuracy4", ((nltk.classify.accuracy( new_classifier4, training_set )) * 100) )
# print( "New classifier accuracy5", ((nltk.classify.accuracy( new_classifier5, training_set )) * 100) )
# print( "New classifier accuracy6", ((nltk.classify.accuracy( new_classifier6, training_set )) * 100) )
# print( "New classifier accuracy7", ((nltk.classify.accuracy( new_classifier7, training_set )) * 100) )
# print( "New classifier accuracy8", ((nltk.classify.accuracy( new_classifier8, training_set )) * 100) )
# # print( "New classifier accuracy9", ((nltk.classify.accuracy( new_classifier9, testing_set )) * 100) )

def AccessNewClassifier(text):
    feats = find_features( text.lower() )
    return new_classifier9.classify( feats )


print( AccessNewClassifier( "good acting." ) )

