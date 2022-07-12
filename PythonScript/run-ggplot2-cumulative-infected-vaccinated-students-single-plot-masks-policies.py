import os
import sys
import pandas
import numpy
from plotnine import *
from pathlib import Path
from statsmodels.tsa.seasonal import seasonal_decompose

def main():
	if len(sys.argv) < 4:
		print("Error, parameters are missing: python run-ggplot2-cumulative-infected-vaccinated-students.py path num_traces type_of_screening")
		exit()

	long_path																= str(sys.argv[1])
	num_traces																= str(sys.argv[2])
	type_of_screening														= str(sys.argv[3])
	quarantine_policies														= ["NovDecPolicy", "JanFebPolicy", "NoQuarantinePolicy"]
	quarantine_policies_pretty												= ["Nov/Dec", "Jan/Feb", "Without quarantine policy"]
	virus_prevalence														= ["Prob-0.001", "Prob-0.02", "Prob-0.046"]
	virus_prevalence_pretty													= ["Low", "Medium", "High"]
	vaccine_efficacy														= ["Vaccine Efficacy 100", "Vaccine Efficacy 70", "Vaccine Efficacy 50"]
	policies																= ["D1", "Without Screening"]
	mask_policies															= ["No Mask", "No Mask - FFP2", "Surg - FFP2"]
	day_name					 											= "Monday"
	vaccinated_students_perc												= ["0", "10", "40", "70"]
	cut																		= 3
	period																	= 7
	j																		= 0

	for quarantine_policy in quarantine_policies:
		for policy in policies:	
			if policy == "D1" and quarantine_policy in ["JanFebPolicy", "NoQuarantinePolicy"]:
				continue

			for mask_policy in mask_policies:
				if (policy == "D1" and mask_policy in ["No Mask - FFP2", "Surg - FFP2"]) or quarantine_policy == "NoQuarantinePolicy" and mask_policy in ["No Mask - FFP2", "Surg - FFP2"]:
					continue

				my_plot														= None
				my_plot_derivative											= None
				my_plot_derivative_spline									= None
				df_plot														= None
				df_plot_derivative											= None
				df_plot_derivative_spline									= None
				
				for efficacy in vaccine_efficacy:
					i 														= 0
					for prevalence in virus_prevalence:
						paths												= []
						type_pretty											= []
						for vaccinated_students in vaccinated_students_perc:
							if policy == "Without Screening":
								paths.append(Path(__file__).parent / ("../mean-results/" + long_path + "/" + prevalence + "/WithCountermeasures/WithVaccinatedStudents/" + quarantine_policy + "/Omicron/" + mask_policy.replace(" ", "").replace("-", "") + "/" + efficacy.replace(" ", "") + "/" + policy.replace(" ", "") + "/mean_" + vaccinated_students + "_WithoutScreening_" + num_traces + ".csv"))
							else:
								paths.append(Path(__file__).parent / ("../mean-results/" + long_path + "/" + prevalence + "/WithCountermeasures/WithVaccinatedStudents/" + quarantine_policy + "/Omicron/" + mask_policy.replace(" ", "").replace("-", "") + "/" + efficacy.replace(" ", "") + "/" + policy.replace(" ", "") + "/Monday/mean_" + vaccinated_students + "_D1_Monday_" + type_of_screening + "_" + num_traces + ".csv"))
							type_pretty.append(vaccinated_students + "%")
							
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

							decomposition									= seasonal_decompose(total_infected_derivative.loc[0:(num_days-cut), 'slope'], model='additive', period=period)
							
							total_infected_derivative_spline['day']			= df_mean.loc[:, 'day'].append(df_mean.loc[:, 'day'], ignore_index=True).append(df_mean.loc[:, 'day'], ignore_index=True).append(df_mean.loc[:, 'day'], ignore_index=True)
							total_infected_derivative_spline['values']		= total_infected_derivative['slope'].append(decomposition.trend, ignore_index=True).append(decomposition.seasonal, ignore_index=True).append(decomposition.resid, ignore_index=True)
							total_infected_derivative_spline['values_type']	= pandas.Series(numpy.repeat("slope", num_days)).append(pandas.Series(numpy.repeat("trend", num_days)), ignore_index=True).append(pandas.Series(numpy.repeat("seasonal", num_days)), ignore_index=True).append(pandas.Series(numpy.repeat("resid", num_days)), ignore_index=True)



							df_mod 											= total_infected
							df_mod['type'] 									= 'Total infected'
							df_mod['type_pretty'] 							= type_pretty[k]
							df_mod['vaccine_efficacy']						= efficacy + "%"
							df_mod['prevalence']							= virus_prevalence_pretty[i]
							if df_plot is None:
								df_plot 									= df_mod
							else:
								df_plot 									= df_plot.append(df_mod, ignore_index=True)

							df_mod_derivative								= total_infected_derivative
							df_mod_derivative['type']	 					= 'Total infected derivative'
							df_mod_derivative['type_pretty']		 		= type_pretty[k]
							df_mod_derivative['vaccine_efficacy']			= efficacy + "%"
							df_mod_derivative['prevalence']					= virus_prevalence_pretty[i]
							if df_plot_derivative is None:
								df_plot_derivative							= df_mod_derivative
							else:
								df_plot_derivative 							= df_plot_derivative.append(df_mod_derivative, ignore_index=True)
							
							df_mod_derivative_spline						= total_infected_derivative_spline.loc[total_infected_derivative_spline['day'] <= num_days-cut, :]
							df_mod_derivative_spline['type'] 				= 'Total infected derivative spline'
							df_mod_derivative_spline['type_pretty']			= type_pretty[k]
							df_mod_derivative_spline['vaccine_efficacy']	= efficacy + "%"
							df_mod_derivative_spline['prevalence']			= virus_prevalence_pretty[i]
							if df_plot_derivative_spline is None:
								df_plot_derivative_spline					= df_mod_derivative_spline
							else:
								df_plot_derivative_spline 					= df_plot_derivative_spline.append(df_mod_derivative_spline, ignore_index=True)

							k												= k + 1

						i 													= i + 1

				df_plot.type_pretty = pandas.Categorical(df_plot.type_pretty, \
													ordered = True, \
													categories = ["0%", "10%", "40%", "70%"])

				df_plot.vaccine_efficacy = pandas.Categorical(df_plot.vaccine_efficacy, \
													ordered = True, \
													categories = ["Vaccine Efficacy 100%", "Vaccine Efficacy 70%", "Vaccine Efficacy 50%"])
				
				df_plot.prevalence = pandas.Categorical(df_plot.prevalence, \
													ordered = True, \
													categories = ["Low", "Medium", "High"])

				df_plot_derivative.type_pretty = pandas.Categorical(df_plot_derivative.type_pretty, \
													ordered = True, \
													categories = ["0%", "10%", "40%", "70%"])

				df_plot_derivative.vaccine_efficacy = pandas.Categorical(df_plot_derivative.vaccine_efficacy, \
													ordered = True, \
													categories = ["Vaccine Efficacy 100%", "Vaccine Efficacy 70%", "Vaccine Efficacy 50%"])
				
				df_plot_derivative.prevalence = pandas.Categorical(df_plot_derivative.prevalence, \
													ordered = True, \
													categories = ["Low", "Medium", "High"])


				df_plot_derivative_spline.type_pretty = pandas.Categorical(df_plot_derivative_spline.type_pretty, \
													ordered = True, \
													categories = ["0%", "10%", "40%", "70%"])

				df_plot_derivative_spline.vaccine_efficacy = pandas.Categorical(df_plot_derivative_spline.vaccine_efficacy, \
													ordered = True, \
													categories = ["Vaccine Efficacy 100%", "Vaccine Efficacy 70%", "Vaccine Efficacy 50%"])
				
				df_plot_derivative_spline.prevalence = pandas.Categorical(df_plot_derivative_spline.prevalence, \
													ordered = True, \
													categories = ["Low", "Medium", "High"])

				df_plot_derivative_spline = df_plot_derivative_spline[df_plot_derivative_spline['values_type'] == "trend"]
				
				
				my_plot = (ggplot(df_plot) \
			 		+ aes(x = 'day', y = 'cumulative_infected', color = 'type_pretty') \
			 		+ geom_line() \
			 		+ facet_grid('prevalence ~ vaccine_efficacy') \
			    	+ labs(title = quarantine_policies_pretty[j] + ", " + policy + " (" + mask_policy + ")", x = 'day', y = 'cumulative infected', color = 'Percentages of students vaccination')) \
			    	+ scale_x_continuous(breaks=[0, 10, 20, 30, 40, 50, 60]) \
			    	+ scale_color_manual(values=["#FF0000", "#00FF00", "#0000FF", "#FF00FF"]) \
			    	+ theme(plot_title = element_text(face="bold"), axis_title_x  = element_text(face="bold"), axis_title_y = element_text(face="bold"), legend_title = element_text(face="bold"))

				my_plot_derivative = (ggplot(df_plot_derivative) \
			 		+ aes(x = 'day', y = 'slope', color = 'type_pretty') \
			 		+ geom_line() \
			 		+ facet_grid('prevalence ~ vaccine_efficacy') \
			    	+ labs(title = quarantine_policies_pretty[j] + ", " + policy + " (" + mask_policy + ")", x = 'day', y = 'slope', color = 'Percentages of students vaccination')) \
			    	+ scale_x_continuous(breaks=[0, 10, 20, 30, 40, 50, 60]) \
			    	+ scale_color_manual(values=["#FF0000", "#00FF00", "#0000FF", "#FF00FF"]) \
			    	+ theme(plot_title = element_text(face="bold"), axis_title_x  = element_text(face="bold"), axis_title_y = element_text(face="bold"), legend_title = element_text(face="bold"))

				my_plot_derivative_spline = (ggplot(df_plot_derivative_spline) \
			 		+ aes(x = 'day', y = 'values', color = 'type_pretty') \
			 		+ geom_line() \
			 		+ facet_grid('prevalence ~ vaccine_efficacy') \
			    	+ labs(title = quarantine_policies_pretty[j] + ", " + policy + " (" + mask_policy + ")", x = 'day', y = 'trend', color = 'Percentages of students vaccination')) \
			    	+ scale_x_continuous(breaks=[0, 10, 20, 30, 40, 50, 60]) \
			    	+ scale_color_manual(values=["#FF0000", "#00FF00", "#0000FF", "#FF00FF"]) \
			    	+ ylim(0, 30) \
			    	+ theme(plot_title = element_text(face="bold"), axis_title_x  = element_text(face="bold"), axis_title_y = element_text(face="bold"), legend_title = element_text(face="bold"))

				my_plot.save('../plot-ggplot2/' + long_path + '/plot_' + quarantine_policy + '_' + policy.replace(" ", "") + '_' + mask_policy.replace(" ", "").replace("-", "") + '_cumulative', dpi=600)
				df_plot.to_csv('../plot-ggplot2/' + long_path + '/plot_' + quarantine_policy + '_' + policy.replace(" ", "") + '_' + mask_policy.replace(" ", "").replace("-", "") + '_cumulative.csv')

				my_plot_derivative.save('../plot-ggplot2/' + long_path + '/plot_' + quarantine_policy + '_' + policy.replace(" ", "") + '_' + mask_policy.replace(" ", "").replace("-", "") + '_slope', dpi=600)
				df_plot_derivative.to_csv('../plot-ggplot2/' + long_path + '/plot_' + quarantine_policy + '_' + policy.replace(" ", "")+ '_' + mask_policy.replace(" ", "").replace("-", "") + '_slope.csv')

				my_plot_derivative_spline.save('../plot-ggplot2/' + long_path + '/plot_' + quarantine_policy + '_' + policy.replace(" ", "") + '_' + mask_policy.replace(" ", "").replace("-", "") + '_trend', dpi=600)
				df_plot_derivative_spline.to_csv('../plot-ggplot2/' + long_path + '/plot_' + quarantine_policy + '_' + policy.replace(" ", "") + '_' + mask_policy.replace(" ", "").replace("-", "") + '_trend.csv')

		j																	= j + 1

main();