#!/bin/bash
echo "Simulation in progress..."
/usr/share/NetLogo/6.1.1/netlogo-headless.sh --model ../SchoolSEIRModel.nlogo --experiment Network --threads 24
echo "Simulation finished."
