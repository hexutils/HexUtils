#!/bin/bash

# USER INPUTS
CMSSW_release=CMSSW_12_2_0
CMSSW_release_name=    #Leave this blank if you don't know what it is.  It's just a marker in case you have multiple identical directories. No need for the underscore.
SCRAM_ARCH_name="amd64_gcc900" # Leave slc6/7 out


MACHINESPECS="$(uname -a)"
echo "Machine specifics: ${MACHINESPECS}"
declare -i FOUND_EL6=0
if [[ "${MACHINESPECS}" == *"el6"* ]]; then
  FOUND_EL6=1
else
  for evar in $(env); do
    if [[ "$evar" == *"SINGULARITY_IMAGE_HUMAN"* ]]; then
      # This means you are running in a condor job with a singularity image loaded.
      if [[ "$evar" == *"rhel6"* ]] || [[ "$evar" == *"slc6"* ]]; then
        FOUND_EL6=1
      fi
    fi
  done
fi


if [[ ${FOUND_EL6} -eq 1 ]]; then
  SCRAM_ARCH_name="slc6_${SCRAM_ARCH_name}"
else
  SCRAM_ARCH_name="slc7_${SCRAM_ARCH_name}"
fi

export SCRAM_ARCH=${SCRAM_ARCH_name}

if [[ -z ${CMSSW_release_name+x} ]]; then
  CMSSW_release_name="${CMSSW_release}"
else
  CMSSW_release_name="${CMSSW_release}_${CMSSW_release_name}"
fi

#--Here there be dragons----
export CMS_PATH=/cvmfs/cms.cern.ch
source /cvmfs/cms.cern.ch/cmsset_default.sh
scramv1 p -n ${CMSSW_release_name} CMSSW $CMSSW_release
cd ${CMSSW_release_name}/src
eval $(scramv1 runtime -sh)

# new upstream-only ignores user's cmssw, but makes cms-init much, much faster
git cms-init --upstream-only

#######################################
# No CMSSW packages beyond this point #
#######################################

# HexUtils
git clone git@github.com:hexutils/HexUtils.git

# MELA
#git clone git@github.com:JHUGen/JHUGenMELA.git
#./JHUGenMELA/setup.sh -j

# MELA Analytics
#git clone git@github.com:MELALabs/MelaAnalytics.git

#########################
#  DeepAK8 fat jet tagger
# #######################
# check out the package - note, need ssh key in gitlab.cern.ch
# because this is top secret code that needs to be password protected apparently
# and thus, the user must either configure ssh keys or manually type their password.
# the latter ruins the whole "run this install script, get a coffee, use the ntuplemaker" workflow.
# git clone ssh://git@gitlab.cern.ch:7999/DeepAK8/NNKit.git -b ver_2018-03-08_for94X
git clone ssh://git@gitlab.cern.ch:7999/TreeMaker/NNKit.git -b ver_2018-03-08

#export LD_PRELOAD=/cvmfs/cms.cern.ch/slc7_amd64_gcc700/cms/cmssw/CMSSW_10_2_22/external/slc7_amd64_gcc700/lib/libjemalloc.so.2
#scram b -j
scram b -j 16

# see comment in patchesToSource.sh
rm $CMSSW_BASE/lib/$SCRAM_ARCH/.poisonededmplugincache
