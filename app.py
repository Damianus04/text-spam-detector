from flask import Flask, render_template, url_for, request
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import pandas as pd
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.externals import joblib


app = Flask(__name__)
bootstrap = Bootstrap(app)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/predict', methods=['POST'])
def predict():
    df = pd.read_csv("data/YoutubeSpamMergeddata.csv", encoding='ISO-8859-1')
    df_data = df[["CONTENT", "CLASS"]]
    # Features and Labels
    df_x = df_data['CONTENT']
    df_y = df_data.CLASS
# Extract Feature With CountVectorizer
    corpus = df_x
    cv = CountVectorizer()
    X = cv.fit_transform(corpus)  # Fit the Data
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(
        X, df_y, test_size=0.33, random_state=42)
    # Naive Bayes Classifier
    from sklearn.naive_bayes import MultinomialNB
    clf = MultinomialNB()
    clf.fit(X_train, y_train)
    clf.score(X_test, y_test)
    # Alternative Usage of Saved Model
    # ytb_model = open("naivebayes_spam_model.pkl","rb")
    # clf = joblib.load(ytb_model)

    if request.method == 'POST':
        comment = request.form['comment']
        data = [comment]
        vect = cv.transform(data).toarray()
        my_prediction = clf.predict(vect)
    return render_template('result.html', prediction=my_prediction)


if __name__ == '__main__':
    app.run(debug=True)


# from flask import Flask, render_template, url_for, request
# import pandas as pd
# import pickle
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.naive_bayes import MultinomialNB
# from sklearn.externals import joblib

# app = Flask(__name__)


# @app.route('/')
# def home():
#     return render_template("home.html")


# @app.route('/predict', methods=['POST'])
# def predict():
#     # return render_template("result.html")
#     df = pd.read_csv('data/YoutubeSpamMergeddata.csv', encoding='utf-8')
#     df_data = df[["CONTENT", "CLASS"]]

#     # Features and Labels
#     df_x = df_data['CONTENT']
#     df_y = df_data.CLASS

#     # Extract Feature with CountVectorizer
#     corpus = df_x
#     bow = CountVectorizer()
#     X = bow.fit_transform(corpus)  # fit the Data
#     from sklearn.model_selection import train_test_split
#     X_train, X_test, y_train, y_test = train_test_split(
#         X, df_y, test_size=0.33, random_state=42)

#     # Naive Bayes Classifier
#     from sklearn.naive_bayes import MultinomialNB
#     clf = MultinomialNB()
#     clf.fit(X_train, y_train)
#     clf.score(X_test, y_test)

#     # Alternative Usage of saved model
#     # ytb_model = open('naivebayes_spam_model.pkl', 'rb')
#     # clf = joblib.load(ytb_model)

#     if request.method == 'POST':
#         comment = request.form('comment')
#         data = [comment]
#         vect = bow.transform(data).toarray()
#         my_prediction = clf.predict(vect)
#     return render_template('result.html', prediction=my_prediction)


# if __name__ == '__main__':
#     app.run(debug=True)
