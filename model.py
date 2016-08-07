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

def fromFile(filename):
	with open(filename) as f:
		header = f.readline()[:-1]
	input = header.split(";")[0]
	input = input.split(",")
	output = header.split(";")[1]
	output = output.split(",")
	data = numpy.genfromtxt(filename, delimiter=",", skip_header=1)
	return Model(input, output, data)
