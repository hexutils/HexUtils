#!/bin/bash
set -euo pipefail
cd /afs/cern.ch/work/j/jejeffre/public/HEP_Ex_Tools/HexUtils/HexUtils/CMSSW_12_2_0/src
eval `scramv1 runtime -sh`
cd /afs/cern.ch/work/j/jejeffre/public/HEP_Ex_Tools/HexUtils/HexUtils
TREEFILENAME=$(sed $1!d signal_trees.txt)
python3 OnShellTreeTaggerTest.py -i $TREEFILENAME -o Tagges_Signal_Trees -b branchlist.txt 2>&1
