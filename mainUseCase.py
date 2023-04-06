# dont forget to run pip install -r requirements.txt
import os
from pprint import pprint

import spacy.tokens

import UseCase.Actor
import helperFunctions
import plantUML
from UserStory import UserStory

###pipeline
"""
format of user story . As a ..... , i want to , so that   ...... .
0-getting file
1-file preproccessing (detection of line rules . starting of 
    sentence is as and middle word i want to ,so that and full stop .((not done yet))
2-sentence separation . (done)
3-actor detection       (done)
4-use case extraction for each actor. (done)
5-drawing. (done)



"""
# get sentences
file = helperFunctions.getFile ()
sentences = helperFunctions.getSentencesFromFile ( file )
pprint ( sentences )
# reduce sentences
# removes determinants , aux verbs and adjectives.
sentences = helperFunctions.reduceSentences ( sentences )

# get actors .
actorsList = UserStory.extractActors ( sentences )
for actor in actorsList:
    pprint ( actor.name )
actors = [ ]

#for each sentence , get its actor and its use case . and put use case in actor's use case list
for i, sent in enumerate ( sentences ):
    actor=None
    usecasess, actor = UserStory.extractUseCase ( sent )                        ##x is a use case
    # for x in usecasess:
    #     actor.addUseCase(x)


    #if there is an actor saved . then add use case to it . if not append actor object that has use case list in it .
    foundActor = [ actorExtracted for actorExtracted in actors if actor.name == actorExtracted.name ]
    if foundActor.__len__()!= 0:
        index=-1
        for i,act in enumerate(actors):
            if foundActor[0].name == act.name:
                index=i
                break
        actors[index].usecases.append ( actor.usecases )

    else:
        actors.append(actor)

for actor in actors:
    print (actor.name)
    for actorusecase in actor.usecases:
        print(actorusecase)


filename = "other/usecasediagram1111.txt"
filename2 = "other/usecasediagram1111.png"
if os.path.exists ( filename ) and os.path.exists ( filename2 ):
    os.remove ( filename )
    os.remove ( filename2 )
else:
    print ( "The file does not exist" )

os.system ( "pip install plantuml" )
usecasemodel = plantUML.UseCaseModel ( filename )
usecasemodel.addCustomMessage ( "left to right direction" )

for actor in actors:
    #usecasemodel.addActor ( actor.name )
    for i,usecasesobj in enumerate(actor.usecases):
        if usecasesobj!=[]:
            if type(usecasesobj) == list:
                for useCaseObj in usecasesobj:
                    usecasemodel.addUseCase ( useCaseObj )
                    usecasemodel.addUseCasetoActor ( actor.name, useCaseObj )
            else :
                usecasemodel.addUseCase ( usecasesobj )
                usecasemodel.addUseCasetoActor ( actor.name, usecasesobj )
            for key in actor.dependencies.keys():
                if key != None:
                    if actor.usecases[ key ]==usecasesobj:
                        usecasemodel.addUseCase2toUseCase1(usecasesobj,actor.usecases[actor.dependencies [ key ]] )

usecasemodel.closeFile ()
os.system ( "python -m plantuml " + filename )





