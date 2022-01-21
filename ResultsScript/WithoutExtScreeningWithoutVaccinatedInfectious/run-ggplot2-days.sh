#!/bin/bash
python3 run-ggplot2-mean-days.py "$@"
python3 run-ggplot2-single-plot-days.py "$@"
python3 run-ggplot2-infected-days.py "$@"
python3 run-ggplot2-cumulative-infected-days.py "$@"
python3 run-ggplot2-new-infected-days.py "$@"