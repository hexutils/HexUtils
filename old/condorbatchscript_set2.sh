#!/bin/bash
set -euo pipefail
cd /afs/cern.ch/work/l/lkang/JHU_Higgs/HexUtils/CMSSW_12_2_0/src/HexUtils
eval $(scram ru -sh)
TREEFILENAME=$(sed $1!d CJLSTtrees_2022-03-08.txt)
./batchTreeTagger.py -i $TREEFILENAME -s 18002_ACsamples_testntuples -o /eos/user/l/lkang/Active_Research/TaggedTrees/GenComp_125GeV -b CJLSTbranches.txt 2>&1
