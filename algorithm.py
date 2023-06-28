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
attributes = {}
IRelations={}


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


# concepts : step 9
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
classes = [ ]


# class extraction rules :
def crule2():
    print ( "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@" )
    print ( "class extraction from concepts:" )
    specific_indicators = {"type", "number", "date", "reference", "no", "code", "volume", "birth", "id", "address",
                           "name"}
    business_env = [ "database", "record", "information", "organization", "detail", "website", "computer" ]
    global classes
    classes = conceptList
    for concept in classes:
        if concept in business_env:
            classes.remove ( concept )
            continue

        conceptnlp = helperFunctions.nlp ( concept )
        for ent in conceptnlp.ents:
            if ent.text in conceptList:
                classes.remove ( ent.text )
                continue
        if concept in specific_indicators:
            classes.remove ( concept )
            continue
    for tok in tokens:
        if tok.ent_type_ == "PERSON" or tok.ent_type_ == "GPE":
            print ( "token text: ", tok.text, ", token type:", tok.ent_type_ )
            if tok.text.lower () in classes:
                classes.remove ( tok.text.lower () )

    print ( " classes : ", classes )
    print ( "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@" )


# extract attributes from previously specified patterns .
def ExtractAttributes(sentences):
    print ( "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@" )
    print ( "in arules():" )
    global attributes
    matcher = Matcher ( helperFunctions.nlp.vocab )
    sentences = helperFunctions.nlp ( sentences )

    verbsForAttributePattern = [ "identified", "known", "represented", "denoted", "described" ]
    prepsForAttributePattern = [ "with", "by" ]
    AUX = [ "are", "is" ]

    # attribute pattern 1 : details about user are .......
    attp1 = [ {"LOWER": "details"}, {"POS": "ADP"}, {"POS": "NOUN"}, {"POS": "AUX", "LOWER": {"IN": AUX}}, {"OP": "+"} ]

    # attribute pattern 2 : A ... is identified with .... , ..... .
    attp2Verbs = [ "identified", "known", "represented", "denoted", "described" ]
    attp2 = [ {"POS": "DET"}, {"POS": "NOUN"}, {"POS": "AUX", "LOWER": {"IN": AUX}},
              {"POS": "VERB", "DEP": "ROOT", "LOWER": {"IN": attp2Verbs}}, {"POS": "ADP"},
              {"OP": "+"} ]

    # attribute pattern 3 : every ...  contains  .... , ..... .
    attp3Verbs = [ "has", "have", "show", "shows", "contain", "contains", "include", "includes" ]
    attp3 = [ {"POS": "DET", "OP": "*"}, {"POS": "NOUN"}, {"POS": "VERB", "DEP": "ROOT", "LOWER": {"IN": attp3Verbs}},
              {"OP": "+"} ]

    # attribute pattern 4 : name is unique WITHIN user .
    uniqueSyn = [ "different", "alone", "unique", "unequaled", "unequalled", "unparalleled", "singular" ]
    attp4 = [ {"POS": "NOUN", "DEP": "nsubj"}, {"POS": "AUX", "LOWER": {"IN": AUX}},
              {"POS": "ADJ", "DEP": "acomp"},
              {"LOWER": "within"}, {"POS": "DET", "OP": "*"},
              {"POS": "NOUN"}
              ]
    # attribute pattern 5 : ... is required for every className
    requiredSyns = [ "required", "necessitate", "asked", "postulated", "needed", "take", "involve", "called",
                     "demanded", "expected", "commanded", "wanted", "needed", "needful", "required", "requisited",
                     "compulsory", "mandatory", "claimed" ]
    attp5 = [ {"POS": "NOUN", "DEP": "nsubjpass "}, {"POS": "AUX", "LOWER": {"IN": AUX}},
              {"POS": "VERB", "DEP": "ROOT", "LOWER": {"IN": requiredSyns}},
              {"POS": "ADP", "LOWER": "for"}, {"POS": "DET", "OP": "*"},
              {"POS": "NOUN", "DEP": "pobj"}
              ]

    matcher.add ( "attp1", [ attp1 ], greedy="LONGEST" )
    matcher.add ( "attp2", [ attp2 ], greedy="LONGEST" )
    matcher.add ( "attp3", [ attp3 ], greedy="LONGEST" )
    matcher.add ( "attp4", [ attp4 ], greedy="LONGEST" )
    matcher.add ( "attp5", [ attp5 ], greedy="LONGEST" )
    for sentence in sentences.sents:

        matches = matcher ( sentence )
        for match_id, start, end in matches:
            string_id = helperFunctions.nlp.vocab.strings [ match_id ]  # Get string representation
            span = sentence [ start:end ]  # The matched span
            atts = [ ]
            classIs = ""
            # print ( string_id )
            skipnext = False
            for I, token in enumerate ( span ):
                if skipnext == True:
                    skipnext = False
                    continue
                if string_id == "attp1":
                    if token.pos_ == "NOUN" and token.dep_ == "pobj":
                        classIs = token.text.lower ()
                    if token.pos_ == "NOUN" and (token.dep_ == "attr" or token.dep_ == "conj"):
                        atts.append ( token.text )
                elif string_id == "attp2":
                    if (token.pos_ == "NOUN" or token.pos_ == "PROPN") and (
                            token.dep_ == "nsubjpass" or token.dep_ == "nsubj"):
                        classIs = token.text.lower ()
                    elif (token.pos_ == "NOUN" or token.pos_ == "PROPN"):
                        compoundnoun = ""
                        if token.dep_ == "compound":
                            if len ( span ) > I + 1:
                                if span [ I + 1 ].pos_ == "NOUN" or span [ I + 1 ].pos_ == "PROPN":
                                    compoundnoun = token.text + "_" + span [ I + 1 ].text
                        if compoundnoun != "":
                            atts.append ( compoundnoun )
                            skipnext = True
                            continue
                        else:
                            atts.append ( token.text )
                elif string_id == "attp3":
                    if token.pos_ == "NOUN" and token.dep_ == "nsubj":
                        classIs = token.text.lower ()
                    if token.pos_ == "NOUN" and (token.dep_ == "dobj" or token.dep_ == "attr" or token.dep_ == "conj"):
                        atts.append ( token.text )
                elif string_id == "attp4":
                    if token.pos_ == "NOUN" and token.dep_ == "nsubj":
                        atts.append ( token.text )
                    if token.pos_ == "NOUN" and (token.dep_ == "dobj" or token.dep_ == "pobj" or token.dep_ == "conj"):
                        classIs = token.text.lower ()
                elif string_id == "attp5":
                    if token.pos_ == "NOUN" and token.dep_ == "nsubjpass ":
                        atts.append ( token.text )
                    if token.pos_ == "NOUN" and (token.dep_ == "dobj" or token.dep_ == "pobj" or token.dep_ == "conj"):
                        classIs = token.text.lower ()

            # remove duplicate
            atts = list ( dict.fromkeys ( atts ) )
            # add attributes to its class
            if classIs != "":
                attributes [ classIs ] = atts

    print ( "attributes are :: ", attributes )

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


# extract inheritance relation from previously specified patterns .
def ExtractInheritanceR(sentences):
    print ( "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@" )
    print ( "in ExtractInheritanceR():" )
    global IRelations


    matcher = Matcher ( helperFunctions.nlp.vocab )
    #patterns
    # inheritance pattern 1 : type of xxxxx  are xxxxxxx
    #uniqueSyn = [ "different", "alone", "unique", "unequaled", "unequalled", "unparalleled", "singular" ]
    AUX = [ "are", "is" ]
    TYPEWORD=["types","type"]
    inherRp1= [ {"POS": "NOUN", "DEP": "nsubj" , "LOWER":{"IN": TYPEWORD }}, {"POS": "ADP","DEP":"prep" },
                {"POS": "NOUN", "DEP": "pobj"},
                {"POS": "AUX", "DEP": "ROOT" , "LOWER":{"IN": AUX}},
                {"OP": "*"}
              ]

    # pattern 2 :  x is a xxx
    inherRp2 = [ {"POS": "NOUN", "DEP": "nsubj"},
                 {"POS": "AUX", "DEP": "ROOT", "LOWER": "is"},
                 {"POS": "DET", "DEP": "det", "LOWER": {"IN": ["a","an"]}},
                 {"POS": "NOUN"}
                 ]

    # pattern 3 :  .... could be a .... or ...
    inherRp3 = [ {"POS": "NOUN", "DEP": "nsubj"},
                 {"POS": "AUX", "DEP": "aux", "LOWER": {"IN": ["may","can","could","might"]}},
                 {"POS": "AUX", "DEP": "ROOT", "LOWER": "be" },
                 {"POS": "DET", "DEP": "det", "LOWER": {"IN": ["a","an"]}},
                 {"POS": "NOUN"},{"OP": "*"}
                ]

    # pattern 4 :  .... is a subclass of ....
    inherRp4 = [ {"POS": "NOUN", "DEP": "nsubj"},
                 {"POS": "AUX", "DEP": "ROOT", "LOWER": "is"},
                 {"POS": "DET", "DEP": "det", "LOWER": "a" },
                 {"LOWER": "subclass" ,"DEP": "compound"},
                 {"POS": "NOUN", "DEP": "attr", "LOWER": "class"},
                 {"POS": "ADP", "DEP": "prep", "LOWER": "of"},
                 {"POS": "NOUN"},
                 {"OP": "*"}
                 ]

    matcher.add("inheritanceRelationPattern1",[inherRp1],greedy="LONGEST")
    matcher.add("inheritanceRelationPattern2",[inherRp2],greedy="LONGEST")
    matcher.add("inheritanceRelationPattern3",[inherRp3],greedy="LONGEST")
    matcher.add("inheritanceRelationPattern4",[inherRp4],greedy="LONGEST")


    sentences = helperFunctions.nlp ( sentences )

    for sentence in sentences.sents:
        matches = matcher ( sentence )
        for match_id, start, end in matches:
            string_id = helperFunctions.nlp.vocab.strings [ match_id ]  # Get string representation
            span = sentence [ start:end ]  # The matched span
            rels = [ ] #relations
            classIs = ""
            # print ( string_id )
            skipnext = False
            for I, token in enumerate ( span ):
                if skipnext == True:
                    skipnext = False
                    continue
                if string_id == "inheritanceRelationPattern1":
                    text=""
                    if token.pos_=="ADJ" and token.dep_=="amod":
                        text = token.text+"_"
                        if span[I+1].pos_ == "NOUN" and (span[I+1].dep_ == "attr" or span[I+1].dep_ == "conj"):
                            text += span[I+1].text
                            rels.append ( text )
                            skipnext=True

                    if token.pos_ == "NOUN" and (token.dep_ == "attr" or token.dep_ == "conj"):
                        rels.append ( token.text )

                    elif token.pos_ == "NOUN" and token.dep_ == "pobj":
                        classIs = token.text.lower ()
                if string_id == "inheritanceRelationPattern2":
                    if token.pos_ == "NOUN" and token.dep_ == "nsubj":
                        rels.append ( token.text.lower() )
                    elif token.pos_ == "NOUN" and (token.dep_ == "attr" or token.dep_ == "conj"):
                        classIs = token.text.lower ()
                if string_id == "inheritanceRelationPattern3":
                    if token.pos_ == "NOUN" and token.dep_ == "nsubj":
                        rels.append ( token.text.lower () )
                    elif token.pos_ == "NOUN" and (token.dep_ == "attr" or token.dep_ == "conj"):
                        classIs = token.text.lower ()
                if string_id == "inheritanceRelationPattern4":
                    if token.pos_ == "NOUN" and token.dep_ == "nsubj":
                        rels.append ( token.text.lower () )
                    elif token.pos_ == "NOUN" and (token.dep_ == "pobj" or token.dep_ == "conj"):
                        classIs = token.text.lower ()

            # remove duplicate
            rels = list ( dict.fromkeys ( rels ) )
            # bind relation to its class
            if classIs != "":
                IRelations [ classIs ] = rels



    print ( "inheritance relations are :: ", IRelations )



