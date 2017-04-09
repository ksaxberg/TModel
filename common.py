from matplotlib import cm
from matplotlib import colors
from matplotlib import colorbar
from matplotlib import gridspec
from matplotlib import rcParams
from decimal import Decimal
import matplotlib.pyplot as plt
import numpy as np
import math

#### Parameters for manipulation
DEBUG = False
alphaMin = 0.1
alphaMax = 2 
alphaExample = 0.2 
alphaSumExample = 0.2
betaMin = 0.1 
betaMax = 3
betaExample = 1.2 
betaSumExample = 1.6
stepValueAlpha = 0.1
stepValueBeta = 0.1
useGravitySumThresh = True
deleteFromOriginalNetworkSum = False
gravitySumDistThresh = 400 
gravitySumDistThreshMinimum = 0 
#### End


def alphaIterate():
    return np.arange(alphaMin, alphaMax, stepValueAlpha)

def alphaSize():
    return len(alphaIterate())

def betaIterate():
    return np.arange(betaMin, betaMax, stepValueBeta)

def betaSize():
    return len(betaIterate())

def formatScientific(x):
    return "{:.2E}".format(Decimal(x))


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
    #if DEBUG: print("x length: {}\ny length: {}\n".format(len(x), len(y)))
    A = np.vstack([x_values, np.ones(len(x_values))]).T
    slope, intercept = np.linalg.lstsq(A, y_values)[0]
    return slope, intercept


def singleRegression(x, y):
    """
    Runs through a single regression, returning slope, intercept, r2
    """
    #slope, intercept = linRegress(x, y)
    #predicted = [slope*i + intercept for i in x]
    #r2 = rSquared(predicted, y)
    #return slope, intercept, r2
    expForFactor = math.floor(min([math.log(i, 10) for i in x]))
    factor = 1/(10**expForFactor)
    adjust = [factor*i for i in x]
    slope, intercept = linRegress(adjust, y)
    predicted = [slope*i + intercept for i in adjust]
    r2 = rSquared(predicted, y)
    return (slope*factor), intercept, r2


def plotBoth(roadDataList, z, slope, intercept, zSum, slopeSum, interceptSum, name="img", titleString="", rowExampleGravity=[], rowExampleSumGravity=[]):
    """ Makes four countour plots, box plot and saves to the specified filename

    File will be saved into current directory as a png, input matrix z must
    be of the size [xval, yval] as indicated
    """
    #rcParams.update({'font.size': 7, 'xtick.labelsize': 4 })
    rcParams.update({'font.size': 7})

    xval = betaIterate()
    yval = alphaIterate()
    fig = plt.figure(figsize=(10, 10), dpi=200)
    #fig.set_size_inches(5, 5)
    gs = gridspec.GridSpec(4, 4)
    
    #### First Row Option 1: Single large boxplot
    #box1 = fig.add_subplot(gs[0,:])
    #box1.boxplot(roadDataList, 0, 'rs', 0)
    #box1.set_xlabel('Traffic Data Range')
    ####    End 

    #### First Row Option 2: Gravity plot and GravitySums plot
    if not rowExampleGravity:
        raise ValueError("""Plot wants to show Alpha=1, Beta=1 gravity regression
            but regression values not passed in as rowA1B1ofGravity""")
    
    ####  GRAVITY Plot
    scatter = fig.add_subplot(gs[0:2, 0:2])
    m = slope[int(round((alphaExample - alphaMin)/stepValueAlpha))][int(round((betaExample - betaMin)/stepValueBeta))]
    b = intercept[int(round((alphaExample - alphaMin)/stepValueAlpha))][int(round((betaExample - betaMin)/stepValueBeta))]
    predictions = [x*m + b for x in rowExampleGravity]
    predictions_noInt = [x*m for x in rowExampleGravity]
    scatter.scatter(rowExampleGravity, predictions, c='b', marker='x', label="predictions")
    scatter.scatter(rowExampleGravity, predictions_noInt, c='g', marker='+', alpha=0.5, label="predictions without intercept")
    scatter.scatter(rowExampleGravity, roadDataList, c='r', marker='+', alpha=0.3, label="actual") 
    scatter.set_xlabel('Gravity Val input')
    scatter.set_title("Gravity where alpha={}, beta={} \nm={} b={}".format(alphaExample, betaExample,
                      formatScientific(m), formatScientific(b)))
    scatter.set_ylabel('Number of People')
    scatter.legend(loc="upper left", frameon=False)
    ####    End
    ####  GRAVITY SUMS Plot
    scatter = fig.add_subplot(gs[0:2, 2:])
    m = slopeSum[int(round((alphaSumExample - alphaMin)/stepValueAlpha))][int(round((betaSumExample - betaMin)/stepValueBeta))]
    b = interceptSum[int(round((alphaSumExample - alphaMin)/stepValueAlpha))][int(round((betaSumExample - betaMin)/stepValueBeta))]
    predictions = [x*m + b for x in rowExampleSumGravity]
    predictions_noInt = [x*m for x in rowExampleSumGravity]
    scatter.scatter(rowExampleSumGravity, predictions, c='b', marker='x', label="predictions")
    scatter.scatter(rowExampleSumGravity, predictions_noInt, c='g', marker='+', alpha = 0.5, label="predictions without intercept")
    scatter.scatter(rowExampleSumGravity, roadDataList, c='r', marker='+', alpha=0.3, label="actual") 
    scatter.set_xlabel('Gravity Sum Val input')
    scatter.set_title("Gravity Sum where alpha={}, beta={} \nm={} b={}".format(alphaSumExample, betaSumExample,
                      formatScientific(m), formatScientific(b)))
    scatter.set_ylabel('Number of People')
    scatter.legend(loc="upper left", frameon=False)
    ####    End


    # Gravity R Value
    sub1 = fig.add_subplot(gs[2:4, 0:2])
    norm = colors.Normalize(0, 1.01)
    cmap = cm.get_cmap('nipy_spectral', 100)
    # arange of the following is partial setup for colorbar
    CS = sub1.contourf(xval, yval, z, np.arange(0, 1.01, .01),
                     cmap=cmap, norm=norm,  vmin=0, vmax=1.01)
    sub1.set_xlabel('Beta')
    sub1.set_ylabel('Alpha')
    if titleString:
        sub1.set_title(titleString+' R^2 Values')
    plt.colorbar(CS, )

    ######## Gravity intercept LOG
    ### Gravity Intercept
    ##CS = sub2.contourf(xval, yval, intercept, np.arange(0, 10, 0.1),
    ##                 cmap=cmap, norm=norm,  vmin=0, vmax=10)
    ## Gravity Intercept
    #sub2 = fig.add_subplot(gs[2:4,2:])
    #norm = colors.Normalize(0, 10)
    #cmap = cm.get_cmap('nipy_spectral', 100)
    ## arange of the following is partial setup for colorbar
    ##CS = sub2.contourf(xval, yval, intercept, rang,
    ##                 cmap=cmap, norm=norm)
    #CS = sub2.contourf(xval, yval, intercept, 100, cmap=cmap)
    #sub2.set_xlabel('Beta')
    #sub2.set_ylabel('Alpha')
    #if titleString:
    #    sub2.set_title(titleString+' Intercept Values')
    #plt.colorbar(CS, )


    # Gravity Sum R Value
    sub3 = fig.add_subplot(gs[2:4,2:])
    norm = colors.Normalize(0, 1.01)
    cmap = cm.get_cmap('nipy_spectral', 100)
    # arange of the following is partial setup for colorbar
    CS = sub3.contourf(xval, yval, zSum, np.arange(0, 1.01, .01),
                     cmap=cmap, norm=norm,  vmin=0, vmax=1.01)
    sub3.set_xlabel('Beta')
    sub3.set_ylabel('Alpha')
    if titleString:
        sub3.set_title(titleString+' Sum R^2 Values')
    plt.colorbar(CS, )


    ####### Gravity Sum Intercept
    ######sub4 = fig.add_subplot(gs[4:6,2:])
    ######norm = colors.Normalize(0, 10)
    ######cmap = cm.get_cmap('nipy_spectral', 100)
    ######CS = sub4.contourf(xval, yval, interceptSum, np.arange(0, 10, 0.1),
    ######                 cmap=cmap, norm=norm,  vmin=0, vmax=10)
    ## Gravity Sum Intercept
    #sub4 = fig.add_subplot(gs[4:6,2:])
    ## arange of the following is partial setup for colorbar
    #CS = sub4.contourf(xval, yval, interceptSum, 100)
    #sub4.set_xlabel('Beta')
    #sub4.set_ylabel('Alpha')
    #if titleString:
    #    sub4.set_title(titleString+' Sum Intercept Values')
    #plt.colorbar(CS, )

    # Update Change space between subplots, save image
    gs.update(wspace=1, hspace=1)
    if name[-4:] != '.png':
        #fig.savefig(name+'.png', bbox_inches='tight')
        fig.savefig(name+'.png', dpi=900)
    else:
        fig.savefig(name)
