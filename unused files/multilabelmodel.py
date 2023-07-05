import pickle
import string

import matplotlib.pyplot as plt
from nltk.corpus import stopwords
import re
import pandas as pd
import numpy as np
from sklearn.naive_bayes import GaussianNB, MultinomialNB
from sklearn.metrics import accuracy_score, hamming_loss, f1_score
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from skmultilearn.problem_transform import BinaryRelevance
from skmultilearn.problem_transform import LabelPowerset
import neattext as nt
import neattext.functions as nfx
from skmultilearn.problem_transform import ClassifierChain


class model:
    df=pd.read_csv ( 'data.csv' )
    tfidf = TfidfVectorizer()
    Xfeatures=None
    corpus=None
    model_label_pwoerset=None
    def __int__(self):
        print("-> in constructor of multi label model ")

        self.convertTypes ()
        self.removeNoise ()
        model.Xfeatures = model.tfidf.fit_transform ( model.corpus ).toarray ()
        X_train, X_test, y_train, y_test = self.transform_split ( )
        result,model.model_label_pwoerset = self.build_model ( MultinomialNB (), LabelPowerset, X_train, y_train,
                                                               X_test, y_test )
        print ( model.model_label_pwoerset )
        self.saveModel ()

    def explatoryanalysis(self):

        print (model.df )
        print (  model.df.head () )
        print (  model.df.dtypes )

    def convertTypes(self)     :

        model.df [ 'user' ] =  model.df [ 'user' ].astype ( float )
        model.df [ 'music' ] =  model.df [ 'music' ].astype ( float )
        model.df [ 'employee' ] =  model.df [ 'employee' ].astype ( float )
        model.df [ 'book' ] =  model.df [ 'book' ].astype ( float )
        model.df [ 'website' ] =  model.df [ 'website' ].astype ( float )
        model.df [ 'credit card' ] =  model.df [ 'credit card' ].astype ( float )
        model.df [ 'shopping cart' ] =  model.df [ 'shopping cart' ].astype ( float )
        model.df [ 'patient' ] =  model.df [ 'patient' ].astype ( float )

    def removeNoise(self):

        model.df [ 'attribute' ].apply ( lambda x: nt.TextFrame ( x ).noise_scan () )
        model.corpus =  model.df [ 'attribute' ].apply ( nfx.remove_special_characters )
        return model.corpus

    def transform_split(self):

        y = model.df [ [ 'user', 'music', 'employee', 'book', 'website', 'credit card', 'shopping cart', 'patient' ] ]
        X_train, X_test, y_train, y_test = train_test_split ( model.Xfeatures, y, test_size=0.30, random_state=42 )
        return X_train, X_test, y_train, y_test

    def build_model(self, model, mlb_estimator, xtrain, ytrain, xtest, ytest):
        clf = mlb_estimator ( model )
        clf.fit ( xtrain, ytrain )
        clf_predictions = clf.predict ( xtest )
        acc = accuracy_score ( ytest, clf_predictions )
        f1_sco = f1_score ( ytest, clf_predictions, average='micro' )
        hamloss = hamming_loss ( ytest, clf_predictions )
        result = {"accuracy:": acc, "f1score": f1_sco, "hamming_loss": hamloss}
        return result, clf

    def saveModel(self):
        filename = ('finalized_model.sav')
        pickle.dump ( model.model_label_pwoerset, open ( filename, 'wb' ) )
        # Save the vectorizer
        vec_file = ('vectorizer.sav')
        pickle.dump ( model.tfidf, open ( vec_file, 'wb' ) )

    def predict(self, text):

        vec_example = model.tfidf.transform ( [ text ] )
        result = model.model_label_pwoerset.predict ( vec_example ).toarray ()
        self.getpredictedclass ( result )
        return result

    def getpredictedclass(self,result2):
        if result2 [ 0 ] [ 0 ] == 1:
            print ( "user" )
        if result2 [ 0 ] [ 1 ] == 1:
            print ( "music" )
        if result2 [ 0 ] [ 2 ] == 1:
            print ( "employee" )
        if result2 [ 0 ] [ 3 ] == 1:
            print ( "book" )
        if result2 [ 0 ] [ 4 ] == 1:
            print ( "website" )
        if result2 [ 0 ] [ 5 ] == 1:
            print ( "credit card" )
        if result2 [ 0 ] [ 6 ] == 1:
            print ( "shopping cart" )
        if result2 [ 0 ] [ 7 ] == 1:
            print ( "patient" )
