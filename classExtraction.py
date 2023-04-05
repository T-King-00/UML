import re

import numpy
from transformers import pipeline

import helperFunctions
from helperFunctions import isExists


def extractClasses(sentence):
    sentence=helperFunctions.nlp(sentence)
    ruleC1(sentence)
    return possibleClasses

classEntities=[]
possibleClasses=[]

def ruleC1(sentence):
    business_env = [ "database", "record", "system", "information", "organization", "detail", "website", "computer" ]
    global possibleClasses
    skip_next = False
    for i,token in enumerate(sentence):
        #skip actor , which is first noun
        if i==2:
            continue

        # Check if we need to skip the token
        if skip_next:
            skip_next = False
            continue

        if token.pos_=="NOUN":
            if isExists ( token.lemma_, possibleClasses ):
                continue
            if token.pos_ == "NOUN" and token.text not in business_env:
                # Check if the next token is a noun (compound)
                if token.dep_ == "compound":
                    possibleClasses.append ( token.lemma_ + '_' + sentence [ i + 1 ].lemma_ )
                    skip_next = True  # Skip the next token
                # Check if the next token is a gerund
                elif sentence [ i + 1 ].tag_ == "VBG" and  sentence.__len__()!=i+1:
                    possibleClasses.append ( token.lemma_ + '_' + sentence [ i + 1 ].text )
                    skip_next = True  # Skip the next token

                # if the next token is nor a noun nor a gerund, add the token as a class
                else:
                    possibleClasses.append ( token.lemma_ )


            #print("token is a noun ",token.lemma_)
        #     # Check if the token is a gerund
        # elif token.tag_ == "VBG":
        #     if isExists ( token.lemma_, possibleClasses ):
        #         continue
        # # Check if the next token is a noun
        #     if sentence [ i + 1 ].pos_ == "NOUN":
        #         possibleClasses.append ( token.text + '_' + sentence [ i + 1 ].lemma_ )
        #         skip_next = True  # Skip the next token
        if token.dep_=="dobj":
            if isExists ( token.lemma_, possibleClasses ):
                continue
            possibleClasses.append ( token.lemma_ )
    return possibleClasses


def findPossible_ClassFor_Att(att,classesFromFreq,ClassEntities):
    classifier = pipeline ( "zero-shot-classification",model="facebook/bart-large-mnli" )
    #pip install accelerate
    candidate_labels = [ classs for classs in classesFromFreq ]
    for i,c in enumerate(classesFromFreq):
        classesFromFreq[i]=c.title()

    print(candidate_labels)
    result = classifier ( att, candidate_labels=candidate_labels, )
    print(result[ 'labels' ])
    print ( result [ 'scores' ] )
    array = numpy.array ( result [ 'scores' ] )
    max_index_percentage = array.argmax ()
    label=result['labels'][max_index_percentage]
    label=label.title()
    index=classesFromFreq.index(label)
    if not helperFunctions.isExists(att,ClassEntities [ index ].classAttributes):
        if ClassEntities[index].className!=att:
            ClassEntities [ index ].classAttributes.append(att)
            print ( "class:", ClassEntities [ index ].className, " atts : ", ClassEntities [ index ].classAttributes )


def isAttribute(att):
    business_env = [ "people","database", "record", "system", "information", "organization", "detail", "website", "computer" ]

    for tok in att:
        if att in business_env:
            return False
        else:
            return True