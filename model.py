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
		self.selectedVariables = [self.getVariableIndex(i) for i in self.activeVariables[:2]]
		self.selection = []
		self.subscribers = []

	def setActiveVar(self,name):
		#activates variables to be shown in the matrix
		if not name in self.activeVariables:
			self.activeVariables.append(name)

	def setPassiveVar(self,name):
		#deactivates variables to be shown in the matrix
		if name in self.activeVariables:
			self.activeVariables.remove(name)

	def getVariableIndex(self,name):
		#returns final index of given variablename
		if name in self.inputNames:
			return self.inputNames.index(name)
		else:
			if name in self.outputNames:
				return len(self.inputNames) + self.outputNames.index(name)

	def getIndexVariable(self, index):
		#returns variablename ofr given final index
		if index < len(self.inputNames) :
			return self.inputNames[index]
		else :
			return self.outputNames[index - len(self.inputNames)]

	def getSelectedVariables(self):
		#returns list of all activated variables names
		return tuple(self.selectedVariables)
	def setSelectedVariables(self,var1, var2):
		self.selectedVariables = [var1, var2]

	def setSelection(self, indices):
		#sets list of selected datarows for brushing and linking
		self.selection = indices
		for sub in self.subscribers:
			sub.refresh()

	def resetSelection(self):
		#resets list of selected datarows
		self.selection = []
		for sub in self.subscribers:
			sub.refresh()

	def subscribeSelection(self, subscriber):
		#ad to list of all selection subscribers
		self.subscribers.append(subscriber)

def fromFile(filename):
	with open(filename) as f:
		header = f.readline()[:-1]
	input = header.split(";")[0]
	input = input.split(",")
	output = header.split(";")[1]
	output = output.split(",")
	data = numpy.genfromtxt(filename, delimiter=",", skip_header=1)
	return Model(input, output, data)
