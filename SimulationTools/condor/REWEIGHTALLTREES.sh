#!/bin/bash

file="ALLSAMPLENAMES.txt"

while read -r line; do

echo -e "$line\n"

sed -e "s/SAMPLENAME/$line/g" condor_UL.sub > tempcondor.sub

condor_submit tempcondor.sub

done <$file
