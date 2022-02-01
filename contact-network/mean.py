import os
import sys
import pandas
import math
import numpy as np
from plotnine import *
from pathlib import Path

def main():
	types														= ['number-of-contacts', 'contacts-time']

	for type in types:
		path													= Path(__file__).parent / ("Results/" + type + "/")
		files													= os.listdir(path)
		num_files												= len(files)
		counter													= 0
		mean 													= None
		variance												= None

		for file in files:
			matrix          									= np.genfromtxt(str(path) + "/" + file, delimiter=" ", dtype=int)

			if mean is None:
		 		mean 											= matrix
			else:
		 		mean 											= mean + (matrix - mean) / counter

			if variance is None:
		 		variance 										= np.zeros([290, 290], dtype=int)
			else:
		 		variance 										= variance + ((counter-1) / counter) * (matrix - mean) ** 2

			counter												= counter + 1

		variance 												= variance / (counter-1)

		std														= np.sqrt(variance)

		left   									        	 	= mean - 1.96 * (std / math.sqrt(counter))
		right	           										= mean + 1.96 * (std / math.sqrt(counter))

		np.savetxt('mean-results/mean_' + type + '.csv', mean, delimiter=",")
		np.savetxt('mean-results/variance_' + type + '.csv', variance, delimiter=",")
		np.savetxt('mean-results/left_' + type + '.csv', left, delimiter=",")
		np.savetxt('mean-results/right_' + type + '.csv', right, delimiter=",")

main();