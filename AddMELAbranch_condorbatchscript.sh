#!/bin/bash
set -euo pipefail
cd /afs/cern.ch/work/l/lkang/JHU_Higgs/HexUtils/CMSSW_12_2_0/src/HexUtils
eval $(scram ru -sh)
eval $(./AnalysisTools/JHUGenMELA/MELA/setup.sh env standalone)
TREEFILENAME=$(sed $1!d AddMELAbranch_SIGtrees.txt)
python3 MELA_rw_widthmass_SAVVAS.py $TREEFILENAME 2>&1

