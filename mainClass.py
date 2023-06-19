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
from collections import OrderedDict
from pprint import pprint
from multilabelmodel import model
import helperFunctions
from UserStory import UserStory
from other.classRules import Extraction



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
        sentence=helperFunctions.nlp(sentence)
        Extract=Extraction()
        isClass1=Extract.C1( sentence )
        isClass2=Extract.C2( sentence )
        isClass3=Extract.C3( sentence )
        isClass4=Extract.C4( sentence )
        isClass5=Extract.C5( sentence )


        token1, isClass1 = Extract.A1 ( sentence )
        token2, isClass2 = Extract.A2 ( sentence )
        token3, isClass3 = Extract.A3 ( sentence )
        token4, isClass4 = Extract.A4 ( sentence )
        token5, isClass5 = Extract.A5 ( sentence )
        token6, isClass6 = Extract.A6 ( sentence )
        token7, isClass7 = Extract.A7 ( sentence )





    possibleClasses=Extraction.possibleClasses
    possibleClasses=list(dict.fromkeys(possibleClasses))
    print("possible classses ############")

    for classObj in possibleClasses:
        print(classObj)

    possibleAttributes = Extraction.possibleAttributes
    print ( "possible attributes ############" )

    for attObj in     possibleAttributes:
        print(attObj)





#model part to guess attribute of which class
model=model()
model.__int__()
text="place attribute here "
result=model.predict(text)
model.getpredictedclass(result)
