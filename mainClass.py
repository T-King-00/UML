###pipeline
"""
format of user story . As a ..... , i want to , so that   ...... .
0-getting file
1-file preproccessing (detection of line rules . starting of
    sentence is as and middle word i want to ,so that and full stop .((not done yet))
2-sentence separation . ()
3-class entities        ()
4-class atributes ()
5-class relation ()
5-drawing. (done)
"""
import pickle
from pprint import pprint
from multilabelmodel import model
import numpy
from Cython import typeof
from sklearn.feature_extraction.text import TfidfVectorizer
from transformers import pipeline

import classExtraction
import helperFunctions
from ClassEntity import ClassEntity
from UserStory import UserStory
from hellpingFiles import concept



if __name__ == '__main__':
    # get sentences

    file = helperFunctions.getFile ()
    sentences = helperFunctions.getSentencesFromFile ( file )

    # removes determinants , aux verbs and adjectives.
    sentencesPreprocessed=helperFunctions.preprocess(sentences)
    sentences1=helperFunctions.reduceSentences(sentences)

    pprint(sentences1)

    actors = UserStory.extractActors ( sentences )

    possibleClasses=[]
    possibleAttributes = [ ]

    for i,sentence in enumerate(sentencesPreprocessed):
        v = sentencesPreprocessed [ i].find ( "so that" )
        sentence = sentencesPreprocessed [ i ] [ 0:v ]
        sentence=sentence+ " ."
        print(sentence)
        possibleClassesForOneSentence=classExtraction.extractClasses(sentence)
        for x in possibleClassesForOneSentence:
            possibleClasses.append ( x ) if x not in possibleClasses else None








#model part to guess attribute of which class
model=model()
model.__int__()
text="place attribute here "
result=model.predict(text)
model.getpredictedclass(result)
