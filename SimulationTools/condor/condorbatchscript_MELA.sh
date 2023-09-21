#!/bin/bash
set -euo pipefail

#cd /afs/cern.ch/work/l/lkang/JHU_Higgs/JHUGen/CMSSW_11_1_9/src/genproductions/bin/JHUGen/offshell_JHUGen/CMSSW_11_1_9/src
cd /afs/cern.ch/work/l/lkang/JHU_Higgs/JHUGen/CMSSW_12_4_11_patch3/src/genproductions/bin/JHUGen/EW_offshell_JHUGen/CMSSW_12_4_11_patch3/src/

eval $(scram ru -sh)
eval $(JHUGenMELA/MELA/setup.sh env)

export LD_LIBRARY_PATH=/cvmfs/cms.cern.ch/slc7_amd64_gcc820/external/lhapdf/6.2.3-f9f0c7ff52c430bdce541de202b20196/lib/:${LD_LIBRARY_PATH}
#export LHAPDF_DATA_PATH=/cvmfs/cms.cern.ch/slc7_amd64_gcc820/external/lhapdf/6.2.3-f9f0c7ff52c430bdce541de202b20196/share/LHAPDF/:${LHAPDF_DATA_PATH}
export LHAPDF_DATA_PATH=/cvmfs/cms.cern.ch/slc7_amd64_gcc820/external/lhapdf/6.2.3-f9f0c7ff52c430bdce541de202b20196/share/LHAPDF/

#cd /afs/cern.ch/work/l/lkang/JHU_Higgs/JHUGen/CMSSW_11_1_9/src/genproductions/bin/JHUGen/offshell_JHUGen/JHUGenerator
cd /afs/cern.ch/work/l/lkang/JHU_Higgs/JHUGen/CMSSW_12_4_11_patch3/src/genproductions/bin/JHUGen/EW_offshell_JHUGen/JHUGenerator

./JHUGen $(cat JHUGen_gridpacks_UL/$2_input/JHUGen.input) Seed=123456 DataFile=/afs/cern.ch/work/g/gritsan/public_write/lkang/InclusiveCuts/JHUGen_OffshellVBF_4l_grids_13TeV/$2/Out VBFoffsh_run=$1
