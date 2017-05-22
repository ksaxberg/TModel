import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib import colors
from matplotlib import colorbar
from matplotlib import gridspec
from matplotlib import rcParams
from decimal import Decimal
import numpy as np
import math

#### Parameters for manipulation
DEBUG = False
alphaMin = 0.1
alphaMax = 2
alphaExample = 0.2
alphaSumExample = 0.6
betaMin = 0.1
betaMax = 3
betaExample = 1.2
betaSumExample = 1.5
stepValueAlpha = 0.1
stepValueBeta = 0.1
useGravitySumThresh = True
deleteFromOriginalNetworkSum = False
gravitySumDistThresh = 300
gravitySumDistThreshMinimum = 0
automaticBestMatch = True
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


def otherOne(pred, meas):
    """ Another measure of fit for the data

    """
    return .9

def otherTwo(pred, meas):
    return .6

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
    expForFactor = math.floor(min([math.log(abs(i), 10) for i in x]))
    factor = 1/(10**expForFactor)
    adjust = [factor*i for i in x]
    slope, intercept = linRegress(adjust, y)
    predicted = [slope*i + intercept for i in adjust]
    r2 = rSquared(predicted, y)
    return (slope*factor), intercept, r2


def singleRegressionPlus(x, y):
    """
    Runs through a single regression, returning slope, intercept, r2
    """
    expForFactor = math.floor(min([math.log(abs(i), 10) for i in x]))
    factor = 1/(10**expForFactor)
    adjust = [factor*i for i in x]
    slope, intercept = linRegress(adjust, y)
    predicted = [slope*i + intercept for i in adjust]
    r2 = rSquared(predicted, y)
    otherValue = otherOne(predicted, y)
    secondOtherValue = otherTwo(predicted, y)
    return (slope*factor), intercept, r2, otherValue, secondOtherValue

def matrixMaximum(matrix):
    """
    Special value R^2, should be between 0 and 1
    """
    maxSoFar = 0
    rowSoFar = 0
    colSoFar = 0
    for i, rows in enumerate(matrix):
        for j, col in enumerate(rows):
            if col > maxSoFar:
                maxSoFar= col
                rowSoFar = i
                colSoFar = j
    return rowSoFar, colSoFar, maxSoFar


def plotBoth(roadDataList, z, otherValues, secondOtherValues, slope, intercept, zSum, otherSumValues, secondOtherSumValues, slopeSum, interceptSum, name="img", titleString="", rowExampleGravity=[], rowExampleSumGravity=[], useRange=False, rangeData=([],[])):
    """ Makes four countour plots, box plot and saves to the specified filename

    File will be saved into current directory as a png, input matrix z must
    be of the size [xval, yval] as indicated
    """
    #rcParams.update({'font.size': 7, 'xtick.labelsize': 4 })
    rcParams.update({'font.size': 7})

    xval = betaIterate()
    yval = alphaIterate()
    fig = plt.figure(figsize=(10, 10), dpi=200)
    #fig = plt.figure(figsize=(10, 15), dpi=300)
    #fig.set_size_inches(5, 5)
    #gs = gridspec.GridSpec(8, 4)
    gs = gridspec.GridSpec(4, 4)

    #### First Row Option 1: Single large boxplot
    #box1 = fig.add_subplot(gs[0,:])
    #box1.boxplot(roadDataList, 0, 'rs', 0)
    #box1.set_xlabel('Traffic Data Range')
    ####    End

    # Some calculations if we are using range
    rowExampleGravity_sorted = []
    rowExampleSumGravity_sorted = []
    minimData_sorted = []
    maximData_sorted = []
    minimData_sum_sorted = []
    maximData_sum_sorted = []
    if useRange:
        minimData = rangeData[0]
        maximData = rangeData[1]
        coll_grav = []
        for i in range(len(rowExampleGravity)):
            coll_grav += [(rowExampleGravity[i], minimData[i], maximData[i])]
        coll_grav_sort = sorted(coll_grav, key=lambda tup: tup[0])
        for x in coll_grav_sort:
            rowExampleGravity_sorted += [x[0]]
            minimData_sorted += [x[1]]
            maximData_sorted += [x[2]]
        #Now gravity sum
        coll_grav_sum = []
        for i in range(len(rowExampleSumGravity)):
            coll_grav_sum += [(rowExampleSumGravity[i], minimData[i], maximData[i])]
        coll_grav_sum_sort = sorted(coll_grav_sum, key=lambda tup: tup[0])
        for x in coll_grav_sum_sort:
            rowExampleSumGravity_sorted += [x[0]]
            minimData_sum_sorted += [x[1]]
            maximData_sum_sorted += [x[2]]
        

    #### First Row Option 2: Gravity plot and GravitySums plot
    if not rowExampleGravity:
        raise ValueError("""Plot wants to show Alpha=1, Beta=1 gravity regression
            but regression values not passed in as rowA1B1ofGravity""")
    if(not automaticBestMatch):
        ####  GRAVITY Plot
        scatter = fig.add_subplot(gs[0:2, 0:2])
        m = slope[int(round((alphaExample - alphaMin)/stepValueAlpha))][int(round((betaExample - betaMin)/stepValueBeta))]
        b = intercept[int(round((alphaExample - alphaMin)/stepValueAlpha))][int(round((betaExample - betaMin)/stepValueBeta))]
        predictions = [x*m + b for x in rowExampleGravity]
        predictions_noInt = [x*m for x in rowExampleGravity]
        scatter.scatter(rowExampleGravity, predictions, c='b', marker='x', label="predictions")
        scatter.scatter(rowExampleGravity, predictions_noInt, c='g', marker='+', alpha=0.5, label="predictions without intercept")
        if not useRange:
            scatter.scatter(rowExampleGravity, roadDataList, c='r', marker='+', alpha=0.3, label="actual")
        else:
            scatter.scatter(rowExampleGravity, roadDataList, c='r', marker='+', alpha=0.3, label="actual")
            scatter.fill_between(rowExampleGravity_sorted, minimData_sorted, maximData_sorted, facecolor='red', alpha=0.1)
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
        if not useRange:
            scatter.scatter(rowExampleSumGravity, roadDataList, c='r', marker='+', alpha=0.3, label="actual")
        else:
            scatter.scatter(rowExampleSumGravity, roadDataList, c='r', marker='+', alpha=0.3, label="actual")
            scatter.fill_between(rowExampleSumGravity_sorted, minimData_sum_sorted, maximData_sum_sorted, facecolor='red', alpha=0.1)
        scatter.set_xlabel('Gravity Sum Val input')
        scatter.set_title("Gravity Sum where alpha={}, beta={} \nm={} b={}".format(alphaSumExample, betaSumExample,
                          formatScientific(m), formatScientific(b)))
        scatter.set_ylabel('Number of People')
        scatter.legend(loc="upper left", frameon=False)
        ####    End
    else:
        ####  GRAVITY Plot
        scatter = fig.add_subplot(gs[0:2, 0:2])
        alphaBestInd, betaBestInd, bestR2 = matrixMaximum(z)
        alphaInd = alphaBestInd*stepValueAlpha - alphaMin
        betaInd = betaBestInd*stepValueBeta - betaMin
        m = slope[alphaBestInd][betaBestInd]
        b = intercept[alphaBestInd][betaBestInd]
        predictions = [x*m + b for x in rowExampleGravity]
        predictions_noInt = [x*m for x in rowExampleGravity]
        scatter.scatter(rowExampleGravity, predictions, c='b', marker='x', label="predictions")
        scatter.scatter(rowExampleGravity, predictions_noInt, c='g', marker='+', alpha=0.5, label="predictions without intercept")
        if not useRange:
            scatter.scatter(rowExampleGravity, roadDataList, c='r', marker='+', alpha=0.3, label="actual")
        else:
            scatter.scatter(rowExampleGravity, roadDataList, c='r', marker='+', alpha=0.3, label="actual")
            scatter.fill_between(rowExampleGravity_sorted, minimData_sorted, maximData_sorted, facecolor='red', alpha=0.1)
        scatter.set_xlabel('Gravity Val input')
        scatter.set_title("Best Gravity was r2={:.3f} at alpha={}, beta={} \nm={} b={}".format(bestR2, alphaInd, betaInd,
                          formatScientific(m), formatScientific(b)))
        scatter.set_ylabel('Number of People')
        scatter.legend(loc="upper left", frameon=False)
        ####    End
        ####  GRAVITY SUMS Plot
        scatter = fig.add_subplot(gs[0:2, 2:])
        alphaSumsBestInd, betaSumsBestInd, bestSumR2 = matrixMaximum(zSum)
        alphaInd = alphaSumsBestInd*stepValueAlpha - alphaMin
        betaInd = betaSumsBestInd*stepValueBeta - betaMin
        m = slopeSum[alphaSumsBestInd][betaSumsBestInd]
        b = interceptSum[alphaSumsBestInd][betaSumsBestInd]
        predictions = [x*m + b for x in rowExampleSumGravity]
        predictions_noInt = [x*m for x in rowExampleSumGravity]
        scatter.scatter(rowExampleSumGravity, predictions, c='b', marker='x', label="predictions")
        scatter.scatter(rowExampleSumGravity, predictions_noInt, c='g', marker='+', alpha = 0.5, label="predictions without intercept")
        if not useRange:
            scatter.scatter(rowExampleSumGravity, roadDataList, c='r', marker='+', alpha=0.3, label="actual")
        else:
            scatter.scatter(rowExampleSumGravity, roadDataList, c='r', marker='+', alpha=0.3, label="actual")
            scatter.fill_between(rowExampleSumGravity_sorted, minimData_sum_sorted, maximData_sum_sorted, facecolor='red', alpha=0.1)
        scatter.set_xlabel('Gravity Sum Val input')
        scatter.set_title("Best Gravity Sum was r2={:.3f} at alpha={}, beta={} \nm={} b={}".format(bestSumR2, alphaInd, betaInd,
                          formatScientific(m), formatScientific(b)))
        scatter.set_ylabel('Number of People')
        scatter.legend(loc="upper left", frameon=False)
        ####    End


    #### R Value
    # Gravity
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


    # Gravity Sum
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



    ####### Other one
    #### Gravity
    ###sub1 = fig.add_subplot(gs[4:6, 0:2])
    ###norm = colors.Normalize(0, 1.01)
    ###cmap = cm.get_cmap('nipy_spectral', 100)
    #### arange of the following is partial setup for colorbar
    ###CS = sub1.contourf(xval, yval, otherValues, np.arange(0, 1.01, .01),
    ###                 cmap=cmap, norm=norm,  vmin=0, vmax=1.01)
    ###sub1.set_xlabel('Beta')
    ###sub1.set_ylabel('Alpha')
    ###if titleString:
    ###    sub1.set_title(titleString+' Other One ')
    ###plt.colorbar(CS, )


    #### Gravity Sum
    ###sub3 = fig.add_subplot(gs[4:6,2:])
    ###norm = colors.Normalize(0, 1.01)
    ###cmap = cm.get_cmap('nipy_spectral', 100)
    #### arange of the following is partial setup for colorbar
    ###CS = sub3.contourf(xval, yval, otherSumValues, np.arange(0, 1.01, .01),
    ###                 cmap=cmap, norm=norm,  vmin=0, vmax=1.01)
    ###sub3.set_xlabel('Beta')
    ###sub3.set_ylabel('Alpha')
    ###if titleString:
    ###    sub3.set_title(titleString+' Sum Other One Values')
    ###plt.colorbar(CS, )


    ####### Second Other One
    #### Gravity
    ###sub1 = fig.add_subplot(gs[6:8, 0:2])
    ###norm = colors.Normalize(0, 1.01)
    ###cmap = cm.get_cmap('nipy_spectral', 100)
    #### arange of the following is partial setup for colorbar
    ###CS = sub1.contourf(xval, yval, secondOtherValues, np.arange(0, 1.01, .01),
    ###                 cmap=cmap, norm=norm,  vmin=0, vmax=1.01)
    ###sub1.set_xlabel('Beta')
    ###sub1.set_ylabel('Alpha')
    ###if titleString:
    ###    sub1.set_title(titleString+' Second Other One ')
    ###plt.colorbar(CS, )


    #### Gravity Sum
    ###sub3 = fig.add_subplot(gs[6:8,2:])
    ###norm = colors.Normalize(0, 1.01)
    ###cmap = cm.get_cmap('nipy_spectral', 100)
    #### arange of the following is partial setup for colorbar
    ###CS = sub3.contourf(xval, yval, secondOtherSumValues, np.arange(0, 1.01, .01),
    ###                 cmap=cmap, norm=norm,  vmin=0, vmax=1.01)
    ###sub3.set_xlabel('Beta')
    ###sub3.set_ylabel('Alpha')
    ###if titleString:
    ###    sub3.set_title(titleString+' Sum Second Other One Values')
    ###plt.colorbar(CS, )


    # Update Change space between subplots, save image
    gs.update(wspace=1, hspace=1)
    if name[-4:] != '.png':
        #fig.savefig(name+'.png', bbox_inches='tight')
        fig.savefig(name+'.png', dpi=900)
    else:
        fig.savefig(name)
