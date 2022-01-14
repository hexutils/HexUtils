#!/bin/bash
set -euo pipefail
cd /afs/cern.ch/work/s/skyriaco/Offshell_Trees_new/Treetagger/HexUtils
TREEFILENAME=$(sed $1!d VBF_files.txt)
python3 batchTreeTagger.py -i $TREEFILENAME -o /eos/user/s/skyriaco/Offshell/VBF/ -b branches.txt 2>&1
