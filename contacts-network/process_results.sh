#!/bin/bash
cd $1/contacts-time
for filename in *;
do
	tr -d "[" < $filename | tr -d "]" | tr -s " " > "processed_$filename"
	rm $filename
done

cd ../number-of-contacts
for filename in *;
do
	tr -d "[" < $filename | tr -d "]" | tr -s " " > "processed_$filename"
	rm $filename
done