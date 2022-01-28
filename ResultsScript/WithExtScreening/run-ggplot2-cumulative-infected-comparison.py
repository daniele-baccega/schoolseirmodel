import os
import sys
import pandas
from plotnine import *
from pathlib import Path

def main():
	if len(sys.argv) < 2:
		print("Error, parameters are missing: python run-ggplot2-cumulative-infected-comparison.py path")
		exit()

	long_path									= str(sys.argv[1])
	n											= 36
	paths										= []
	type_of_npis_pretty							= []

	paths.append(Path(__file__).parent / ("../../mean-results/" + long_path + "/WithCountermeasures/WithoutVaccinatedInfectious/WithoutScreening/mean_WithoutScreening.csv"))
	paths.append(Path(__file__).parent / ("../../mean-results/" + long_path + "/WithoutCountermeasures/WithoutVaccinatedInfectious/WithoutScreening/mean_WithoutScreening.csv"))
	type_of_npis_pretty.append("With NPIs")
	type_of_npis_pretty.append("Without NPIs")
		
	my_plot										= None
	df_plot										= None
	k											= 0
	population									= 240
	
	for path in paths:
		df_mean          						= pandas.read_csv(str(path), index_col=0)

		total_infected 							= pandas.DataFrame(columns=['day', 'cumulative_infected'])
		
		total_infected['day'] 					= df_mean.loc[:, 'day']
		total_infected['cumulative_infected'] 	= population - (df_mean.loc[:, 'susceptible'] + df_mean.loc[:, 'susceptible-in-quarantine'] + df_mean.loc[:, 'susceptible-in-quarantine-external-1'] + df_mean.loc[:, 'susceptible-in-quarantine-external-2'] + \
														        df_mean.loc[:, 'exposed'] + df_mean.loc[:, 'exposed-in-quarantine'] + df_mean.loc[:, 'exposed-in-quarantine-external-1'] + df_mean.loc[:, 'exposed-in-quarantine-external-2'])

		total_infected 							= total_infected.iloc[1:]

		df_mod 									= total_infected
		df_mod['type'] 							= 'Total infected'
		df_mod['type_of_npis_pretty'] 			= type_of_npis_pretty[k]
		if df_plot is None:
			df_plot 							= df_mod
		else:
			df_plot 							= df_plot.append(df_mod, ignore_index=True)

		k										= k + 1
								      		        
	df_plot.type_of_npis_pretty = pandas.Categorical(df_plot.type_of_npis_pretty, \
							   		    ordered = True, \
							   		    categories = ["With NPIs", "Without NPIs"])

	my_plot = (ggplot(df_plot) \
		+ aes(x='day', y = 'cumulative_infected', color = 'type', linetype = 'type_of_npis_pretty') \
		+ geom_line() \
		+ geom_hline(yintercept=240, linetype="dotted") \
    	+ labs(title = "Impact of NPIs", x = 'day', y = 'cumulative infected', color = 'Agent type', linetype = 'NPIs')) \
    	+ scale_color_manual(values=['#990000']) \
    	+ scale_x_continuous(breaks=[0, 5, 10, 15, 20, 25, 30, 35]) \
    	+ theme(plot_title = element_text(face="bold"), axis_title_x  = element_text(face="bold"), axis_title_y = element_text(face="bold"), legend_title = element_text(face="bold"))
		
	my_plot.save('../../plot-ggplot2/' + long_path + '/ComparisonWithAndWithoutCountermeasures/plot_cumulative-infected-comparison', dpi=600)
	df_plot.to_csv('../../plot-ggplot2/' + long_path + '/ComparisonWithAndWithoutCountermeasures/plot-file/plot_cumulative-infected-comparison.csv')
main();
