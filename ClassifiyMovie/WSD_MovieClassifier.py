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
import os.path
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC,LinearSVC,NuSVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier




# Ind_day_sense = "day_sense.txt"
# Ind_movie_sense = "movie_sense.txt"
from nltk.tokenize import sent_tokenize, word_tokenize, PunktSentenceTokenizer

class NewClassifier(ClassifierI):
    def __init__(self,*classifiers):
        self._classifiers=classifiers

    def classify(self,features):
        votes=[]
        for c in self._classifiers:
            v=c.classify(features)
            votes.append(v)
        return mode(votes)

def word_feats_extrnl(words):
    return dict([(word, True) for word in nltk.bigrams(word_tokenize(words))])

def find_features(words):
    return dict([(word, True) for word in nltk.bigrams(word_tokenize(words))])


with open("E:\Project\MyProject\ClassifiyMovie\movie.txt",encoding='utf-8', errors='ignore')as f:
    movie_content = f.readlines()

with open("E:\Project\MyProject\ClassifiyMovie\other.txt", encoding='utf-8', errors='ignore') as f:
    day_content = f.readlines()

dayfeats = []
moviefeats = []

for s in sent_tokenize(str(day_content)):
    dayfeats.append((word_feats_extrnl(s.lower()), 'other'))

for s in sent_tokenize(str(movie_content)):
    moviefeats.append((word_feats_extrnl(s.lower()), 'movie'))

len_of_day = int(len(dayfeats) * 3 / 4)
len_of_movie = int(len(moviefeats) * 3 / 4)

training_set = dayfeats[:len_of_day] + moviefeats[:len_of_movie]
testing_set = dayfeats[len_of_day:] + moviefeats[len_of_movie:]

NB_classifier = nltk.NaiveBayesClassifier.train(training_set)
print("NB accuracy",(nltk.classify.accuracy(NB_classifier,testing_set))*100)

LSV_classifier=SklearnClassifier(LinearSVC())
LSV_classifier.train(training_set)
print("LSVC accuracy",(nltk.classify.accuracy(LSV_classifier,testing_set))*100)

LR_classifier=SklearnClassifier(LogisticRegression())
LR_classifier.train(training_set)
print("LR accuracy",(nltk.classify.accuracy(LR_classifier,testing_set))*100)

# Random_classifier=SklearnClassifier(RandomForestClassifier())
# Random_classifier.train(training_set)
# print("Random Forest accuracy",(nltk.classify.accuracy(Random_classifier,testing_set))*100)
#
# svc_classifier=SklearnClassifier(SVC())
# svc_classifier.train(training_set)
# print("SVC classifier accuracy",(nltk.classify.accuracy(svc_classifier,testing_set))*100)
#
#
# nusvc_classifier=SklearnClassifier(NuSVC())
# nusvc_classifier.train(training_set)
# print("NUSVC classifier accuracy",(nltk.classify.accuracy(nusvc_classifier,testing_set))*100)
#
# decision_classifier=SklearnClassifier(DecisionTreeClassifier())
# decision_classifier.train(training_set)
# print("Decision classifier accuracy",(nltk.classify.accuracy(decision_classifier,testing_set))*100)
#
# neural_classifier=SklearnClassifier(MLPClassifier())
# neural_classifier.train(training_set)
# print("neural classifier accuracy",(nltk.classify.accuracy(neural_classifier,testing_set))*100)
#
# k_classifier=SklearnClassifier(KNeighborsClassifier())
# k_classifier.train(training_set)
# print("k classifier accuracy",(nltk.classify.accuracy(k_classifier,testing_set))*100)
#

new_classifier=NewClassifier(NB_classifier,LSV_classifier,LR_classifier)
print("New classifier accuracy",((nltk.classify.accuracy(new_classifier,testing_set))*100))

def AccessNewClassifier(text):
    feats = find_features(text.lower())
    return new_classifier.classify(feats)


print(AccessNewClassifier("plot is good"))