import os
import sys
import pandas
from plotnine import *
from pathlib import Path

def main():
	if len(sys.argv) < 7:
		print("Error, parameters are missing: python run-ggplot2-traces-comparison.py path policy day_name num_traces type_of_screening measure")
		exit()

	long_path									= str(sys.argv[1])
	policy 										= str(sys.argv[2])
	day_name 									= str(sys.argv[3])
	num_traces									= str(sys.argv[4])
	type_of_screening							= str(sys.argv[5])
	measure										= str(sys.argv[6])
	type_pretty									= []
	vaccinated_students_perc					= ["0", "10", "40", "70"]
	type_of_stats								= ["mean", "variance", "left", "right"]
		
	my_plot										= None
	df_plot										= None
	
	for type_of_stat in type_of_stats:
		paths_num_traces						= []
		paths_1000								= []
		for vaccinated_students in vaccinated_students_perc:
			paths_num_traces.append(Path(__file__).parent / ("../mean-results/" + long_path + "/" + policy + "/" + day_name + "/" + type_of_stat + "_" + vaccinated_students + "_" + policy + "_" + day_name + "_" + type_of_screening + "_" + num_traces + ".csv"))
			paths_1000.append(Path(__file__).parent / ("../mean-results/" + long_path + "/" + policy + "/" + day_name + "/" + type_of_stat + "_" + vaccinated_students + "_" + policy + "_" + day_name + "_" + type_of_screening + "_1000.csv"))	
			type_pretty.append(vaccinated_students + "%")

		k										= 0

		for path_num_traces, path_1000 in zip(paths_num_traces, paths_1000):
			df_mean_num_traces     				= pandas.read_csv(str(path_num_traces), index_col=0)
			df_mean_1000        				= pandas.read_csv(str(path_1000), index_col=0)

			diff		 						= pandas.DataFrame(columns=['day', measure])
			diff['day']							= df_mean_num_traces.loc[:, 'day']
			diff[measure]						= df_mean_num_traces.loc[:, measure] - df_mean_1000.loc[:, measure]

			df_mod 								= diff
			df_mod['type'] 						= measure
			df_mod['stat']						= type_of_stat
			df_mod['type_pretty']				= type_pretty[k]
			if df_plot is None:
				df_plot 						= df_mod
			else:
				df_plot 						= df_plot.append(df_mod, ignore_index=True)

			k									= k + 1
								      		        
	df_plot.type_pretty = pandas.Categorical(df_plot.type_pretty, \
										ordered = True, \
										categories = ["0%", "10%", "40%", "70%"])
	
	my_plot = (ggplot(df_plot) \
 		+ aes(x = 'day', y = measure, color = 'type_pretty') \
 		+ geom_line() \
    	+ labs(title = "Comparison (difference of " + measure + ", " + num_traces + "-1000)", x = 'day', y = measure, color = 'Percentages of vaccination')) \
    	+ scale_x_continuous(breaks=[0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]) \
    	+ facet_wrap('stat', scales = 'free_y') \
    	+ theme(plot_title = element_text(face="bold"), axis_title_x  = element_text(face="bold"), axis_title_y = element_text(face="bold"), legend_title = element_text(face="bold"), subplots_adjust={'wspace': 0.25})

	my_plot.save('../plot-ggplot2/' + long_path + '/' + policy + '/' + day_name + '/Comparison/plot_comparison-' + num_traces + '-1000_' + measure, dpi=600)
	df_plot.to_csv('../plot-ggplot2/' + long_path + '/' + policy + '/' + day_name + '/Comparison/plot_comparison-' + num_traces + '-1000_' + measure + '.csv')

main();