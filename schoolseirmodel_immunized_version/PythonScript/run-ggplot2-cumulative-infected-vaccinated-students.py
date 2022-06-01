import os
import sys
import pandas
import numpy
from plotnine import *
from pathlib import Path
from statsmodels.tsa.seasonal import seasonal_decompose

def main():
	if len(sys.argv) < 6:
		print("Error, parameters are missing: python run-ggplot2-cumulative-infected-vaccinated-students.py path policy day_name num_traces type_of_screening")
		exit()

	long_path											= str(sys.argv[1])
	policy												= str(sys.argv[2])
	day_name 											= str(sys.argv[3])
	num_traces											= str(sys.argv[4])
	type_of_screening									= str(sys.argv[5])
	paths												= []
	type_pretty											= []
	vaccinated_students_perc							= ["0", "10", "40", "70"]

	for vaccinated_students in vaccinated_students_perc:
		if policy == "WithoutScreening":
			paths.append(Path(__file__).parent / ("../mean-results/" + long_path + "/" + policy + "/mean_" + vaccinated_students + "_" + policy + "_" + num_traces + ".csv"))
		else:
			paths.append(Path(__file__).parent / ("../mean-results/" + long_path + "/" + policy + "/" + day_name + "/mean_" + vaccinated_students + "_" + policy + "_" + day_name + "_" + type_of_screening + "_" + num_traces + ".csv"))
		type_pretty.append(vaccinated_students + "%")
		
	my_plot												= None
	my_plot_derivative									= None
	my_plot_derivative_spline							= None
	df_plot												= None
	df_plot_derivative									= None
	df_plot_derivative_spline							= None
	k													= 0
	
	for path in paths:
		df_mean        	  								= pandas.read_csv(str(path), index_col=0)

		population										= df_mean.loc[0, 'susceptible'] + df_mean.loc[0, 'num-immunized']

		total_infected 									= pandas.DataFrame(columns=['day', 'cumulative_infected'])
		total_infected_derivative 						= pandas.DataFrame(columns=['day', 'slope'])
		total_infected_derivative_spline				= pandas.DataFrame(columns=['day', 'values', 'values_type'])
		
		total_infected['day']							= df_mean.loc[:, 'day']
		total_infected['cumulative_infected'] 			= (population - (df_mean.loc[:, 'susceptible'] + df_mean.loc[:, 'susceptible-in-quarantine'] + df_mean.loc[:, 'susceptible-in-quarantine-external-1'] + df_mean.loc[:, 'susceptible-in-quarantine-external-2'] +\
														 	         	 df_mean.loc[:, 'exposed'] + df_mean.loc[:, 'exposed-in-quarantine'] + df_mean.loc[:, 'exposed-in-quarantine-external-1'] + df_mean.loc[:, 'exposed-in-quarantine-external-2'] + df_mean.loc[:, 'num-immunized'] + df_mean.loc[:, 'num-immunized-in-quarantine'] + df_mean.loc[:, 'num-immunized-in-quarantine-external-1'] + df_mean.loc[:, 'num-immunized-in-quarantine-external-2']))
		total_infected 									= total_infected.iloc[1:]

		total_infected_derivative['day']				= df_mean.loc[:, 'day']
		total_infected_derivative['slope']				= pandas.Series(numpy.gradient(total_infected.loc[:, 'cumulative_infected']))
		

		num_days										= len(df_mean.loc[:, 'day'])

		decomposition									= seasonal_decompose(total_infected_derivative.loc[0:(num_days-2), 'slope'], model='multiplicable', period=7)
		
		total_infected_derivative_spline['day']			= df_mean.loc[:, 'day'].append(df_mean.loc[:, 'day'], ignore_index=True).append(df_mean.loc[:, 'day'], ignore_index=True).append(df_mean.loc[:, 'day'], ignore_index=True)
		total_infected_derivative_spline['values']		= total_infected_derivative['slope'].append(decomposition.trend, ignore_index=True).append(decomposition.seasonal, ignore_index=True).append(decomposition.resid, ignore_index=True)
		total_infected_derivative_spline['values_type']	= pandas.Series(numpy.repeat("slope", num_days)).append(pandas.Series(numpy.repeat("trend", num_days)), ignore_index=True).append(pandas.Series(numpy.repeat("seasonal", num_days)), ignore_index=True).append(pandas.Series(numpy.repeat("resid", num_days)), ignore_index=True)



		df_mod 											= total_infected
		df_mod['type'] 									= 'Total infected'
		df_mod['type_pretty'] 							= type_pretty[k]
		if df_plot is None:
			df_plot 									= df_mod
		else:
			df_plot 									= df_plot.append(df_mod, ignore_index=True)

		df_mod_derivative								= total_infected_derivative
		df_mod_derivative['type']	 					= 'Total infected derivative'
		df_mod_derivative['type_pretty']		 		= type_pretty[k]
		if df_plot_derivative is None:
			df_plot_derivative							= df_mod_derivative
		else:
			df_plot_derivative 							= df_plot_derivative.append(df_mod_derivative, ignore_index=True)

		df_mod_derivative_spline						= total_infected_derivative_spline
		df_mod_derivative_spline['type'] 				= 'Total infected derivative spline'
		df_mod_derivative_spline['type_pretty']			= type_pretty[k]
		if df_plot_derivative_spline is None:
			df_plot_derivative_spline					= df_mod_derivative_spline
		else:
			df_plot_derivative_spline 					= df_plot_derivative_spline.append(df_mod_derivative_spline, ignore_index=True)

		k												= k + 1
		

	df_plot_derivative_spline.values_type = pandas.Categorical(df_plot_derivative_spline.values_type, \
										ordered = True, \
										categories = ["slope", "trend", "seasonal", "resid"])

	policy_pretty 										= "D1"

	if policy == "WithoutScreening":
		policy_pretty									= "without screening"

	
	my_plot = (ggplot(df_plot) \
 		+ aes(x = 'day', y = 'cumulative_infected', color = 'type_pretty') \
 		+ geom_line() \
    	+ labs(title = "Students vaccination (" + policy_pretty + " policy)", x = 'day', y = 'cumulative infected', color = 'Percentages of vaccination')) \
    	+ scale_x_continuous(breaks=[0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]) \
    	+ scale_color_manual(values=["#FF0000", "#00FF00", "#0000FF", "#FF00FF"]) \
    	+ theme(plot_title = element_text(face="bold"), axis_title_x  = element_text(face="bold"), axis_title_y = element_text(face="bold"), legend_title = element_text(face="bold"))

	my_plot_derivative = (ggplot(df_plot_derivative) \
 		+ aes(x = 'day', y = 'slope', color = 'type_pretty') \
 		+ geom_line() \
    	+ labs(title = "Students vaccination (" + policy_pretty + " policy)", x = 'day', y = 'slope', color = 'Percentages of vaccination')) \
    	+ scale_x_continuous(breaks=[0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]) \
    	+ scale_color_manual(values=["#FF0000", "#00FF00", "#0000FF", "#FF00FF"]) \
    	+ theme(plot_title = element_text(face="bold"), axis_title_x  = element_text(face="bold"), axis_title_y = element_text(face="bold"), legend_title = element_text(face="bold"))

	my_plot_derivative_spline = (ggplot(df_plot_derivative_spline) \
 		+ aes(x = 'day', y = 'values', color = 'type_pretty') \
 		+ geom_line() \
    	+ labs(title = "Students vaccination (" + policy_pretty + " policy)", x = 'day', y = 'values', color = 'Percentages of vaccination')) \
    	+ scale_x_continuous(breaks=[0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]) \
    	+ facet_wrap('values_type') \
    	+ scale_color_manual(values=["#FF0000", "#00FF00", "#0000FF", "#FF00FF"]) \
    	+ theme(plot_title = element_text(face="bold"), axis_title_x  = element_text(face="bold"), axis_title_y = element_text(face="bold"), legend_title = element_text(face="bold"))

	day_name 											= "/" + day_name

	if policy == "WithoutScreening":
		day_name 										= ""

	my_plot.save('../plot-ggplot2/' + long_path + '/' + policy + day_name + '/plot_cumulative_infected', dpi=600)
	df_plot.to_csv('../plot-ggplot2/' + long_path + '/' + policy + day_name + '/plot_cumulative_infected.csv')

	my_plot_derivative.save('../plot-ggplot2/' + long_path + '/' + policy + day_name + '/plot_cumulative_infected_derivative', dpi=600)
	df_plot_derivative.to_csv('../plot-ggplot2/' + long_path + '/' + policy + day_name + '/plot_cumulative_infected_derivative.csv')

	my_plot_derivative_spline.save('../plot-ggplot2/' + long_path + '/' + policy + day_name + '/plot_cumulative_infected_derivative_spline', dpi=600)
	df_plot_derivative_spline.to_csv('../plot-ggplot2/' + long_path + '/' + policy + day_name + '/plot_cumulative_infected_derivative_spline.csv')

main();