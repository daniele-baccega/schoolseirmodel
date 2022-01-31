import os
import sys
import pandas
from plotnine import *
from pathlib import Path

def main():
	if len(sys.argv) < 3:
		print("Error, parameters are missing: python run-ggplot2-positive-comparison.py path num_traces")
		exit()

	long_path												= str(sys.argv[1])
	num_traces												= str(sys.argv[2])
	types_of_screening										= ["Screening25", "Screening50", "Screening100"]
	types_of_screening_pretty								= ["Screening 25%", "Screening 50%", "Screening 100%"]
	policies												= ["A1", "D1", "D2"]
	policies_pretty											= ["A1", "D1", "D2"]

	my_plot													= None
	df_plot													= None
	j														= 0

	for policy in policies:
		k													= 0
		for type_of_screening in types_of_screening:
			path 											= Path(__file__).parent / ("../mean-results/" + long_path + "/" + policy + "/mean-days/mean_" + policy + "_" + type_of_screening + "_" + num_traces + "_mean-days.csv")
			
			df_mean          								= pandas.read_csv(str(path), index_col=0)

			positive_screened								= pandas.DataFrame(columns=['day', 'fraction'])
			positive_screened['day'] 						= df_mean.loc[:, 'day']
			positive_screened['fraction']					= df_mean['num-of-positive-students'] / df_mean['num-of-screened-students']

			positive_screened								= positive_screened.loc[1:, :]

			df_mod 											= positive_screened
			df_mod['policy'] 								= policies_pretty[j]
			df_mod['screening'] 							= types_of_screening_pretty[k]
			if df_plot is None:
				df_plot 									= df_mod
			else:
				df_plot 									= df_plot.append(df_mod, ignore_index=True)

			k												= k + 1

		j													= j + 1
								      		        
	df_plot.group = pandas.Categorical(df_plot.policy, \
							   		   ordered = True, \
							   		   categories = ["A1", "D1", "D2"])
								      		        
	df_plot.screening = pandas.Categorical(df_plot.screening, \
							   		    ordered = True, \
							   		    categories = ["Screening 100%", "Screening 50%", "Screening 25%"])

	my_plot = (ggplot(df_plot) \
		+ aes(x='day', y = 'fraction', color = 'policy') \
    	+ geom_line() \
    	+ labs(title = "Comparison between policies", x = 'day', y = 'positive discovered / screened', color = 'screening')) \
    	+ facet_wrap('screening', nrow=1, ncol=3) \
    	+ theme(subplots_adjust = {'wspace': 0.25}) \
    	+ scale_x_continuous(breaks=[0, 5, 10, 15, 20, 25, 30, 35])
		
	my_plot.save('../plot-ggplot2/' + long_path + '/ComparisonBetweenPolicies/plot-positive-comparison', dpi=600)
	df_plot.to_csv('../plot-ggplot2/' + long_path + '/ComparisonBetweenPolicies/plot-file/plot-positive-comparison.csv')

main();