import os
import sys
import pandas
from plotnine import *
from pathlib import Path

def main():
	if len(sys.argv) < 3:
		print("Error, parameters are missing: python run-ggplot2-mean.py measure num_traces")
		exit()

	measure										= str(sys.argv[1])
	num_traces									= str(sys.argv[2])
	type_pretty									= []
	vaccinated_students_perc					= ["0", "10", "40"]#, "70"]
	type_of_stats								= ["mean", "variance", "left", "right"]
	columns										= ['day', 'susceptible', 'exposed', 'infected',
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
		
	my_plot										= None
	df_plot										= None
	
	for type_of_stat in type_of_stats:
		paths_num_traces						= []
		paths_1000								= []
		for perc in vaccinated_students_perc:
			paths_num_traces.append(Path(__file__).parent / ("../../mean-results/StochasticArrivals/WithExtScreening/Prob-0.001/WithCountermeasures/WithVaccinatedStudents/D1/Monday/" + type_of_stat + "_" + perc + "_D1_Monday-" + num_traces + ".csv"))
			paths_1000.append(Path(__file__).parent / ("../../mean-results/StochasticArrivals/WithExtScreening/Prob-0.001/WithCountermeasures/WithVaccinatedStudents/D1/Monday/" + type_of_stat + "_" + perc + "_D1_Monday-1000.csv"))
			type_pretty.append(perc + "%")

		k											= 0

		for path_num_traces, path_1000 in zip(paths_num_traces, paths_1000):
			df_mean_num_traces        				= pandas.read_csv(str(path_num_traces), index_col=0)
			df_mean_num_traces.columns				= columns

			df_mean_1000        					= pandas.read_csv(str(path_1000), index_col=0)
			df_mean_1000.columns 					= columns


			diff		 							= pandas.DataFrame(columns=['day', measure])
			diff['day']								= df_mean_num_traces.loc[:, 'day']
			diff[measure]							= df_mean_num_traces.loc[:, measure] - df_mean_1000.loc[:, measure]

			df_mod 									= diff
			df_mod['type'] 							= measure
			df_mod['stat']							= type_of_stat
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
 		+ aes(x = 'day', y = measure, color = 'type_pretty') \
 		+ geom_line() \
    	+ labs(title = "Comparison (difference of " + measure + ", " + num_traces + "-1000)", x = 'day', y = measure, color = 'Percentages of vaccination')) \
    	+ scale_x_continuous(breaks=[0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]) \
    	+ facet_wrap('stat', scales = 'free_y') \
    	+ theme(plot_title = element_text(face="bold"), axis_title_x  = element_text(face="bold"), axis_title_y = element_text(face="bold"), legend_title = element_text(face="bold"), subplots_adjust={'wspace': 0.25})

	my_plot.save('../../plot-ggplot2/StochasticArrivals/WithExtScreening/Prob-0.001/WithCountermeasures/WithVaccinatedStudents/D1/Monday/Comparison/plot_comparison-' + num_traces + '-1000_' + measure, dpi=600)
	df_plot.to_csv('../../plot-ggplot2/StochasticArrivals/WithExtScreening/Prob-0.001/WithCountermeasures/WithVaccinatedStudents/D1/Monday/Comparison/plot_comparison-' + num_traces + '-1000_' + measure + '.csv')

main();