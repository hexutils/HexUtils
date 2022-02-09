# HexUtils

## Installing

1. Copy the install.sh locally.
2. Specify the CMSSW_release you want to use at the top of install.sh. Currently **CMSSW_12_2_0** is recommended.
3. ```source install.sh``` will check out the CMSSW release and HexUtils repository, and build everything.

## Dependencies

All of these tools can be run outside of a CMSSW environment on any machine. To make sure you are using compatible version fo the required dependencies, please refer to the guidelines below. Note that these versions numbers are consistent with the CMSSW release which is used for code development but are not explicitly required. 

- Python 3.9.6
- ROOT 6.22 (with pyROOT compiled for Python3)
- numpy 1.17.5
- root-numpy 4.8.0
- tqdm 4.62.2

## Features

[Being updated for new version]

## Usage

### Target Trees

[More to come]
CJLSTtrees.txt

### Target Branches

[Being updated for new version]
CJLSTbranches.txt

### Example

[More to come]
./batchTreeTagger.py -i /eos/cms/store/group/phys_higgs/cmshzz4l/cjlst/RunIILegacy/200205_CutBased/MC_2016_CorrectBTag/OffshellAC/gg/ggTo2e2mu_0PMH125Contin_MCFM701/ZZ4lAnalysis.root -s 200205_CutBased -o ./ -b CJLSTbranches.txt

## Batch Submission

[Being updated for new version]
condorbatchscript.sh
condor.sub
