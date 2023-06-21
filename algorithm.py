import regex

import helperFunctions

import nltk
from nltk.corpus import wordnet

# sentencesAfterRemovingstopwords
sentencesWithoutSW = {}
stopwordsList = [ ]

tokens = [ ]
conceptList = [ ]
noun_phrases = [ ]

stopwordsFound = [ ]


# step1 remove stop words and save them in a list
# returns list of stop words found after passing one sentence at a time
def getStopWords(sentence):
    global stopwordsFound
    for token in sentence:
        if token.is_stop:
            stopwordsFound.append ( token.lower_ )

    return stopwordsFound

word_frequencies={}
# step 2
def calculate_word_frequencies(sentences):
    global word_frequencies
    keys = [ ]
    wordsCountInAllSent = {}
    # Initializing the dictionary with zero values
    for word in conceptList:
             wordsCountInAllSent [ word ] = 0

    for key in   sentences.keys():
        # Count the occurrences of each word
        for word in sentences[key]:
            word=helperFunctions.nlp(word)
            wordsCountInAllSent [ word.text ] =  wordsCountInAllSent [  word.text ]+1

    print ( wordsCountInAllSent )
    print ( wordsCountInAllSent.values () )
    # Calculate the frequency of each word
    word_frequencies = {key: wordsCountInAllSent [ key ] / len ( sentences.keys() ) for key in wordsCountInAllSent.keys ()}
    return word_frequencies


def stemmingWholeDocument(sentences):
    wordStems = [ ]
    for sent in sentences:
        sent = helperFunctions.nlp ( sent )
        for word in sent:
            wordStems.append ( word.lemma_ )
    return wordStems


def parsingWholeDocument(sentences):
    global tokens
    for sent in sentences:
        sent = helperFunctions.nlp ( sent )

        for word in sent:
            tokens.append ( word )
    return tokens


def extractNounsVerbs(tokens):
    nounsAndVerbs = [ ]
    for doc in tokens:
        # extract proper nouns and verb
        if doc.pos_ == "PROPN" or doc.pos_ == "VERB":
            text = doc.lemma_
            nounsAndVerbs.append ( text.lower () )
    return nounsAndVerbs


# remove duplicates of stopwordslist
def removingDublicatesSw():
    stopwordsList1 = [ ]
    global stopwordsList
    [ stopwordsList1.append ( x ) for x in stopwordsList if x not in stopwordsList1 ]
    stopwordsList = stopwordsList1
    print ( stopwordsList1 )


# removing stop words returning sentencesWithoutSW dictionary
def generateSentencesFreeFromStopWords(sentences):
    global stopwordsList
    for i, sent in enumerate ( sentences ):
        sent = helperFunctions.nlp ( sent )
        stopwordsFound = getStopWords ( sent )

        sentenceAfterRemovingSW = [ ]
        print ( "ORIGINAL SENTENCE " )
        print ( sent.text )

        for obj in sent:
            if obj.lower_ == ".":
                continue
            for word in stopwordsFound:
                if obj.lower_ == word:
                    if obj.lower_ in sentenceAfterRemovingSW:
                        sentenceAfterRemovingSW.remove ( obj.lower_ )
                        stopwordsList.append ( obj.lower_ )
                    break
                if obj.lower_ not in sentenceAfterRemovingSW:
                    sentenceAfterRemovingSW.append ( obj.lower_ )
        # after
        print ( "SENTENCE AFTER REMOVING SW #######" )
        print ( sentenceAfterRemovingSW )
        sentencesWithoutSW [ i ] = sentenceAfterRemovingSW
        print ( "***************************" )


nounsAndVerbs = [ ]


# step 6
def extraction(sentences):
    global conceptList
    global noun_phrases
    global tokens
    global nounsAndVerbs
    # nouns and verbs
    nounsAndVerbs = extractNounsVerbs ( tokens )
    for sentenceObj in sentences:
        objNlp = helperFunctions.nlp ( sentenceObj )
        ##extract noun phrases
        for i, chunk in enumerate ( objNlp.noun_chunks ):
            noun_phrases.append ( chunk.text )

    # remove duplicates
    conceptList = list ( dict.fromkeys ( conceptList ) )
    noun_phrases = list ( dict.fromkeys ( noun_phrases ) )
    return conceptList


# step 7
def extractPhrasesWithoutSW():
    global noun_phrases


# step 9

generalizationList = {}
def findGeneralization():
    wordsSynonyms = {}
    wordshyponyms = {}
    global generalizationList
    # Finding hyponyms and synonyms
    for concept in conceptList:
        hyponyms = [ ]
        synonums = [ ]
        for stn in wordnet.synsets ( concept ):
            for l in stn.lemmas ():
                stringobj = l.name ()
                stringobj=helperFunctions.nlp(stringobj)
                for doc in stringobj:
                    varobj = ""
                    i = 0
                    for o in stringobj:
                        i += 1
                        if len ( o ) > 2:
                            if i == 1:
                                if doc.pos_ == "PROPN":
                                    varobj = doc.lemma_.lower ()
                                else:
                                    varobj = doc.text.lower ()

                            else:
                                if doc.pos_ == "PROPN":
                                    varobj += "_"+doc.lemma_.lower ()
                                else:
                                    varobj +="_"+ doc.text.lower ()
                    synonums.append ( varobj )
            wordsSynonyms [ concept ] = synonums
            for l in stn.hyponyms ():
                stringobj = l.name ()
                stringobj = regex.split ( r'[`\-=~!@#$%^&*()_+\[\]{};\'\\:"|<,./<>?]', stringobj )
                varobj = ""
                i = 0
                for o in stringobj:
                    i += 1
                    if len ( o ) > 2:
                        if i == 1:
                            varobj += o
                        else:
                            varobj += "_" + o

                hyponyms.append ( varobj )
            wordshyponyms [ concept ] = hyponyms

            # wordes having same meaning
    print ( "synonyms of ", conceptList [ 1 ], wordsSynonyms [ conceptList [ 1 ] ] )
    print ( "hypo of ", conceptList [ 1 ], wordshyponyms [ conceptList [ 1 ] ] )



    # words having is a relationship
    for outIndex, ct1 in enumerate ( conceptList ):
        print ( "ct1:", ct1 )
        for inIndex, ct2 in enumerate ( conceptList ):
            print ( "           ct2:",ct2 )
            if ct2 == ct1:
                continue
            try:
                if ct2 in wordsSynonyms[ct1]:
                    generalizationList[ct1]=ct2
            except:
                print("not found key in words synonyms")


    print ( "generalization list", generalizationList )


#class identification rules

def crule1():
    conceptList2=[]
    for nounphrase in noun_phrases:
        np = helperFunctions.nlp ( nounphrase )
        stringNP = ""
        i = 0
        for doc in np:
            if not doc.is_stop and not doc.is_space:
                i += 1
                if i == 1:
                    if doc.pos_ == "PROPN" or doc.pos_ == "NOUN":
                        stringNP += doc.text.lower ()
                    else:
                        stringNP += doc.text.lower ()
                else:

                    if doc.pos_ == "PROPN" or doc.pos_ == "NOUN":
                        stringNP += "_" + doc.text .lower()
                    else:
                        stringNP += "_" + doc.text.lower ()

        conceptList2.append ( stringNP )
        conceptList2 = list ( dict.fromkeys ( conceptList2 ) )


