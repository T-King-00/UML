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
from pprint import pprint

import numpy
from transformers import pipeline

import classExtraction
import helperFunctions
from ClassEntity import ClassEntity
from hellpingFiles import concept



if __name__ == '__main__':
    # get sentences

    #file = helperFunctions.getFileByUrl ( fileURL='https://raw.githubusercontent.com/T-King-00/Gp-AutomationOfBaTasks/tony/university.txt' )
    file = helperFunctions.getFile ()
    sentences = helperFunctions.getSentencesFromFile ( file )

    # removes determinants , aux verbs and adjectives.

    sentencesPreprocessed=helperFunctions.preprocess(sentences)
    sentences1=helperFunctions.reduceSentences(sentences)
    pprint(sentences1)
    classesFromFreq=concept.getClassesFromFrequency ( sentences )

    ClassEntities=[]
    for classs in classesFromFreq:
        classEnt=ClassEntity(classs)
        ClassEntities.append(classEnt)

    pclasses = None

    for i,sentence in enumerate(sentencesPreprocessed):
        v = sentencesPreprocessed [ i].find ( "so that" )
        sentence = sentencesPreprocessed [ i ] [ 0:v ]
        sentence=sentence+ " ."
        attributes = [ ]
        x=sentence
        pclasses=classExtraction.extractClasses(x)

        tokensOffAllSentences=helperFunctions.get_token_sentences(sentences1)
        sentence=helperFunctions.nlp(sentence)
        #print(sentence)
        noun_chunks = list ( sentence.noun_chunks )
        for chunk in noun_chunks:
            if len ( chunk ) == 2 and chunk [ 0 ].pos_ == 'NOUN' and chunk [ 1 ].pos_ == 'NOUN':
                print ( chunk.text )
                try :
                    index=classesFromFreq.index ( chunk [ 0 ].lemma_ )
                    if index!=-1:
                        if not helperFunctions.isExists ( chunk [ 1 ].lemma_, ClassEntities [ index ].classAttributes ):
                            ClassEntities [ index ].classAttributes.append ( chunk [ 1 ].lemma_ )
                except ValueError:
                    continue



        for word in pclasses:
            #if doesnt exits then its an attribute
            if not helperFunctions.isExists(word,classesFromFreq):
                if classExtraction.isAttribute(word):
                    attributes.append(word)
        #if not found in main classes due to frequency . then its an attribute .
        #helperFunctions.displayRender ( x )
        found=None
        #print ( attributes )
        for att in attributes:
             found = False
             for entity in ClassEntities:
                 if  helperFunctions.isExists(att,entity.classAttributes):
                     found=True
             if not found:
                 classExtraction.findPossible_ClassFor_Att ( att, classesFromFreq, ClassEntities )

    for c in ClassEntities:
        print("class name : ", c.className)
        for att in c.classAttributes:
            print ( "atts  : ", att )
        print("############################")




