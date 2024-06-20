#!/bin/bash 

python MakeInputRoot_rb.py ./input/Untagged.root 
python MakeInputRoot_rb.py ./input/VHtagged.root 
python MakeInputRoot_rb.py ./input/VBFtagged.root 

##python SymSyst.py ./input/Untagged.inp.root > symUn
##python SymSyst.py ./input/VHtagged.inp.root > symVH
##python SymSyst.py ./input/VBFtagged.inp.root > symVBF

mv ./input/Untagged.inp.root ./input/Untagged.input.root
mv ./input/VBFtagged.inp.root ./input/VBFtagged.input.root
mv ./input/VHtagged.inp.root ./input/VHtagged.input.root

python DatacardMaker.py ./input/Untagged.input.root
python DatacardMaker.py ./input/VBFtagged.input.root
python DatacardMaker.py ./input/VHtagged.input.root
