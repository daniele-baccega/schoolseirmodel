import os
import sys
import pandas
import math
from plotnine import *
from pathlib import Path

def main():
	if len(sys.argv) < 7:
		print("Error, parameters are missing: python run-ggplot2-mean.py path policy day_name vaccinated_students_% num_traces type_of_screening [type_of_screening ...]")
		exit()

	long_path													= str(sys.argv[1])
	policy 														= str(sys.argv[2])
	day_name 													= str(sys.argv[3])
	vaccinated_students											= str(sys.argv[4])
	num_traces													= str(sys.argv[5])
	paths														= []
	type_of_screening											= []
	type_of_screening_pretty									= []

	if not "WithVaccinatedStudents" in long_path:
		vaccinated_students										= ""

	index 														= 6
	while index < len(sys.argv):
		if str(sys.argv[index]) == "WithoutScreening":
			paths.append(Path(__file__).parent / ("../Results/" + long_path + "/" + str(sys.argv[index]) + "/Results" + vaccinated_students))
		else:
			paths.append(Path(__file__).parent / ("../Results/" + long_path + "/" + policy + "/" + "/Results" + vaccinated_students + day_name + sys.argv[index]))
		
		type_of_screening.append(str(sys.argv[index]))
		type_of_screening_pretty.append(str(sys.argv[index]).capitalize().replace('25', ' 25%').replace('50', ' 50%').replace('100', ' 100%').replace('Without', 'Without '))
		
		index 													= index + 1

	k															= 0
	
	for path in paths:
		files													= os.listdir(path)
		counter													= 0
		df_mean													= None
		df_variance												= None
		df_std													= None
		
		for file in files:
			df          										= pandas.read_csv(str(path) + "/" + file, sep='\t', index_col=False)

			del df['seedRun']
			del df['classroom-in-quarantine']

			if df_mean is None:
				df_mean 										= df
			else:
				df_mean 										= df_mean + (df - df_mean) / counter

			if df_variance is None:
				df_variance 									= df
				for col in df_variance.columns:
					df_variance[col].values[:] 					= 0
			else:
				df_variance 									= df_variance + ((counter-1) / counter) * (df - df_mean) ** 2

			counter												= counter + 1

			if counter == int(num_traces):
				break;

		df_variance 											= df_variance / (counter-1)

		df_std													= df_variance.transform('sqrt')

		df_left   								        	 	= df_mean - 1.96 * (df_std / math.sqrt(counter))
		df_right	           									= df_mean + 1.96 * (df_std / math.sqrt(counter))

		df_variance['day']										= df['day']
		df_left['day']											= df['day']
		df_right['day']											= df['day']

		if vaccinated_students != "":
			vaccinated_students 								+= "_"

		if type_of_screening[k] == "WithoutScreening":
			df_mean.to_csv('../mean-results/' + long_path + '/WithoutScreening/mean_' + vaccinated_students + type_of_screening[k] + '_' + num_traces + '.csv', float_format="%.4f")
			df_variance.to_csv('../mean-results/' + long_path + '/WithoutScreening/variance_' + vaccinated_students + type_of_screening[k] + '_' + num_traces + '.csv', float_format="%.4f")
			df_left.to_csv('../mean-results/' + long_path + '/WithoutScreening/left_' + vaccinated_students + type_of_screening[k] + '_' + num_traces + '.csv', float_format="%.4f")
			df_right.to_csv('../mean-results/' + long_path + '/WithoutScreening/right_' + vaccinated_students + type_of_screening[k] + '_' + num_traces + '.csv', float_format="%.4f")
		else:
			df_mean.to_csv('../mean-results/' + long_path + '/' + policy + "/" + day_name + '/mean_' + vaccinated_students + policy + "_" + day_name + '_' + type_of_screening[k] + '_' + num_traces + '.csv', float_format="%.4f")
			df_variance.to_csv('../mean-results/' + long_path + '/' + policy + "/" + day_name + '/variance_' + vaccinated_students + policy + "_" + day_name + '_' + type_of_screening[k] + '_' + num_traces + '.csv', float_format="%.4f")
			df_left.to_csv('../mean-results/' + long_path + '/' + policy + "/" + day_name + '/left_' + vaccinated_students + policy + "_" + day_name + '_' + type_of_screening[k] + '_' + num_traces + '.csv', float_format="%.4f")
			df_right.to_csv('../mean-results/' + long_path + '/' + policy + "/" + day_name + '/right_' + vaccinated_students + policy + "_" + day_name + '_' + type_of_screening[k] + '_' + num_traces + '.csv', float_format="%.4f")
		
		k 														= k + 1
main();