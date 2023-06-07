#!/cvmfs/cms.cern.ch/slc7_amd64_gcc900/cms/cmssw/CMSSW_12_2_0/external/slc7_amd64_gcc900/bin/python3

import importlib.util
import sys, getopt
import os
import glob
import time
from pathlib import Path
import re
import argparse

def main(raw_args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--ifile', type=str, nargs='+', required=True)
    parser.add_argument('-o', '--outdr', type=str, required=True)
    parser.add_argument('-b', '--bfile', type=str, required=True)
    parser.add_argument('-l', '--lhe2root', action="store_true")
    parser.add_argument('-m', '--mcfmprob', type=str, default='')
    parser.add_argument('-j', '--jhuprob', type=str, default='')
    parser.add_argument('-h', '--hmass', type=float, default=125)
    parser.add_argument('-z', '--zprime', type=float, nargs=2, default=0)
    parser.add_argument('-c', '--couplings', type=str, default='')
    parser.add_argument('-v', '--verbose', type=int, default=0, choices=[0,1,2,3,4,5])
    parser.add_argument('-ow', '--overwrite', action="store_true")
    args = parser.parse_args(raw_args)
    
    template_input = '\nMELAcalc.py -i <inputfile> -o <outputdir> -b <branchfile> (-l <lhe2root>) (-m <mcfmprob>) (-j <jhuprob>) (-z <mass> <width>) (-h <mass>)(-c <couplings file>)\n'
    
    inputfiles = args.ifile
    pthsubdirs = inputfiles
    outputdir = args.outdr
    branchfile = args.bfile
    lhe2root = args.lhe2root
    mcfmprob = args.mcfmprob
    jhuprob = args.jhuprob
    zp = args.zprime
    higgs_mass = args.hmass
    couplings = args.couplings
    overwrite = args.overwrite
    
    
    if lhe2root: from AnalysisTools.Utils.MELA_Weights_lhe2root import addprobabilities
    else: from AnalysisTools.Utils.MELA_Weights import addprobabilities

    if not outputdir.endswith("/"):
        outputdir = outputdir+"/"

    if not pthsubdir.endswith("/"):
        pthsubdir = pthsubdir+"/"

    pthsubdir = pthsubdir.split("/")[-2]

    for inputfile, pthsubdir in zip(inputfiles, pthsubdirs):
        if not os.path.exists(inputfile):
            print("\nERROR: \tROOT file '" + inputfile + "' cannot be located. Please try again with valid input.\n")
            print('MELAcalc.py -i <inputfile> -s <subdirectory> -o <outputdir> -b <branchfile>\n')
            exit()

        if not os.path.exists(branchfile):
            print("\nERROR: \tBranches list '" + branchfile + "' cannot be located. Please try again with valid input.\n")
            print('MELAcalc.py -i <inputfile> -s <subdirectory> -o <outputdir> -b <branchfile>\n')
            exit()

        if pthsubdir not in inputfile:
            print("\nERROR: \tSubdirectory '" + pthsubdir + "' is not in the input path. Please try again with valid input.\n")
            print('MELAcalc.py -i <inputfile> -s <subdirectory> -o <outputdir> -b <branchfile>\n')
            exit()
                
        if couplings != '':
            lst_of_couplings = []
            if not os.path.exists(couplings):
                print("\nERROR: \tCouplings file" + couplings +" Cannot be located. Please try again with valid input.\n")
            with open(couplings) as f:
                couplings = f.readlines()
                coupling_template = "couplings must be of form <coupling name>-<value> for each line"
                for coupling_duo in couplings:
                    coupling_duo = coupling_duo.strip('\n\t').split('-')
                    coupling_duo[1] = float(coupling_duo[1])
                    
                    if coupling_duo == '':
                        continue
                    
                    elif len(coupling_duo) != 2:
                        print(coupling_template)
                        print(template_input)
                        exit()
                    
                    lst_of_couplings.append(coupling_duo)
                    

        print("\n================ Reading user input ================\n")

        print("Input PTree is '{}'".format(inputfile))
        print("Path subdirectory is '{}'".format(pthsubdir))
        print("Output directory is '{}'".format(outputdir[:-1]))
        print("Branch list file is '{}'".format(branchfile))
        if jhuprob: print("JHUGen Prob is '{}'".format(jhuprob))
        if zp: print("ZPrime mass/width =",
                            "{:.2f}/{:.2f}".format(*zp),
                            "with 'Higgs' mass of {:.2f}".format(higgs_mass))
        if couplings:
            print("The following couplings are explicily used:")
            print(*(i[0] + ' = ' + str(i[1]).strip() for i in lst_of_couplings), sep='\n')
        else:
            couplings = [None]
            
        if lhe2root: print("MELA parser expecting lhe2root branch names")
        else: print("MELA parser expecting CJLST branch names")

        #================ Set input file path and output file path ================
        
        filename = inputfile
        branchlistpath = branchfile
        tagtreepath = outputdir

        ind = filename.split("/").index(pthsubdir)

        tagtreefile = "/".join(filename.split("/")[ind:])
        outtreefilename = tagtreepath+tagtreefile

        print("\n================ Processing user input ================\n")

        if not os.path.exists(filename):
            print("ERROR: \t'" + filename + "' does not exist!\n")
            exit()

        elif os.path.exists(outtreefilename):
            
            if overwrite:
                print("WARNING: Overwriting", outtreefilename, "\n")
                os.remove(outtreefilename)
            else:
                print("ERROR: \t'" + outtreefilename + "' or parts of it already exist!\n")
                exit()

        else:
            print("Pre-existing output PTree not found --- safe to proceed")
            if not os.path.exists("/".join(outtreefilename.split("/")[:-1])):
                Path("/".join(outtreefilename.split("/")[:-1])).mkdir(True, True)

        print("Read '"+filename+"'\n")
        print("Write '"+outtreefilename+"'\n")

        with open(branchlistpath) as f:
            branchlist = [line.rstrip() for line in f]

        print(branchlist)
        
        if zp: #bool('') = False, bool('any string') =  True  
            if mcfmprob:
                #addprobabilities(filename, outtreefilename, branchlist, "eventTree", SampleHypothesisMCFM = mcfmprob)
                addprobabilities(filename, outtreefilename, branchlist, "ZZTree/candTree", 
                                SampleHypothesisMCFM = mcfmprob, ZP=zp, couplings=lst_of_couplings,
                                verbosity=args.verbose, HM=higgs_mass)
            elif jhuprob:
                addprobabilities(filename, outtreefilename, branchlist, "eventTree", 
                                SampleHypothesisJHUGen = jhuprob, ZP=zp, couplings=lst_of_couplings,
                                verbosity=args.verbose, HM=higgs_mass)
                #addprobabilities(filename, outtreefilename, branchlist, "ZZTree/candTree", SampleHypothesisJHUGen = mcfmprob)
            elif (jhuprob) and (mcfmprob):
                addprobabilities(filename, outtreefilename, branchlist, "eventTree", 
                                SampleHypothesisMCFM = mcfmprob, SampleHypothesisJHUGen = jhuprob, ZP=zp, 
                                couplings=lst_of_couplings, verbosity=args.verbose, HM=higgs_mass)
            else:
                addprobabilities(filename, outtreefilename, branchlist, "eventTree", ZP=zp, couplings=lst_of_couplings,
                                verbosity=args.verbose, HM=higgs_mass)
                #addprobabilities(filename, outtreefilename, branchlist, "ZZTree/candTree")
        else:
            if mcfmprob:
                #addprobabilities(filename, outtreefilename, branchlist, "eventTree", SampleHypothesisMCFM = mcfmprob)
                addprobabilities(filename, outtreefilename, branchlist, "ZZTree/candTree", 
                                SampleHypothesisMCFM = mcfmprob, couplings=lst_of_couplings, verbosity=args.verbose, HM=higgs_mass)
            elif jhuprob:
                addprobabilities(filename, outtreefilename, branchlist, "eventTree", 
                                SampleHypothesisJHUGen = jhuprob, couplings=lst_of_couplings, verbosity=args.verbose, HM=higgs_mass)
                #addprobabilities(filename, outtreefilename, branchlist, "ZZTree/candTree", SampleHypothesisJHUGen = mcfmprob)
            elif (jhuprob) and (mcfmprob):
                addprobabilities(filename, outtreefilename, branchlist, "eventTree", 
                                SampleHypothesisMCFM = mcfmprob, SampleHypothesisJHUGen = jhuprob, couplings=lst_of_couplings,
                                verbosity=args.verbose, HM=higgs_mass)
            else:
                addprobabilities(filename, outtreefilename, branchlist, "eventTree", couplings=lst_of_couplings, verbosity=args.verbose, HM=higgs_mass)
                #addprobabilities(filename, outtreefilename, branchlist, "ZZTree/candTree")
            
if __name__ == "__main__":
    main()
