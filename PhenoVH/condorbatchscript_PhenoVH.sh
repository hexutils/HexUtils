#!/bin/bash
set -euo pipefail
cd /afs/cern.ch/work/l/lkang/JHU_Higgs/HexUtils/CMSSW_12_2_0/src/HexUtils
eval $(scram ru -sh)
TREEFILENAME=$(sed $1!d CJLSTtrees_PhenoVH.txt)
./PTreeMaker_PhenoVH.py -i $TREEFILENAME -s cjlst -o /afs/cern.ch/work/l/lkang/JHU_Higgs/HexUtils/CMSSW_12_2_0/src/HexUtils/PhenoVH -b CJLSTbranches.txt -c True 2>&1
