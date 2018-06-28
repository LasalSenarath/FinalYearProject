import operator
import pypyodbc
from nltk.classify import NaiveBayesClassifier
import nltk
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC,LinearSVC,NuSVC
from sklearn.tree import DecisionTreeClassifier
from nltk.classify import ClassifierI
import re
from statistics import mode, StatisticsError

#last correct Unigrm
class NewClassifier(ClassifierI):
    def __init__(self,*classifiers):
        self._classifiers=classifiers

    def classify(self,features):
        votes=[]
        for c in self._classifiers:

            v=c.classify(features)
            votes.append(v)
        return mode(votes)

    def confidence(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)

        choice_votes = votes.count(mode(votes))
        conf = choice_votes / len(votes)
        return conf




# def word_feats(words):
#   return dict([(word, True) for word in words])
def word_feats(words):
  return dict([(words, True)])

with open('Actor.txt', 'r') as actor:
    data_actor = actor.read().replace(',', ' ')
    actor_vocab = nltk.word_tokenize(data_actor)

with open('Plot.txt','r') as plot:
    data_plot = plot.read().replace(',', ' ')
    plot_vocab = nltk.word_tokenize(data_plot)

with open('Theme.txt','r') as theme:
    data_theme = theme.read().replace(',', ' ')
    theme_vocab = nltk.word_tokenize(data_theme)

actor_features = [(word_feats(act), 'actor') for act in actor_vocab]
plot_features = [(word_feats(plo), 'plot') for plo in plot_vocab]
theme_feature=[(word_feats(the), 'theme') for the in theme_vocab]
# other_feature=[(word_feats(ot), 'other') for ot in other_vocab]


len_of_actor = int(len(actor_features) * 3 / 4)
len_of_plot = int(len(plot_features) * 3 / 4)
len_of_theme = int(len(theme_feature) * 3 / 4)


train_set = actor_features[:len_of_actor] + plot_features[:len_of_plot] + theme_feature[:len_of_theme]
test_set = actor_features[len_of_actor:] + plot_features[len_of_plot:] + theme_feature[len_of_theme:]


#NaiveBayesClassifier
NB_classifier = NaiveBayesClassifier.train(train_set)

#LogisticRegression
LR_classifier=SklearnClassifier(LogisticRegression())
LR_classifier.train(train_set)
#Linear Support Vector Classification
LSV_classifier=SklearnClassifier(LinearSVC())
LSV_classifier.train(train_set)
#RandomForestClassifier
RF_classifier=SklearnClassifier(RandomForestClassifier())
RF_classifier.train(train_set)
#DecisionTreeClassifier
DT_classifier=SklearnClassifier(DecisionTreeClassifier())
DT_classifier.train(train_set)
#Multi-layer Perceptron classifier
# MLP_classifier=SklearnClassifier(MLPClassifier())
# MLP_classifier.train(train_set)
#K Nearest Neighbors Classification
KN_classifier=SklearnClassifier(KNeighborsClassifier())
KN_classifier.train(train_set)

#NewClassifier
# new_classifier=NewClassifier(NB_classifier,LR_classifier,LSV_classifier,RF_classifier,DT_classifier,KN_classifier)
new_classifier=NewClassifier(RF_classifier,DT_classifier,KN_classifier)

# print("NB Accuracy: ",(nltk.classify.accuracy(NB_classifier,test_set))*100)
# print("LR Accuracy: ",(nltk.classify.accuracy(LR_classifier,test_set))*100)
# print("LSV Accuracy: ",(nltk.classify.accuracy(LSV_classifier,test_set))*100)
# print("RF Accuracy: ",(nltk.classify.accuracy(RF_classifier,test_set))*100)
# print("DT Accuracy: ",(nltk.classify.accuracy(DT_classifier,test_set))*100)
# print("KN Accuracy: ",(nltk.classify.accuracy(KN_classifier,test_set))*100)
# print("New Accuracy: ",(nltk.classify.accuracy(new_classifier,test_set))*100)
print("------------------------------------------------------------------------------")
print("NB Accuracy: ",(nltk.classify.accuracy(NB_classifier,train_set))*100)
print("LR Accuracy: ",(nltk.classify.accuracy(LR_classifier,train_set))*100)
print("LSV Accuracy: ",(nltk.classify.accuracy(LSV_classifier,train_set))*100)
print("RF Accuracy: ",(nltk.classify.accuracy(RF_classifier,train_set))*100)
print("DT Accuracy: ",(nltk.classify.accuracy(DT_classifier,train_set))*100)
print("KN Accuracy: ",(nltk.classify.accuracy(KN_classifier,train_set))*100)
# print("New Accuracy: ",(nltk.classify.accuracy(new_classifier,train_set))*100)

actor = 0
plot = 0
theme =0


sentence ="plot is nice"

final_result = re.sub('[\s]+',' ',sentence)
words = final_result.split(' ')
a=re.findall(r'(?<=\s)\$\d+(?=\s)', sentence)
# print(a)

tokenized = nltk.word_tokenize(sentence)
tagged = nltk.pos_tag(tokenized)

# NNPArray1 = ([(word)for word, tag in tagged if tag in ('NN', 'NNP', 'JJ', 'VBZ','VBD','NNS','PDT','PRP')])
# print(NNPArray1)
NNPArray = ([(word)for word, tag in tagged if tag in ('NN', 'NNS', 'NNP', 'JJ', 'JJR', 'JJS','RB', 'VBN')])
# print(NNPArray)

stopwords = ['i']
for stop_word in list(NNPArray):
    if stop_word in stopwords:
        NNPArray.remove(stop_word)
new_words = [stop_word for stop_word in NNPArray if stop_word not in stopwords]+a
# print(new_words)
# print()
# print("---------------lenght---------------")
# print(len(words))
print("=================================================")
print('NaiveBayes Classifier')
for word in new_words:
    NBResult = NB_classifier.classify(word_feats(word))
    # print(word,classResult)
    if NBResult == 'actor':
        actor = actor + 1
    if NBResult == 'plot':
        plot = plot + 1
    if NBResult == 'theme':
        theme = theme + 1

statsNB = {'actor': (float(actor) / len(words)), 'plot': (float(plot) / len(words)), 'theme': (float(theme) / len(words))}
maximumNB = max(statsNB.items(), key=operator.itemgetter(1))[0]
print( maximumNB, statsNB.pop( maximumNB ))

print('--------------------------------------------------------------------------------')
print('LogisticRegression Classifier')
actor = 0
plot = 0
theme =0


for word in new_words:
    LRResult = LR_classifier.classify(word_feats(word))
    # print(word,classResultSK)
    if LRResult == 'actor':
        actor = actor + 1
    if LRResult == 'plot':
        plot = plot + 1
    if LRResult == 'theme':
        theme = theme + 1


statsLR = {'actor': (float(actor) / len(words)), 'plot': (float(plot) / len(words)), 'theme': (float(theme) / len(words))}
maximumLR = max(statsLR.items(), key=operator.itemgetter(1))[0]
print( maximumLR, statsLR.pop( maximumLR ))


print('--------------------------------------------------------------------------------')
print('LinearSVC Classifier')
actor = 0
plot = 0
theme =0


for word in new_words:
    LSVCResult= LSV_classifier.classify(word_feats(word))
    # print(word,classResultSK)
    if LSVCResult == 'actor':
        actor = actor + 1
    if LSVCResult == 'plot':
        plot = plot + 1
    if LSVCResult == 'theme':
        theme = theme + 1
    if LSVCResult == 'other':
        other = other + 1

statsLSVC = {'actor': (float(actor) / len(words)), 'plot': (float(plot) / len(words)), 'theme': (float(theme) / len(words))}
maximumLSVC = max(statsLSVC.items(), key=operator.itemgetter(1))[0]
print( maximumLSVC, statsLSVC.pop( maximumLSVC ))

print('--------------------------------------------------------------------------------')
print('RandomForest Classifier')
actor = 0
plot = 0
theme =0


for word in new_words:
    RFResult = RF_classifier.classify(word_feats(word))
    if RFResult == 'actor':
        actor = actor + 1
    if RFResult == 'plot':
        plot = plot + 1
    if RFResult == 'theme':
        theme = theme + 1


statsRF = {'actor': (float(actor) / len(words)), 'plot': (float(plot) / len(words)), 'theme': (float(theme) / len(words))}
maximumRF = max( statsRF.items(), key=operator.itemgetter( 1 ) )[0]
print( maximumRF, statsRF.pop( maximumLSVC ) )


print('--------------------------------------------------------------------------------')
print('DecisionTree Classifier ')
actor = 0
plot = 0
theme =0

for word in new_words:
    DTResult = DT_classifier.classify(word_feats(word))
    # print(word,classResultSK)
    if DTResult == 'actor':
        actor = actor + 1
    if DTResult == 'plot':
        plot = plot + 1
    if DTResult == 'theme':
        theme = theme + 1

statsDT = {'actor': (float( actor ) / len( words )), 'plot': (float( plot ) / len( words )),'theme': (float( theme ) / len( words ))}
maximumDT = max( statsDT.items(), key=operator.itemgetter( 1 ) )[0]
print('--------------------------------------------------------------------------------')

print('KNearest Neighbors Classifier')
actor = 0
plot = 0
theme =0
for word in new_words:
    KNResult = KN_classifier.classify(word_feats(word))
    # print(word,classResultk_classifier)
    if KNResult=='actor':
        actor=actor + 1
    if KNResult=='plot':
        plot=plot + 1
    if KNResult=='theme':
        theme=theme + 1


statsKN = {'actor': (float( actor ) / len( words )), 'plot': (float( plot ) / len( words )),'theme': (float( theme ) / len( words ))}
maximumKN = max( statsKN.items(), key=operator.itemgetter( 1 ) )[0]
print( maximumKN, statsKN.pop( maximumKN ) )

print('--------------------------------------------------------------------------------')
print('New Classifier')
actor = 0
plot = 0
theme =0

for word in new_words:
    try:
        NewResult = new_classifier.classify(word_feats(word))
        if NewResult=='actor':
            actor = actor + 1
        if NewResult=='plot':
            plot = plot + 1
        if NewResult=='theme':
            theme=theme + 1
    except:
        pass
statsNEW = {'actor': (float( actor ) / len( words )), 'plot': (float( plot ) / len( words )),'theme': (float( theme ) / len( words ))}
maximumNEW = max( statsNEW.items(), key=operator.itemgetter( 1 ) )[0]
print( maximumNEW, statsNEW.pop( maximumNEW ) )

