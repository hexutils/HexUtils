#!/cvmfs/cms.cern.ch/slc7_amd64_gcc900/cms/cmssw/CMSSW_12_2_0/external/slc7_amd64_gcc900/bin/python3

import importlib.util
import sys, getopt
import os
import glob
import time
from pathlib import Path
import re

def main(argv):
    
    template_input = '\nMELAcalc.py -i <inputfile> -s <subdirectory> -o <outputdir> -b <branchfile> (-l <lhe2root>) (-m <mcfmprob>) (-j <jhuprob>) (-z <zprime/higgs input>)\n'
    
    inputfile = ''
    pthsubdir = ''
    outputdir = ''
    branchfile = ''
    lhe2root = ''
    mcfmprob = ''
    jhuprob = ''
    zPrime_Higgs = ''
    removesubtrees = ''
    try:
        opts, args = getopt.getopt(argv,"hi:s:o:b:l:m:j:z:",["ifile=","subdr=","outdr=","bfile=","lhe2root=","mcfmprob=","jhuprob=","zprime="])
    except getopt.GetoptError:
        print(template_input)
        exit()
    for opt, arg in opts:
        if opt == '-h' or opt == '--help':
            print(template_input)
            exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-s", "--subdr"):
            pthsubdir = arg
        elif opt in ("-o", "--outdr"):
            outputdir = arg
        elif opt in ("-b", "--bfile"):
            branchfile = arg
        elif opt in ("-l", "--lhe2root"):
            lhe2root = arg
        elif opt in ("-m", "--mcfmprob"):
            mcfmprob = arg
        elif opt in ("-j", "--jhuprob"):
            jhuprob = arg
        elif opt in ("-z", "--zprime"):
            zPrime_Higgs = arg
        
    if not all([inputfile, pthsubdir, outputdir, branchfile]):
        print(template_input)
        exit()

    if not outputdir.endswith("/"):
        outputdir = outputdir+"/"

    if not pthsubdir.endswith("/"):
        pthsubdir = pthsubdir+"/"

    pthsubdir = pthsubdir.split("/")[-2]

    lhe2root = lhe2root.replace(" ", "").capitalize()

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

    if len(lhe2root) > 0:
        if lhe2root not in ["True", "False"]:
            print("\nERROR: \tOption '-l' is expected to be True or False. Please try again with valid input.\n")
            print('PTreeMaker.py -i <inputfile> -s <subdirectory> -o <outputdir> -b <branchfile> (-l <lhe2root>)\n')
            exit()
    else: lhe2root = "True"

    lhe2root = eval(lhe2root)
    
    if zPrime_Higgs != '':
        zPrime_Higgs = [i.split('-') for i in zPrime_Higgs.split('_')]
        if len(zPrime_Higgs) != 2 or len(zPrime_Higgs[0]) != 3 or len(zPrime_Higgs[1]) != 2:
            print("\nERROR: \tOption '-z' is expected to be of form ZPrime-(Mass)-(Width)_Higgs-(Mass) in GeV")
            print(template_input)
            exit()

    print("\n================ Reading user input ================\n")

    print("Input PTree is '{}'".format(inputfile))
    print("Path subdirectory is '{}'".format(pthsubdir))
    print("Output directory is '{}'".format(outputdir[:-1]))
    print("Branch list file is '{}'".format(branchfile))
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

    if not lhe2root: from AnalysisTools.Utils.MELA_Weights import addprobabilities
    else: from AnalysisTools.Utils.MELA_Weights_lhe2root import addprobabilities
    
    if zPrime_Higgs: #bool('') = False, bool('any string') =  True  
        if mcfmprob:
            #addprobabilities(filename, outtreefilename, branchlist, "eventTree", SampleHypothesisMCFM = mcfmprob)
            addprobabilities(filename, outtreefilename, branchlist, "ZZTree/candTree", SampleHypothesisMCFM = mcfmprob, ZHiggs=zPrime_Higgs)
        elif jhuprob:
            addprobabilities(filename, outtreefilename, branchlist, "EventBranch", SampleHypothesisJHUGen = jhuprob, ZHiggs=zPrime_Higgs)
            #addprobabilities(filename, outtreefilename, branchlist, "ZZTree/candTree", SampleHypothesisJHUGen = mcfmprob)
        elif (jhuprob) and (mcfmprob):
            addprobabilities(filename, outtreefilename, branchlist, "eventTree", SampleHypothesisMCFM = mcfmprob, SampleHypothesisJHUGen = jhuprob, ZHiggs=zPrime_Higgs)
        else:
            addprobabilities(filename, outtreefilename, branchlist, "eventTree", ZHiggs=zPrime_Higgs)
            #addprobabilities(filename, outtreefilename, branchlist, "ZZTree/candTree")
    else:
        if mcfmprob:
            #addprobabilities(filename, outtreefilename, branchlist, "eventTree", SampleHypothesisMCFM = mcfmprob)
            addprobabilities(filename, outtreefilename, branchlist, "ZZTree/candTree", SampleHypothesisMCFM = mcfmprob)
        elif jhuprob:
            addprobabilities(filename, outtreefilename, branchlist, "EventBranch", SampleHypothesisJHUGen = jhuprob)
            #addprobabilities(filename, outtreefilename, branchlist, "ZZTree/candTree", SampleHypothesisJHUGen = mcfmprob)
        elif (jhuprob) and (mcfmprob):
            addprobabilities(filename, outtreefilename, branchlist, "eventTree", SampleHypothesisMCFM = mcfmprob, SampleHypothesisJHUGen = jhuprob)
        else:
            addprobabilities(filename, outtreefilename, branchlist, "eventTree")
            #addprobabilities(filename, outtreefilename, branchlist, "ZZTree/candTree")
            
if __name__ == "__main__":
    main(sys.argv[1:])
