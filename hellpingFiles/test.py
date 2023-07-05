import numpy as np
import pandas as pd
import spacy
from gensim.corpora import Dictionary
from nltk.corpus import wordnet

from regex import regex
import numpy as np
import pandas as pd
import spacy
import helperFunctions


def findSynonyms(word):

    wordsSynonyms = {}
    wordshyponyms = {}
    # Finding hyponyms and synonym
    hyponyms = [ ]
    synonums = [ ]
    for stn in wordnet.synsets ( word ):
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
        wordsSynonyms [ word ] = synonums
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
        wordshyponyms [ word ] = hyponyms

        # wordes having same meaning

    print ( "synonyms of ", word, wordsSynonyms [ word ] )
    print ( "hypo of ", word, wordshyponyms [ word ] )
    return wordsSynonyms [ word ]

#main function
# main function

if __name__ == '__main__':

    sentence="Details about customer are identifier,first name ,last name , address."
    sentence2="Member want to look up books by title."


    sent=helperFunctions.nlp(sentence)


    for word in sent:
        print(word.text,"  : "  , word.pos_,word.dep_, word.is_stop,"  :  " ,word.tag_,word.ent_type_)
    findSynonyms("composed")
    for x in findSynonyms("composed"):
        x=helperFunctions.nlp(x)
        print(x)



