#!/bin/bash

echo "Running the command: run-ggplot2-mean.py $@"
python3 run-ggplot2-mean.py "$@"


if ! [[ $1 == *"WithVaccinatedStudents"* ]] && ! [[ $1 == *"NovDecPolicyvsOldPolicy"* ]] && ! [[ $1 == *"WithoutCountermeasures"* ]]; then
  echo "Running the command: run-ggplot2-single-plot.py $@"
  python3 run-ggplot2-single-plot.py "$@"
  echo "Running the command: run-ggplot2-infected.py $@"
  python3 run-ggplot2-infected.py "$@"
  echo "Running the command: run-ggplot2-cumulative-infected.py $@"
  python3 run-ggplot2-cumulative-infected.py "$@"
  echo "Running the command: run-ggplot2-new-infected.py $@"
  python3 run-ggplot2-new-infected.py "$@"
fi