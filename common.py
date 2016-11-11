from matplotlib import cm
from matplotlib import colors
from matplotlib import colorbar
import matplotlib.pyplot as plt
import numpy as np
import math

alphaMin = 0.1
alphaMax = 2
betaMin = 0.1
betaMax = 1
stepValueAlpha = 0.1
stepValueBeta = stepValueAlpha


def alphaIterate():
    return np.arange(alphaMin, alphaMax, stepValueAlpha)


def betaIterate():
    return np.arange(betaMin, betaMax, stepValueBeta)


def numBetaEntries():
    return int(math.ceil((betaMax-betaMin)/stepValueBeta))


def rSquared(pred, meas):
    """ Calculate r^2 value.

    Calculates r^2 between predicted and measured data values.
    Measured value must be second argument.
    """
    # sum(pred - meas)^2
    # divided by sum(pred - mean)^2
    mean = sum(meas)/len(meas)
    meanError = sum([(meas[i] - mean)**2 for i in range(len(pred))])
    sqrError = sum([(pred[i]-meas[i])**2 for i in range(len(pred))])
    return 1-sqrError/meanError


def linRegress(x, y):
    """ Calculate the regression of x, y

    Uses numpy's linalg.lstsq method to calculate a regression, returning
    slope, intercept
    """
    x_values = np.array(x)
    y_values = np.array(y)
    A = np.vstack([x_values, np.ones(len(x_values))]).T
    slope, intercept = np.linalg.lstsq(A, y_values)[0]
    return slope, intercept


def makePlot(z, name="img", title=""):
    """ Makes a countour plot and saves to the specified filename

    File will be saved into current directory as a png, input matrix z must
    be of the size [xval, yval] as indicated
    """
    xval = betaIterate()
    yval = alphaIterate()
    fig, ax = plt.subplots(1, 1, )
    norm = colors.Normalize(0, 1.01)
    cmap = cm.get_cmap('inferno', 100)
    # arange of the following is partial setup for colorbar
    CS = ax.contourf(xval, yval, z, np.arange(0, 1.01, .01),
                     cmap=cmap, norm=norm,  vmin=0, vmax=1.01)
    ax.set_xlabel('Beta')
    ax.set_ylabel('Alpha')
    if title:
        plt.title(title)
    plt.colorbar(CS,)
    if name[-4:] != '.png':
        fig.savefig(name+'.png', bbox_inches='tight')
    else:
        fig.savefig(name, bbox_inches='tight')
