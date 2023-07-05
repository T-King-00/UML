###pipeline
"""
format of user story . As a ..... , i want to , so that   ...... .
0-getting file
1-file preproccessing (detection of line rules . starting of
    sentence is as and middle word i want to ,so that and full stop .((not done yet))
2-sentence separation . ()
3-class entities        ()
4-class atributes ()
5-class relation ()
5-drawing. (done)
"""
# ibraries
import os

from spacy.matcher import Matcher

import plantUML
from ClassEntity import ClassEntity
from hellpingFiles.concept import getClassesFromFrequency2
import helperFunctions
import algorithm




if __name__ == '__main__':

    # variables
    file = helperFunctions.getFile ("userStories/text.txt")
    sentences = helperFunctions.getSentencesFromFile ( file )
    sentences = algorithm.preprocess1 ( sentences )

    sentences2 = ' '.join ( sentences )
    print ( sentences2 )

    sentences3 = algorithm.preprocess ( sentences2 )
    print ( sentences3 )
    listOfSentences = sentences3.split ( "." )

    algorithm.stemmingWholeDocument ( listOfSentences )
    algorithm.parsingWholeDocument ( listOfSentences )

    algorithm.generateSentencesFreeFromStopWords ( listOfSentences )
    algorithm.extraction ( listOfSentences )
    algorithm.removingDublicatesSw ()

    print ( "main####" )
    print ( "nouns and verbs:", algorithm.nounsAndVerbs )
    print ( "stopwords found : ", algorithm.stopwordsFound )
    print ( "concepts before :", algorithm.conceptList )

    concepts_Tokens= algorithm.concept ( listOfSentences )

    print ( "conceptList:", algorithm.conceptList )
    print ( "concept tokens:", concepts_Tokens )
    algorithm.findGeneralization ()
    print ( "generalization list :: ", algorithm.generalizationList.items () )
    algorithm.extractClassByRules ()
    getClassesFromFrequency2 ( algorithm.sentencesWithoutSW.values () )

    print ( "concept list : ", algorithm.conceptList )

    algorithm.ExtractAttributes ( sentences2 )
    algorithm.ExtractMethods ( sentences2 )
    print(algorithm.methodsClasses)

    algorithm.ExtractInheritanceR ( sentences2 )
    algorithm.ExtractAggregationR ( sentences2 )
    algorithm.ExtractCompositionR ( sentences2 )



    #creating uml model and rendering picture for output
    filename = "other/classDiagram-1.txt"
    filename2 = "other/classDiagram-1.png"
    if os.path.exists ( filename ) and os.path.exists ( filename2 ):
        os.remove ( filename )
        os.remove ( filename2 )
    else:
        print ( "The file does not exist" )

    os.system ( "pip install plantuml" )
    classModel = plantUML.ClassModel ( filename )


    #adding classes and attributes to model
    for classVar in algorithm.classes:
        classEntity = ClassEntity ( classVar )
        if classEntity.className in algorithm.attributes.keys():
            for x in algorithm.attributes [ classEntity.className ]:
                classEntity.addAttributeToClass ( x )
        classModel.addClass ( classEntity.className )
        for att in classEntity.classAttributes:
            classModel.addMorFtoClass ( classEntity.className, att, '+' )
    for key in algorithm.attributes.keys ():
        if key not in algorithm.classes:
            classModel.addClass ( key )
            for att in algorithm.attributes [ key ]:
                classModel.addMorFtoClass ( key, att, '+' )

    # adding relationshions to model
    for class1 in algorithm.IRelations.keys():
        if class1 not in algorithm.classes:
            classModel.addClass ( class1 )
            for class2 in algorithm.IRelations [ class1 ]:
                classModel.addExtensionRelation ( class1, class2)

    # adding relationshions to model
    for class1 in algorithm.AggRelations.keys ():
        if class1 not in algorithm.classes:
            classModel.addClass ( class1 )
            for class2 in algorithm.AggRelations [ class1 ]:
                classModel.addAggregationRelation ( class1, class2 )
        else:
            for class2 in algorithm.AggRelations [ class1 ]:
                classModel.addAggregationRelation ( class1, class2 )

    classModel.closeFile ()
    os.system ( "python -m plantuml " + filename )























# gives error in calculating
# freq=algorithm.calculate_word_frequencies(algorithm.sentencesWithoutSW)
#
#
# print("freq: ",freq)
# for key in freq.keys():
#     if freq[key]>0.02:
#         print ("    ",key,":  " ,freq[key])
#
#


#  calculating words count and word feq
#
# count=0
# for val in sentencesWithoutSW.keys():
#     count+= len ( sentencesWithoutSW[val ] )
# print(count)


#
# #model part to guess attribute of which class
# model=model()
# model.__int__()
# text.txt="place attribute here "
# result=model.predict(text.txt)
# model.getpredictedclass(result)
"""
def calculate_word_frequencies(sentences):

    # Count the occurrences of each word
    word_counts = Counter (
        doc for doc in sentences )

    # Calculate the total number of words
    total_words = sum ( word_counts.values () )

    # Calculate the frequency of each word
    word_frequencies = {word: count / total_words for word, count in word_counts.items ()}

    print("word fre "+ word_frequencies)
    return word_frequencies
"""