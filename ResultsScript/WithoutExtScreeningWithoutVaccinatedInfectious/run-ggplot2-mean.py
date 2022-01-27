import os
import sys
import pandas
import math
from plotnine import *
from pathlib import Path

def main():
	if len(sys.argv) < 5:
		print("Error, parameters are missing: python run-ggplot2-mean.py path policy day_name type_of_screening [type_of_screening ...]")
		exit()

	long_path													= str(sys.argv[1])
	policy 														= str(sys.argv[2])
	day_name 													= str(sys.argv[3])
	n															= 36
	paths														= []
	type_of_screening											= []
	type_of_screening_pretty									= []

	index 														= 4
	while index < len(sys.argv):
		if str(sys.argv[index]) == "WithoutScreening":
			paths.append(Path(__file__).parent / ("../../Results/" + long_path + "/" + str(sys.argv[index]) + "/Results"))
		else:
			paths.append(Path(__file__).parent / ("../../Results/" + long_path + "/" + policy + "/" + "/Results" + day_name + sys.argv[index]))
		
		type_of_screening.append(str(sys.argv[index]))
		type_of_screening_pretty.append(str(sys.argv[index]).capitalize().replace('25', ' 25%').replace('50', ' 50%').replace('100', ' 100%').replace('Without', 'Without '))
		
		index 													= index + 1

	k															= 0
	population													= 240
	
	for path in paths:
		days_to_go_to_quarantine								= 0
		num_of_classroom_in_quarantine							= 0
		num_of_classroom_in_quarantine_first_week				= 0
		days_to_go_to_quarantine_mean							= 0
		days_to_go_to_quarantine_variance						= 0
		files													= os.listdir(path)
		num_files												= len(files)
		counter													= 0
		counter_quarantine										= 0
		df_mean													= None
		df_variance												= None
		df_std													= None
		df_days_quarantine										= None
		df_days_quarantine										= pandas.DataFrame(columns=['trace', 'day', 'type'])
		
		for file in files:
			df          										= pandas.read_csv(str(path) + "/" + file, sep='\t')

			if policy == "D2" and type_of_screening[k] != "WithoutScreening":
				df.columns 										= ['day', 'seedRun', 'susceptible', 'exposed', 'infected',
					                     			   		   	   'removed', 'susceptible-in-quarantine', 'exposed-in-quarantine',
					                     			   		   	   'infected-in-quarantine', 'removed-in-quarantine',
					                     			   		   	   'susceptible-in-quarantine-external-1', 'exposed-in-quarantine-external-1',
					                     			 		   	   'infected-in-quarantine-external-1', 'removed-in-quarantine-external-1',
					                     			 		   	   'susceptible-in-quarantine-external-2', 'exposed-in-quarantine-external-2',
					                     			 		   	   'infected-in-quarantine-external-2', 'removed-in-quarantine-external-2',
					                     			   		   	   'num-of-screened-students', 'num-of-screened-students-external-1', 'num-of-screened-students-external-2',
					                     			   		   	   'num-of-positive-students', 'num-of-positive-students-external-1', 'num-of-positive-students-external-2',
					                     			   		   	   'num-infected-outside', 'classroom-in-quarantine', 'num-of-classroom-in-quarantine',
					                     			   		   	   'classroom-with-at-least-one-infected']
				del df['num-infected-outside']
			else:
				df.columns 										= ['day', 'seedRun', 'susceptible', 'exposed', 'infected',
					                     			   		   	   'removed', 'susceptible-in-quarantine', 'exposed-in-quarantine',
					                     			   		   	   'infected-in-quarantine', 'removed-in-quarantine',
					                     			   		   	   'susceptible-in-quarantine-external-1', 'exposed-in-quarantine-external-1',
					                     			 		   	   'infected-in-quarantine-external-1', 'removed-in-quarantine-external-1',
					                     			 		   	   'susceptible-in-quarantine-external-2', 'exposed-in-quarantine-external-2',
					                     			 		   	   'infected-in-quarantine-external-2', 'removed-in-quarantine-external-2',
					                     			   		   	   'num-of-screened-students', 'num-of-screened-students-external-1', 'num-of-screened-students-external-2',
					                     			   		   	   'num-of-positive-students', 'num-of-positive-students-external-1', 'num-of-positive-students-external-2',
					                     			   		   	   'classroom-in-quarantine', 'num-of-classroom-in-quarantine',
					                     			   		   	   'classroom-with-at-least-one-infected']

			del df['seedRun']

			day 												= 0
			classroom_in_quarantine 							= df['classroom-in-quarantine']
			
			for i in range(0, n):
				if classroom_in_quarantine[i] != "[]":
					day 										= i
					break

			df_days_quarantine.loc[counter, 'type']				= "-"
			
			if day != 0 and day <= 7:
				num_of_classroom_in_quarantine_first_week 	 	= num_of_classroom_in_quarantine_first_week + 1

			if day != 0:
				num_of_classroom_in_quarantine  				= num_of_classroom_in_quarantine + 1

				if counter_quarantine == 0:
					days_to_go_to_quarantine_mean				= day
				else:
					days_to_go_to_quarantine_mean 				= days_to_go_to_quarantine_mean + (day - days_to_go_to_quarantine_mean) / counter_quarantine

				if counter_quarantine == 0:
					days_to_go_to_quarantine_variance			= 0
				else:
					days_to_go_to_quarantine_variance			= days_to_go_to_quarantine_variance + ((counter_quarantine-1) / counter_quarantine) * (day - days_to_go_to_quarantine_mean) ** 2

				counter_quarantine = counter_quarantine + 1

				if df.loc[day, 'num-of-positive-students'] > 0:
					df_days_quarantine.loc[counter, 'type']		= "School screening"
				else:
					df_days_quarantine.loc[counter, 'type']		= "External screening"

			df_days_quarantine.loc[counter, 'trace'] 			= counter
			df_days_quarantine.loc[counter, 'day']				= day
							
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

		df_variance 											= df_variance / (counter-1)

		df_std													= df_variance.transform('sqrt')

		df_left   								        	 	= df_mean - 1.96 * (df_std / math.sqrt(counter))
		df_right	           									= df_mean + 1.96 * (df_std / math.sqrt(counter))

		df_variance['day']										= df['day']
		df_left['day']											= df['day']
		df_right['day']											= df['day']

		if type_of_screening[k] != "WithoutScreening":
			days_to_go_to_quarantine_variance					= days_to_go_to_quarantine_variance / (counter_quarantine-1)

			days_to_go_to_quarantine_std						= math.sqrt(days_to_go_to_quarantine_variance)

			days_to_go_to_quarantine_left						= days_to_go_to_quarantine_mean - 1.96 * (days_to_go_to_quarantine_std / math.sqrt(counter_quarantine))
			days_to_go_to_quarantine_right						= days_to_go_to_quarantine_mean + 1.96 * (days_to_go_to_quarantine_std / math.sqrt(counter_quarantine))

		if type_of_screening[k] == "WithoutScreening":
			df_mean.to_csv('../../mean-results/' + long_path + '/WithoutScreening/mean_' + type_of_screening[k] + '.csv', float_format="%.4f")
			df_variance.to_csv('../../mean-results/' + long_path + '/WithoutScreening/variance_' + type_of_screening[k] + '.csv', float_format="%.4f")
			df_left.to_csv('../../mean-results/' + long_path + '/WithoutScreening/left_' + type_of_screening[k] + '.csv', float_format="%.4f")
			df_right.to_csv('../../mean-results/' + long_path + '/WithoutScreening/right_' + type_of_screening[k] + '.csv', float_format="%.4f")
			df_days_quarantine.to_csv('../../mean-results/' + long_path + '/WithoutScreening/days_to_detect_infection_' + type_of_screening[k] + '.csv', float_format="%.4f")
		else:
			df_mean.to_csv('../../mean-results/' + long_path + '/' + policy + "/" + day_name + '/mean_' + policy + "_" + day_name + '_' + type_of_screening[k] + '.csv', float_format="%.4f")
			df_variance.to_csv('../../mean-results/' + long_path + '/' + policy + "/" + day_name + '/variance_' + policy + "_" + day_name + '_' + type_of_screening[k] + '.csv', float_format="%.4f")
			df_left.to_csv('../../mean-results/' + long_path + '/' + policy + "/" + day_name + '/left_' + policy + "_" + day_name + '_' + type_of_screening[k] + '.csv', float_format="%.4f")
			df_right.to_csv('../../mean-results/' + long_path + '/' + policy + "/" + day_name + '/right_' + policy + "_" + day_name + '_' + type_of_screening[k] + '.csv', float_format="%.4f")
			df_days_quarantine.to_csv('../../mean-results/' + long_path + '/' + policy + "/" + day_name + '/days_to_detect_infection_' + policy + "_" + day_name + '_' + type_of_screening[k] + '.csv', float_format="%.4f")

		prob_of_classroom_in_quarantine_first_week				= num_of_classroom_in_quarantine_first_week / num_files
		
		if type_of_screening[k] != "WithoutScreening":
			print (type_of_screening_pretty[k] + ":")
			print ("Left interval number of days needed to detect infection:", days_to_go_to_quarantine_left)
			print ("Average number of days needed to detect infection: " + str(days_to_go_to_quarantine_mean) + ' +- ' + str(days_to_go_to_quarantine_mean - days_to_go_to_quarantine_left))
			print ("Right interval number of days needed to detect infection:", days_to_go_to_quarantine_right)
			print ("Probability of finding infection within the first week:", prob_of_classroom_in_quarantine_first_week)
			print ("*****************************************************************")

		k 														= k + 1
main();