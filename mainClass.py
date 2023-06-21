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
from collections import OrderedDict, Counter
from pprint import pprint

from hellpingFiles.concept import getClassesFromFrequency
from multilabelmodel import model
import helperFunctions
from UserStory import UserStory
from other.classRules import Extraction
import algorithm

#returns list of stop words found after passing one sentence at a time
def getStopWords(sentence):
    stopwordsFound = [ ]
    for token in sentence:
        if token.is_stop :
            stopwordsFound.append(token.lower_)
    return stopwordsFound

def removeStopWords(sentences):

    sentences=helperFunctions.nlp(sentences)
    for i,sentence in enumerate(sentences):
        token_list = [ ]
        for token in sentence:
            token_list.append ( token.text )
        # Create list of word tokens after removing stopwords
        filtered_sentence = [ ]
        for word in token_list:
            lexeme = helperFunctions.vocab [ word ]
            if lexeme.is_stop == False:
                filtered_sentence.append ( word )
        sentences[i]=filtered_sentence

        print ( filtered_sentence )

        return sentences


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

    #variables
    file = helperFunctions.getFile ()
    sentences = helperFunctions.getSentencesFromFile ( file )
    sentences=helperFunctions.preprocess(sentences)

    algorithm.stemmingWholeDocument(sentences)
    algorithm.parsingWholeDocument(sentences)
    algorithm.generateSentencesFreeFromStopWords(sentences)
    algorithm.extraction(sentences)
    freq=algorithm.calculate_word_frequencies(algorithm.sentencesWithoutSW)
    algorithm.removingDublicatesSw()

    print("main####")

    print("nouns and verbs:" , algorithm.nounsAndVerbs)
    print("noun_phrases:" ,algorithm.noun_phrases)
    print("conceptList:" , algorithm.conceptList)
    print("stopwordsList: ",algorithm.stopwordsList)
    print("freq: ",freq)
    for key in freq.keys():
        if freq[key]>0.02:
            print ("    ",key,":  " ,freq[key])

    print(algorithm.stopwordsFound)

    for nounphrase in algorithm.noun_phrases:
        np=helperFunctions.nlp(nounphrase)
        stringNP=""
        i=0
        for doc in np:
            if not doc.is_stop and not doc.is_space:
                i += 1
                if i == 1:
                    if doc.pos_== "PROPN" or doc.pos_=="NOUN":
                        stringNP += doc.lemma_.lower()
                    else:
                        stringNP += doc.text.lower ()
                else:

                    if doc.pos_ == "PROPN" or doc.pos_=="NOUN":
                        stringNP += "_" + doc.lemma_.lower()
                    else:
                        stringNP += "_" + doc.text.lower()

        algorithm.conceptList.append(stringNP)
        algorithm.conceptList = list ( dict.fromkeys ( algorithm.conceptList ) )

    print("conceptList:" , algorithm.conceptList)

    algorithm.findGeneralization()

    getClassesFromFrequency(sentences)
    algorithm.crule1()







#     #calculating words count and word feq
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
