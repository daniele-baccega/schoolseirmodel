import os
import sys
import pandas
from plotnine import *
from pathlib import Path

def main():
	if len(sys.argv) < 4:
		print("Error, parameters are missing: python run-ggplot2-cumulative-infected-vaccinated-students.py path num_traces type_of_screening")
		exit()

	long_path										= str(sys.argv[1])
	num_traces										= str(sys.argv[2])
	type_of_screening								= str(sys.argv[3])
	vaccine_efficacy								= ["Vaccine Efficacy 100", "Vaccine Efficacy 90", "Vaccine Efficacy 70"]
	policies										= ["D1", "Without Screening"]
	day_name 										= "Monday"
	vaccinated_students_perc						= ["0", "10", "40", "70"]
	my_plot											= None
	df_plot											= None

	for efficacy in vaccine_efficacy:
		for policy in policies:
			paths										= []
			type_pretty									= []
			for vaccinated_students in vaccinated_students_perc:
				if policy == "Without Screening":
					paths.append(Path(__file__).parent / ("../mean-results/" + long_path + "/" + efficacy.replace(" ", "") + "/" + policy.replace(" ", "") + "/mean_" + vaccinated_students + "_WithoutScreening_" + num_traces + ".csv"))
				else:
					paths.append(Path(__file__).parent / ("../mean-results/" + long_path + "/" + efficacy.replace(" ", "") + "/" + policy.replace(" ", "") + "/Monday/mean_" + vaccinated_students + "_D1_Monday_" + type_of_screening + "_" + num_traces + ".csv"))
				type_pretty.append(vaccinated_students + "%")
				
			k											= 0
			
			for path in paths:
				df_mean          						= pandas.read_csv(str(path), index_col=0)

				population								= df_mean.loc[0, 'susceptible']

				total_infected 							= pandas.DataFrame(columns=['day', 'cumulative_infected'])
				
				total_infected['day']					= df_mean.loc[:, 'day']
				total_infected['cumulative_infected'] 	= (population - (df_mean.loc[:, 'susceptible'] + df_mean.loc[:, 'susceptible-in-quarantine'] + df_mean.loc[:, 'susceptible-in-quarantine-external-1'] + df_mean.loc[:, 'susceptible-in-quarantine-external-2'] + \
																        df_mean.loc[:, 'exposed'] + df_mean.loc[:, 'exposed-in-quarantine'] + df_mean.loc[:, 'exposed-in-quarantine-external-1'] + df_mean.loc[:, 'exposed-in-quarantine-external-2'])) / population

				total_infected 							= total_infected.iloc[1:]

				df_mod 									= total_infected
				df_mod['type_pretty'] 					= type_pretty[k]
				df_mod['efficacy']						= efficacy + "%"
				df_mod['policy']						= policy
				if df_plot is None:
					df_plot 							= df_mod
				else:
					df_plot 							= df_plot.append(df_mod, ignore_index=True)

				k										= k + 1
								      		        
	df_plot.type_pretty = pandas.Categorical(df_plot.type_pretty, \
										ordered = True, \
										categories = ["0%", "10%", "40%", "70%"])

	df_plot.efficacy = pandas.Categorical(df_plot.efficacy, \
										ordered = True, \
										categories = ["Vaccine Efficacy 100%", "Vaccine Efficacy 90%", "Vaccine Efficacy 70%"])

	df_plot.policy = pandas.Categorical(df_plot.policy, \
										ordered = True, \
										categories = ["D1", "Without Screening"])

	
	my_plot = (ggplot(df_plot) \
 		+ aes(x = 'day', y = 'cumulative_infected', color = 'type_pretty') \
 		+ geom_line() \
 		+ facet_grid('policy ~ efficacy') \
 		+ geom_hline(aes(yintercept=1), color="#000000", linetype="dotted", size=0.3) \
    	+ labs(title = "Students vaccination", x = 'day', y = 'normalized cumulative infected', color = 'Percentages of students vaccination')) \
    	+ scale_x_continuous(breaks=[0, 10, 20, 30, 40, 50, 60]) \
    	+ scale_color_manual(values=["#FF0000", "#00FF00", "#0000FF", "#FF00FF"]) \
    	+ theme(plot_title = element_text(face="bold"), axis_title_x  = element_text(face="bold"), axis_title_y = element_text(face="bold"), legend_title = element_text(face="bold"))

	my_plot.save('../plot-ggplot2/' + long_path + '/plot_normalized_cumulative_infected_single_plot', dpi=600)
	df_plot.to_csv('../plot-ggplot2/' + long_path + '/plot_normalized_cumulative_infected_single_plot.csv')

main();