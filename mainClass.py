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
# ibraries
import os
import pickle
import string
from collections import OrderedDict, Counter
from pprint import pprint

from spacy.matcher import Matcher

import plantUML
from ClassEntity import ClassEntity
from hellpingFiles.concept import getClassesFromFrequency, getClassesFromFrequency2
from multilabelmodel import model
import helperFunctions
from UserStory import UserStory
from other.classRules import Extraction
import algorithm

"""
def calculate_word_frequencies(sentences):

    # Count the occurrences of each word
    word_counts = Counter (
        doc for doc in sentences )

    # Calculate the total number of words
    total_words = sum ( word_counts.values () )

    # Calculate the frequency of each word
    word_frequencies = {word: count / total_words for word, count in word_counts.items ()}

    print("word fre "+ word_frequencies)
    return word_frequencies
"""

if __name__ == '__main__':

    # variables
    file = helperFunctions.getFile ()
    sentences = helperFunctions.getSentencesFromFile ( file )
    sentences = helperFunctions.preprocess ( sentences )

    sentences2 = ' '.join ( sentences )
    print ( sentences2 )

    sentences3 = algorithm.preprocess ( sentences2 )
    print ( sentences3 )
    listOfSentences = sentences3.split ( "." )

    algorithm.stemmingWholeDocument ( listOfSentences )
    algorithm.parsingWholeDocument ( listOfSentences )

    algorithm.generateSentencesFreeFromStopWords ( listOfSentences )
    algorithm.extraction ( listOfSentences )
    algorithm.removingDublicatesSw ()

    print ( "main####" )
    print ( "nouns and verbs:", algorithm.nounsAndVerbs )
    print ( "stopwords found : ", algorithm.stopwordsFound )
    print ( "concepts before :", algorithm.conceptList )
    # storing concepts InFormOftokens
    concepts_Tokens = [ ]
    # find concepts from noun phrases
    i = 0

    for nounphrase in algorithm.noun_phrases:

        np = helperFunctions.nlp ( nounphrase )
        stringNP = ""
        for doc in np:
            if not doc.is_stop and not doc.is_space:
                if (doc.pos_ == "NOUN" or doc.pos_ == "PROPN"):
                    stringNP += doc.lemma_.lower ()
                    concepts_Tokens.append ( doc )

        i = i + 1
        algorithm.conceptList.append ( stringNP )
    # removing duplicates
    algorithm.conceptList = list ( dict.fromkeys ( algorithm.conceptList ) )
    concepts_Tokens = list ( dict.fromkeys ( concepts_Tokens ) )
    print ( "concept tokens ", concepts_Tokens )

    # to get other forms of noun phrases
    matcher = Matcher ( helperFunctions.nlp.vocab )
    pattern0 = [ {"POS": "NOUN"}, {"POS": "ADP"}, {"POS": "NOUN"} ]
    matcher.add ( "noun_det_noun", [ pattern0 ] )
    for sent in listOfSentences:
        sentencenlp = helperFunctions.nlp ( sent )
        matches = matcher ( sentencenlp )
        for match_id, start, end in matches:
            string_id = helperFunctions.nlp.vocab.strings [ match_id ]  # Get string representation
            span = sentencenlp [ start:end ]  # The matched span
            # add to concept list
            algorithm.conceptList.append ( span.text )
            concepts_Tokens.append ( span )

    # removing duplicates
    algorithm.conceptList = list ( dict.fromkeys ( algorithm.conceptList ) )
    concepts_Tokens = list ( dict.fromkeys ( concepts_Tokens ) )

    print ( "conceptList:", algorithm.conceptList )
    print ( "concept tokens:", concepts_Tokens )
    algorithm.findGeneralization ()
    print ( "generalization list :: ", algorithm.generalizationList.items () )
    algorithm.crule2 ()
    getClassesFromFrequency2 ( algorithm.sentencesWithoutSW.values () )

    print ( "concept list : ", algorithm.conceptList )

    algorithm.arules ( sentences2 )

    filename = "other/classDiagram-1.txt"
    filename2 = "other/classDiagram-1.png"
    if os.path.exists ( filename ) and os.path.exists ( filename2 ):
        os.remove ( filename )
        os.remove ( filename2 )
    else:
        print ( "The file does not exist" )

    os.system ( "pip install plantuml" )
    classModel = plantUML.ClassModel ( filename )

    for classVar in algorithm.classes:
        classEntity = ClassEntity ( classVar )
        if classEntity.className in algorithm.attributes.keys():
            for x in algorithm.attributes [ classEntity.className ]:
                classEntity.addAttributeToClass ( x )
        classModel.addClass ( classEntity.className )

        for att in classEntity.classAttributes:
            classModel.addMorFtoClass ( classEntity.className, att, '+' )

    for key in algorithm.attributes.keys ():
        if key not in algorithm.classes:
            classModel.addClass ( key )

            for att in algorithm.attributes [ key ]:
                classModel.addMorFtoClass ( key, att, '+' )

    classModel.closeFile ()
    os.system ( "python -m plantuml " + filename )























# gives error in calculating
# freq=algorithm.calculate_word_frequencies(algorithm.sentencesWithoutSW)
#
#
# print("freq: ",freq)
# for key in freq.keys():
#     if freq[key]>0.02:
#         print ("    ",key,":  " ,freq[key])
#
#


#  calculating words count and word feq
#
# count=0
# for val in sentencesWithoutSW.keys():
#     count+= len ( sentencesWithoutSW[val ] )
# print(count)


#
# #model part to guess attribute of which class
# model=model()
# model.__int__()
# text.txt="place attribute here "
# result=model.predict(text.txt)
# model.getpredictedclass(result)
