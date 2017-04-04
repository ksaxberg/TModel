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


def parseEdges(filename, keys, sumValues=True, addNoise=False, deviation=0):
    """ Parses Edges file into numpy matrix

    Takes an edge-wise file representation of data, and using a keyset
    from population.txt (which must have been parsed first), creates
    a numpy matrix, upper triangular, indexed by those keys.
    The sumValues keyflag allows the user to indicate whether the edgewise
    representation contains duplicates that should be added, sumValues=False,
    or that should be ignored, sumValues=True. Default is True, only the first
    value encountered will be used for each pair.
    Note: No edge-wise pair may have a value of zero

    AddNoise parameter indicates pertubation of the dataset, that the edge
    values will be treated as the average where the std deviation is set 
    as a percentage value, 1 being 100%, of each number. 
    """
    matrix = np.zeros([len(keys), len(keys)])
    with open(filename) as f:
        # Assuming each line is sumValues
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
    return matrix


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
