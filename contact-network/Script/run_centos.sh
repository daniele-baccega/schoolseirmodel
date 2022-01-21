#!/bin/bash
echo "Simulation in progress..."
/home/centos/NetLogo6.2.0/netlogo-headless.sh --model ../SchoolSEIRModel.nlogo --experiment Network --threads 16
echo "Simulation finished."
