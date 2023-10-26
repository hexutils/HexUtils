#!/bin/bash
set -euo pipefail
cd /afs/cern.ch/work/l/lkang/JHU_Higgs/HexUtils/CMSSW_12_2_0/src/HexUtils
eval $(scram ru -sh)
TREEFILENAME=$(sed $1!d CJLSTtrees_UL_test.txt)
./OffShellTreeTagger.py -i $TREEFILENAME -s cjlst -o /eos/user/g/gritsan/Write/TaggedTrees/UL_CJLST_test -b CJLSTbranches.txt -c True 2>&1

