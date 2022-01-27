import os
import sys
import pandas
from plotnine import *
from pathlib import Path

def main():
	if len(sys.argv) < 4:
		print("Error, parameters are missing: python run-ggplot2-mean.py path policy type_of_screening [type_of_screening ...]")
		exit()

	long_path									= str(sys.argv[1])
	policy 										= str(sys.argv[2])
	n											= 36
	paths										= []
	type_of_screening							= []
	type_of_screening_pretty					= []

	index 										= 3
	while index < len(sys.argv):
		if str(sys.argv[index]) == "WithoutScreening":
			paths.append(Path(__file__).parent / ("../../mean-results/" + long_path + "/" + str(sys.argv[index]) + "/mean_" + str(sys.argv[index]) + ".csv"))
		else:
			paths.append(Path(__file__).parent / ('../../mean-results/' + long_path + '/' + policy + '/mean-days/mean_' + policy + '_mean-days_' + str(sys.argv[index]) + '.csv'))
		type_of_screening.append(str(sys.argv[index]))
		type_of_screening_pretty.append(str(sys.argv[index]).capitalize().replace('-', ' ').replace('25', ' 25%').replace('50', ' 50%').replace('100', ' 100%').replace('Without', 'Without '))
		
		index 									= index + 1

	my_plot										= None
	df_plot										= None
	k											= 0
	population									= 240
	
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
                     			   			   	   'num-of-classroom-in-quarantine',
                     			   			   	   'classroom-with-at-least-one-infected']

		new_infected 							= pandas.DataFrame(columns=['day', 'new-infected'])
		
		new_infected['day'] 					= df_mean.loc[:, 'day']
		new_infected['new-infected'] 			= population - (df_mean.loc[:, 'susceptible'] + df_mean.loc[:, 'susceptible-in-quarantine'] + df_mean.loc[:, 'susceptible-in-quarantine-external-1'] + df_mean.loc[:, 'susceptible-in-quarantine-external-2'] + \
														        df_mean.loc[:, 'exposed'] + df_mean.loc[:, 'exposed-in-quarantine'] + df_mean.loc[:, 'exposed-in-quarantine-external-1'] + df_mean.loc[:, 'exposed-in-quarantine-external-2'])
		new_infected['new-infected']			= new_infected['new-infected'].diff()

		new_infected 							= new_infected.iloc[1:]

		df_mod 									= new_infected
		df_mod['type'] 							= 'New infected'
		df_mod['type_of_screening_pretty'] 		= type_of_screening_pretty[k]
		if df_plot is None:
			df_plot 							= df_mod
		else:
			df_plot 							= df_plot.append(df_mod, ignore_index=True)

		k										= k + 1
								      		        
	df_plot.type_of_screening_pretty = pandas.Categorical(df_plot.type_of_screening_pretty, \
							   		    ordered = True, \
							   		    categories = ["Screening 100%", "Screening 50%", "Screening 25%", "Without screening"])

	my_plot = (ggplot(df_plot) \
		+ aes(x='day', y = 'new-infected', color = 'type', linetype = 'type_of_screening_pretty') \
    	+ geom_line() \
    	+ labs(title = policy + ' policy (with NPIs): new infected', x = 'day', y = 'new infected', color = 'Agent type', linetype = 'type_of_screening_pretty')) \
    	+ scale_color_manual(values=['#990000']) \
    	+ scale_x_continuous(breaks=[0, 5, 10, 15, 20, 25, 30, 35]) \
    	+ theme(plot_title = element_text(face="bold"), axis_title_x  = element_text(face="bold"), axis_title_y = element_text(face="bold"), legend_title = element_text(face="bold"))
		
	my_plot.save('../../plot-ggplot2/' + long_path + '/' + policy + '/mean-days/plot-' + policy + '_new-infected', dpi=600)
	df_plot.to_csv('../../plot-ggplot2/' + long_path + '/' + policy + '/mean-days/plot-file/plot-' + policy + '_new-infected.csv')
main();
