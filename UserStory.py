import re
from pprint import pprint
from textacy.spacier import utils as spacy_utils

from spacy import matcher
from spacy.matcher import Matcher, DependencyMatcher

import helperFunctions
from UseCase.Actor import Actor



class UserStory ():
    def extractActor(sentence):
        actorObj = None
        sentenceNlp = helperFunctions.nlp ( sentence )
        for chunk in sentenceNlp.noun_chunks:

            actorObj = Actor ( chunk.text )
            # remove an or a .
            identifier = actorObj.name.find ( "a " )
            identifier2 = actorObj.name.find ( "an " )
            if identifier >= 0:
                actorObj.name = actorObj.name.replace ( "a ", "" )
            elif identifier2 >= 0:
                actorObj.name = actorObj.name.replace ( "an ", "" )
            # checks in list if there is an actor with same name .
            break
        return actorObj

    # recieves not processed sentences .
    actors=[]
    def extractActors(sentences):
        global actors
        actors=[]
        for sentence in sentences:
            sentenceNlp = helperFunctions.nlp ( sentence )
            actorObj = UserStory.extractActor ( sentence )
            if not any ( obj.name == actorObj.name for obj in actors ):
                actors.append ( actorObj )

        return actors

    #extracts main use case of a sentence
    def extractUseCase(sentence1):
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        print("in extractusecase()")
        global actors
        #helperFunctions.displayRender(sentence)
        doc=helperFunctions.nlp(sentence1)
        actorName = UserStory.extractActor ( sentence1 )
        index = -1
        foundActor = [ actorExtracted for actorExtracted in actors if actorName.name == actorExtracted.name ]
        if foundActor.__len__ () != 0:
            index = -1
            for i, act in enumerate ( actors ):
                if foundActor [ 0 ].name == act.name:
                    index = i
                    break
        verb=None
        usecase=None
        usecases=[]
        for i,sentence in enumerate(doc.sents):
            #if the root verb is want search for another the xcomp which is next to root.
            helperFunctions.printtags(sentence1)
            if sentence.root.lemma_=="want" :
                for tok in doc:
                    if tok.pos_=="VERB" and (tok.dep_=="xcomp" or tok.dep_=="advcl"):
                        verb=tok
                        print ( "sentence xcomp verb", tok.lemma_ )
                        break
            elif sentence.root.is_space==True :
                for tok in doc:
                    if tok.pos_=="VERB" and (tok.dep_=="xcomp" or tok.dep_=="advcl"):
                        if tok.lemma_=="want" or tok.lemma_=="be":
                            continue
                        verb=tok
                        print ( "sentence xcomp verb", tok.lemma_ )
                        break
            else :
                print ( "sentence root", sentence.root )
                verb = sentence.root;


        #gets object , and then object dependents
        object=" "
        if verb!=None:
            object=spacy_utils.get_objects_of_verb(verb)
        #if object is founnd , get dependents.
        if len(object):
            object_dependents = [ token for token in object[0].subtree if token.i > object[0].i ]
            object_dependents_Txt = [ token.text for token in object[0].subtree if token.i > object[0].i ]
            print ("object dependents", object_dependents_Txt )
            if len(object_dependents):
                usecase=verb.text+" "+ object[0].text + ' '+" ".join(object_dependents_Txt)
            else:
                usecase = verb.text + " " + object [ 0 ].text
        else :
            usecase = verb.text
            object_dependents=[]


        print ("usecase is : ", usecase )

        #write if condition for token after verb to see if it aftr or on or of or any other prepositions
            # get verb dependents which can be  another use case .
        usecase2 = UserStory.extractDependencyUseCase ( sentence, verb, object_dependents )
        if usecase2 is not None:
                print ( "usecase2 is : ", usecase2 )
                usecases.append ( usecase2 )
                actors[index].addUseCase ( usecase2 )
                usecases.append ( usecase )
                actors[index].addUseCase ( usecase )
                actors[index].addDependency ( usecase, usecase2 )
        else:
            prepphrase=UserStory.extract_verb_and_prep_phrase(doc)
            if prepphrase!=None and  prepphrase:
                if re.search ( prepphrase, usecase ):
                    usecase = usecase
                else :
                    usecase=usecase +" " + prepphrase

            usecases.append ( usecase )
            actors[index].addUseCase ( usecase )
        return usecases,actors[index]

    def extractDependencyUseCase(sentence, verb, object_dependents):
            # two cases : if there is object dependents , if not .
            if len ( object_dependents ):
                x = object_dependents.pop ()
                verb_dependents = [ token for token in verb.subtree if token.i > verb.i + 1 ]
                verb_dependents_Txt = [ token.text for token in verb.subtree if token.i > verb.i + 1 ]
                print ( "verb_dependents", verb_dependents_Txt )

            else:
                verb_dependents = [ token for token in verb.subtree if token.i > verb.i  ]
                verb_dependents_Txt = [ token.text for token in verb.subtree if token.i > verb.i ]
                print ( "verb_dependents", verb_dependents_Txt )
                WORDS = [ "after", "depend on" ]
                if len(verb_dependents):
                    for i,tok in enumerate(verb_dependents):
                        if verb_dependents [ i ].dep_ == "prep" and verb_dependents [ i ].pos_ == "ADP" and verb_dependents [ i ].lemma_ in WORDS:

                            print ( verb_dependents [ i ].text )
                            dependents = [ token for token in verb.subtree if token.i > verb_dependents [ i ].i ]
                            dependents_txt = [ token.text for token in verb.subtree if token.i > verb_dependents [ i ].i ]
                            dependentsListAfterLem = [ ]
                            for i,tok in  enumerate(dependents):
                                if tok.is_space or tok.text == "." or (tok.text=="so" and dependents[i+1].text=="that"):
                                    continue
                                dependentsListAfterLem.append ( tok.lemma_ )
                            usecase2 = " ".join ( dependentsListAfterLem )
                            print ( usecase2 )
                            return usecase2

                # get what comes after this dependent word .
    def extract_verb_and_prep_phrase(doc):
        root_verb = ''
        prep_phrase = ''
        first_pp = ""
        second_pp = ""
        for i, token in enumerate ( doc ):
            if token.dep_ == 'ROOT':  # find the root verb
                root_verb = token.text
                for k, tok in enumerate ( doc ):
                    if tok.i >= token.i:
                        WORDSDependency=["after","depend on"]
                        if tok.dep_ == 'prep' and tok.pos_=="ADP" and tok.text not in WORDSDependency:  # find the preposition
                            # Traverse the subtree of the preposition to get the entire prepositional phrase
                            prep_tokens = [ t for t in tok.subtree ]
                            prep_phrase = ' '.join ( [ t.text for t in prep_tokens ] )
                            break



        return  prep_phrase


    def extractCase(sentence):
        UserStory.extractU ( sentence )
        matcher = Matcher ( helperFunctions.nlp.vocab )
        compoundVerbs = [ ]
        v = sentence.find ( "so that" )
        sentence = sentence [ 0:v ]
        actor = UserStory.extractActor ( sentence )
       #  x = helperFunctions.nlp ( sentence )
       #  # verb det noun ,, verb the noun
       #  pattern000=[ {"POS": "VERB"}, {"POS": "NOUN"}]
       #  pattern00 =[ {"POS": "VERB"}, {"POS": "NOUN"}, {"POS": "ADP", "OP": "!"}, {"POS": "NOUN", "OP": "!"}]
       #
       #
       #  pattern0 = [ [ {"POS": "VERB"}, {"POS": "DET"}, {"POS": "NOUN"} ],
       #               [ {"POS": "VERB"}, {"POS": "NOUN"}, {"POS": "ADP"}, {"POS": "VERB"}, {"POS": "NOUN"} ]
       #              ]
       #  want_nounPattern = [ {"lower": "want"}, {"POS": "NOUN"}, {"POS": "PART", "OP": "*"},
       #                       {"POS": "VERB"} ]
       #
       #  pattern2 = [ {"POS": "VERB"}, {"POS": "NOUN"}, {"POS": "PART"}, {"POS": "AUX"}, {"POS": "VERB"} ]
       #  pattern3 = [ {"POS": "VERB"}, {"POS": "DET", "OP": "*"}, {"POS": "NOUN"} ]
       #  pattern4 = [ {"POS": "VERB"}, {"POS": "ADP"}, {"POS": "NOUN"} ]
       #  pattern5 = [ {"DEP": "dobj", "POS": "NOUN"}, {"DEP": "amod"}, {"DEP": "prep"}, {"DEP": "pobj"} ]
       #  pattern6 = [ {"DEP": "root"}, {"DEP": "dobj"}, {"DEP": "prep"}, {"POS": "PRON", "OP": "*"},
       #               {"POS": "NOUN", "OP": "+"} ]
       #  pattern1 = [ {"POS": "VERB"}, {"POS": "NOUN"} ]
       #  matcher.add ( "pattern00", [pattern00] )
       #  matcher.add ( "pattern000",  [pattern000])
       # #  matcher.add ( "want_nounPattern", [ want_nounPattern ] )
       # #  matcher.add ( "verbPhrase2", [ pattern2 ] )
       # # # matcher.add ( "verbPhrase3", [ pattern3 ] )
       # #  matcher.add ( "verbPhrase", pattern0 )
       # #  matcher.add ( "verbPhrase4", [ pattern4 ] )
       # #
       # #  matcher.add ( "pattern5", [ pattern5 ] )
       # #  matcher.add ( "pattern6", [ pattern6 ] )
       # #  matcher.add ( "verb-want-noun", [ pattern1 ] )
       #
       #  matches = matcher ( x )
       #  for match_id, start, end in matches:
       #      string_id = helperFunctions.nlp.vocab.strings [ match_id ]  # Get string representation
       #      span = x [ start:end ]  # The matched span
       #      if string_id == "verb-want-noun":
       #          if span [ 0 ].text.txt == "want" and span [ 1 ].pos_ == "NOUN":
       #              continue
       #      if string_id == "verbPhrase2":
       #          verb4 = span [ 4 ].lemma_
       #          nounx = span [ 1 ].lemma_
       #          newSentence = verb4 + " " + nounx
       #          span = newSentence
       #      if span is not None:  #
       #          print(string_id)
       #          compoundVerbs.append ( span )
       #      if span is not None:  # to get only the fist part of use case .
       #          break
       #  pprint ( compoundVerbs )
        compoundVerbs = list ( dict.fromkeys ( compoundVerbs ) )
        return compoundVerbs, actor


