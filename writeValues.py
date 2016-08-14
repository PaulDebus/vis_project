import numpy


def write(name):
    modname = name.split('.')[0]
    import importlib
    mod = importlib.__import__(modname)
    numSamples = 500
    L = numpy.random.normal(2000, 20, numSamples)
    B = numpy.random.normal(50, 2, numSamples)
    H = numpy.random.normal(100, 2, numSamples)
    X = numpy.random.normal(1000, 300, numSamples)
    P = numpy.random.normal(1000, 500, numSamples)
    E = numpy.random.normal(20000, 2000, numSamples)

    lines = []
    for i in range(numSamples):
        lines.append(mod.run(L[i], B[i], H[i], X[i], P[i], E[i]))

    with open(name, "w") as f:
        f.write(
            "Length, Width, Height, ForceLocation, Force, YoungsModulus; Va, Vb, MaxMoment, Deflection")
        f.write("\n")
        for line in lines:
            f.write(",".join([str(i) for i in line]))
            f.write("\n")
