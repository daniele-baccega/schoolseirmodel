#!/bin/bash

echo "Running the command: run-ggplot2-mean-days.py $@"
python3 run-ggplot2-mean-days.py "$@"


if ! [[ $1 == *"WithVaccinatedStudents"* ]] && ! [[ $1 == *"OldPolicyvsNewPolicy"* ]] && ! [[ $1 == *"WithoutCountermeasures"* ]]; then
  echo "Running the command: run-ggplot2-single-plot-days.py $@"
  python3 run-ggplot2-single-plot-days.py "$@"
  echo "Running the command: run-ggplot2-infected-days.py $@"
  python3 run-ggplot2-infected-days.py "$@"
  echo "Running the command: run-ggplot2-cumulative-infected-days.py $@"
  python3 run-ggplot2-cumulative-infected-days.py "$@"
  echo "Running the command: run-ggplot2-new-infected-days.py $@"
  python3 run-ggplot2-new-infected-days.py "$@"
fi