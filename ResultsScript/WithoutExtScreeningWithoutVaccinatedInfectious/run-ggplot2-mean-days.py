import os
import sys
import pandas
import math
from plotnine import *
from pathlib import Path

def main():
	if len(sys.argv) < 4:
		print("Error, parameters are missing: python run-ggplot2-mean-days.py path policy type_of_screening [type_of_screening ...]")
		exit()

	long_path														= str(sys.argv[1])
	policy 															= str(sys.argv[2])
	day_names 														= ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
	type_of_screening												= []
	type_of_screening_pretty										= []
	n																= 36

	if policy == "D2":
		day_names 													= ["MondayWednesday", "TuesdayThursday", "WednesdayFriday"]

	types_of_means													= ["mean", "variance", "left", "right"]

	for type_of_mean in types_of_means:
		index 														= 4
		paths														= []

		while index < len(sys.argv):
			path_list 												= []

			for day_name in day_names:
				path_list.append(Path(__file__).parent / ("../../mean-results/" + long_path + "/" + policy + "/" + day_name + "/" + type_of_mean + "_" + policy + "_" + day_name + "_" + str(sys.argv[index]) + ".csv"))

			type_of_screening.append(str(sys.argv[index]))
			type_of_screening_pretty.append(str(sys.argv[index]).capitalize().replace('-', ' ').replace('25', ' 25%').replace('50', ' 50%').replace('100', ' 100%').replace('Without', 'Without '))
			paths.append(path_list)

			index 													= index + 1

		k															= 0
		population													= 240
		
		for path_list in paths:
			df_mean													= None
			df_variance												= None
			df_std													= None
			counter													= 0
			
			for path in path_list:
				df          										= pandas.read_csv(str(path), index_col=0)

				df.columns 											= ['day', 'susceptible', 'exposed', 'infected',
					                     			   			   	   'removed', 'susceptible-in-quarantine', 'exposed-in-quarantine',
					                     			   			   	   'infected-in-quarantine', 'removed-in-quarantine',
					                     			   			   	   'susceptible-in-quarantine-external-1', 'exposed-in-quarantine-external-1',
					                     			 			   	   'infected-in-quarantine-external-1', 'removed-in-quarantine-external-1',
					                     			 			   	   'susceptible-in-quarantine-external-2', 'exposed-in-quarantine-external-2',
					                     			 			   	   'infected-in-quarantine-external-2', 'removed-in-quarantine-external-2',
					                     			   			   	   'num-of-screened-students', 'num-of-screened-students-external-1', 'num-of-screened-students-external-2',
					                     			   			   	   'num-of-positive-students', 'num-of-positive-students-external-1', 'num-of-positive-students-external-2',
					                     			   			   	   'num-of-classroom-in-quarantine',
					                     			   			   	   'classroom-with-at-least-one-infected']

				if df_mean is None:
					df_mean 										= df
				else:
					df_mean 										= df_mean + df

				counter												= counter + 1

			df_mean													= df_mean / counter

			df_mean.to_csv('../../mean-results/' + long_path + '/' + policy + '/mean-days/' + type_of_mean + '_' + policy + '_mean-days_' + type_of_screening[k] + '.csv', float_format="%.4f")
		
			k 														= k + 1
main();