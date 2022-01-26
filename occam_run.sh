#!/bin/bash
occam-run -n $1 netlogo/netlogo:620 /usr/bin/bash -c "./start.sh /archive/home/dbaccega/schoolseirmodel/${2} 24"
