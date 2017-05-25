#Gravity Law Regression
Estimating traffic flow based on application of Gravity Law.

Note: Lingering large number precision issues still need to be addressed.


Usage:

	gravityBoth.py expects 3 commandline inputs, one with the population,
	one with the distances between cities, one with the actual measures
	of vehicles traveling on the road. This will create an image output
	for the run of both gravity and gravity sum for the data given.
	The image is intended for calibration of model parameters, and
	runs over a reasonable subset of the parameter space known for models.

	For now, data format can be seen from the test files.
        Ranges of confidence on the data are also supported graphically,
        simply switch useErrorBound parameter in common.py to true, and
        provide the data file where each line has the following format:
        "cityA, cityB, value, minInterval, maxInterval"
        The graph will plot these bounds on the actual data, so the model
        fit can be checked.

    Assumed order of cities in each dimension is the same order as specified in population.txt.
	However, model default is to run in "edge-wise" mode, where distance
	and measured data is listed by the vertices on the edge.

	Example run:

	  python3 gravityBoth.py ./test/population.txt ./test/distance.txt ./test/roadData.txt
      Note: the files must be provided in the order above, but the names do not matter.


Explanation of data and collection techniques:

    For most of the AADT traffic datasets (including AZ24Node, AZ9Test, North
    East AZ, Oregon, WAandOR, Washington), data was collected from government
    AADT traffic data publications. Different techniques were involved, as
    there is acknowledged variability in the quality of the AADT data due to
    sensor issues, maintenance, and road closures. On the stretch of road
    connecting two places of interest, some datasets include an average of the
    lowest 3-5 AADT values and others include a number representing the lower
    part of the distribution of values along the stretch of road, usually
    around the first quantile. The "addNoise" feature in parseData is included to give
    support to the idea that the trends seen are resistent to mild pertubation
    of the actual road data values, that the exact data is not necessary.
    A more complete list of heuristics used is being developed with "TheWest"
    dataset, as two independent parties use the guidelines to develop a set of
    data.

Explanation of files:

	Core files:
	  gravity.py, gravitySum.py, parseData.py, common.py, gravityBoth.py
	The file common.py contains a list of parameters to vary to change the
	graphical output, alpha and beta iteration values. gravityBoth.py is
	intended as a command line interface for gravity.py and gravitySum.py.
    The file gravitySum_ContribRegress.py changes the way in which gravitySum
    calculates the regression, moving the constant term (intercept) to be
    a part of each partial sum, instead of on the already-summed values.

    ParseData includes an option for adding noise to edge values as follows:

	    Every listed edge value is treated as the mean for a standard normal,
        and the variation is this percentage value multiplied by the mean. This
        is intended to verify model robustness in the face of data pertubation.
        The AADT road data is known to have variable collection quality, and having
	    model calibration resistent to mild pertubation is indicative of the
	    applicability of the model.


	runBoth.sh is called as follows:
	  bash runBoth.sh <FolderContaining3Files> <TagForImage> x
	This is intended as a simple interface to running gravityBoth.py.
	This will automatically call gravityBoth with the predefined file names,
	requiring common naming convention as seen in the test folder. The
	tag for image is intended to allow multiple model run outputs to be
	distinguished, without having potentially lengthy names from using
	the containing folder as the name. The variable x is the intended
	noise for the model run.


	clean.sh:
	Simple intended to remove compiled python files as well as images.

    Explanation of Parameters in common.py
    <ul>
        <li>DEBUG - allows debug statements to be toggled from the program, allowing for some understanding of errors. </li>
        <li>alphaMin - the minimum value of alpha to be considered</li>
        <li>alphaMax - the maximum value of alpha to be considered</li>
        <li>alphaExample - a hard-coded example value for graphing (gravity graph)</li>
        <li>alphaSumExample - a hard-coded example value for graphing (gravity sum graph)</li>
        <li>betaMin - the minimum value of beta to be considered</li>
        <li>betaMax - the maximum value of beta to be considered</li>
        <li>betaExample - a hard-coded example value for graphing (gravity graph)</li>
        <li>betaSumExample - a hard-coded example value for graphing (gravity sum graph)</li>
        <li>stepValueAlpha - the step value of alpha, resolution to consider</li>
        <li>stepValueBeta - the step value of beta, resolution to consider</li>
        <li>useGravitySumThresh - limit gravitySum partial sums based on a distance threshold </li>
        <li>deleteFromOriginalNetworkSum - when thresholding, delete original edgewise connections from network if they surpass threshold</li>
        <li>gravitySumDistThresh - when thresholding, upper bound for distance </li>
        <li>gravitySumDistThreshMinimum - when thresholding, lower bound for distance</li>
        <li>automaticBestMatch - instead of hard coded graph values, plot the highest R^2 value in the alpha&beta space</li>
        <li>contributionSplit - adjusts how the regression in gravitySums is completed, whether the constant term is associated with the partials or on the sum of partials </li>
        <li>useErrorBound - provide a data file (measuredDataEdge) with lower and upper bounds, will include those in the plot </li>
    </ul>

