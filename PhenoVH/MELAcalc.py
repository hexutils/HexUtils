#!/cvmfs/cms.cern.ch/slc7_amd64_gcc900/cms/cmssw/CMSSW_12_2_0/external/slc7_amd64_gcc900/bin/python3

import importlib.util
import sys, getopt
import os
import glob
import time
from pathlib import Path
import re


def main(argv):
    inputfile = ''
    pthsubdir = ''
    outputdir = ''
    branchfile = ''
    removesubtrees = ''
    try:
        opts, args = getopt.getopt(argv,"hi:s:o:b:",["ifile=","subdr=","outdr=","bfile="])
    except getopt.GetoptError:
        print('\nMELAcalc.py -i <inputfile> -s <subdirectory> -o <outputdir> -b <branchfile>\n')
        exit()
    for opt, arg in opts:
        if opt == '-h' or opt == '--help':
            print('\nMELAcalc.py -i <inputfile> -s <subdirectory> -o <outputdir> -b <branchfile>\n')
            exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-s", "--subdr"):
            pthsubdir = arg
        elif opt in ("-o", "--outdr"):
            outputdir = arg
        elif opt in ("-b", "--bfile"):
            branchfile = arg

    if not all([inputfile, pthsubdir, outputdir, branchfile]):
        print('\nMELAcalc.py -i <inputfile> -s <subdirectory> -o <outputdir> -b <branchfile>\n')
        exit()

    if not outputdir.endswith("/"):
        outputdir = outputdir+"/"

    if not pthsubdir.endswith("/"):
        pthsubdir = pthsubdir+"/"

    pthsubdir = pthsubdir.split("/")[-2]

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

    print("\n================ Reading user input ================\n")

    print("Input PTree is '{}'".format(inputfile))
    print("Path subdirectory is '{}'".format(pthsubdir))
    print("Output directory is '{}'".format(outputdir[:-1]))
    print("Branch list file is '{}'".format(branchfile))


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

    from AnalysisTools.Utils.MELA_Weights import addprobabilities

    #addprobabilities(filename, outtreefilename, branchlist, "eventTree")
    addprobabilities(filename, outtreefilename, branchlist, "ZZTree/candTree")

if __name__ == "__main__":
    main(sys.argv[1:])
