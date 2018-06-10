from nltk.classify import NaiveBayesClassifier
import nltk
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC,LinearSVC
from sklearn.tree import DecisionTreeClassifier
from nltk.classify import ClassifierI
from statistics import mode

class NewClassifier(ClassifierI):
    def __init__(self,*classifiers):
        self._classifiers=classifiers

    def classify(self,features):
        votes=[]
        for c in self._classifiers:
            v=c.classify(features)
            votes.append(v)
        return mode(votes)


def word_feats(words):
    return dict([(word, True) for word in words])




with open('Actor.txt', 'r') as actor:
    data_actor = actor.read().replace(',', ' ')
    actor_vocab = nltk.word_tokenize(data_actor)


with open('Plot.txt','r') as polt:
    data_polt = polt.read().replace(',', ' ')
    polt_vocab = nltk.word_tokenize(data_polt)

with open('Rating.txt','r') as rating:
    data_rating = rating.read().replace(',', ' ')
    rating_vocab = nltk.word_tokenize(data_rating)

with open('Technology.txt','r') as technology:
    data_technology = technology.read().replace(',', ' ')
    technology_vocab = nltk.word_tokenize(data_technology)

with open('Theme.txt','r') as theme:
    data_theme = theme.read().replace(',', ' ')
    theme_vocab = nltk.word_tokenize(data_theme)

with open('Other.txt','r') as other:
    data_other = other.read().replace(',', ' ')
    other_vocab = nltk.word_tokenize(data_other)


actor_features = [(word_feats(act), 'actor') for act in actor_vocab]
polt_features = [(word_feats(pol), 'polt') for pol in polt_vocab]
rating_feature=[(word_feats(rat), 'rating') for rat in rating_vocab]
technology_feature=[(word_feats(tec), 'technology') for tec in technology_vocab]
theme_feature=[(word_feats(the), 'theme') for the in theme_vocab]
other_feature=[(word_feats(ot), 'other') for ot in other_vocab]

train_set = actor_features + polt_features + rating_feature + technology_feature + theme_feature + other_feature

classifier = NaiveBayesClassifier.train(train_set)

classifierSK=SklearnClassifier(LogisticRegression())
classifierSK.train(train_set)

LSVS_classifier=SklearnClassifier(LinearSVC())
LSVS_classifier.train(train_set)

Random_classifier=SklearnClassifier(RandomForestClassifier())
Random_classifier.train(train_set)

# svc_classifier=SklearnClassifier(SVC())
# svc_classifier.train(train_set)

decision_classifier=SklearnClassifier(DecisionTreeClassifier())
decision_classifier.train(train_set)


actor = 0
polt = 0
rating =0
technology =0
theme =0
other =0

sentence = "picture qulity is fantastic "
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


print('NaiveBayes Classifier')
for word in new_words:

    classResult = classifier.classify(word_feats(word))
    print(word,classResult)
    if classResult == 'actor':
        actor = actor + 1
    if classResult == 'polt':
        polt = polt + 1
    if classResult == 'rating':
        rating = rating+ 1
    if classResult == 'technology':
        technology= technology + 1
    if classResult == 'theme':
        theme = theme + 1
    if classResult == 'other':
        other = other + 1

# actor polt rating technology theme other
print('Actor: ' + str(float(actor) / len(words)))
print('Polt: ' + str(float(polt) / len(words)))
print('Rating: ' + str(float(rating) / len(words)))
print('Technology: ' + str(float(technology) / len(words)))
print('Theme: ' + str(float(theme) / len(words)))
print('Other: ' + str(float(other) / len(words)))

print("naive bayes accuracy",(nltk.classify.accuracy(classifier,train_set))*100)


print('-------------------------------------')
print('LogisticRegression Classifier')

actor = 0
polt = 0
rating =0
technology =0
theme =0
other =0



for word in new_words:
    classResultSK = classifierSK.classify(word_feats(word))
    print(word,classResultSK)
    if classResult == 'actor':
        actor = actor + 1
    if classResult == 'polt':
        polt = polt + 1
    if classResult == 'rating':
        rating = rating + 1
    if classResult == 'technology':
        technology = technology + 1
    if classResult == 'theme':
        theme = theme + 1
    if classResult == 'other':
        other = other + 1

# actor polt rating technology theme other
print( 'Actor: ' + str( float( actor ) / len( words ) ) )
print( 'Polt: ' + str( float( polt ) / len( words ) ) )
print( 'Rating: ' + str( float( rating ) / len( words ) ) )
print( 'Technology: ' + str( float( technology ) / len( words ) ) )
print( 'Theme: ' + str( float( theme ) / len( words ) ) )
print( 'Other: ' + str( float( other ) / len( words ) ) )

print("SklearnClassifier accuracy",(nltk.classify.accuracy(classifierSK,train_set))*100)


print('-------------------------------------')
print('LinearSVC Classifier')



actor = 0
polt = 0
rating =0
technology =0
theme =0
other =0



for word in new_words:
    classResultSK = LSVS_classifier.classify(word_feats(word))
    print(word,classResultSK)
    if classResult == 'actor':
        actor = actor + 1
    if classResult == 'polt':
        polt = polt + 1
    if classResult == 'rating':
        rating = rating + 1
    if classResult == 'technology':
        technology = technology + 1
    if classResult == 'theme':
        theme = theme + 1
    if classResult == 'other':
        other = other + 1

# actor polt rating technology theme other
print( 'Actor: ' + str( float( actor ) / len( words ) ) )
print( 'Polt: ' + str( float( polt ) / len( words ) ) )
print( 'Rating: ' + str( float( rating ) / len( words ) ) )
print( 'Technology: ' + str( float( technology ) / len( words ) ) )
print( 'Theme: ' + str( float( theme ) / len( words ) ) )
print( 'Other: ' + str( float( other ) / len( words ) ) )

print("Linear SVC accuracy",(nltk.classify.accuracy(LSVS_classifier,train_set))*100)


print('-------------------------------------')
print('RandomForest Classifier')



actor = 0
polt = 0
rating =0
technology =0
theme =0
other =0



for word in new_words:
    classResultSK = Random_classifier.classify(word_feats(word))
    print(word,classResultSK)
    if classResult == 'actor':
        actor = actor + 1
    if classResult == 'polt':
        polt = polt + 1
    if classResult == 'rating':
        rating = rating + 1
    if classResult == 'technology':
        technology = technology + 1
    if classResult == 'theme':
        theme = theme + 1
    if classResult == 'other':
        other = other + 1

# actor polt rating technology theme other
print( 'Actor: ' + str( float( actor ) / len( words ) ) )
print( 'Polt: ' + str( float( polt ) / len( words ) ) )
print( 'Rating: ' + str( float( rating ) / len( words ) ) )
print( 'Technology: ' + str( float( technology ) / len( words ) ) )
print( 'Theme: ' + str( float( theme ) / len( words ) ) )
print( 'Other: ' + str( float( other ) / len( words ) ) )

print("Random Forest accuracy",(nltk.classify.accuracy(Random_classifier,train_set))*100)



print('-------------------------------------')
print('decision_classifier ')

actor = 0
polt = 0
rating =0
technology =0
theme =0
other =0



for word in new_words:
    classResultSK = decision_classifier.classify(word_feats(word))
    print(word,classResultSK)
    if classResult == 'actor':
        actor = actor + 1
    if classResult == 'polt':
        polt = polt + 1
    if classResult == 'rating':
        rating = rating + 1
    if classResult == 'technology':
        technology = technology + 1
    if classResult == 'theme':
        theme = theme + 1
    if classResult == 'other':
        other = other + 1

# actor polt rating technology theme other
print( 'Actor: ' + str( float( actor ) / len( words ) ) )
print( 'Polt: ' + str( float( polt ) / len( words ) ) )
print( 'Rating: ' + str( float( rating ) / len( words ) ) )
print( 'Technology: ' + str( float( technology ) / len( words ) ) )
print( 'Theme: ' + str( float( theme ) / len( words ) ) )
print( 'Other: ' + str( float( other ) / len( words ) ) )

print("Decission Classifier accuracy",(nltk.classify.accuracy(decision_classifier,train_set))*100)
# classifier classifierSK LSVS_classifier Random_classifier decision_classifier

# new_classifier=NewClassifier(classifier,classifierSK,LSVS_classifier,Random_classifier,decision_classifier)
new_classifier=NewClassifier(Random_classifier,decision_classifier)
print("new classifier accuracy",((nltk.classify.accuracy(new_classifier,train_set))*100))