#!/bin/bash
./run-ggplot2-days.sh StochasticArrivals/WithExtScreening/Prob-0.0001/WithCountermeasures A1 WithoutScreening Screening25 Screening50 Screening100

./run-ggplot2-days.sh StochasticArrivals/WithExtScreening/Prob-0.0001/WithCountermeasures D1 WithoutScreening Screening25 Screening50 Screening100

./run-ggplot2-days.sh StochasticArrivals/WithExtScreening/Prob-0.0001/WithCountermeasures D2 WithoutScreening Screening25 Screening50 Screening100

python3 run-ggplot2-positive-comparison.py StochasticArrivals/WithExtScreening/Prob-0.0001/WithCountermeasures


./run-ggplot2-days.sh StochasticArrivals/WithExtScreening/Prob-0.001/WithCountermeasures A1 WithoutScreening Screening25 Screening50 Screening100

./run-ggplot2-days.sh StochasticArrivals/WithExtScreening/Prob-0.001/WithCountermeasures D1 WithoutScreening Screening25 Screening50 Screening100

./run-ggplot2-days.sh StochasticArrivals/WithExtScreening/Prob-0.001/WithCountermeasures D2 WithoutScreening Screening25 Screening50 Screening100

python3 run-ggplot2-positive-comparison.py StochasticArrivals/WithExtScreening/Prob-0.001/WithCountermeasures


./run-ggplot2-days.sh StochasticArrivals/WithExtScreening/Prob-0.01/WithCountermeasures A1 WithoutScreening Screening25 Screening50 Screening100

./run-ggplot2-days.sh StochasticArrivals/WithExtScreening/Prob-0.01/WithCountermeasures D1 WithoutScreening Screening25 Screening50 Screening100

./run-ggplot2-days.sh StochasticArrivals/WithExtScreening/Prob-0.01/WithCountermeasures D2 WithoutScreening Screening25 Screening50 Screening100

python3 run-ggplot2-positive-comparison.py StochasticArrivals/WithExtScreening/Prob-0.01/WithCountermeasures