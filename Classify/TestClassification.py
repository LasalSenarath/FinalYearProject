from nltk.classify import NaiveBayesClassifier
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier
from nltk.classify import ClassifierI
from statistics import mode
import pandas as pd
import nltk
import csv
import operator
import pickle
#Dileep's last

class VoteClassifier(ClassifierI):
    # def __init__(self, *classifiers):
    #     self._classifiers = classifiers

    def __init__(self, NB, LR, LSVS, RF, DT):
        self.hybClaswithVotes = {}
        self.NB = NB
        self.LR = LR
        self.LSVS = LSVS
        self.RF = RF
        self.DT = DT

    def classifyAll(self, sentence):
        hybVotes = []
        eachVote = {}

        hybVotes.append(self.NB.classify(word_feats(sentence)))
        hybVotes.append(self.LR.classify(word_feats(sentence)))
        hybVotes.append(self.LSVS.classify(word_feats(sentence)))
        hybVotes.append(self.RF.classify(word_feats(sentence)))
        hybVotes.append(self.DT.classify(word_feats(sentence)))

        NBRes = self.NB.prob_classify(word_feats(sentence))
        for label in NBRes.samples():
            eachVote[label] = NBRes.prob(label)
        maximumNB = max(eachVote.items(), key=operator.itemgetter(1))[0]
        self.addToHybridVotes(maximumNB, eachVote.get(maximumNB))
        print(self.hybClaswithVotes)

        eachVote = {}
        LRRes = self.LR.prob_classify(word_feats(sentence))
        for label in LRRes.samples():
            eachVote[label] = LRRes.prob(label)
        maximumLR = max(eachVote.items(), key=operator.itemgetter(1))[0]
        self.addToHybridVotes(maximumLR, eachVote.get(maximumLR))
        print(self.hybClaswithVotes)

        eachVote = {}
        RFRes = self.RF.prob_classify(word_feats(sentence))
        for label in RFRes.samples():
            eachVote[label] = RFRes.prob(label)
        maximumRF = max(eachVote.items(), key=operator.itemgetter(1))[0]
        self.addToHybridVotes(maximumRF, eachVote.get(maximumRF))
        print(self.hybClaswithVotes)

        eachVote = {}
        DTRes = self.DT.prob_classify(word_feats(sentence))
        for label in DTRes.samples():
            eachVote[label] = DTRes.prob(label)
        maximumDT = max(eachVote.items(), key=operator.itemgetter(1))[0]
        self.addToHybridVotes(maximumDT, eachVote.get(maximumDT))
        print(self.hybClaswithVotes)

        # eachVote = {}
        # LSVSRes = self.LSVS.prob_classify(word_feats(sentence))
        # for label in DTRes.samples():
        #     eachVote[label] = DTRes.prob(label)
        # maximumDT = max(eachVote.items(), key=operator.itemgetter(1))[0]
        # self.addToHybridVotes(maximumDT, eachVote.get(maximumDT))
        # print(self.hybClaswithVotes)

        try:
            print(str(hybVotes))
            return mode(hybVotes)
        except:
            maxx = max(self.hybClaswithVotes.items(), key=operator.itemgetter(1))[0]
            return maxx


    def confidence(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)

        choice_votes = votes.count(mode(votes))
        conf = choice_votes / len(votes)* 100
        return conf

    def addToHybridVotes(self, sentiment, vote):
        if self.hybClaswithVotes.get(sentiment) == None:
            self.hybClaswithVotes[sentiment] = vote
        else:
            localMax = max(self.hybClaswithVotes.get(sentiment), vote)
            if localMax != self.hybClaswithVotes.get(sentiment):
                self.hybClaswithVotes[sentiment] = vote

def word_feats(words):
     return dict([(word, True) for word in words])


def addToVotes(sentiment, vote, classifierReswithVotes):
    if classifierReswithVotes.get(sentiment) == None:
        classifierReswithVotes[sentiment] = vote
    else:
        localMax = max(classifierReswithVotes.get(sentiment), vote)
        if localMax != classifierReswithVotes.get(sentiment):
            classifierReswithVotes[sentiment] = vote
    print(str(classifierReswithVotes))

def returnLastValue():
    with open( 'Actor.txt', 'r' ) as actor:
        data_actor = actor.read().replace( ',', ' ' )
        actor_vocab = nltk.word_tokenize( data_actor )

    with open( 'Plot.txt', 'r' ) as plot:
        data_plot = plot.read().replace( ',', ' ' )
        plot_vocab = nltk.word_tokenize( data_plot )

    with open( 'Theme.txt', 'r' ) as theme:
        data_theme = theme.read().replace( ',', ' ' )
        theme_vocab = nltk.word_tokenize( data_theme )

    with open( 'Other.txt', 'r' ) as other:
        data_other = other.read().replace( ',', ' ' )
        other_vocab = nltk.word_tokenize( data_other )

    actor_features = [(word_feats( act ), 'actor') for act in actor_vocab]
    plot_features = [(word_feats( plo ), 'plot') for plo in plot_vocab]
    theme_feature = [(word_feats( the ), 'theme') for the in theme_vocab]
    other_feature = [(word_feats( ot ), 'other') for ot in other_vocab]

    train_set = actor_features + plot_features + theme_feature + other_feature

    NBclassifier = NaiveBayesClassifier.train(train_set)

    LR_classifier = SklearnClassifier(LogisticRegression())
    LR_classifier.train(train_set)

    LSVS_classifier = SklearnClassifier(LinearSVC())
    LSVS_classifier.train(train_set)

    Random_classifier = SklearnClassifier(RandomForestClassifier())
    Random_classifier.train(train_set)

    decision_classifier = SklearnClassifier(DecisionTreeClassifier())
    decision_classifier.train(train_set)


    classifierReswithVotes = {}
    classifierResult = []

    NBactor = 0
    NBplot = 0
    NBtheme = 0
    NBother = 0

    # actor plot theme other
    LRactor = 0
    LRplot = 0
    LRtheme = 0
    LRother = 0

    SVMactor = 0
    SVMplot = 0
    SVMtheme = 0
    SVMother = 0

    RFactor = 0
    RFplot = 0
    RFtheme = 0
    RFother = 0

    DTactor = 0
    DTplot = 0
    DTtheme = 0
    DTother = 0

    line = "good actor"
    sentence = "".join(line)
    sentence = sentence.lower()
    words = sentence.split(' ')
    # actor plot theme other
    for word in words:
        NBclassResult = NBclassifier.classify(word_feats(word))
        if NBclassResult == 'actor':
            NBactor = NBactor + 1
        if NBclassResult == 'plot':
            NBplot = NBplot + 1
        if NBclassResult == 'theme':
            NBtheme = NBtheme + 1
        if NBclassResult == 'other':
            NBother = NBother + 1
        # actor plot theme other
        classResultLR = LR_classifier.classify(word_feats(word))
        if classResultLR == 'actor':
            LRactor = LRactor + 1
        if classResultLR == 'plot':
            LRplot = LRplot + 1
        if classResultLR == 'theme':
            LRtheme = LRtheme + 1
        if classResultLR == 'other':
            LRother = LRother + 1

        # actor plot theme other
        classResultSVM = LSVS_classifier.classify(word_feats(word))
        if classResultSVM == 'actor':
            SVMactor = SVMactor + 1
        if classResultSVM == 'plot':
            SVMplot = SVMplot + 1
        if classResultSVM == 'theme':
            SVMtheme = SVMtheme + 1
        if classResultSVM == 'other':
            SVMother = SVMother + 1


        classResultRandom = Random_classifier.classify(word_feats(word))
        # actor plot theme other
        if classResultRandom == 'actor':
            RFactor = RFactor + 1
        if classResultRandom == 'plot':
            RFplot = RFplot+ 1
        if classResultRandom == 'theme':
            RFtheme = RFtheme + 1
        if classResultRandom == 'other':
            RFother = RFother + 1

        classResultDT = decision_classifier.classify(word_feats(word))
        # actor plot theme other
        if classResultDT == 'actor':
            DTactor = DTactor + 1
        if classResultDT == 'plot':
            DTplot = DTplot + 1
        if classResultDT == 'theme':
            DTtheme = DTtheme + 1
        if classResultDT == 'other':
            DTother= DTother + 1

    # actor plot theme other
    statsNB = {'actor': (float(NBactor) / len(words)), 'plot': (float(NBplot) / len(words)), 'theme': (float(NBtheme) / len(words)), 'other': (float(NBother) / len(words))}
    maximumNB = max(statsNB.items(), key=operator.itemgetter(1))[0]
    classifierResult.append(maximumNB)
    addToVotes(maximumNB, statsNB.pop(maximumNB), classifierReswithVotes)

    statsLR = {'actor': (float(LRactor) / len(words)), 'plot': (float(LRplot) / len(words)), 'theme': (float(LRtheme) / len(words)), 'other': (float(LRother) / len(words))}
    maximumLR = max(statsLR.items(), key=operator.itemgetter(1))[0]
    classifierResult.append(maximumLR)
    addToVotes(maximumLR, statsLR.pop(maximumLR), classifierReswithVotes)

    statsSVM = {'actor': (float(SVMactor) / len(words)), 'plot': (float(SVMplot) / len(words)), 'theme': (float(SVMtheme) / len(words)), 'other': (float(SVMother) / len(words))}
    maximumSVM = max(statsSVM.items(), key=operator.itemgetter(1))[0]
    classifierResult.append(maximumSVM)
    addToVotes(maximumSVM, statsSVM.pop(maximumSVM), classifierReswithVotes)

    statsRF = {'actor': (float(RFactor) / len(words)), 'plot': (float(RFplot) / len(words)), 'theme': (float(RFtheme) / len(words)), 'other': (float(RFother) / len(words))}
    maximumRF = max(statsRF.items(), key=operator.itemgetter(1))[0]
    classifierResult.append(maximumRF)
    addToVotes(maximumRF, statsRF.pop(maximumRF), classifierReswithVotes)


    statsDT = {'actor': (float(DTactor) / len(words)), 'plot': (float(DTplot) / len(words)), 'theme': (float(DTtheme) / len(words)), 'other': (float(DTother) / len(words))}
    maximumDT = max(statsDT.items(), key=operator.itemgetter(1))[0]
    classifierResult.append(maximumDT)
    addToVotes(maximumDT, statsDT.pop(maximumDT), classifierReswithVotes)

    print(str(classifierResult))

    try:
        normalRes = mode(classifierResult)
    except:
        maxx = max(classifierReswithVotes.items(), key=operator.itemgetter(1))[0]
        normalRes = maxx

    hybrid_classifier = VoteClassifier(NBclassifier, LR_classifier, LSVS_classifier, Random_classifier, decision_classifier)
    print("sentence :" + sentence)
    hybridRes = hybrid_classifier.classifyAll(sentence)

    print("Normal Result", normalRes)
    print("Hybrid Result", hybridRes)

    print("------------------------------------------------------------------------------")

if __name__ == "__main__":
    returnLastValue()