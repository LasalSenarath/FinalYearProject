import nltk
import random
from nltk.classify.scikitlearn import SklearnClassifier
from nltk.classify import ClassifierI
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from statistics import mode
from nltk.tokenize import word_tokenize
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC, LinearSVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
import PreProcessing.TestPreprocessing as TP
import DataExtraction.IMDbBasicDetailsExtraction as IMD



class VoteClassifier(ClassifierI):
    def __init__(self, *classifiers):
        self._classifiers = classifiers

    def classify(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        act = votes.count("actor")
        plo = votes.count("polt")
        the = votes.count("theme")

        # print(act, plo, the)
        if max(act, plo, the) > 2:
            vote = mode(votes)
        else:
            vote = "other"
        return vote

    def confidence(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        # print(votes)
        act = votes.count( "actor" )
        plo = votes.count( "polt" )
        the = votes.count( "theme" )

        if max(act, plo, the) > 2:
            choice_votes = votes.count(mode(votes))
        else:
            choice_votes = list(set(votes)).__len__()

        conf = choice_votes / len(votes)
        return conf



short_Actor = open("E:\Project\MyProject\Classify\Actor.txt", "r").read()
short_Plot = open("E:\Project\MyProject\Classify\Plot.txt", "r").read()
short_Theme= open("E:\Project\MyProject\Classify\Theme.txt", "r").read()

documents = []
all_words = []


for r in short_Actor.split('.'):
    documents.append((r, "actor"))
    wordsn = word_tokenize(r)
    for word in wordsn:
        all_words.append(word.lower())



for r in short_Plot.split('.'):
    documents.append((r, "plot"))
    wordsn = word_tokenize(r)
    for word in wordsn:
        all_words.append(word.lower())

for r in short_Theme.split('.'):
    documents.append((r, "theme"))
    wordsn = word_tokenize(r)
    for word in wordsn:
        all_words.append(word.lower())


all_words = nltk.FreqDist(all_words)

word_features = list(all_words.keys())[:1000]


def find_features(document):
    words = word_tokenize(document)
    features = {}
    for ws in word_features:
        features[ws] = (ws in words)
    return features


featureSets = [(find_features(rev), category) for (rev, category) in documents]
random.shuffle(featureSets)

# training_set = featureSets[:750]
# testing_set = featureSets[750:]

training_set = featureSets[:360]
testing_set = featureSets[360:]


NB_classifier = nltk.NaiveBayesClassifier.train(training_set)
# classifier.show_most_informative_features(15)


MNB_classifier = SklearnClassifier(MultinomialNB())
MNB_classifier.train(training_set)


LR_classifier = SklearnClassifier(LogisticRegression())
LR_classifier.train(training_set)

# stochastic gradient descent
SGD_classifier = SklearnClassifier(SGDClassifier())
SGD_classifier.train(training_set)

SV_classifier = SklearnClassifier(SVC())
SV_classifier.train(training_set)

LSV_classifier = SklearnClassifier(LinearSVC())
LSV_classifier.train(training_set)

RF_classifier = SklearnClassifier(RandomForestClassifier())
RF_classifier.train(training_set)

DT_classifier = SklearnClassifier( DecisionTreeClassifier())
DT_classifier.train(training_set)

KN_classifier = SklearnClassifier(KNeighborsClassifier())
KN_classifier.train(training_set)

# print("NB Accuracy: ",(nltk.classify.accuracy(NB_classifier,testing_set))*100)
# print("MNB Accuracy: ",(nltk.classify.accuracy(MNB_classifier,testing_set))*100)
# print("LR Accuracy: ",(nltk.classify.accuracy(LR_classifier,testing_set))*100)
# print("SGD Accuracy: ",(nltk.classify.accuracy(SGD_classifier,testing_set))*100)
# print("SVC Accuracy: ",(nltk.classify.accuracy(SV_classifier,testing_set))*100)
# print("LSVC Accuracy: ",(nltk.classify.accuracy(LSV_classifier,testing_set))*100)
# print("RF Accuracy: ",(nltk.classify.accuracy(RF_classifier,testing_set))*100)
# print("DT Accuracy: ",(nltk.classify.accuracy(DT_classifier,testing_set))*100)
# print("KN Accuracy: ",(nltk.classify.accuracy(KN_classifier,testing_set))*100)


# voted_classifier1 = VoteClassifier(MNB_classifier,LR_classifier,SGD_classifier)
# voted_classifier2 = VoteClassifier(MNB_classifier,LR_classifier,LSV_classifier)
# voted_classifier3 = VoteClassifier(MNB_classifier,LR_classifier,RF_classifier)
# voted_classifier4 = VoteClassifier(MNB_classifier,SGD_classifier,RF_classifier)
# voted_classifier5 = VoteClassifier(MNB_classifier,SGD_classifier,LSV_classifier)
# voted_classifier6 = VoteClassifier(SGD_classifier,LSV_classifier,RF_classifier)
# voted_classifier7 = VoteClassifier(LR_classifier,LSV_classifier,RF_classifier)
# voted_classifier8 = VoteClassifier(LR_classifier,SGD_classifier,RF_classifier)
# voted_classifier9 = VoteClassifier(LR_classifier,SGD_classifier,LSV_classifier)
# voted_classifier10 = VoteClassifier(MNB_classifier,LSV_classifier,RF_classifier)


# print("voted_classifier Algorithm Accuracy percentage1:",(nltk.classify.accuracy(voted_classifier1, training_set))*100)
# print("voted_classifier Algorithm Accuracy percentage2:",(nltk.classify.accuracy(voted_classifier2, training_set))*100)
# print("voted_classifier Algorithm Accuracy percentage3:",(nltk.classify.accuracy(voted_classifier3, training_set))*100)
# print("voted_classifier Algorithm Accuracy percentage4:",(nltk.classify.accuracy(voted_classifier4, training_set))*100)
# print("voted_classifier Algorithm Accuracy percentage5:",(nltk.classify.accuracy(voted_classifier5, training_set))*100)
# print("voted_classifier Algorithm Accuracy percentage6:",(nltk.classify.accuracy(voted_classifier6, training_set))*100)
# print("voted_classifier Algorithm Accuracy percentage7:",(nltk.classify.accuracy(voted_classifier7, training_set))*100)
# print("voted_classifier Algorithm Accuracy percentage8:",(nltk.classify.accuracy(voted_classifier8, training_set))*100)
# print("voted_classifier Algorithm Accuracy percentage9:",(nltk.classify.accuracy(voted_classifier9, training_set))*100)
# print("voted_classifier Algorithm Accuracy percentage10:",(nltk.classify.accuracy(voted_classifier10, training_set))*100)



def classifiedLabel(text):
    feats = find_features(text)
    return LR_classifier.classify(feats)





# print(classifiedLabel("Poor Direction, Poor and over acting. No any suitable event combination. "))










