#!/bin/bash

# USER INPUTS
CMSSW_release=CMSSW_12_2_0
CMSSW_release_name=    #Leave this blank if you don't know what it is.  It's just a marker in case you have multiple identical directories. No need for the underscore.
SCRAM_ARCH_name="amd64_gcc900" # Leave slc6/7 out
SCRAM_ARCH_name="slc7_${SCRAM_ARCH_name}"
export SCRAM_ARCH=${SCRAM_ARCH_name}

if [ $# -eq 0 ] || [ ${1,,} = "lgc" ] || [ ${1,,} = "cuda" ] || [ ${1,,} = "gpu" ]
  then
    echo "Loading LGC computing environment v103 with CUDA support"
    # Loading LHC Computing Grid software stack release 103cuda. More stable/applicable than CMSSW. https://lcginfo.cern.ch/
    source /cvmfs/sft.cern.ch/lcg/views/LCG_103cuda/x86_64-centos7-gcc11-opt/setup.sh
  else
    echo "Loading CMSSW computing environment v12_2_0"
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
fi

#######################################
# No CMSSW packages beyond this point #
#######################################

# Loading LHC Computing Grid software stack release 103cuda. More stable/applicable than CMSSW. https://lcginfo.cern.ch/
#source /cvmfs/sft.cern.ch/lcg/views/LCG_103cuda/x86_64-centos7-gcc11-opt/setup.sh

# HexUtils
git clone https://github.com/lk11235/HexUtils.git

./HexUtils/JHUGenMELA/MELA/setup.sh
eval $(./HexUtils/JHUGenMELA/MELA/setup.sh env standalone)

# MELA Analytics
#git clone git@github.com:MELALabs/MelaAnalytics.git

scram b -j 16


if ! { [ $# -eq 0 ] || [ ${1,,} = "lgc" ] || [ ${1,,} = "cuda" ] || [ ${1,,} = "gpu" ] }
  then
    echo "Removing .poisonededmplugincache"
    # see comment in patchesToSource.sh
    rm $CMSSW_BASE/lib/$SCRAM_ARCH/.poisonededmplugincache
fi
