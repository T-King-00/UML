from difflib import SequenceMatcher

import helperFunctions
from helperFunctions import nlp


class Actor ():

    def __init__(self, actorName):
        self.name = actorName
        self.usecases = [ ]
        self.dependencies={}

    def checkSimilarityB2UseCases(self, t1):
        t1tokens = nlp ( t1 )
        print ( "token -> ", t1 )
        isSimilar=False
        for i, x in enumerate ( self.usecases ):
            v = x.find ( t1tokens [ 0 ].text )
            tokens2=helperFunctions.nlp(x)
            if v > -1 :
                if len ( tokens2 ) > len ( t1tokens ) or len(tokens2) < len(t1tokens) :
                    self.usecases [ i ] = x
                    isSimilar= False
                    break
                else:
                    similarity = t1tokens.similarity ( tokens2 )
                    are_similar = similarity > 0.8  # Adjust the threshold as per your requirement
                    print ( are_similar )  # Output: True
                    if are_similar :
                        print ( self.usecases [ i ] )
                        isSimilar= True
                        break
                    else:
                        self.usecases [ i ] = x
                        isSimilar = False
                        break

        """ count = sum(1 for item in bool_list if item) #count of true
                if count> len(t1tokens)/2 :
                        self.usecases [ i ] = x.replace ( x, t1 )
        """
        return isSimilar







    def addUseCase(self, useCase):
        if not self.checkSimilarityB2UseCases ( useCase ):
            self.usecases.append ( useCase )
            print("use case is added to actor ")


    def addDependency(self,r1,r2):
        foundUseCase1index=None
        foundUseCase2index=None
        for i, usecase in enumerate ( self.usecases ):
            if usecase == r1:
                foundUseCase1index =  i
            elif usecase == r2 :
                foundUseCase2index = i
        if foundUseCase1index!= None and foundUseCase2index!=None:
            self.dependencies[foundUseCase1index]=foundUseCase2index


###############################
