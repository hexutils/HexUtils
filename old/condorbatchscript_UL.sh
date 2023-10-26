#!/bin/bash
set -euo pipefail
cd /afs/cern.ch/work/l/lkang/JHU_Higgs/HexUtils/CMSSW_12_2_0/src/HexUtils
eval $(scram ru -sh)
TREEFILENAME=$(sed $1!d CJLSTtrees_UL.txt)
./batchTreeTagger.py -i $TREEFILENAME -s Trees -o /eos/user/l/lkang/Active_Research/TaggedTrees/PROD_ULminimalsamplestest_e2c98351/TaggedTrees/ -b CJLSTbranches.txt -c True 2>&1
