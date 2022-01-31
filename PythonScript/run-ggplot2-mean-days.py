import os
import sys
import pandas
import math
from plotnine import *
from pathlib import Path

def main():
	if len(sys.argv) < 6:
		print("Error, parameters are missing: python run-ggplot2-mean-days.py path policy vaccinated_students_% num_traces type_of_screening [type_of_screening ...]")
		exit()

	long_path														= str(sys.argv[1])
	policy 															= str(sys.argv[2])
	vaccinated_students												= str(sys.argv[3])
	num_traces														= str(sys.argv[4])
	day_names 														= ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
	type_of_screening												= []
	type_of_screening_pretty										= []

	if not "WithVaccinatedStudents" in long_path:
		vaccinated_students											= ""
	else:
		vaccinated_students											+= "_"

	if policy == "D2":
		day_names 													= ["MondayWednesday", "TuesdayThursday", "WednesdayFriday"]

	types_of_means													= ["mean", "variance", "left", "right"]

	for type_of_mean in types_of_means:
		index 														= 5
		paths														= []

		while index < len(sys.argv):
			path_list 												= []

			for day_name in day_names:
				if str(sys.argv[index]) == "WithoutScreening":
					path_list.append(Path(__file__).parent / ("../mean-results/" + long_path + "/" + policy + "/" + day_name + "/" + type_of_mean + "_" + vaccinated_students + "_" + str(sys.argv[index]) + "_" + num_traces + ".csv"))
				else:
					path_list.append(Path(__file__).parent / ("../mean-results/" + long_path + "/" + policy + "/" + day_name + "/" + type_of_mean + "_" + vaccinated_students + policy + "_" + day_name + "_" + str(sys.argv[index]) + "_" + num_traces + ".csv"))

			type_of_screening.append(str(sys.argv[index]))
			type_of_screening_pretty.append(str(sys.argv[index]).capitalize().replace('-', ' ').replace('25', ' 25%').replace('50', ' 50%').replace('100', ' 100%').replace('Without', 'Without '))
			paths.append(path_list)

			index 													= index + 1

		k															= 0
		
		for path_list in paths:
			df_mean													= None
			df_variance												= None
			df_std													= None
			counter													= 0
			
			for path in path_list:
				df          										= pandas.read_csv(str(path), index_col=0)

				if df_mean is None:
					df_mean 										= df
				else:
					df_mean 										= df_mean + df

				counter												= counter + 1

			df_mean													= df_mean / counter

			df_mean.to_csv('../mean-results/' + long_path + '/' + policy + '/mean-days/' + type_of_mean + '_' + vaccinated_students + policy + '_' + type_of_screening[k] + '_' + num_traces + '_mean-days.csv', float_format="%.4f")
		
			k 														= k + 1
main();