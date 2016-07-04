import numpy


class Stats(object):
    def __init__(self, values):
        self.min = numpy.min(values)
        self.max = numpy.max(values)
        self.mean = numpy.mean(values)
        self.var = numpy.var(values)
        self.std = numpy.std(values)
        self.hist = numpy.histogram(values)
