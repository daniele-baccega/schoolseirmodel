import os
import sys
import pandas
import statistics
from plotnine import *
from pathlib import Path

def main():
	if len(sys.argv) < 5:
		print("Error, parameters are missing: python run-ggplot2-cumulative-infected-vaccinated-students.py path policy day_name type_of_screening")
		exit()

	long_path										= str(sys.argv[1])
	policy											= str(sys.argv[2])
	day_name 										= str(sys.argv[3])
	type_of_screening								= str(sys.argv[4])
	paths											= []
	type_pretty										= []
	vaccinated_students_perc						= ["0", "10", "40", "70"]
	k												= 0
	my_plot											= None
	df_plot											= None

	for vaccinated_students in vaccinated_students_perc:
		if policy == "WithoutScreening":
			paths.append(Path(__file__).parent / ("../Results/" + long_path + "/" + policy + "/Results" + vaccinated_students))
		else:
			paths.append(Path(__file__).parent / ("../Results/" + long_path + "/" + policy + "/Results" + vaccinated_students + day_name + type_of_screening))
		type_pretty.append(vaccinated_students + "%")

				
	for path in paths:
		files										= os.listdir(path)
		counter										= 0

		for file in files:
			df 										= pandas.read_csv(str(path) + "/" + file, sep='\t', index_col=False)

			population								= df.loc[0, 'susceptible']

			total_infected 							= pandas.DataFrame(columns=['day', 'final_infected', 'type_pretty'])

			total_infected['day']					= df.loc[:, 'day']
			total_infected['final_infected']	 	= population - (df.loc[:, 'susceptible'] + df.loc[:, 'susceptible-in-quarantine'] + df.loc[:, 'susceptible-in-quarantine-external-1'] + df.loc[:, 'susceptible-in-quarantine-external-2'] + \
 															        df.loc[:, 'exposed'] + df.loc[:, 'exposed-in-quarantine'] + df.loc[:, 'exposed-in-quarantine-external-1'] + df.loc[:, 'exposed-in-quarantine-external-2'])
			total_infected['type_pretty']			= type_pretty[k]

			if df_plot is None:
				df_plot 							= total_infected
			else:
				df_plot 							= df_plot.append(total_infected, ignore_index=True)

			counter									= counter + 1

		k											= k + 1

	day_name 										= "/" + day_name

	if policy == "WithoutScreening":
		day_name 									= ""

	df_plot = df_plot[df_plot.day == 60]
	df_plot.to_csv('../plot-ggplot2/' + long_path + '/' + policy + day_name + '/plot_final_infected_distribution.csv')

	policy_pretty 									= "D1"

	if policy == "WithoutScreening":
		policy_pretty								= "without screening"

	vaccine_efficacy								= long_path[-2:]

	if vaccine_efficacy == "00":
		vaccine_efficacy							= long_path[-3:]
	
	my_plot = (ggplot(df_plot) \
		+ aes(x = 'final_infected') \
		+ geom_histogram(aes(y = '..density..'), color="black", bins = 70) \
		+ facet_wrap('type_pretty', scales = 'free_y') \
		+ labs(title = "Final infected distribution (" + policy_pretty + " policy, vaccine efficacy " + vaccine_efficacy + "%)", x = 'final infected', y = 'density') \
		+ geom_density(alpha=.2, fill="#FF0000") \
		+ theme(subplots_adjust={'wspace': 0.25}, plot_title = element_text(face="bold"), axis_title_x  = element_text(face="bold"), axis_title_y = element_text(face="bold"), legend_title = element_text(face="bold")))

	my_plot.save('../plot-ggplot2/' + long_path + '/' + policy + day_name + '/plot_final_infected_distribution', dpi=600)

main();