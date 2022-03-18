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
	quarantine_policies								= ["NovDecPolicy", "JanFebPolicy"]
	quarantine_policies_pretty						= ["Nov/Dec", "Jan/Feb"]
	vaccine_efficacy								= ["Vaccine Efficacy 100", "Vaccine Efficacy 90", "Vaccine Efficacy 70"]
	policies										= ["D1", "Without Screening"]
	day_name 										= "Monday"
	vaccinated_students_perc						= ["0", "10", "40", "70"]
	my_plot											= None
	df_plot											= None
	i												= 0

	for quarantine_policy in quarantine_policies:
		for efficacy in vaccine_efficacy:
			for policy in policies:
				if policy == "D1" and quarantine_policy == "JanFebPolicy":
					continue

				paths										= []
				type_pretty									= []
				for vaccinated_students in vaccinated_students_perc:
					if policy == "Without Screening":
						paths.append(Path(__file__).parent / ("../mean-results/" + long_path + "/" + quarantine_policy + "/Omicron/" + efficacy.replace(" ", "") + "/" + policy.replace(" ", "") + "/mean_" + vaccinated_students + "_WithoutScreening_" + num_traces + ".csv"))
					else:
						paths.append(Path(__file__).parent / ("../mean-results/" + long_path + "/" + quarantine_policy + "/Omicron/" + efficacy.replace(" ", "") + "/" + policy.replace(" ", "") + "/Monday/mean_" + vaccinated_students + "_D1_Monday_" + type_of_screening + "_" + num_traces + ".csv"))
					type_pretty.append(vaccinated_students + "%")
					
				k											= 0
				
				for path in paths:
					df_mean          						= pandas.read_csv(str(path), index_col=0)
					df_left          						= pandas.read_csv(str(path).replace("mean_", "left_"), index_col=0)
					df_right          						= pandas.read_csv(str(path).replace("mean_", "right_"), index_col=0)

					
					population								= df_mean.loc[0, 'susceptible'] + df_mean.loc[0, 'num-vaccinated-susceptible'] + df_mean.loc[0, 'num-vaccinated-removed']

					total_infected 							= pandas.DataFrame(columns=['day', 'cumulative_infected'])
					
					total_infected['day']					= df_mean.loc[:, 'day']
					total_infected['cumulative_infected'] 	= (population - (df_mean.loc[:, 'susceptible'] + df_mean.loc[:, 'susceptible-in-quarantine'] + df_mean.loc[:, 'susceptible-in-quarantine-external-1'] + df_mean.loc[:, 'susceptible-in-quarantine-external-2'] + df_mean.loc[:, 'num-vaccinated-susceptible'] + df_mean.loc[:, 'num-vaccinated-susceptible-in-quarantine'] + df_mean.loc[:, 'num-vaccinated-susceptible-in-quarantine-external-1'] + df_mean.loc[:, 'num-vaccinated-susceptible-in-quarantine-external-2'] +\
														       df_mean.loc[:, 'exposed'] + df_mean.loc[:, 'exposed-in-quarantine'] + df_mean.loc[:, 'exposed-in-quarantine-external-1'] + df_mean.loc[:, 'exposed-in-quarantine-external-2'] + df_mean.loc[:, 'num-vaccinated-exposed'] + df_mean.loc[:, 'num-vaccinated-exposed-in-quarantine'] + df_mean.loc[:, 'num-vaccinated-exposed-in-quarantine-external-1'] + df_mean.loc[:, 'num-vaccinated-exposed-in-quarantine-external-2'] + df_mean.loc[0, 'num-vaccinated-removed'])) / population
					total_infected['left'] 					= (population - (df_left.loc[:, 'susceptible'] + df_left.loc[:, 'susceptible-in-quarantine'] + df_left.loc[:, 'susceptible-in-quarantine-external-1'] + df_left.loc[:, 'susceptible-in-quarantine-external-2'] + df_left.loc[:, 'num-vaccinated-susceptible'] + df_left.loc[:, 'num-vaccinated-susceptible-in-quarantine'] + df_left.loc[:, 'num-vaccinated-susceptible-in-quarantine-external-1'] + df_left.loc[:, 'num-vaccinated-susceptible-in-quarantine-external-2'] +\
														       df_left.loc[:, 'exposed'] + df_left.loc[:, 'exposed-in-quarantine'] + df_left.loc[:, 'exposed-in-quarantine-external-1'] + df_left.loc[:, 'exposed-in-quarantine-external-2'] + df_left.loc[:, 'num-vaccinated-exposed'] + df_left.loc[:, 'num-vaccinated-exposed-in-quarantine'] + df_left.loc[:, 'num-vaccinated-exposed-in-quarantine-external-1'] + df_left.loc[:, 'num-vaccinated-exposed-in-quarantine-external-2'] + df_left.loc[0, 'num-vaccinated-removed'])) / population
					total_infected['right'] 				= (population - (df_right.loc[:, 'susceptible'] + df_right.loc[:, 'susceptible-in-quarantine'] + df_right.loc[:, 'susceptible-in-quarantine-external-1'] + df_right.loc[:, 'susceptible-in-quarantine-external-2'] + df_right.loc[:, 'num-vaccinated-susceptible'] + df_right.loc[:, 'num-vaccinated-susceptible-in-quarantine'] + df_right.loc[:, 'num-vaccinated-susceptible-in-quarantine-external-1'] + df_right.loc[:, 'num-vaccinated-susceptible-in-quarantine-external-2'] +\
														       df_right.loc[:, 'exposed'] + df_right.loc[:, 'exposed-in-quarantine'] + df_right.loc[:, 'exposed-in-quarantine-external-1'] + df_right.loc[:, 'exposed-in-quarantine-external-2'] + df_right.loc[:, 'num-vaccinated-exposed'] + df_right.loc[:, 'num-vaccinated-exposed-in-quarantine'] + df_right.loc[:, 'num-vaccinated-exposed-in-quarantine-external-1'] + df_right.loc[:, 'num-vaccinated-exposed-in-quarantine-external-2'] + df_right.loc[0, 'num-vaccinated-removed'])) / population


					total_infected 							= total_infected.iloc[1:]


					df_mod 									= total_infected
					df_mod['type_pretty'] 					= type_pretty[k]
					df_mod['efficacy']						= efficacy + "%"
					df_mod['policy']						= policy

					if policy == "Without Screening":
						df_mod['policy'] 				    = "W0 (" + quarantine_policies_pretty[i] + ")"

					if df_plot is None:
						df_plot 							= df_mod
					else:
						df_plot 							= df_plot.append(df_mod, ignore_index=True)

					k										= k + 1

		i													= i + 1


	df_plot.type_pretty = pandas.Categorical(df_plot.type_pretty, \
										ordered = True, \
										categories = ["0%", "10%", "40%", "70%"])

	df_plot.efficacy = pandas.Categorical(df_plot.efficacy, \
										ordered = True, \
										categories = ["Vaccine Efficacy 100%", "Vaccine Efficacy 90%", "Vaccine Efficacy 70%"])

	df_plot.policy = pandas.Categorical(df_plot.policy, \
										ordered = True, \
										categories = ["D1", "W0 (Nov/Dec)", "W0 (Jan/Feb)"])

	
	my_plot = (ggplot(df_plot) \
 		+ aes(x = 'day', y = 'cumulative_infected', color = 'type_pretty') \
 		+ geom_line() \
	 	#+ geom_ribbon(aes(ymin='left', ymax='right'), alpha=0.2)
 		+ facet_grid('policy ~ efficacy') \
 		+ geom_hline(aes(yintercept=1), color="#000000", linetype="dotted", size=0.3) \
    	+ labs(title = "Students vaccination", x = 'day', y = 'normalized cumulative infected', color = 'Percentages of students vaccination')) \
    	+ scale_x_continuous(breaks=[0, 10, 20, 30, 40, 50, 60]) \
    	+ scale_color_manual(values=["#FF0000", "#00FF00", "#0000FF", "#FF00FF"]) \
    	+ theme(plot_title = element_text(face="bold"), axis_title_x  = element_text(face="bold"), axis_title_y = element_text(face="bold"), legend_title = element_text(face="bold"))

	my_plot.save('../plot-ggplot2/' + long_path + '/plot_normalized_cumulative_infected_single_plot_omicron', dpi=600)
	df_plot.to_csv('../plot-ggplot2/' + long_path + '/plot_normalized_cumulative_infected_single_plot_omicron.csv')

main();