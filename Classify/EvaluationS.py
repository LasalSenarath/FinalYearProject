import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB
from nltk.tokenize import word_tokenize
from statistics import mode
from nltk.classify import ClassifierI

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

    def accuracy_predict(predict_MNB, predict_LinSVC, predict_LogR, actual):
        count = 0
        for i in range(len(predict_LinSVC)):
            if ((predict_LinSVC[i] == predict_MNB[i]) or (predict_LogR[i] == predict_LinSVC[i]) or (
                    predict_MNB[i] == predict_LogR[i])):
                voted_predict = mode([predict_LogR[i], predict_MNB[i], predict_LinSVC[i]])
                if voted_predict == actual[i]:
                    count = count + 1
        accuracy = float(count) / len(actual)
        return accuracy

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

# import data from text files
short_Actor = open("Actor.txt", "r").read()
short_Plot = open("Plot.txt", "r").read()
short_Theme= open("Theme.txt", "r").read()

documents = []
all_words = []

# Tag the dataset with relevent data category
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

def accuracy_predict(predict_array, actual, type):
        count = 0
        for i in range(len(predict_array)):
            if predict_array[i] == actual[i]:
                count = count + 1
        accuracy = float(count) / len(predict_array)
        prediction_array[type][1].append(accuracy)
        return accuracy

Accuracy_array = [ ]

prediction_array = [[0 for i in range(2)] for i in range(4)]

prediction_array[0][0] = "MNB"
prediction_array[0][1] = []
prediction_array[1][0] = "LSVC"
prediction_array[1][1] = []
prediction_array[2][0] = "LR"
prediction_array[2][1] = []
prediction_array[3][0] = "vot"
prediction_array[3][1] = []

train = documents[:120] + documents[160:280] + documents[320:440]

act = []
plo = []
the = []


act.append(documents[:120])
plo.append(documents[160:280])
the.append(documents[320:440])

bag_prediction = []
x_train = []
y_train = []
for train_element in train:
    x_train.append(train_element[0])
    y_train.append(train_element[1])

test = documents[120:160] + documents[280:320] + documents[440:]
x_test = []
y_test = []

for test_element in test:
    x_test.append(test_element[0])
    y_test.append(test_element[1])

# Count Vectorizer
count_vector = CountVectorizer()
x_train_cv = count_vector.fit_transform(x_train)
x_test_cv = count_vector.transform(x_test)

actual = np.array(y_test)

# Multinomial Naive Bayes Classifier
multinomialNB_classifier = MultinomialNB()

multinomialNB_classifier.fit(x_train_cv, y_train)
prediction_MNB = multinomialNB_classifier.predict(x_test_cv)

actual = np.array(y_test)

acc_MNB= accuracy_predict(predict_array=prediction_MNB, actual=actual, type=0)

#Linear SVC Classifier
linearSVC_classifier = LinearSVC()
linearSVC_classifier.fit(x_train_cv, y_train)

prediction_LSVC = linearSVC_classifier.predict(x_test_cv)

acc_LSVC = accuracy_predict(predict_array=prediction_LSVC, actual=actual, type=1)

# Logistic Regression Classifier
logisticRegression_classifier = LogisticRegression()

logisticRegression_classifier.fit(x_train_cv, y_train)
prediction_LogR = logisticRegression_classifier.predict(x_test_cv)

acc_LogR = accuracy_predict(predict_array=prediction_LogR, actual=actual, type=2)


# Voted Classifier
voted_accuracy = VoteClassifier.accuracy_predict(predict_MNB=prediction_MNB, predict_LogR=prediction_LogR, predict_LinSVC=prediction_LSVC, actual=actual)

prediction_array[3][1].append(voted_accuracy)

# calculate average accuracy of each classifier
for prediction in prediction_array:
    Accuracy_array.append((prediction[0], np.mean(prediction[1])))
Accuracy_array.sort(key=lambda x: x[1])
print(Accuracy_array)