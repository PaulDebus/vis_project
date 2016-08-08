import numpy

from stats import Stats


class Model(object):
    def __init__(self, inputNames, outputNames, data):
        self.inputNames = inputNames
        self.outputNames = outputNames
        self.data = data
        self.stats = [Stats(col) for col in data.T]
        self.corrmat = numpy.corrcoef(data.T)
        self.activeVariables = self.inputNames + self.outputNames
        if len(self.activeVariables)>7:
            self.activeVariables=self.activeVariables[:7]
        self.selectedVariables = self.activeVariables[:2]

    def setActiveVar(self,name):
        if not name in self.activeVariables:
            self.activeVariables.append(name)

    def setPassiveVar(self,name):
        if name in self.activeVariables:
            self.activeVariables.remove(name)

    def getVariableIndex(self,name):
        if name in self.inputNames:
            return self.inputNames.index(name)
        else:
            if name in self.outputNames:
                return len(self.inputNames) + self.outputNames.index(name)
    def getIndexVariable(self, index):
        if index < len(self.inputNames) -1:
            return self.inputNames[index]
        else :
            return self.outputNames[index - len(self.inputNames)]

    def getSelectedVariables(self):
        return tuple(self.selectedVariables)
    def setSelectedVariables(self,var1, var2):
        title1 = self.getIndexVariable(var1)
        title2 = self.getIndexVariable(var2)
        self.selectedVariables = [title1, title2]

def fromFile(filename):
    with open(filename) as f:
        header = f.readline()[:-1]
    input = header.split(";")[0]
    input = input.split(",")
    output = header.split(";")[1]
    output = output.split(",")
    data = numpy.genfromtxt(filename, delimiter=",", skip_header=1)
    return Model(input, output, data)
