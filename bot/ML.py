import pickle
import re #регулярные выражения
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

import time
    
import joblib

#DecisionTreeClassifier()
model_pipeline = Pipeline([
    ("vecorizer", TfidfVectorizer(tokenizer = lambda x: _tokenize(x))),
    ("model",     MultinomialNB())
]
)

def _tokenize(word):
    out = []
    for i in range(len(word)):
        out.append(word[i])
        out.append(word[i] + str(i))
    return out




def learn():
    import pickle
    # читаем сохраненные данные
    with open('distance1.data', 'rb') as file:  
    # сохраняем данные как двоичный поток
        data = pickle.load(file)
    corpus = data[0]
    labels = data[1]

    X = corpus
    y = labels
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 42)
    start = time.time()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 42)
    end = time.time()
    duration = round(end - start, 2)
    print("Train-test split: " + str(duration) + " secs")
    start = time.time()
    model_pipeline.fit(X_train, y_train)
    end = time.time()
    duration = round(end - start, 2)
    return "Training: " + str(duration) + " secs"



'''def ML_T92(st):
    filename = 'model.sav'
    model = joblib.load(filename)
    voc = pickle.load(open("tfidf1.pkl", 'rb'))
    tf1_new = TfidfVectorizer(tokenizer = lambda x: _tokenize(x), vocabulary = voc, decode_error="replace")

    X_tf1 = tf1_new.fit_transform(['пчем'])
    pins = st
    pins = re.findall(r'[а-ё]+', pins.lower())
    X_tf1 = tf1_new.fit_transform(pins)
    ree = model.predict(X_tf1)
    answer = ''
    for p in ree:
        answer += str(p) + ' '
    return answer
'''

def ML_T9_line(st):
    pins = st
    pins = re.findall(r'[а-ё]+', pins.lower())
    line = ''
    for pin in pins:
        if len(pin) > 1:
            line += model_pipeline.predict([pin])[0] + ' '
        else:
            line += pin + ' '
    return line
    