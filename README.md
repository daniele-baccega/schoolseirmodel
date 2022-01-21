## INTRODUCTION
Many governments enforced physical distancing measures to control the spread of **COVID-19** to avoid the collapse of fragile and overloaded health care systems. Following the physical distancing measures, the closures of schools seemed unavoidable to control and reduce the transmission of the pathogen, given the potentially high-risk settings of these environments. Nevertheless, leaving the closure of schools as an extreme and last resource is a top priority of governments, therefore different non-pharmaceutical interventions in the school settings were implemented to reduce the risk of transmission. Through a detailed Agent-Based Model simulation experiment [1, 5], we study the efficacy of active surveillance strategies in the school environment. Simulations settings employed in the experiments provide hypothetical although realistic scenarios which allow us to identify the most suitable control strategy according to the viral circulation period to avoid massive school closures. The significance of risk reduction through the policies assessed in this work is relevant for public health authorities and school administrators.

## WHAT IS IT?
This is an **Agent-Based Model (ABM)**, developed in the multi-agent programmable modeling environment **NetLogo version 6.1.1** [2], to study the spread of COVID-19 infections within an explanatory scholastic environment, and to evaluate in such an environment the effectiveness of non-pharmaceutical interventions (NPIs), such as distancing requirements, screening testing, and environment ventilation.
The model components are:

- The environment including both physical spaces and social contact structure of the population;
- The COVID-19 progression model;
- The NPIs’ logic modeled to contain the COVID-19 spread.

The modeled environment is a school constituted of at most 12 classrooms (arranged on three floors), shared spaces (i.e. entrance, gym, hallways, bathrooms, stairs, medical room, teachers’ office, and principal’s office). In detail, each floor consists of one hallway that connects all the rooms and one bathroom only for the students. The school entrance, the medical room, the gym, the principal’s office, the teachers’ office and the teachers’ bathroom are on the first floor. Moreover, each classroom is characterized by twenty desks (rightly distanced from each other), one teacher desk, and the blackboard.

## HOW IT WORKS
There are four different types of agents: _students_, _teachers_, _principals_ and _janitors_.
In particular:

- _Students_ can go to their classroom, to the students' bathroom on the same floor of their classroom, to the principal's office, to the gym, to the hallways, etc.
- _Teachers_ can go to the classrooms, to the teacher's room, to the teachers' bathroom on the ground floor, to the hallways, etc.
- _Principals_ can go to the principal's office, to the teachers' bathroom on the ground floor, to the hallways etc.
- _Janitors_ can go to the medical room, to the teachers' bathroom, to che hallways etc.

There are two different contagion models:

- _Aerosol_ [3]: accumulation of quanta concentration in the main places and of quanta inhaled for each agent. Type of ventilation used: 3 ACH (Air Changes per Hour)<sup>1</sup>. 
- _Contact_ [4]: accumulation of the contact time among a susceptible agent and an infected one. We considered a contact area of 2.1 * 2.1 m<sup>2</sup>}.

<sup>1</sup> Air Changes per Hour (ACH) means that in 1 hour 300.000 L (or analogous 300 m<sup>2</sup>) of external air are entered into the considere room.

## HOW TO USE IT (on Linux)
At first, you need to download [**NetLogo 6.1.1**](https://ccl.northwestern.edu/netlogo/6.1.1/).

After that, to run a configuration you need to create a configuration file (with .conf extension) specifying the values to assign for each (or for some) parameters (described below). In the _ExampleOfConfigurationFile_ directory you can find some examples of configuration files. After that, you can run the configuration in this way (**it's necessary to specify the correct path to netlogo-headless.sh into the start.sh script, for example \~/NetLogo6.1.1/netlogo-headless.sh**):
```
./start.sh ConfigurationFileName NumberOfThreads
```
For example:
```
./start.sh ExampleOfConfigurationFile/Example1.conf 24
```

----

There are lots of parameters in this model. Here I describe the parameters that you can modify in the _Interface Tab_:

- _students-per-classroom_: number of students for each classroom.
- _num-floors_: number of school's floors.
- _num-classrooms-per-floor_: number of classrooms for each floor. The total number of classrooms is equal to _num-floors_ * _num-classrooms-per-floor_ (minimum 1, maximum 12).
- _init-infected_: initial number of infected agents.
- _init-infected-type_: the _init-infected_ will be of this type (_anyone_, _students_, _teachers_, _principals_ or _janitors_).
- _num-groups_: number of groups in which the classrooms are divided (1 not staggered admissions, 2 staggered admissions).
- _mean-incubation-duration-in-days_: average number of incubation days.
- _mean-infection-duration-in-days_: average number of infection days.
- _num-of-quarantine-days_: number of quarantine days.
- _dad-%_: percentage of distance learning.
- _prob-go-bathroom_: probability to go to the bathroom.
- _prob-go-blackboard_: probability to go to the blackboard.
- _prob-go-somewhere-during-interval_: probability to go somewhere during the interval.
- _prob-go-principal_: probability to go to the principal's office.
- _prob-old-teachers_: probability that a teacher belongs to the _old_ category.
- _prob-old-janitor_: probability that a janitor belongs to the _old_ category.
- _prob-outside-contagion-young_: probability that an agent that belongs to the _young_ category gets the infection outside the school.
- _prob-outside-contagion-regular_: probability that an agent that belongs to the _regular_ category gets the infection outside the school.
- _prob-outside-contagion-old_: probability that an agent that belongs to the _old_ category gets the infection outside the school.
- _prob-symptomatic-young_: probability to show symptoms when a _young_ agent becomes infected.
- _prob-symptomatic-regular_: probability to show symptoms when a _regular_ agent becomes infected.
- _prob-symptomatic-old_: probability to show symptoms when a _old_ agent becomes infected.
- _prob-external-screening-1_: probability to swab a student outside the school because this student follows activities that involve screening campaings.
- _prob-external-screening-2_: probability to swab an infected students outside the school.
- _lesson-duration-in-minutes_: duration of a single lesson in minutes.
- _days-of-simulation_: number of simulation days for each execution of the simulator.
- _run#_: unique identifier of the running execution.
- _tick-duration-in-seconds_: NetLogo temporal tick.
- _results-dir-name_: name of the results' directory.
- _temperature-measurement_: temperature measurement type (at the entrance).
- _ventilation-type-h-1_: ventilation type implemented in all rooms but not in the hallways.
- _mask-type_: mask type used by agents.
- _fraction-of-population-wearing-mask_: fraction of all agents that use the mask.
- _whole-classroom-quarantined?_: we can use two diffentent _quarantine_ policies:
	- First, if we find an infected student in a classroom, we put the whole classroom in quarantine.
	- Second, if we find an infected student in a classroom, we put only this student in quarantine and we swab all the other students in the same classroom. If we find other _num-infected-needed-to-quarantine-whole-classroom_ - 1 infected students we put the whole classroom in quarantine, otherwise we'll swab again all the other students in the same classroom after _number-of-after-days-special-swab_ days. Again, if we find other _num-infected-needed-to-quarantine-whole-classroom_ - 1 infected we put the whole classroom in quarantine.
- _num-infected-needed-to-quarantine-whole-classroom_: number of infected students needed to quarantine the whole classroom with the second _quarantine_ policy.
- _number-of-after-days-special-swab_: number of days after that, with the second _quarantine_ policy, we swab again all the other students in the same classroom of the infected student that we found.
- _staggered-admissions?_: staggered admissions (with _num-groups_ groups).
- _spaced-desks?_: spaced desks (social distancing).
- _outside-contagion?_: possibility to get the infection outside the school.
- _interval-in-front-of-classroom?_: possibility to go at most in front of their classroom during the interval and not elsewhere (the agents can always go to the bathroom).
- _external-screening?_: external screening (outside tha school).
- _vaccinated-teachers?_: vaccinated teachers (immunized).
- _vaccinated-principals?_: vaccinated principals (immunized).
- _vaccinated-janitors?_: vaccinated janitors (immunized).
- _fraction-of-vaccinated-students_: fraction of vaccinated students.
- _fraction-of-vaccinated-teachers_: fraction of vaccinated teachers.
- _fraction-of-vaccinated-janitors_: fraction of vaccinated janitors.
- _vaccine-efficacy_: vaccine efficacy for vaccinated subjects.
- _screening-policy_: infection control stategy (or screening policy); we consider four different screening policies:
	- **A1**: all every week
	- **D1**: 1/4 of the class every week, in rotation
	- **D2**: 1/4 of the class every week, in rotation, spread over two days of the week
	- **W0**: no screening
- _first-day-of-week_: day of the week on which school's screening takes place; In the case of D2 policy, one half of the group is swabbed on this day.
- _second-day-of-week_: parameter used in the case of the D2 policy; the other half of the group is swabbed on this day.
- _screening-adhesion-%_: percentage of students' adhesion to the screening campaign.

----

Each run produce an output file and for each day we get the following information:

- _day_
- _seedRun_
- _susceptible_
- _exposed_
- _infected_
- _removed_
- _susceptible-in-quarantine_
- _exposed-in-quarantine_
- _infected-in-quarantine_
- _removed-in-quarantine_
- _susceptible-in-quarantine-external-1_
- _exposed-in-quarantine-external-1_
- _infected-in-quarantine-external-1_
- _removed-in-quarantine-external-1_
- _susceptible-in-quarantine-external-2_
- _exposed-in-quarantine-external-2_
- _infected-in-quarantine-external-2_
- _removed-in-quarantine-external-2_
- _num-of-screened-students_
- _num-of-screened-students-external-1_
- _num-of-screened-students-external-2_
- _num-of-positive-students_
- _num-of-positive-students-external-1_
- _num-of-positive-students-external-2_
- _num-vaccinated-susceptible_
- _num-vaccinated-exposed_
- _num-vaccinated-infected_
- _num-vaccinated-removed_
- _num-vaccinated-susceptible-in-quarantine_
- _num-vaccinated-exposed-in-quarantine_
- _num-vaccinated-infected-in-quarantine_
- _num-vaccinated-removed-in-quarantine_
- _num-vaccinated-susceptible-in-quarantine-external-1_
- _num-vaccinated-exposed-in-quarantine-external-1_
- _num-vaccinated-infected-in-quarantine-external-1_
- _num-vaccinated-removed-in-quarantine-external-1_
- _num-vaccinated-susceptible-in-quarantine-external-2_
- _num-vaccinated-exposed-in-quarantine-external-2_
- _num-vaccinated-infected-in-quarantine-external-2_
- _num-vaccinated-removed-in-quarantine-external-2_
- _num-infected-outside_
- _classroom-in-quarantine_
- _num-of-classroom-in-quarantine_
- _classroom-with-at-least-one-infected_

## EXTERNAL INPUT
The model needed some external input files inside a _Utils_ directory:

- **Seed.txt**: this file contains the seed.
- **ClassroomsScheduling.txt**: this file contains the teachers' scheduling on the five weekly days; each teacher has an associated identifier (it's important to not overlap the teachers between different classroom in the same hour). It's necessary to specify the scheduling for each interested classroom and for each day there must be six lessons.
- **StaggeredClassroomsScheduling.txt**: this file contains the teachers' scheduling in the case of staggered admissions.
- **GymTeachers.txt**: this file contains the identifier of the gym teachers.

## EXTENDING THE MODEL
- Fix the measure-temperature function
- Fix the create-supply-teacher function
- Fix the create-supply-janitor function
- Fix the copy-teacher function
- Fix the copy-janitor function
- Introduce some features such as:
	- Possibility of reinfection

## REFERENCES
[1] Daniele Baccega. _SchoolSEIRModel_. _2021_. URL: https://github.com/daniele-baccega/schoolseirmodel.

[2] Wilensky, U. _(1999)_. _NetLogo._ http://ccl.northwestern.edu/netlogo/. Center for Connected Learning and Computer-Based Modeling, Northwestern University, Evanston, IL.

[3] Savvas Gkantonas et al. _airborne.cam: a risk calculator of SARSCoV-2 aerosol transmission under well-mixed ventilation conditions_. _2021_. URL: https://airborne.cam.

[4] Nicolas Hoertel et al. _«A stochastic agent-based model of the SARS-CoV-2 epidemic in France»_. In: _Nature medicine 26.9 (2020)_, pp. 1417–1421.

[5] PAPER JASS

## COPYRIGHT AND LICENSE

Copyright _Daniele Baccega, Simone Pernice, Pietro Terna, Paolo Castagno, Marco Beccuti, Matteo Sereno_

![CC BY-NC-SA 3.0](http://ccl.northwestern.edu/images/creativecommons/byncsa.png)

This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 3.0 License.  To view a copy of this license, visit https://creativecommons.org/licenses/by-nc-sa/3.0/ or send a letter to Creative Commons, 559 Nathan Abbott Way, Stanford, California 94305, USA.
