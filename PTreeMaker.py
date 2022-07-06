#!/cvmfs/cms.cern.ch/slc7_amd64_gcc900/cms/cmssw/CMSSW_12_2_0/external/slc7_amd64_gcc900/bin/python3

import importlib.util

if importlib.util.find_spec("numpy") is None: 
    print("\nERROR: Please make sure that numpy is installed via 'pip3 install --user numpy' before running this tool.\n")
    exit()
if importlib.util.find_spec("tqdm") is None: 
    print("\nERROR: Please make sure that tqdm is installed via 'pip3 install --user tqdm' before running this tool.\n")
    exit()
if importlib.util.find_spec("root_numpy") is None: 
    print("\nERROR: Please make sure that root_numpy is installed via 'pip3 install --user root_numpy' before running this tool.\n")
    exit()

import sys, getopt
import os
import glob
import ROOT
from math import sqrt
import time
from pathlib import Path
import re
from tqdm import trange, tqdm
import numpy as np
from array import *
from collections import Counter
from decimal import *
import root_numpy
from root_numpy import array2tree, tree2array
import subprocess

from AnalysisTools.data import gConstants as gConstants
from AnalysisTools.data import cConstants as cConstants
from AnalysisTools.Utils.Discriminants import *

def main(argv):
    inputfile = ''
    pthsubdir = ''
    outputdir = ''
    branchfile = ''
    removesubtrees = ''
    try:
        opts, args = getopt.getopt(argv,"hi:s:o:b:c:",["ifile=","subdr=","outdr=","bfile=","clean="])
    except getopt.GetoptError:
        print('\nPTreeMaker.py -i <inputfile> -s <subdirectory> -o <outputdir> -b <branchfile> (-c <removesubtrees>)\n')
        exit()
    for opt, arg in opts:
        if opt == '-h' or opt == '--help':
            print('\nPTreeMaker.py -i <inputfile> -s <subdirectory> -o <outputdir> -b <branchfile> (-c <removesubtrees>)\n')
            exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-s", "--subdr"):
            pthsubdir = arg
        elif opt in ("-o", "--outdr"):
            outputdir = arg
        elif opt in ("-b", "--bfile"):
            branchfile = arg
        elif opt in ("-c", "--clean"):
            removesubtrees = arg

    if not all([inputfile, pthsubdir, outputdir, branchfile]):
        print('\nPTreeMaker.py -i <inputfile> -s <subdirectory> -o <outputdir> -b <branchfile> (-c <removesubtrees>)\n')
        exit()

    if not outputdir.endswith("/"):
        outputdir = outputdir+"/"

    if not pthsubdir.endswith("/"):
        pthsubdir = pthsubdir+"/"

    pthsubdir = pthsubdir.split("/")[-2]

    removesubtrees = removesubtrees.replace(" ", "").capitalize()

    if not os.path.exists(inputfile):
        print("\nERROR: \tROOT file '" + inputfile + "' cannot be located. Please try again with valid input.\n")
        print('PTreeMaker.py -i <inputfile> -s <subdirectory> -o <outputdir> -b <branchfile> (-c <removesubtrees>)\n')
        exit()

    if not os.path.exists(branchfile):
        print("\nERROR: \tBranches list '" + branchfile + "' cannot be located. Please try again with valid input.\n")
        print('PTreeMaker.py -i <inputfile> -s <subdirectory> -o <outputdir> -b <branchfile> (-c <removesubtrees>)\n')
        exit()

    if pthsubdir not in inputfile:
        print("\nERROR: \tSubdirectory '" + pthsubdir + "' is not in the input path. Please try again with valid input.\n")
        print('PTreeMaker.py -i <inputfile> -s <subdirectory> -o <outputdir> -b <branchfile> (-c <removesubtrees>)\n')
        exit()

    if len(removesubtrees) > 0:
        if removesubtrees not in ["True", "False"]:
            print("\nERROR: \tOption '-c' is expected to be True or False. Please try again with valid input.\n")
            print('PTreeMaker.py -i <inputfile> -s <subdirectory> -o <outputdir> -b <branchfile> (-c <removesubtrees>)\n')
            exit()
    else: removesubtrees = "True"

    removesubtrees = eval(removesubtrees)

    print("\n================ Reading user input ================\n")

    print("Input CJLST TTree is '{}'".format(inputfile))
    print("Path subdirectory is '{}'".format(pthsubdir))
    print("Output directory is '{}'".format(outputdir[:-1]))
    print("Branch list file is '{}'".format(branchfile))
    if removesubtrees: print("Subtrees will be removed after combination")
    else: print("Subtrees will be maintained after combination")

    print("\n================ Processing user input ================\n")

    #================ Set input file path and output file path ================
    
    filename = inputfile
    branchlistpath = branchfile
    tagtreepath = outputdir

    ind = filename.split("/").index(pthsubdir)

    tagtreefile = "/".join(filename.split("/")[ind:])
    tagtreefilename = tagtreepath+tagtreefile

    print("Read '"+filename+"'\n")
    print("Write '"+tagtreefilename+"'\n")

    D2jetZHSpline = ROOT.TFile("AnalysisTools/data/cconstants/SmoothKDConstant_m4l_DjjZH_13TeV.root").Get("sp_gr_varReco_Constant_Smooth")
    D2jetWHSpline = ROOT.TFile("AnalysisTools/data/cconstants/SmoothKDConstant_m4l_DjjWH_13TeV.root").Get("sp_gr_varReco_Constant_Smooth")
    D2jetVBFSpline = ROOT.TFile("AnalysisTools/data/cconstants/SmoothKDConstant_m4l_DjjVBF_13TeV.root").Get("sp_gr_varReco_Constant_Smooth")

    DbkgkinSpline4e = ROOT.TFile("AnalysisTools/data/cconstants/SmoothKDConstant_m4l_Dbkgkin_4e_13TeV.root").Get("sp_gr_varReco_Constant_Smooth")
    DbkgkinSpline4mu = ROOT.TFile("AnalysisTools/data/cconstants/SmoothKDConstant_m4l_Dbkgkin_4mu_13TeV.root").Get("sp_gr_varReco_Constant_Smooth")
    DbkgkinSpline2e2mu = ROOT.TFile("AnalysisTools/data/cconstants/SmoothKDConstant_m4l_Dbkgkin_2e2mu_13TeV.root").Get("sp_gr_varReco_Constant_Smooth")

    DggbkgkinSpline4e = ROOT.TFile("AnalysisTools/data/cconstants/SmoothKDConstant_m4l_Dggbkgkin_4e_13TeV.root").Get("sp_gr_varReco_Constant_Smooth")
    DggbkgkinSpline4mu = ROOT.TFile("AnalysisTools/data/cconstants/SmoothKDConstant_m4l_Dggbkgkin_4mu_13TeV.root").Get("sp_gr_varReco_Constant_Smooth")
    DggbkgkinSpline2e2mu = ROOT.TFile("AnalysisTools/data/cconstants/SmoothKDConstant_m4l_Dggbkgkin_2e2mu_13TeV.root").Get("sp_gr_varReco_Constant_Smooth")

    DbkgjjEWQCDSpline4lHadVH = ROOT.TFile("AnalysisTools/data/cconstants/SmoothKDConstant_m4l_DbkgjjEWQCD_4l_HadVHTagged_13TeV.root").Get("sp_gr_varReco_Constant_Smooth")
    DbkgjjEWQCDSpline2l2lHadVH = ROOT.TFile("AnalysisTools/data/cconstants/SmoothKDConstant_m4l_DbkgjjEWQCD_2l2l_HadVHTagged_13TeV.root").Get("sp_gr_varReco_Constant_Smooth")

    DbkgjjEWQCDSpline4lJJVBF = ROOT.TFile("AnalysisTools/data/cconstants/SmoothKDConstant_m4l_DbkgjjEWQCD_4l_JJVBFTagged_13TeV.root").Get("sp_gr_varReco_Constant_Smooth")
    DbkgjjEWQCDSpline2l2lJJVBF = ROOT.TFile("AnalysisTools/data/cconstants/SmoothKDConstant_m4l_DbkgjjEWQCD_2l2l_JJVBFTagged_13TeV.root").Get("sp_gr_varReco_Constant_Smooth")

    #WPCshift = 1
    WPCshift2jv = 0.46386/(1. - 0.46386)
    WPCshift2jz = 0.91315/(1. - 0.91315)
    WPCshift2jw = 0.88384/(1. - 0.88384)

    cConstants_list = cConstants.init_cConstants()
    gConstants_list = gConstants.init_gConstants()

    useQGTagging = False

    #================ Check existence of output and set up target branches ================

    print("================ Check output location and set up branches ================\n")

    if not os.path.exists(filename):
        print("ERROR: \t'" + filename + "' does not exist!\n")
        exit()

    elif os.path.exists(tagtreefilename) or glob.glob(tagtreefilename.replace(".root", "_subtree*.root")):
        print("ERROR: \t'" + tagtreefilename + "' or parts of it already exist!\n\tNote that part to all of the final eventTree can be reconstructed from its subtree files if necessary.\n")
        exit()

    else:
        print("Pre-existing output TTree not found --- safe to proceed")
        if not os.path.exists("/".join(tagtreefilename.split("/")[:-1])):
            Path("/".join(tagtreefilename.split("/")[:-1])).mkdir(True, True)

        branchlist = []

        with open(branchlistpath) as f:
            blist = [line.rstrip() for line in f]

        for branch in blist:
            if branch: branchlist.append(branch)

        f = ROOT.TFile(filename, 'READ')

        treenames = ["candTree", "candTree_failed"]

        #================ Loop over target trees ================

        d = f.Get("ZZTree")
        fobjects = [key.GetName() for key in d.GetListOfKeys()]

        for tind, tree in enumerate(treenames):
            if tree not in fobjects:
                continue
            
            print("\n================ Reading events from '" + tree + "' and calculating new branches ================\n")

            t = f.Get("ZZTree/"+tree)

            treebranches = [ x.GetName() for x in t.GetListOfBranches() ]

            branchdict = {}
            signfixdict = {}

            for branch in branchlist:
                if "-" in branch and branch in treebranches:
                    signfixdict[branch.replace("-", "m")] = array('f',[0])
                    t.SetBranchAddress(branch, signfixdict[branch.replace("-", "m")])
                    branchdict[branch.replace("-", "m")] = [] 

            branchdict["EventTag"] = []
            branchdict["Dbkg"] = []
            branchdict["Dbsi"] = []
            branchdict["Bin40"] = []
            branchdict["D2jVBF"] = []
            branchdict["D2jZH"] = []
            branchdict["D2jWH"] = []

            for ent in trange(t.GetEntries()):

                #================ Loop over events ================

                while t.GetEntry(ent):

                    #================ Fill failed events with dummy and skip to loop over branches ================

                    branchdict["Bin40"].append(f.Get("ZZTree/Counters").GetBinContent(40))
                    if tree == "candTree_failed":
                        branchdict["EventTag"].append(-999)
                        branchdict["Dbkg"].append(-999)
                        branchdict["Dbsi"].append(-999)
                        branchdict["D2jVBF"].append(-999)
                        branchdict["D2jZH"].append(-999)
                        branchdict["D2jWH"].append(-999)
                        for key in signfixdict.keys():
                            branchdict[key].append(signfixdict[key][0])
                        break

                    #================ Tagging event by category ================

                    ZZMass = t.ZZMass

                    tag = "none"
 
                    D_VBF2j = DVBF2j_ME(t.p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal, t.p_JJQCD_SIG_ghg2_1_JHUGen_JECNominal, ZZMass, cConstants_list)
                    branchdict["D2jVBF"].append(D_VBF2j)
                    WP_VBF2j = getDVBF2jetsWP(ZZMass, useQGTagging)

                    D_WHh = DWHh_ME(t.p_HadWH_SIG_ghw1_1_JHUGen_JECNominal, t.p_JJQCD_SIG_ghg2_1_JHUGen_JECNominal, t.p_HadWH_mavjj_JECNominal, t.p_HadWH_mavjj_true_JECNominal, ZZMass, cConstants_list)
                    branchdict["D2jWH"].append(D_WHh)
                    WP_WHh = getDWHhWP(ZZMass, useQGTagging)

                    D_ZHh = DZHh_ME(t.p_HadWH_SIG_ghw1_1_JHUGen_JECNominal, t.p_JJQCD_SIG_ghg2_1_JHUGen_JECNominal, t.p_HadWH_mavjj_JECNominal, t.p_HadWH_mavjj_true_JECNominal, ZZMass, cConstants_list)
                    branchdict["D2jZH"].append(D_ZHh)
                    WP_ZHh = getDZHhWP(ZZMass, useQGTagging)

                    if( t.nExtraLep==0 and (((t.nCleanedJetsPt30==2 or t.nCleanedJetsPt30==3) and t.nCleanedJetsPt30BTagged_bTagSF<=1) or (t.nCleanedJetsPt30>=4 and t.nCleanedJetsPt30BTagged_bTagSF==0)) and D_VBF2j>WP_VBF2j ):
                        tag = "VBF"

                    elif( t.nExtraLep==0 and (t.nCleanedJetsPt30==2 or t.nCleanedJetsPt30==3 or (t.nCleanedJetsPt30>=4 and t.nCleanedJetsPt30BTagged_bTagSF==0)) and (D_WHh>WP_WHh or D_ZHh>WP_ZHh)):
                        tag = "VH"

                    #================ Saving category tag ================

                    if tag == "VBF": branchdict["EventTag"].append(1)
                    elif tag == "VH": branchdict["EventTag"].append(2)
                    else: branchdict["EventTag"].append(0)

                    #================ Calculating EW discriminants ================

                    ZZFlav = t.Z1Flav * t.Z2Flav

                    if tag == "VBF":

                        D1 = D_bkg_kin_VBFdecay(t.p_JJVBF_S_SIG_ghv1_1_MCFM_JECNominal,t.p_HadZH_S_SIG_ghz1_1_MCFM_JECNominal,t.p_HadWH_S_SIG_ghw1_1_MCFM_JECNominal,t.p_JJVBF_BKG_MCFM_JECNominal,t.p_HadZH_BKG_MCFM_JECNominal,t.p_HadWH_BKG_MCFM_JECNominal,t.p_JJQCD_BKG_MCFM_JECNominal,t.p_HadZH_mavjj_JECNominal,t.p_HadZH_mavjj_true_JECNominal,t.p_HadWH_mavjj_JECNominal,t.p_HadWH_mavjj_true_JECNominal,t.pConst_JJVBF_S_SIG_ghv1_1_MCFM_JECNominal,t.pConst_HadZH_S_SIG_ghz1_1_MCFM_JECNominal,t.pConst_HadWH_S_SIG_ghw1_1_MCFM_JECNominal,t.pConst_JJVBF_BKG_MCFM_JECNominal,t.pConst_HadZH_BKG_MCFM_JECNominal,t.pConst_HadWH_BKG_MCFM_JECNominal,t.pConst_JJQCD_BKG_MCFM_JECNominal,cConstants_list,ZZFlav,ZZMass)

                        D2 = D_int_trigphase([t.p_JJVBF_S_SIG_ghv1_1_MCFM_JECNominal, t.p_JJVBF_BKG_MCFM_JECNominal, t.p_JJVBF_S_BSI_ghv1_1_MCFM_JECNominal, t.pConst_JJVBF_S_SIG_ghv1_1_MCFM_JECNominal, t.pConst_JJVBF_BKG_MCFM_JECNominal])

                    elif tag == "VH":
                        
                        D1 = D_bkg_kin_HadVHdecay(t.p_JJVBF_S_SIG_ghv1_1_MCFM_JECNominal,t.p_HadZH_S_SIG_ghz1_1_MCFM_JECNominal,t.p_HadWH_S_SIG_ghw1_1_MCFM_JECNominal,t.p_JJVBF_BKG_MCFM_JECNominal,t.p_HadZH_BKG_MCFM_JECNominal,t.p_HadWH_BKG_MCFM_JECNominal,t.p_JJQCD_BKG_MCFM_JECNominal,t.p_HadZH_mavjj_JECNominal,t.p_HadZH_mavjj_true_JECNominal,t.p_HadWH_mavjj_JECNominal,t.p_HadWH_mavjj_true_JECNominal,t.pConst_JJVBF_S_SIG_ghv1_1_MCFM_JECNominal,t.pConst_HadZH_S_SIG_ghz1_1_MCFM_JECNominal,t.pConst_HadWH_S_SIG_ghw1_1_MCFM_JECNominal,t.pConst_JJVBF_BKG_MCFM_JECNominal,t.pConst_HadZH_BKG_MCFM_JECNominal,t.pConst_HadWH_BKG_MCFM_JECNominal,t.pConst_JJQCD_BKG_MCFM_JECNominal,cConstants_list,ZZFlav,ZZMass)

                        D2 = D_int_trigphase_avg([t.p_HadZH_S_SIG_ghz1_1_MCFM_JECNominal, t.p_HadZH_BKG_MCFM_JECNominal, t.p_HadZH_S_BSI_ghz1_1_MCFM_JECNominal, t.pConst_HadZH_S_SIG_ghz1_1_MCFM_JECNominal, t.pConst_HadZH_BKG_MCFM_JECNominal, t.p_HadWH_S_SIG_ghw1_1_MCFM_JECNominal, t.p_HadWH_BKG_MCFM_JECNominal, t.p_HadWH_S_BSI_ghw1_1_MCFM_JECNominal, t.pConst_HadWH_S_SIG_ghw1_1_MCFM_JECNominal, t.pConst_HadWH_BKG_MCFM_JECNominal])

                    #================ Calculating gg discriminants ================

                    #elif tag == "none":
                    else:

                        D1 = D_bkg_kin(t.p_GG_SIG_ghg2_1_ghz1_1_JHUGen,t.p_QQB_BKG_MCFM,cConstants_list,ZZFlav,ZZMass)

                        D2 = D_int_trigphase([t.p_GG_SIG_kappaTopBot_1_ghz1_1_MCFM, t.p_GG_BKG_MCFM, t.p_GG_BSI_kappaTopBot_1_ghz1_1_MCFM, t.pConst_GG_SIG_kappaTopBot_1_ghz1_1_MCFM, t.pConst_GG_BKG_MCFM])

                    #================ Saving calculated discriminants ================

                    branchdict["Dbkg"].append(D1)
                    branchdict["Dbsi"].append(D2)

                    #================ Saving signed branches ================

                    for key in signfixdict.keys():
                        branchdict[key].append(signfixdict[key][0])

                    break

            print("\n================ Selecting and cloning branches from '"+tree+"' ================\n")

            for i in trange(len(treebranches)):
                branch = treebranches[i]
                if branch not in branchlist or "-" in branch:
                    t.SetBranchStatus(branch, 0)

            ftemptree = ROOT.TFile(tagtreefilename.replace(".root", "_subtree"+str(tind)+".root"), "CREATE")
            
            t.SetObject('eventTree', 'eventTree')

            exec("new{} = t.CloneTree(-1, 'fast')".format(tree))

            for key in branchdict.keys():
                exec("array2tree(np.array(branchdict['{}'], dtype=[('{}', np.single)]), tree=new{})".format(key, key, tree))

            print("\n================ Saving processed '"+tree+"' ================\n")

            exec("new{}.SetName('eventTree')".format(tree))

            exec("new{}.Write()".format(tree))

            ftemptree.Close()
            
            print("Modified '{}' written to '{}'".format(tree, tagtreefilename.replace(".root", "_subtree"+str(tind)+".root")))

        f.Close()

        print("\n================ Building and saving final merged eventTree ================\n")

        mergecmd = "hadd -O {}".format(tagtreefilename)

        for i in range(len(treenames)):
            if os.path.exists(tagtreefilename.replace(".root", "_subtree"+str(i)+".root")):
                mergecmd = mergecmd + " {}".format(tagtreefilename.replace(".root", "_subtree"+str(i)+".root"))
        
        process = subprocess.Popen(mergecmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        process.communicate()

        print("Merged eventTree written to '{}'\n".format(tagtreefilename))

        if removesubtrees:
            for i in range(len(treenames)):
                if os.path.exists(tagtreefilename.replace(".root", "_subtree"+str(i)+".root")):
                    os.remove(tagtreefilename.replace(".root", "_subtree"+str(i)+".root"))

        f = ROOT.TFile(tagtreefilename, 'READ')
        t = f.Get("eventTree")
        t.Print()
        f.Close()
        print("")

if __name__ == "__main__":
    main(sys.argv[1:])
