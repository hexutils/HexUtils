# HexUtils

## Installing

Follow these instructions if you are isntalling these tools on **LXPLUS** or a similar service which has CMSSW releases available. Otherwise, simply clone this repository into your working area, compile, and read on. Reference the **Rockfish** section at the bottom for more information on using the Rockfish cluster.
1. Copy the install.sh locally.
2. Specify the ```CMSSW_release``` you want to use at the top of install.sh. Currently **CMSSW_12_2_0** is recommended.
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

## Rockfish (and persistent sessions in general)

The Rockfish cluster does not yet have CMSSW available, but should still be compatible with these tools as long as you have the above dependencies available for your user. 

One thing to note is that the procedure for choosing your login node is different from that of LXPLUS. For LXPLUS it is suitable to ```ssh [user]@lxplus333@cern.ch```, for example, to specify node 333. For Rockfish, one must ```ssh [user]@login.rockfish.jhu.edu``` and then once logged in, ```ssh login03```, for example, to connect to node 3. This is very important to note for the sake of reattaching a previously running session. 

When connecting to Rockfish (or LXPLUS), you can use screen or tmux to make sure that your session continues to run long after you disconnect. tmux is recommended for reasons which I will not go into here.

You will want a consistent and dependable way to keep track of your ssh nodes so that you have a history of where you logged in (and therefore, where you left your remote sessions). My suggested method is to add these lines to your ```~/.bashrc``` file (or equivalent .zshrc, etc) file in your home directory:
```
if [ $TERM != "dumb" ]; then
	cur_DATE=$(date)
	cur_HOST=$(hostname)
	echo $cur_DATE" "$cur_HOST >> ~/lastrockfish
fi
```
Doing so will append your login node to the file ```~/lastrockfish``` every time you login. Executing ```tail ~/lastrockfish``` will recall your most recent connections so that you can find and reattach your active tmux session. 

However, when running multiple jobs or running particularly long-lasting jobs, we recommend utilizaing our batch submission method detailed above in **Batch Submission**. Keep in mind that verbose log files and all subtrees are saved as our tool runs, so you should have no problem even in the case that any of your submitted jobs fail while running non-interactively.
