

class ClassEntity ():

    def __init__(self,className):
        self.className=className
        self.classAttributes=[]
        self.classMethods=[]

    def addAttributeToClass(self, attribute):
        self.classAttributes.append(attribute)

    def addMethodToClass(self, method):
        self.classAttributes.append(method)

