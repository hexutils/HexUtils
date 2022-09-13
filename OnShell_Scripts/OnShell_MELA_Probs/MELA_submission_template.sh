#!/bin/bash
set -euo pipefail
CMSSW
eval `scramv1 runtime -sh`
UTILS
eval $(./AnalysisTools/JHUGenMELA/MELA/setup.sh env standalone)
COMMAND
