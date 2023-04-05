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
    def extractActors(sentences):
        actors = [ ]
        for sentence in sentences:
            sentenceNlp = helperFunctions.nlp ( sentence )
            actorObj = UserStory.extractActor ( sentence )
            if not any ( obj.name == actorObj.name for obj in actors ):
                actors.append ( actorObj )

        return actors

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
                        """
                        if tok.dep_ == 'prep':  # find the preposition
                            # Traverse the subtree of the preposition to get the entire prepositional phrase
                            prep_tokens = [ t for t in tok.subtree ]
                            prep_phrase = ' '.join ( [ t.text for t in prep_tokens ] )
                            break
                        """
                        if tok.dep_ == "prep" and tok.head.pos_ == "VERB":
                            first_pp = tok.text
                            for child in tok.children:
                                if child.dep_ == "pobj":
                                    first_pp += " " + child.text

                        if tok.dep_ == "prep" and tok.head.pos_ != "VERB":
                            prep2_tokens = [ t for t in tok.subtree ]
                            second_pp = ' '.join ( [ t.text for t in prep2_tokens ] )

        return root_verb, prep_phrase, first_pp, second_pp

    def extractCase(sentence):
        UserStory.extractU ( sentence )
        matcher = Matcher ( helperFunctions.nlp.vocab )
        compoundVerbs = [ ]
        v = sentence.find ( "so that" )
        sentence = sentence [ 0:v ]
        actor = UserStory.extractActor ( sentence )
       #  x = helperFunctions.nlp ( sentence )
       #  # verb det noun ,, verb the noun
       #
       #
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
       #          if span [ 0 ].text == "want" and span [ 1 ].pos_ == "NOUN":
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
       #
       #  pprint ( compoundVerbs )
        compoundVerbs = list ( dict.fromkeys ( compoundVerbs ) )

        return compoundVerbs, actor

    def extractUseCase(sentence):
        #helperFunctions.displayRender(sentence)
        doc=helperFunctions.nlp(sentence)
        actor = UserStory.extractActor ( sentence )
        verb=None
        for sentence in doc.sents:
            #if the root verb is want search for another the xcomp which is next to root.
            if sentence.root.lemma_=="want":
                for tok in doc:
                    if tok.pos_=="VERB" and tok.dep_=="xcomp":
                        verb=tok
                        print ( "sentence xcomp verb", tok.lemma_ )
                        continue
            else :
                print ( "sentence root", sentence.root )
                verb = sentence.root;

            #gets object , and then object dependents
            object=spacy_utils.get_objects_of_verb(verb)
            #if object is founnd , get dependents.
            if object!=None:
                object_dependents = [ token.text for token in object[0].subtree if token.i > object[0].i ]
                print ("object dependents", object_dependents )
                usecase=verb.text+" "+ object[0].text+" " +" ".join(object_dependents)
                print(usecase)

            return usecase,actor
