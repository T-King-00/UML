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
import string
from collections import OrderedDict, Counter
from pprint import pprint

from spacy.matcher import Matcher

from hellpingFiles.concept import getClassesFromFrequency
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

    #variables
    file = helperFunctions.getFile ()
    sentences = helperFunctions.getSentencesFromFile ( file )
    sentences=helperFunctions.preprocess(sentences)
    sentences2=' '.join(sentences)


    print(sentences2)
    sentences2=algorithm.preprocess(sentences2)
    print(sentences2)
    listOfSentences=sentences2.split(".")


    algorithm.stemmingWholeDocument(listOfSentences)
    algorithm.parsingWholeDocument(listOfSentences)

    algorithm.generateSentencesFreeFromStopWords(listOfSentences)
    algorithm.extraction(listOfSentences)
    algorithm.removingDublicatesSw()

    print("main####")
    print("nouns and verbs:" , algorithm.nounsAndVerbs)
    print("stopwords found : ",algorithm.stopwordsFound)

    #find concepts from noun phrases
    for nounphrase in algorithm.noun_phrases:
        np=helperFunctions.nlp(nounphrase)
        stringNP=""
        i=0
        for doc in np:
            if not doc.is_stop and not doc.is_space:
                if doc.pos_=="NOUN":
                     stringNP += doc.lemma_.lower()
        algorithm.conceptList.append(stringNP)
        algorithm.conceptList = list ( dict.fromkeys ( algorithm.conceptList ) )

    #to get other forms of noun phrases
    matcher = Matcher ( helperFunctions.nlp.vocab )
    pattern0 = [ {"POS": "NOUN"}, {"POS": "ADP"}, {"POS": "NOUN"}  ]
    matcher.add("noun_det_noun",[pattern0])
    for sent in listOfSentences:
        sentencenlp=helperFunctions.nlp(sent)
        matches = matcher ( sentencenlp )
        for match_id, start, end in matches:
            string_id = helperFunctions.nlp.vocab.strings [ match_id ]  # Get string representation
            span = sentencenlp [ start:end ]  # The matched span
            #add to concept list
            algorithm.conceptList.append ( span.text )
            algorithm.conceptList = list ( dict.fromkeys ( algorithm.conceptList ) )



    print("conceptList:" , algorithm.conceptList)

    algorithm.findGeneralization()
    print("generalization list :: ", algorithm.generalizationList.items())
    getClassesFromFrequency(listOfSentences)
    algorithm.crule2()






    #gives error in calculating
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
