#!/bin/bash
set -euo pipefail
cd /afs/cern.ch/work/j/jejeffre/public/HEP_Ex_Tools/HexUtils/HexUtils/CMSSW_12_2_0/src
eval `scramv1 runtime -sh`
cd /afs/cern.ch/work/j/jejeffre/public/HEP_Ex_Tools/HexUtils/HexUtils
python3 MakeAllTemplates.py All_Templates_Untagged_gammaH_High_Stat Processed_ggH_Signal_Trees.txt
