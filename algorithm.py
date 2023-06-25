import regex
from spacy.matcher import matcher
from spacy import matcher
from spacy.matcher import Matcher, DependencyMatcher

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

def preprocess(text):
    if not text.endswith ( "." ):
        text += "."
    doc = helperFunctions.nlp ( text )
    for token in doc:
        # check for compound words
        if token.text == ",":
            text = text.replace ( token.text, " and " )
        if token.dep_ == "compound":
            text = text.replace ( token.text + " " + token.head.text, token.text + "_" + token.head.text )
        # check for gerund followed by a noun
        if token.pos_ == "VERB" and token.tag_ == "VBG" and token.head.pos_ == "NOUN":
            text = text.replace ( token.text + " " + token.head.text, token.text + "_" + token.head.text )
        # check if a noun is followed by a gerund
        if token.pos_ == "NOUN" and token.head.pos_ == "VERB" and token.head.tag_ == "VBG":
            text = text.replace ( token.head.text + " " + token.text, token.head.text + "_" + token.text )
        # check for adjectives followed by a noun
        if token.pos_ == "ADJ" and token.head.pos_ == "NOUN":
            text = text.replace ( token.text + " " + token.head.text, token.text + "_" + token.head.text )
    return text
# step1 remove stop words and save them in a list
# returns list of stop words found after passing one sentence at a time
def getStopWords(sentence):
    global stopwordsFound
    for token in sentence:
        if token.is_stop:
            stopwordsFound.append ( token.lower_ )
    return stopwordsFound


word_frequencies = {}


# concepts : step 2
def calculate_word_frequencies(sentences):
    global word_frequencies
    keys = [ ]
    wordsCountInAllSent = {}
    # Initializing the dictionary with zero values
    for word in conceptList:
        wordsCountInAllSent [ word ] = 0

    for key in sentences.keys ():
        # Count the occurrences of each word
        for word in sentences [ key ]:
            word = helperFunctions.nlp ( word )
            if word.text in sentences.values ():
                wordsCountInAllSent [ word.text ] = wordsCountInAllSent [ word.text ] + 1

    print ( wordsCountInAllSent )
    print ( wordsCountInAllSent.values () )
    # Calculate the frequency of each word
    word_frequencies = {key: wordsCountInAllSent [ key ] / len ( sentences.keys () ) for key in
                        wordsCountInAllSent.keys ()}
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
        if doc.pos_ == "NOUN" or doc.pos_ == "VERB":
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
        sentencesWithoutSW [ i ] = sentenceAfterRemovingSW


nounsAndVerbs = [ ]


# concepts : step 6
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


# concepts : step 7
def extractPhrasesWithoutSW():
    global noun_phrases


#concepts : step 9
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
                stringobj = helperFunctions.nlp ( stringobj )
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
                                    varobj += "_" + doc.lemma_.lower ()
                                else:
                                    varobj += "_" + doc.text.lower ()
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
        for inIndex, ct2 in enumerate ( conceptList ):
            if ct2 == ct1:
                continue
            try:
                if ct2 in wordsSynonyms [ ct1 ]:
                    generalizationList [ ct1 ] = ct2
                    try:
                        if ct1 == generalizationList [ ct2 ]:
                            del generalizationList [ ct1 ]
                    except:
                        print ( "not found key in generalizationList in condition if 2 " )
            except:
                print ( "not found key in words synonyms" )

    print ( "generalization list", len ( generalizationList.items () ) )




# class identification rules
classes=[]


#class extraction rules :
def crule2():
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print("class extraction from concepts:")
    specific_indicators = {"type", "number", "date", "reference","no","code","volume","birth","id","address","name"}
    business_env = ["database", "record", "information", "organization", "detail", "website", "computer"]
    global classes
    classes=conceptList
    for concept in classes:
        if concept in business_env:
            classes.remove(concept)
            continue

        conceptnlp=helperFunctions.nlp(concept)
        for ent in conceptnlp.ents:
            if ent.text in conceptList:
                classes.remove ( ent.text )
                continue
        if concept in specific_indicators:
            classes.remove(concept)
            continue
    for tok in tokens:
            if tok.ent_type_ =="PERSON" or  tok.ent_type_ == "GPE":
                print ( "token text: ", tok.text,", token type:" ,tok.ent_type_ )
                if tok.text.lower() in classes:
                    classes.remove ( tok.text.lower() )

    print(" classes : " , classes)
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")


attributes= {}
def arules(sentences):
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print("in arules():")
    verbsForAttributePattern=["identified","known" , "represented" , "denoted" , "described" ]
    prepsForAttributePattern=["with","by" ]
    global attributes
    matcher = Matcher ( helperFunctions.nlp.vocab )
    sentences = helperFunctions.nlp ( sentences )

    for sentence in sentences.sents:
        #attribute pattern 1 : details about user are .......
        attp1=[ {"LOWER": "details"}, {"POS": "ADP"} , {"POS": "NOUN"},{"POS": "AUX"},{"OP": "+"} ]
        attp2=[ {"LOWER": "details"}, {"POS": "ADP"} , {"POS": "NOUN"},{"POS": "AUX"},{"OP": "+"} ]
        matcher.add ( "attp1", [ attp1 ] )
        matcher.add ( "attp2", [ attp2 ] )
        matches = matcher ( sentence )
        for match_id, start, end in matches:
            string_id = helperFunctions.nlp.vocab.strings [ match_id ]  # Get string representation
            span = sentence [ start:end ]  # The matched span
            atts=[]
            print(string_id)
            for I,token in enumerate(span):
                if string_id=="attp1":
                    if token.pos_=="NOUN" and token.dep_=="pobj":
                        classIs=token.text
                    if token.pos_=="NOUN" and (token.dep_=="attr" or token.dep_=="conj"):
                        atts.append(token.text)
            #remove duplicate
            atts= list ( dict.fromkeys ( atts ) )
            #add attributes to its class
            attributes[classIs]=atts

    print("attributes are :: ",attributes)



    """
    for sentence in sentences.sents:
        for i,word in enumerate(sentence):

            if word.is_sent_start:
                print (word, word.pos_)
                if word.text.lower() in classes:
                    print(f"word  -> {word.text} is in classses list")
            if word.pos_=="VERB" and word.text in verbsForAttributePattern:
                print("verb is in pattern ( true ).", word.text)
                if sentence[i+1].text.lower() in prepsForAttributePattern:
                    print("prep true , " , sentence[i+1].text)
                    if sentence[i+2].is_stop:
                        if sentence[i+3].pos_=="NOUN" or sentence[i+3].pos_=="PROPN":
                            attributes.append ( sentence [ i + 3 ].text )
                    elif sentence[i+2].pos_=="NOUN" or sentence[i+2].pos_=="PROPN":
                        attributes.append(sentence[i+2].text)
                    break
    """












