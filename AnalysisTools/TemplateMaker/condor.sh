#!/bin/bash
set -euo pipefail
cd /afs/cern.ch/work/l/lkang/Analysis/SMEFT/CMSSW_12_2_0/src/HexUtils/AnalysisTools/TemplateMaker
scramv1 runtime -sh
COMMAND=$(sed $1!d condor_kappaQ.txt)
$COMMAND
