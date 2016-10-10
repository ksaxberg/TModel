# TModel
Estimating traffic flow based on application of Gravity Law.

Note: Some difference is shown in the output of this program in comparison 
	to Matlab implementations of this regression. The difference is 
	minor, and may be due to algorithmic differences in handling
	large number inputs. Further verification of the algorithms 
	should be undertaken. 

Usage:
	Gravity.py expects 3 commandline inputs, one with the population, 
	one with the distances between cities, one with the actual measures
	of vehicles traveling on the road. For now, data format can be seen
	from the test files. Assumed order of cities in each dimension:
	same order as specified in population.txt. 

	python3 gravity.py ./test/population.txt ./test/distance.txt ./test/roadData.txt

	This will print out a large matrix of regressions, for beta varying from 
	.1 to 2.0 by .1 incremends
	
	The gravity.py file can also be imported to include regression analysis.
