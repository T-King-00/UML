import re

import helperFunctions
from UserStory import UserStory
conceptList = [ ]
noun_phrases = [ ]


def preprocess(sentences):
    for i, sentence in enumerate ( sentences ):
        v = sentences [ i ].find ( "so that" )
        sentences [ i ] = sentences [ i ] [ 0:v ]
        regex = r"[!\"#\$%&\\(\)\*\+,-\./:;<=>\?@\[\\\]\^_`{\|}~”“]"
        # r'[^\w\s]'
        sentences [ i ] = re.sub ( regex, "", sentence )  # Remove punctuation
        # sentences [ i ] = sentence.replace ( '\r\n', '' )  # Remove newline
        print ( sentences [ i ] )

    return sentences


def stemmingAlgorithm(words):
    for i, word in enumerate ( words ):
        doc = helperFunctions.nlp ( word )
        for t in doc:
            words [ i ] = t.lemma_
    return words


def parser(sentences):
    global conceptList
    global noun_phrases
    # nouns
    for sentenceObj in sentences:
        objNlp = helperFunctions.nlp ( sentenceObj )
        for doc in objNlp:
            # extract proper nouns and verb
            if doc.pos_ == "PROPN" or doc.pos_ == "VERB":
                conceptList.append ( doc.lemma_ )
        ##extract noun phrases
        for i, chunk in enumerate ( objNlp.noun_chunks ):
            noun_phrases.append ( chunk.text )
            if i == 0:
                continue;
            if chunk.text not in conceptList:
                conceptList.append ( chunk.text )
            else:
                continue



    # remove dublicates
    conceptList = list ( dict.fromkeys ( conceptList ) )
    noun_phrases = list ( dict.fromkeys ( noun_phrases ) )
    return conceptList


def removestopwords_from_conceptlist():
    global conceptList
    global noun_phrases

    conceptList.append ( [ x for x in noun_phrases ] )
    conceptList = list ( dict.fromkeys ( conceptList ) )


classes = {""}




###  main part
def getClassesFromFrequency(sentences):
    from spacy.lang.en import stop_words as stop_words

    stop_words_found = [ ]
    countOfWords = 0
    stop_words = stop_words.STOP_WORDS
    wordsinDoc = {}
    # find stop words and puntuation marks .
    for i,sentence in enumerate(sentences):
        v = sentences [ i ].find ( "so that" )
        sentences [ i ] = sentences [ i ] [ 0:v ]
        sentence = sentences [ i ] .lower ()
        sentence = helperFunctions.nlp ( sentence )

        for tok in sentence:
            # tok = [ token for token in sentence if not token.is_punct ]
            if tok.is_stop:
                stop_words_found.append ( tok.text )
            else:
                countOfWords = countOfWords + 1
                if tok.lemma_ not in wordsinDoc:
                    wordsinDoc [ tok.lemma_ ] = 0
                wordsinDoc [ tok.lemma_ ] = wordsinDoc [ tok.lemma_ ] + 1
    if stop_words_found is None:
        print ( "is nnone" )
    stop_words_found = list ( dict.fromkeys ( stop_words_found ) )
    print ( stop_words_found )
    print ( wordsinDoc )
    print ( countOfWords )
    frequency = {}
    classFoundFromFreq = [ ]
    for key in wordsinDoc:
        freq = wordsinDoc [ key ] / countOfWords
        WORDSNOTCLASS=["organization","able","date","number","database", "record", "information", "detail", "website", "computer","type", "number", "date", "reference","no","code","volume","birth","id","address","name","list"]
        frequency [ key ] = freq
        if frequency [ key ] >= 0.02:
            keyNlp = helperFunctions.nlp ( key )
            for doc in keyNlp:
                if doc.pos_ != "VERB" and doc.text not in WORDSNOTCLASS:
                    classFoundFromFreq.append ( key )
            print ( frequency [ key ], key )

    frequency = sorted ( frequency.items (), key=lambda x: x [ 1 ] )
    classFoundFromFreq=sorted(classFoundFromFreq)

    #print ( frequency )
    print ( "classes from freq", classFoundFromFreq )
    return classFoundFromFreq
    # wordsAfterLemmaization = stemmingAlgorithm ( list ( wordsinDoc.keys () ) )
    # print ( wordsAfterLemmaization )

    # print ( conceptListVar )

    # pipe = pipeline ( model="facebook/bart-large-mnli" )
    # result = pipe ( "I have a problem with my iphone that needs to be resolved asap!",
    #                 candidate_labels=[ "urgent", "not urgent", "phone", "tablet", "computer" ],
    #                 )
    # print ( result [ "scores" ] )

    ###pipeline
