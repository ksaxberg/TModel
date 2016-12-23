import sys
import numpy as np


if __name__=="__main__":
    #Assumes called like python this.py file.txt .2
    # Where the trailing number is the percentage for stddev
    dev = float(sys.argv[2])
    with open(sys.argv[1]) as f:
        for line in f:
            c1, c2, traffic = line.split(',')
            traffic2 = np.random.normal(float(traffic), dev*float(traffic))
            print("{}".format(', '.join([c1,c2,str(int(round(traffic2)))])))
