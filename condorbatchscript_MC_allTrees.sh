#!/bin/bash
set -euo pipefail
cd /afs/cern.ch/work/l/lkang/JHU_Higgs/HexUtils/CMSSW_12_2_0/src/HexUtils
eval $(scram ru -sh)
TREEFILENAME=$(sed $1!d CJLSTtrees_MC_allPOWHEG.txt)
./OffShellTreeTagger.py -i $TREEFILENAME -s cjlst -o /eos/user/g/gritsan/Write/TaggedTrees/OffshellTemplateTrees20220923/nominal -b CJLSTbranches.txt -c True 2>&1

