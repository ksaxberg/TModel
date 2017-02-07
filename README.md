# TModel
Estimating traffic flow based on application of Gravity Law.

Note: Lingering large number precision issues still need to be addressed. 


Usage:
	gravityBoth.py expects 3 commandline inputs, one with the population, 
	one with the distances between cities, one with the actual measures
	of vehicles traveling on the road. This will create an image output
	for the run of both gravity and gravity sum for the data given.
	The image is intended for calibration of model parameters, and 
	runs over a reasonable subset of the parameter space known for models.	

	For now, data format can be seen from the test files. Assumed order 
	of cities in each dimension is the same order as specified in population.txt. 
	However, model default is to run in "edge-wise" mode, where distance 
	and measured data is listed by the vertices on the edge. 

	Example run: 
	  python3 gravityBoth.py ./test/population.txt ./test/distance.txt ./test/roadData.txt

	

Explanation of files:
	Core files:
	  gravity.py, gravitySum.py, parseData.py, common.py, gravityBoth.py
	The file common.py contains a list of parameters to vary to change the
	graphical output, alpha and beta iteration values. gravityBoth.py is 
	intended as a command line interface for gravity.py and gravitySum.py.


	addNoise.py is called as follows:
	  python addNoise.py ./test/roadData.txt .2 	
	The first parameter is the road data set, where the second is the 
	percentage variation. In this case, 20% variation. Every listed edge
	value is treated as the mean for a standard normal, and the variation
	is this percentage value multiplied by the mean. This is intended to 
	verify model robustness in the face of data pertubation. The AADT
	road data is known to have variable collection quality, and having 
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

	
	network.py is only partially implemented, intented to be an object
	oriented approach to running the model through python, rather than
	command line scripting. This is intended to ease in the querrying 
	of the calibrated model.	
