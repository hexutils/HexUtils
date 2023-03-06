#!/bin/bash
set -euo pipefail
cd /afs/cern.ch/work/l/lkang/JHU_Higgs/HexUtils/CMSSW_12_2_0/src/HexUtils
eval $(scram ru -sh)
TREEFILENAME=$(sed $1!d CJLSTtrees.txt)
./batchTreeTagger.py -i $TREEFILENAME -s 200205_CutBased -o /eos/user/l/lkang/Active_Research/TaggedTrees/MinimalSMTemplate_withsystematics -b CJLSTbranches.txt -c True 2>&1
