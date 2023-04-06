class PlantUml ():
    def __init__(self, fileName):
        self.file = open ( fileName, "a" )
        self.file.write ( f""" @startuml \n""" )

    def addCustomMessage(self, msg):
        self.file.write ( f""" {msg} \n""" )

    def closeFile(self):
        self.file.write ( f""" @enduml \n""" )
        self.file.close ()


########################################################
# childclassses
# firstchild
class UseCaseModel ( PlantUml ):
    def __init__(self, fileName):
        super ().__init__ ( fileName )

    def addActor(self, actorName):
        self.file.write ( f""": {actorName}:\n""" )

    def addUseCase(self, useCaseName):
        self.file.write ( f""" usecase "{useCaseName}" \n""" )

    def addUseCasetoActor(self, actorName, useCaseName):
        self.file.write ( f""" :{actorName}: --> ({useCaseName})\n""" )

    def addUseCase2toUseCase1(self, usecase1, usecase2):
        self.file.write ( f""" ({usecase1}) .> ({usecase2}) : include \n""" )

    def addCustomMessage(self, msg):
        super ().addCustomMessage ( msg )

    def closeFile(self):
        super ().closeFile ()


########################################
# Secondchild
class ClassModel ( PlantUml ):
    def __init__(self, fileName):
        super ().__init__ ( fileName )

    ##Declaring classes
    def addClass(self, className):
        self.file.write ( f""" class {className} \n""" )

    def addAClass(self, className):
        self.file.write ( f""" abstract class {className} \n""" )

    def addAbstract(self, abstract):
        self.file.write ( f""" abstract {abstract} \n""" )

    def addAnnotation(self, annotation):
        self.file.write ( f""" annotation {annotation} \n""" )

    def addInterface(self, interfaceName):
        self.file.write ( f""" interface {interfaceName} \n""" )

    def addEnum(self, eNum):
        self.file.write ( f""" enum  {eNum} \n""" )

    def addStruct(self, structName):
        self.file.write ( f""" struct  {structName} \n""" )

    def addCircle(self, structName):
        self.file.write ( f""" struct  {structName} \n""" )

    # Relations between Classes
    def addExtensionRelation(self, Class1, Class2):
        self.file.write ( f""" {Class1} <|-- {Class2} \n""" )

    def addCompositionRelation(self, Class1, Class2):
        self.file.write ( f""" {Class1} *-- {Class2} \n""" )

    def addAggregationRelation(self, Class1, Class2):
        self.file.write ( f""" {Class1} o-- {Class2} \n""" )

    def addDottedRelation(self, Class1, Class2):
        self.file.write ( f""" {Class1} .. {Class2} \n""" )

    def addBinaryRelation(self, Class1, Class2):
        self.file.write ( f""" {Class1} -- {Class2} \n""" )

    def addRealisationRelation(self, Class1, Class2):
        self.file.write ( f""" {Class1} <|.. {Class2} \n""" )

    def addAssociationRelation(self, Class1, Class2):
        self.file.write ( f""" {Class1} --> {Class2} \n""" )

    def addGeneralizationRelation(self, Class1, Class2):
        self.file.write ( f""" {Class1} --|> {Class2} \n""" )

    ##Adding Methods or Fields with visibility
    def addMorFtoClass(self, ClassName, MorFname, visibility='+'):
        if (visibility == '-'):
            self.file.write ( f"""{ClassName} : - {MorFname}\n""" )
            self.file.write ( f"""{ClassName} : + set{MorFname}\n""" )
            self.file.write ( f"""{ClassName} : + get{MorFname}\n""" )
        else:
            self.file.write ( f"""{ClassName} : + {MorFname}\n""" )

    ##Adding association class
    def addAssoClass(self, Class1, Class2, AssoClass):
        self.file.write ( f""" ({Class1}, {Class2}) .. {AssoClass} \n""" )

    #####
    def addCustomMessage(self, msg):
        super ().addCustomMessage ( msg )

    def closeFile(self):
        super ().closeFile ()


"""
@startuml
abstract        abstract            #DONE
class           class               #DONE
abstract class  "abstract class"    #DONE
annotation      annotation          #DONE
circle          circle
()              circle_short_form

diamond         diamond
<>              diamond_short_form
entity          entity
enum            enum                #DONE
exception       exception
interface       interface           #DONE
metaclass       metaclass
protocol        protocol
stereotype      stereotype
struct          struct              #DONE
@enduml
+
relations
"""
