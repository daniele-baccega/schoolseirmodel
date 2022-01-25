import os
import sys
import pandas
import math

def main():
	if len(sys.argv) < 4:
		print("Error, parameters are missing: python run-ggplot2-mean.py path policy day_name")
		exit()

	path													= str(sys.argv[1])
	policy 													= str(sys.argv[2])
	day_name 												= str(sys.argv[3])
	n														= 36
	population												= 240
	
	long_path												= "../../Results/" + path + "/" + policy + "/Results" + policy + day_name + "Screening100/"
	files													= os.listdir(long_path)
	num_files												= len(files)
	df_mean													= None
	df_variance												= None
	df_std													= None
	counter													= 0

	for file in files:
		df          										= pandas.read_csv(long_path + "/" + file, sep='\t')

		df.columns 											= ['day', 'seedRun', 'susceptible', 'exposed', 'infected',
			                     				   		   	   'removed', 'susceptible-in-quarantine', 'exposed-in-quarantine',
			                     				   		   	   'infected-in-quarantine', 'removed-in-quarantine',
			                     				   		   	   'susceptible-in-quarantine-external-1', 'exposed-in-quarantine-external-1',
			                     			 			   	   'infected-in-quarantine-external-1', 'removed-in-quarantine-external-1',
			                     			 			   	   'susceptible-in-quarantine-external-2', 'exposed-in-quarantine-external-2',
			                     			 		   		   'infected-in-quarantine-external-2', 'removed-in-quarantine-external-2',
			                     				   		   	   'num-of-screened-students', 'num-of-screened-students-external-1', 'num-of-screened-students-external-2',
			                     				   		   	   'num-of-positive-students', 'num-of-positive-students-external-1', 'num-of-positive-students-external-2',
			                     				   		   	   'num-vaccinated-susceptible', 'num-vaccinated-exposed', 'num-vaccinated-infected', 'num-vaccinated-removed',
			                     				   		   	   'num-vaccinated-susceptible-in-quarantine', 'num-vaccinated-exposed-in-quarantine',
			                     				   		   	   'num-vaccinated-infected-in-quarantine', 'num-vaccinated-removed-in-quarantine',
			                     				   		   	   'num-vaccinated-susceptible-in-quarantine-external-1', 'num-vaccinated-exposed-in-quarantine-external-1',
			                     				   		   	   'num-vaccinated-infected-in-quarantine-external-1', 'num-vaccinated-removed-in-quarantine-external-1',
			                     				   		   	   'num-vaccinated-susceptible-in-quarantine-external-2', 'num-vaccinated-exposed-in-quarantine-external-2',
			                     				   		   	   'num-vaccinated-infected-in-quarantine-external-2', 'num-vaccinated-removed-in-quarantine-external-2',
			                     				   		   	   'num-infected-outside', 'classroom-in-quarantine', 'num-of-classroom-in-quarantine',
			                     			   			   	   'classroom-with-at-least-one-infected']

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

	df_variance 											= df_variance / (counter-1)

	df_std													= df_variance.transform('sqrt')

	df_left   								        	 	= df_mean - 1.96 * (df_std / math.sqrt(counter))
	df_right	           									= df_mean + 1.96 * (df_std / math.sqrt(counter))

	df_left['day']											= df['day']
	df_right['day']											= df['day']

	df_mean.to_csv('../../mean-results/' + path + '/' + policy + '/' + day_name + '/mean_' + policy + "_" + day_name + '.csv', float_format="%.4f")
	df_variance.to_csv('../../mean-results/' + path + '/' + policy + '/' + day_name + '/variance_' + policy + "_" + day_name + '.csv', float_format="%.4f")
	df_left.to_csv('../../mean-results/' + path + '/' + policy + '/' + day_name + '/left_' + policy + "_" + day_name + '.csv', float_format="%.4f")
	df_right.to_csv('../../mean-results/' + path + '/' + policy + '/' + day_name + '/right_' + policy + "_" + day_name + '.csv', float_format="%.4f")

main();