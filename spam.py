# -*- coding: utf-8 -*-

import pandas as pd

messages = pd.read_csv('/content/SMSSpamCollection', sep ='\t',names=['label','message'])

import re 
import nltk
nltk.download('stopwords')
nltk.download('wordnet')

from nltk.corpus import stopwords 
from nltk.stem import WordNetLemmatizer

lem = WordNetLemmatizer()

lemma = []

for i in range(len(messages)):
    review1 = re.sub('[^a-zA-Z]',' ', messages['message'][i])
    review1 = review1.lower()
    review1 = review1.split()
    review1 = [lem.lemmatize(word) for word in review1 if word not in stopwords.words('english')]
    review1 = ' '.join(review1)
    lemma.append(review1)

from sklearn.feature_extraction.text import TfidfVectorizer
cv = TfidfVectorizer(max_features = 2500)
a = cv.fit_transform(lemma).toarray()

y = pd.get_dummies(messages['label'])
y = y.iloc[:,1].values

from sklearn.model_selection import train_test_split
X_train,X_test,Y_train,Y_test = train_test_split(a,y,test_size = 0.2 ,random_state = 0)

from sklearn.naive_bayes import MultinomialNB
spam_model = MultinomialNB().fit(X_train,Y_train)

pred = spam_model.predict(X_test)

from sklearn.metrics import confusion_matrix
confusion = confusion_matrix(Y_test,pred)

confusion

from sklearn.metrics import accuracy_score
score = accuracy_score(Y_test,pred)

print(score)

