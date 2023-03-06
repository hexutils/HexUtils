#!/bin/bash
set -euo pipefail
cd /afs/cern.ch/work/l/lkang/JHU_Higgs/HexUtils/CMSSW_12_2_0/src/HexUtils
eval $(scram ru -sh)
TREEFILENAME=$(sed $1!d CJLSTtrees_MC_validation.txt)
./OffShellTreeTagger.py -i $TREEFILENAME -s cjlst -o /eos/user/l/lkang/Active_Research/TaggedTrees/MC_validation_WPsel_non2junderflow_fix -b CJLSTbranches.txt -c True 2>&1
