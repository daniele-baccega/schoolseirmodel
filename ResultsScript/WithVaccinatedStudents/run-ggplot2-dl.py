import os
import sys
import pandas
from plotnine import *
from pathlib import Path

def main():
	if len(sys.argv) < 2:
		print("Error, parameters are missing: python run-ggplot2-dl.py path policy day_name")
		exit()

	long_path									= str(sys.argv[1])
	policy										= str(sys.argv[2])
	day_name 									= str(sys.argv[3])
	paths										= []
	type_pretty									= []
	vaccinated_students_perc					= ["0", "10", "40"]#, "70"]

	for perc in vaccinated_students_perc:
		paths.append(Path(__file__).parent / ("../../mean-results/" + long_path + "/" + policy + "/" + day_name + "/mean_" + perc + "_" + policy + "_" + day_name + ".csv"))
		type_pretty.append(perc + "%")
		
	my_plot										= None
	df_plot										= None
	k											= 0
	
	for path in paths:
		df_mean          						= pandas.read_csv(str(path), index_col=0)

		df_mean.columns 						= ['day', 'susceptible', 'exposed', 'infected',
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
                     				   		   	   'num-infected-outside', 'num-of-classroom-in-quarantine',
                     			   			   	   'classroom-with-at-least-one-infected']

		total_dad	 							= pandas.DataFrame(columns=['day', 'students', 'dad_type'])
		
		total_dad['day'] 						= df_mean.loc[:, 'day']
		total_dad['students'] 					= df_mean.loc[:, 'susceptible'] + df_mean.loc[:, 'exposed'] + df_mean.loc[:, 'infected'] + df_mean.loc[:, 'removed'] + (int(vaccinated_students_perc[k]) / 100) * 20 * (12 - df_mean.loc[:, 'num-of-classroom-in-quarantine'])
		total_dad['dl_type']					= 'Not distance learning'
		total_dad 								= total_dad.iloc[1:]

		total_dad['students'] = total_dad['students'].cumsum() / 240

		total_not_dad 							= pandas.DataFrame(columns=['day', 'students', 'dad_type'])

		total_not_dad['day'] 					= df_mean.loc[:, 'day']
		total_not_dad['students']				= df_mean.loc[:, 'susceptible-in-quarantine'] + df_mean.loc[:, 'exposed-in-quarantine'] + df_mean.loc[:, 'infected-in-quarantine'] + df_mean.loc[:, 'removed-in-quarantine'] +\
												  df_mean.loc[:, 'susceptible-in-quarantine-external-1'] + df_mean.loc[:, 'exposed-in-quarantine-external-1'] + df_mean.loc[:, 'infected-in-quarantine-external-1'] + df_mean.loc[:, 'removed-in-quarantine-external-1'] +\
												  df_mean.loc[:, 'susceptible-in-quarantine-external-2'] + df_mean.loc[:, 'exposed-in-quarantine-external-2'] + df_mean.loc[:, 'infected-in-quarantine-external-2'] + df_mean.loc[:, 'removed-in-quarantine-external-2'] + (int(vaccinated_students_perc[k]) / 100) * 20 * df_mean.loc[:, 'num-of-classroom-in-quarantine']
		total_not_dad['dl_type']				= 'Distance learning'
		total_not_dad 							= total_not_dad.iloc[1:]

		total_not_dad['students'] = total_not_dad['students'].cumsum() / 240


		df_mod 									= total_dad.append(total_not_dad, ignore_index=True)
		df_mod['type_pretty'] 					= type_pretty[k]
		if df_plot is None:
			df_plot 							= df_mod
		else:
			df_plot 							= df_plot.append(df_mod, ignore_index=True)

		k										= k + 1
								      		        
	df_plot.type_pretty = pandas.Categorical(df_plot.type_pretty, \
							   		    ordered = True, \
							   		    categories = ["0%", "10%", "40%"])#, "70%"])
	
	my_plot = (ggplot(df_plot) \
		+ aes(x = 'day', y = 'students', color = 'dl_type', linetype = 'type_pretty') \
		+ geom_line() \
    	+ labs(title = "Old school's policy vs New school's policy (" + policy + " policy)", x = 'day', y = 'cumulative number of days', color = 'Distance learning type', linetype = 'Policy type')) \
    	+ scale_y_continuous(breaks=[0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]) \
    	+ theme(plot_title = element_text(face="bold"), axis_title_x  = element_text(face="bold"), axis_title_y = element_text(face="bold"), legend_title = element_text(face="bold"))

	my_plot.save('../../plot-ggplot2/' + long_path + '/' + policy + '/' + day_name + '/dl.png', dpi=600)
	df_plot.to_csv('../../plot-ggplot2/' + long_path + '/' + policy + '/' + day_name + '/dl.csv')
main();
