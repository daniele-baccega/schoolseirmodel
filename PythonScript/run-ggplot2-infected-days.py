import os
import sys
import pandas
from plotnine import *
from pathlib import Path

def main():
	if len(sys.argv) < 7:
		print("Error, parameters are missing: python run-ggplot2-infected-days.py path policy day_name vaccinated_students_% num_traces type_of_screening [type_of_screening ...]")
		exit()

	long_path									= str(sys.argv[1])
	policy 										= str(sys.argv[2])
	day_name 									= str(sys.argv[3])
	vaccinated_students							= str(sys.argv[4])
	num_traces									= str(sys.argv[5])
	paths										= []
	type_of_screening							= []
	type_of_screening_pretty					= []

	if not "WithVaccinatedStudents" in long_path:
		vaccinated_students						= ""

	index 										= 6
	while index < len(sys.argv):
		if str(sys.argv[index]) == "WithoutScreening":
			paths.append(Path(__file__).parent / ("../mean-results/" + long_path + "/" + str(sys.argv[index]) + "/mean_" + vaccinated_students + str(sys.argv[index]) + "_" + num_traces + ".csv"))
		else:
			paths.append(Path(__file__).parent / ("../mean-results/" + long_path + "/" + policy + "/mean-days/mean_" + vaccinated_students + policy + "_" + str(sys.argv[index]) + "_" + num_traces + "_mean-days.csv"))
		type_of_screening.append(str(sys.argv[index]))
		type_of_screening_pretty.append(str(sys.argv[index]).capitalize().replace('-', ' ').replace('25', ' 25%').replace('50', ' 50%').replace('100', ' 100%').replace('Without', 'Without '))
		
		index 									= index + 1

	my_plot										= None
	df_plot										= None
	k											= 0
	
	for path in paths:
		df_mean          						= pandas.read_csv(str(path), index_col=0)

		df_mean 								= df_mean.iloc[1:]

		df_mod 									= df_mean.loc[:, ['day', 'infected']]
		df_mod.columns 							= ['day', 'agents']
		df_mod['type'] 							= 'Infected'
		df_mod['type_of_screening_pretty'] 						= type_of_screening_pretty[k]
		if df_plot is None:
			df_plot 							= df_mod
		else:
			df_plot 							= df_plot.append(df_mod, ignore_index=True)
		
		df_mod 									= df_mean.loc[:, ['day', 'infected-in-quarantine']]
		df_mod['infected-in-quarantine']		= df_mod['infected-in-quarantine'] + df_mean['infected-in-quarantine-external-1'] + df_mean['infected-in-quarantine-external-2']
		df_mod.columns 							= ['day', 'agents']
		df_mod['type'] 							= 'Infected in quarantine'
		df_mod['type_of_screening_pretty'] 		= type_of_screening_pretty[k]
		df_plot 								= df_plot.append(df_mod, ignore_index=True)

		k										= k + 1

	df_plot.type = pandas.Categorical(df_plot.type, \
							   		  ordered = True, \
							   		  categories = ["Infected", "Infected in quarantine"])
								      		        
	df_plot.type_of_screening_pretty = pandas.Categorical(df_plot.type_of_screening_pretty, \
							   		    ordered = True, \
							   		    categories = ["Without screening", "Screening 25%", "Screening 50%", "Screening 100%"])

	my_plot = (ggplot(df_plot) \
		+ aes(x='day', y = 'agents', color = 'type') \
    	+ geom_line() \
    	+ labs(title = policy + ' policy (with NPIs): infected and infected in quarantine', x = 'day', y = 'number of infected', color = 'Agent type')) \
		+ facet_wrap('type_of_screening_pretty') \
    	+ scale_color_manual(values=['#990000', '#ff8c1a']) \
    	+ scale_x_continuous(breaks=[0, 5, 10, 15, 20, 25, 30, 35]) \
    	+ theme(plot_title = element_text(face="bold"), axis_title_x  = element_text(face="bold"), axis_title_y = element_text(face="bold"), legend_title = element_text(face="bold"))
		
	my_plot.save('../plot-ggplot2/' + long_path + '/' + policy + '/mean-days/plot-' + policy + '_infected', dpi=600)
	df_plot.to_csv('../plot-ggplot2/' + long_path + '/' + policy + '/mean-days/plot-file/plot-' + policy + '_infected.csv')

main();