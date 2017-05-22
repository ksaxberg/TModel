import numpy as np
import common


def parseDistance(filename):
    """ Parses Distance file into numpy matrix

    Parses a CSV Matrix from file, assumes no headers
    Returns a numpy matrix. Returns full matrix from file
    """
    with open(filename) as f:
        x = f.readlines()
        matrix = np.zeros([len(x), len(x)])
        # Assuming comma delimited, no lines but distance lines
        for i in range(len(x)):
            temp = x[i].split(',')

            for j in range(len(x)):
                current = temp[j]
                current = float(current.strip())
                matrix[i][j] = current
    return matrix


def parseEdges(filename, keys, sumValues=True, errorBounds=False, addNoise=False, deviation=0):
    """ Parses Edges file into numpy matrix

    Takes an edge-wise file representation of data, and using a keyset
    from population.txt (which must have been parsed first), creates
    a numpy matrix, upper triangular, indexed by those keys.
    The sumValues keyflag allows the user to indicate whether the edgewise
    representation contains duplicates that should be added, sumValues=False,
    or that should be ignored, sumValues=True. Default is True, only the first
    value encountered will be used for each pair.
    Note: No edge-wise pair may have a value of zero

    The parameter errorBounds is meant to indicate a file where the data
    has an error range associated with it, so instead of 3 values on each
    line there are 5, with the last two being the minimum and maximum.
    This is meant to aid visualization, so that the calibrated model appears
    within the limits of the confidence of the data.

    AddNoise parameter indicates pertubation of the dataset, that the edge
    values will be treated as the average where the std deviation is set 
    as a percentage value, 1 being 100%, of each number. 
    """
    matrix = np.zeros([len(keys), len(keys)])
    minMatrix = np.zeros([len(keys), len(keys)])
    maxMatrix = np.zeros([len(keys), len(keys)])
    with open(filename) as f:
        # Assuming each line is sumValues
        if not errorBounds:
            for line in f:
                place1, place2, value = line.strip().split(',')
                ind1 = keys[place1.strip()]
                ind2 = keys[place2.strip()]
                # Make ind1 the smaller, upper triang matrix
                if ind1 > ind2:
                    ind1, ind2 = ind2, ind1
                if not sumValues and matrix[ind1][ind2] == 0:
                    if not addNoise:
                        matrix[ind1][ind2] = float(value.strip())
                    else:
                        matrix[ind1][ind2] = np.random.normal(float(value.strip()), deviation*float(value.strip()))
                elif sumValues:
                    if not addNoise:
                        matrix[ind1][ind2] += float(value.strip())
                    else:
                        matrix[ind1][ind2] += np.random.normal(float(value.strip()), deviation*float(value.strip()))
        else:
            for line in f:
                place1, place2, value, minim, maxim = line.strip().split(',')
                ind1 = keys[place1.strip()]
                ind2 = keys[place2.strip()]
                val = float(value.strip())
                minim = float(minim.strip())
                maxim = float(maxim.strip())
                # Make ind1 the smaller, upper triang matrix
                if ind1 > ind2:
                    ind1, ind2 = ind2, ind1
                if not sumValues and matrix[ind1][ind2] == 0:
                    minMatrix[ind1][ind2] = minim
                    maxMatrix[ind1][ind2] = maxim
                    if not addNoise:
                        matrix[ind1][ind2] = val
                    else:
                        matrix[ind1][ind2] = np.random.normal(val, deviation*val)
                elif sumValues:
                    minMatrix[ind1][ind2] += minim
                    maxMatrix[ind1][ind2] += maxim
                    if not addNoise:
                        matrix[ind1][ind2] += val
                    else:
                        matrix[ind1][ind2] += np.random.normal(val, deviation*val)
            # Check the matrix, if min or max are 0, replace with the value in matrix
            #  as this would mean have 0 error on data (from Ferry set)
            for i in range(len(matrix)):
                for j in range(len(matrix[0])):
                    if matrix[i][j] != 0:
                        if minMatrix[i][j] == 0:
                            minMatrix[i][j] = matrix[i][j]
                        if maxMatrix[i][j] == 0:
                            maxMatrix[i][j] = matrix[i][j]
    if not errorBounds:
        return matrix
    else:
        return matrix, minMatrix, maxMatrix


def makeKeys(filename):
    """ Makes city->index keys for Edge parsing from population.txt file

    Population.txt must be csv, first item is city, second is population.
    This parses the csv into a keylist, allowing for transitioning from
    city names into indexes. Assuming edgewise representation contains
    full match pairs for keys.
    """
    # Assuming working with the population file
    d = {}
    with open(filename) as f:
        for i, line in enumerate(f):
            key = line.strip().split(',')[0].strip()
            d[key] = i
    return d.copy()


def parsePopulation(filename):
    """ Makes a dictionary of city, population pairs in population.txt

    Dictionary is in the form index -> [population, cityname]
    """
    d = {}
    with open(filename) as f:
        for i, line in enumerate(f):
            temp = line.strip().split(',')
            d[i] = [float(temp[1].strip()) , temp[0].strip()]
    return d
