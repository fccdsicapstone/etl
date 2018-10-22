#!/bin/bash
#This script should be in the same directory as the unzipped folders from TIGER. 
codes=("01" "04" "05" "06" "08" "09" "10" "12" "13" "16" "17" "18" "19" "20" "21" "22" "23" "24" "25" "26" "27" "28" "29" "30" "31" "32" "33" "34" "35" "36" "37" "38" "39" "40" "41" "42" "44" "45" "46" "47" "48" "49" "50" "51" "53" "54" "55" "56")
for state_code in "${codes[@]}"
do
	echo "Merging state $state_code."
	#Creates a directory for each state.
	dir_name="tl_2018_""$state_code""_roads"
	mkdir $dir_name
	#Moves all road shapefiles (and related data) to the directory.
	mv $(find . -name "tl_2018_""$state_code""*" -depth 2) $dir_name
done