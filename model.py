import numpy

from stats import Stats


class Model(object):
    def __init__(self, inputNames, outputNames, data):
        self.inputNames = inputNames
        self.outputNames = outputNames
        self.data = data
        self.stats = [Stats(col) for col in data.T]
        self.corrmat = numpy.corrcoef(data.T)
        self.activeVariables = self.inputNames + [outputNames[1]]


def fromFile(filename):
    with open(filename) as f:
        header = f.readline()[:-1]
    input = header.split(";")[0]
    input = input.split(",")
    output = header.split(";")[1]
    output = output.split(",")
    data = numpy.genfromtxt(filename, delimiter=",", skip_header=1)
    return Model(input, output, data)
