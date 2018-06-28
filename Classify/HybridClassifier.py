from nltk.classify import NaiveBayesClassifier
import nltk
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC,LinearSVC
from sklearn.tree import DecisionTreeClassifier
from nltk.classify import ClassifierI
from statistics import mode
import operator

class VoteClassifier(ClassifierI):
    # def __init__(self, *classifiers):
    #     self._classifiers = classifiers
    # classifier,LSVS_classifier,decision_classifier,Random_classifier,classifierSK
    def __init__(self, NB, LR, LSVS, RF, DT):
        self.hybClaswithVotes = {}
        self.NB = NB
        self.LR = LR
        self.LSVS = LSVS
        self.RF = RF
        self.DT = DT

    # def classify(self, features):
    #     votes = []
    #     for c in self._classifiers:
    #         v = c.classify(features)
    #         votes.append(v)
    #         ## what happenes when there are 2 modes?
    #     return mode(votes)
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

    def addToHybridVotes(self, sentiment, vote):
        if self.hybClaswithVotes.get(sentiment) == None:
            self.hybClaswithVotes[sentiment] = vote
        else:
            localMax = max(self.hybClaswithVotes.get(sentiment), vote)
            if localMax != self.hybClaswithVotes.get(sentiment):
                self.hybClaswithVotes[sentiment] = vote



def addToHybridVotes(self, sentiment, vote):
    if self.hybClaswithVotes.get( sentiment ) == None:
        self.hybClaswithVotes[sentiment] = vote
    else:
        localMax = max( self.hybClaswithVotes.get( sentiment ), vote )
        if localMax != self.hybClaswithVotes.get( sentiment ):
            self.hybClaswithVotes[sentiment] = vote


def word_feats(words):
    return dict([(word, True) for word in words])

# def find_features(words):
#     return dict([(word, True) for word in nltk.bigrams(word_tokenize(words))])


with open('Actor.txt', 'r') as actor:
    data_actor = actor.read().replace(',', ' ')
    actor_vocab = nltk.word_tokenize(data_actor)

with open('Plot.txt','r') as polt:
    data_polt = polt.read().replace(',', ' ')
    polt_vocab = nltk.word_tokenize(data_polt)

with open('Theme.txt','r') as theme:
    data_theme = theme.read().replace(',', ' ')
    theme_vocab = nltk.word_tokenize(data_theme)

with open('Other.txt','r') as other:
    data_other = other.read().replace(',', ' ')
    other_vocab = nltk.word_tokenize(data_other)

actor_features = [(word_feats(act), 'actor') for act in actor_vocab]
polt_features = [(word_feats(pol), 'polt') for pol in polt_vocab]
theme_feature=[(word_feats(the), 'theme') for the in theme_vocab]


train_set = actor_features + polt_features + theme_feature
# print(train_set)

NB_classifier = NaiveBayesClassifier.train(train_set)
# print(classifier)

LR_classifier=SklearnClassifier(LogisticRegression())
LR_classifier.train(train_set)

LSV_classifier=SklearnClassifier(LinearSVC())
LSV_classifier.train(train_set)

RF_classifier=SklearnClassifier(RandomForestClassifier())
RF_classifier.train(train_set)

SVC_classifier=SklearnClassifier(SVC())
SVC_classifier.train(train_set)

DT_classifier=SklearnClassifier(DecisionTreeClassifier())
DT_classifier.train(train_set)

actor = 0
polt = 0
theme =0

sentence = "good actor"
sentence = sentence.lower()
words = sentence.split(' ')
tokenized = nltk.word_tokenize(sentence)
tagged = nltk.pos_tag(tokenized)

NNPArray = ([(word)for word, tag in tagged if tag in ('NN', 'NNS', 'NNP', 'JJ', 'JJR', 'JJS','RB', 'VBN')])
print(NNPArray)
stopwords = ['i']
for stop_word in list(NNPArray):
    if stop_word in stopwords:
        NNPArray.remove(stop_word)
new_words = [stop_word for stop_word in NNPArray if stop_word not in stopwords]

for word in new_words:

    NB_classResult = NB_classifier.classify(word_feats(word))
    # print(word,classResult)
    if NB_classResult == 'actor':
        actor = actor + 1
    if NB_classResult == 'polt':
        polt = polt + 1
    if NB_classResult == 'theme':
        theme = theme + 1

print('Actor: ' + str(float(actor) / len(words)))
print('Polt: ' + str(float(polt) / len(words)))
print('Theme: ' + str(float(theme) / len(words)))
print("Naive bayes accuracy",(nltk.classify.accuracy(NB_classifier,train_set))*100)
print('-------------------------------------')
# print('LogisticRegression Classifier')
actor = 0
polt = 0
theme =0

for word in new_words:
    LR_classResult = LR_classifier.classify(word_feats(word))
    # print(word,classResultSK)
    if LR_classResult == 'actor':
        actor = actor + 1
    if LR_classResult == 'polt':
        polt = polt + 1
    if LR_classResult == 'theme':
        theme = theme + 1

# actor polt rating technology theme other
print( 'Actor: ' + str( float( actor ) / len( words ) ) )
print( 'Polt: ' + str( float( polt ) / len( words ) ) )
print( 'Theme: ' + str( float( theme ) / len( words ) ) )

print("LR Classifier accuracy",(nltk.classify.accuracy(LR_classifier,train_set))*100)

print('-------------------------------------')
# print('LinearSV Classifier')

actor = 0
polt = 0
theme =0

for word in new_words:
    classResultLSV= LSV_classifier.classify(word_feats(word))
    # print(word,classResultSK)
    if classResultLSV == 'actor':
        actor = actor + 1
    if classResultLSV == 'polt':
        polt = polt + 1
    if classResultLSV == 'theme':
        theme = theme + 1

print( 'Actor: ' + str( float( actor ) / len( words ) ) )
print( 'Polt: ' + str( float( polt ) / len( words ) ) )
print( 'Theme: ' + str( float( theme ) / len( words ) ) )

print("LSV accuracy",(nltk.classify.accuracy(LSV_classifier,train_set))*100)

print('-------------------------------------')
# print('RandomForest Classifier')

actor = 0
polt = 0
theme =0

for word in new_words:
    classResultRF = RF_classifier.classify(word_feats(word))
    # print(word,classResultSK)
    if classResultRF == 'actor':
        actor = actor + 1
    if classResultRF == 'polt':
        polt = polt + 1
    if classResultRF == 'theme':
        theme = theme + 1
    if classResultRF == 'other':
        other = other + 1

# actor polt rating technology theme other
print( 'Actor: ' + str( float( actor ) / len( words ) ) )
print( 'Polt: ' + str( float( polt ) / len( words ) ) )
print( 'Theme: ' + str( float( theme ) / len( words ) ) )

print("RF accuracy",(nltk.classify.accuracy(RF_classifier,train_set))*100)

print('-------------------------------------')
# print('Decision_classifier ')

actor = 0
polt = 0
theme =0

for word in new_words:
    classResultDT = DT_classifier.classify(word_feats(word))
    # print(word,classResultSK)
    if classResultDT == 'actor':
        actor = actor + 1
    if classResultDT == 'polt':
        polt = polt + 1
    if classResultDT == 'theme':
        theme = theme + 1


# actor polt rating technology theme other
print( 'Actor: ' + str( float( actor ) / len( words ) ) )
print( 'Polt: ' + str( float( polt ) / len( words ) ) )
print( 'Theme: ' + str( float( theme ) / len( words ) ) )

print("DT accuracy",(nltk.classify.accuracy(DT_classifier,train_set))*100)

hybrid_classifier = VoteClassifier(NB_classifier,LR_classifier,LSV_classifier,RF_classifier,DT_classifier)
print("hybrid_classifier accuracy",((nltk.classify.accuracy(hybrid_classifier,train_set))*100))
hybridRes = hybrid_classifier.classifyAll( sentence )