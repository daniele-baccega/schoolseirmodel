import os
import sys
import pandas
from plotnine import *
from pathlib import Path

def main():
	if len(sys.argv) < 6:
		print("Error, parameters are missing: python run-ggplot2-cumulative-infected-vaccinated-students.py path policy day_name num_traces type_of_screening")
		exit()

	long_path									= str(sys.argv[1])
	policy										= str(sys.argv[2])
	day_name 									= str(sys.argv[3])
	num_traces									= str(sys.argv[4])
	type_of_screening							= str(sys.argv[5])
	paths										= []
	type_pretty									= []
	vaccinated_students_perc					= ["0", "10", "40", "70"]

	for vaccinated_students in vaccinated_students_perc:
		if policy == "WithoutScreening":
			paths.append(Path(__file__).parent / ("../mean-results/" + long_path + "/" + policy + "/mean_" + vaccinated_students + "_" + policy + "_" + num_traces + ".csv"))
		else:
			paths.append(Path(__file__).parent / ("../mean-results/" + long_path + "/" + policy + "/" + day_name + "/mean_" + vaccinated_students + "_" + policy + "_" + day_name + "_" + type_of_screening + "_" + num_traces + ".csv"))
		type_pretty.append(vaccinated_students + "%")
		
	my_plot										= None
	df_plot										= None
	k											= 0
	
	for path in paths:
		df_mean          						= pandas.read_csv(str(path), index_col=0)

		population								= df_mean.loc[0, 'susceptible']

		infected 								= pandas.DataFrame(columns=['day', 'infected'])

		infected['day']							= df_mean.loc[:, 'day']
		infected['infected']					= df_mean.loc[:, 'infected'] + df_mean.loc[:, 'infected-in-quarantine'] + df_mean.loc[:, 'infected-in-quarantine-external-1'] + df_mean.loc[:, 'infected-in-quarantine-external-2']
		
		df_mod 									= infected
		df_mod['type'] 							= 'Infected'
		df_mod['type_pretty'] 					= type_pretty[k]
		if df_plot is None:
			df_plot 							= df_mod
		else:
			df_plot 							= df_plot.append(df_mod, ignore_index=True)

		k										= k + 1
								      		        
	df_plot.type_pretty = pandas.Categorical(df_plot.type_pretty, \
										ordered = True, \
										categories = ["0%", "10%", "40%", "70%"])

	policy_pretty 								= "D1"

	if policy == "WithoutScreening":
		policy_pretty							= "without screening"
	
	my_plot = (ggplot(df_plot) \
		+ aes(x = 'day', y = 'infected', color = 'type_pretty') \
		+ geom_line() \
		+ labs(title = "Students vaccination (" + policy + " policy)", x = 'day', y = 'infected', color = 'Percentages of vaccination')) \
		+ scale_x_continuous(breaks=[0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]) \
		+ theme(plot_title = element_text(face="bold"), axis_title_x  = element_text(face="bold"), axis_title_y = element_text(face="bold"), legend_title = element_text(face="bold"))

	my_plot.save('../plot-ggplot2/' + long_path + '/' + policy + '/plot_cumulative_infected', dpi=600)
	df_plot.to_csv('../plot-ggplot2/' + long_path + '/' + policy + '/plot_cumulative_infected.csv')

main();