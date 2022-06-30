#!/bin/bash
set -euo pipefail
cd /afs/cern.ch/work/j/jejeffre/public/HEP_Ex_Tools/HexUtils/HexUtils/CMSSW_12_2_0/src
eval `scramv1 runtime -sh`
cd /afs/cern.ch/work/j/jejeffre/public/HEP_Ex_Tools/HexUtils/HexUtils
TREEFILENAME=$(sed $1!d ew_bkg_trees.txt)
python3 OnShellTreeTagger.py -i $TREEFILENAME -o Tagged_EW_Background -b branchlist.txt -d False 2>&1
