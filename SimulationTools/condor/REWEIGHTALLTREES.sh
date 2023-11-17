#!/bin/bash

file="MELAtrees.txt"

while read -r line; do

echo -e "$line\n"

sed -e "s/SAMPLENAME/$line/g" condor_MELA.sub > tempcondor.sub

condor_submit tempcondor.sub

done <$file
