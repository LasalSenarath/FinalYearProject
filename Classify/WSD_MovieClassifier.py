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

# with open("E:\Project\MyProject\Classify\movie.txt",encoding='utf-8', errors='ignore')as f:
#     movie_content = f.readlines()

with open("E:\Project\MyProject\Classify\Other.txt", encoding='utf-8', errors='ignore') as f:
    day_content = f.readlines()

with open("E:\Project\MyProject\Classify\Actor.txt", encoding='utf-8', errors='ignore') as f:
    actor_content = f.readlines()

with open("E:\Project\MyProject\Classify\Plot.txt", encoding='utf-8', errors='ignore') as f:
    plot_content = f.readlines()

with open("E:\Project\MyProject\Classify\Rating.txt", encoding='utf-8', errors='ignore') as f:
    rating_content = f.readlines()

with open("E:\Project\MyProject\Classify\Technology.txt", encoding='utf-8', errors='ignore') as f:
    technology_content = f.readlines()

with open("E:\Project\MyProject\Classify\Theme.txt", encoding='utf-8', errors='ignore') as f:
    theme_content = f.readlines()

dayfeats = []
# moviefeats = []
actorfeats = []
plotfeats = []
ratingfeats = []
technologyfeats = []
themefeats = []

for s in sent_tokenize(str(day_content)):
    dayfeats.append((word_feats_extrnl(s.lower()), 'other'))

# for s in sent_tokenize(str(movie_content)):
#     moviefeats.append((word_feats_extrnl(s.lower()), 'movie'))

for s in sent_tokenize(str(actor_content)):
    actorfeats.append((word_feats_extrnl(s.lower()), 'actor'))

for s in sent_tokenize(str(plot_content)):
    plotfeats.append((word_feats_extrnl(s.lower()), 'plot'))

for s in sent_tokenize(str(rating_content)):
    ratingfeats.append((word_feats_extrnl(s.lower()), 'rating'))

for s in sent_tokenize(str(rating_content)):
    themefeats.append((word_feats_extrnl(s.lower()), 'theme'))

for s in sent_tokenize(str(rating_content)):
    technologyfeats.append((word_feats_extrnl(s.lower()), 'technology'))

len_of_day = int(len(dayfeats) * 3 / 4)
# len_of_movie = int(len(moviefeats) * 3 / 4)
len_of_actor = int(len(actorfeats) * 3 / 4)
len_of_plot = int(len(plotfeats) * 3 / 4)
len_of_rating = int(len(ratingfeats) * 3 / 4)
len_of_theme = int(len(themefeats) * 3 / 4)
len_of_technology = int(len(technologyfeats) * 3 / 4)

training_set = dayfeats[:len_of_day] + actorfeats[:len_of_actor] + plotfeats[:len_of_plot] + ratingfeats[:len_of_rating] + themefeats[:len_of_theme] + technologyfeats[:len_of_technology]
testing_set = dayfeats[len_of_day:] + actorfeats[len_of_actor:] + plotfeats[len_of_plot:] + ratingfeats[len_of_rating:] + themefeats[len_of_theme:] + technologyfeats[len_of_technology:]


# training_set = dayfeats[:len_of_day] + moviefeats[:len_of_movie]
# testing_set = dayfeats[len_of_day:] + moviefeats[len_of_movie:]

# NaiveBayes_classifier = nltk.NaiveBayesClassifier.train( training_set)
# print("Naive Bayes accuracy",(nltk.classify.accuracy(NaiveBayes_classifier,testing_set))*100)

# LSVS_classifier=SklearnClassifier(LinearSVC())
# LSVS_classifier.train(training_set)
# print("Linear SVC accuracy",(nltk.classify.accuracy(LSVS_classifier,testing_set))*100)

LR_classifier=SklearnClassifier(LogisticRegression())
LR_classifier.train(training_set)
print("Logistic Regression accuracy",(nltk.classify.accuracy(LR_classifier,testing_set))*100)
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
# new_classifier=NewClassifier(NaiveBayes_classifier,LSVS_classifier,LR_classifier)
new_classifier=NewClassifier(LR_classifier)

#new_classifier=NewClassifier(decision_classifier,LSVS_classifier,LR_classifier)

print("new classifier accuracy",((nltk.classify.accuracy(new_classifier,testing_set))*100))

def AccessNewClassifier(text):
    feats = find_features(text.lower())
    return new_classifier.classify(feats)
