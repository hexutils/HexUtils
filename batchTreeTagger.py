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

def main(argv):
    inputfile = ''
    pthsubdir = ''
    outputdir = ''
    branchfile = ''
    removesubtrees = ''
    try:
        opts, args = getopt.getopt(argv,"hi:s:o:b:c:",["ifile=","subdr=","outdr=","bfile=","clean="])
    except getopt.GetoptError:
        print('\nbatchTreeTagger.py -i <inputfile> -s <subdirectory> -o <outputdir> -b <branchfile> (-c <removesubtrees>)\n')
        exit()
    for opt, arg in opts:
        if opt == '-h' or opt == '--help':
            print('\nbatchTreeTagger.py -i <inputfile> -s <subdirectory> -o <outputdir> -b <branchfile> (-c <removesubtrees>)\n')
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
        print('\nbatchTreeTagger.py -i <inputfile> -s <subdirectory> -o <outputdir> -b <branchfile> (-c <removesubtrees>)\n')
        exit()

    if not outputdir.endswith("/"):
        outputdir = outputdir+"/"

    if not pthsubdir.endswith("/"):
        pthsubdir = pthsubdir+"/"

    pthsubdir = pthsubdir.split("/")[-2]

    removesubtrees = removesubtrees.replace(" ", "").capitalize()

    if not Path(inputfile).exists():
        print("\nERROR: \tROOT file '" + inputfile + "' cannot be located. Please try again with valid input.\n")
        print('batchTreeTagger.py -i <inputfile> -s <subdirectory> -o <outputdir> -b <branchfile> (-c <removesubtrees>)\n')
        exit()

    if not Path(branchfile).exists():
        print("\nERROR: \tBranches list '" + branchfile + "' cannot be located. Please try again with valid input.\n")
        print('batchTreeTagger.py -i <inputfile> -s <subdirectory> -o <outputdir> -b <branchfile> (-c <removesubtrees>)\n')
        exit()

    if pthsubdir not in inputfile:
        print("\nERROR: \tSubdirectory '" + pthsubdir + "' is not in the input path. Please try again with valid input.\n")
        print('batchTreeTagger.py -i <inputfile> -s <subdirectory> -o <outputdir> -b <branchfile> (-c <removesubtrees>)\n')
        exit()

    if len(removesubtrees) > 0:
        if removesubtrees not in ["True", "False"]:
            print("\nERROR: \tOption '-c' is expected to be True or False. Please try again with valid input.\n")
            print('batchTreeTagger.py -i <inputfile> -s <subdirectory> -o <outputdir> -b <branchfile> (-c <removesubtrees>)\n')
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

    #================ Check existence of output and set up target branches ================

    print("================ Check output location and set up branches ================\n")

    if not Path(filename).exists():
        print("ERROR: \t'" + filename + "' does not exist!\n")
        exit()

    elif Path(tagtreefilename).exists() or glob.glob(tagtreefilename.replace(".root", "_subtree*.root")):
        print("ERROR: \t'" + tagtreefilename + "' or parts of it already exist!\n\tNote that part to all of the final eventTree can be reconstructed from its subtree files if necessary.\n")
        exit()

    else:
        print("Pre-existing output TTree not found --- safe to proceed")
        if not Path("/".join(tagtreefilename.split("/")[:-1])).exists():
            Path("/".join(tagtreefilename.split("/")[:-1])).mkdir(True, True)

        branchlist = []

        with open(branchlistpath) as f:
            blist = [line.rstrip() for line in f]

        for branch in blist:
            if branch: branchlist.append(branch)

        f = ROOT.TFile(filename, 'READ')

        treenames = ["candTree", "candTree_failed"]

        #================ Loop over target trees ================

        for tind, tree in enumerate(treenames):
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

            for ent in trange(t.GetEntries()):

                #================ Loop over events ================

                while t.GetEntry(ent):

                    #================ Fill failed events with dummy and skip to loop over branches ================

                    branchdict["Bin40"].append(f.Get("ZZTree/Counters").GetBinContent(40))
                    if tree == "candTree_failed":
                        branchdict["EventTag"].append(-999)
                        branchdict["Dbkg"].append(-999)
                        branchdict["Dbsi"].append(-999)
                        for key in signfixdict.keys():
                            branchdict[key].append(signfixdict[key][0])
                        break

                    #================ Tagging event by category ================

                    M = t.ZZMass

                    tag = "none"

                    const2jv = WPCshift2jv * D2jetVBFSpline.Eval(M)
                    vars2jv = [t.p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal, t.p_JJQCD_SIG_ghg2_1_JHUGen_JECNominal]
                    if not any(var < 0 for var in vars2jv):
                        if (vars2jv[0]+const2jv*vars2jv[1]) != 0:
                            D2jv = vars2jv[0]/(vars2jv[0]+const2jv*vars2jv[1])
                            if D2jv > 0.5:
                                if (((t.nCleanedJetsPt30>1) and (t.nCleanedJetsPt30<4)) and (t.nCleanedJetsPt30BTagged<2)) or ((t.nCleanedJetsPt30>3) and (t.nCleanedJetsPt30BTagged==0)):
                                    tag = "VBF"
                        else: 
                            D2jv = -999


                    const2jz = WPCshift2jz * D2jetZHSpline.Eval(M)
                    vars2jz = [t.p_HadZH_SIG_ghz1_1_JHUGen_JECNominal, t.p_HadZH_mavjj_JECNominal, t.p_JJQCD_SIG_ghg2_1_JHUGen_JECNominal, t.p_HadZH_mavjj_true_JECNominal]
                    if not any(var < 0 for var in vars2jz):
                        if (vars2jz[0]*vars2jz[1]+const2jz*vars2jz[2]*vars2jz[3]) != 0:
                            D2jz = vars2jz[0]*vars2jz[1]/(vars2jz[0]*vars2jz[1]+const2jz*vars2jz[2]*vars2jz[3])
                            if D2jz > 0.5:
                                if ((t.nCleanedJetsPt30>1) and (t.nCleanedJetsPt30<4)) or ((t.nCleanedJetsPt30>3) and (t.nCleanedJetsPt30BTagged==0)):
                                    tag = "VH"
                        else: 
                            D2jz = -999


                    const2jw = WPCshift2jw * D2jetWHSpline.Eval(M)
                    vars2jw = [t.p_HadWH_SIG_ghw1_1_JHUGen_JECNominal, t.p_HadWH_mavjj_JECNominal, t.p_JJQCD_SIG_ghg2_1_JHUGen_JECNominal, t.p_HadWH_mavjj_true_JECNominal]
                    if not any(var < 0 for var in vars2jw):
                        if (vars2jw[0]*vars2jw[1]+const2jw*vars2jw[2]*vars2jw[3]) != 0:
                            D2jw = vars2jw[0]*vars2jw[1]/(vars2jw[0]*vars2jw[1]+const2jw*vars2jw[2]*vars2jw[3])
                            if D2jw > 0.5:
                                if ((t.nCleanedJetsPt30>1) and (t.nCleanedJetsPt30<4)) or ((t.nCleanedJetsPt30>3) and (t.nCleanedJetsPt30BTagged==0)):
                                    tag = "VH"
                        else: 
                            D2jw = -999

                    #================ Saving category tag ================

                    if tag == "VBF": branchdict["EventTag"].append(1)
                    elif tag == "VH": branchdict["EventTag"].append(2)
                    else: branchdict["EventTag"].append(0)

                    #================ Calculating EW discriminants ================

                    ZZflav = t.Z1Flav * t.Z2Flav

                    if tag == "VBF" or tag == "VH":

                        if tag == "VH":
                            if (abs(ZZflav)==11*11*11*11 or abs(ZZflav)==2*11*11*11*11 or abs(ZZflav)==2*11*11*2*11*11): const1 = DbkgjjEWQCDSpline4lHadVH.Eval(M)
                            elif (abs(ZZflav)==11*11*13*13 or abs(ZZflav)==2*11*11*13*13 or abs(ZZflav)==2*11*11*2*13*13): const1 = DbkgjjEWQCDSpline2l2lHadVH.Eval(M)
                            elif (abs(ZZflav)==13*13*13*13 or abs(ZZflav)==2*13*13*13*13 or abs(ZZflav)==2*13*13*2*13*13): const1 = DbkgjjEWQCDSpline4lHadVH.Eval(M)
                            else:
                                branchdict["Dbkg"].append(-999)
                                branchdict["Dbsi"].append(-999)
                                break

                        elif tag == "VBF":
                            if (abs(ZZflav)==11*11*11*11 or abs(ZZflav)==2*11*11*11*11 or abs(ZZflav)==2*11*11*2*11*11): const1 = DbkgjjEWQCDSpline4lJJVBF.Eval(M)
                            elif (abs(ZZflav)==11*11*13*13 or abs(ZZflav)==2*11*11*13*13 or abs(ZZflav)==2*11*11*2*13*13): const1 = DbkgjjEWQCDSpline2l2lJJVBF.Eval(M)
                            elif (abs(ZZflav)==13*13*13*13 or abs(ZZflav)==2*13*13*13*13 or abs(ZZflav)==2*13*13*2*13*13): const1 = DbkgjjEWQCDSpline4lJJVBF.Eval(M)
                            else:
                                branchdict["Dbkg"].append(-999)
                                branchdict["Dbsi"].append(-999)
                                break

                        var = [t.p_JJVBF_S_SIG_ghv1_1_MCFM_JECNominal, t.p_HadZH_S_SIG_ghz1_1_MCFM_JECNominal, t.p_HadWH_S_SIG_ghw1_1_MCFM_JECNominal, t.p_JJVBF_BKG_MCFM_JECNominal, t.p_HadZH_BKG_MCFM_JECNominal, t.p_HadWH_BKG_MCFM_JECNominal, t.p_JJQCD_BKG_MCFM_JECNominal, t.p_HadZH_mavjj_JECNominal, t.p_HadZH_mavjj_true_JECNominal, t.p_HadWH_mavjj_JECNominal, t.p_HadWH_mavjj_true_JECNominal, t.pConst_JJVBF_S_SIG_ghv1_1_MCFM_JECNominal, t.pConst_HadZH_S_SIG_ghz1_1_MCFM_JECNominal, t.pConst_HadWH_S_SIG_ghw1_1_MCFM_JECNominal, t.pConst_JJVBF_BKG_MCFM_JECNominal, t.pConst_HadZH_BKG_MCFM_JECNominal, t.pConst_HadWH_BKG_MCFM_JECNominal, t.pConst_JJQCD_BKG_MCFM_JECNominal]

                        if any(v == 0 for v in [var[11], var[12], var[13], var[14], var[15], var[16], var[17], var[8], var[10]]) or any(v < 0 for v in var): 
                            D1 = -999

                        else:
                            vbf = var[0]/var[11]
                            zh = var[1]/var[12]
                            wh = var[2]/var[13]
                            constA = 1./(1./var[11]+1./var[12]+1./var[13])

                            vbs = var[3]/var[14]
                            zzz = var[4]/var[15]
                            wzz = var[5]/var[16]
                            qcdzz = var[6]/var[17]
                            constB = 1./(1./var[14]+1./var[15]+1./var[16]+1./var[17])

                            scale_Pmjj_vb=1
                            scale_Pmjj_z = var[7]/var[8]
                            scale_Pmjj_w = var[9]/var[10]

                            vbf *= scale_Pmjj_vb
                            vbs *= scale_Pmjj_vb

                            zh *= scale_Pmjj_z
                            zzz *= scale_Pmjj_z

                            wh *= scale_Pmjj_w
                            wzz *= scale_Pmjj_w

                            PA = (vbf + zh + wh)*constA
                            PB = (vbs + zzz + wzz + qcdzz)*constB

                            d = (PA+const1*PB)
                            if d != 0:
                                D1 = PA/d
                            else:
                                D1 = -999

                        if tag == "VH":
                            if (abs(ZZflav)==11*11*11*11 or abs(ZZflav)==2*11*11*11*11 or abs(ZZflav)==2*11*11*2*11*11): const2 = DbkgjjEWQCDSpline4lHadVH.Eval(M)
                            elif (abs(ZZflav)==11*11*13*13 or abs(ZZflav)==2*11*11*13*13 or abs(ZZflav)==2*11*11*2*13*13): const2 = DbkgjjEWQCDSpline2l2lHadVH.Eval(M)
                            elif (abs(ZZflav)==13*13*13*13 or abs(ZZflav)==2*13*13*13*13 or abs(ZZflav)==2*13*13*2*13*13): const2 = DbkgjjEWQCDSpline4lHadVH.Eval(M)
                            else: 
                                branchdict["Dbkg"].append(-999)
                                branchdict["Dbsi"].append(-999)
                                break

                        elif tag == "VBF":
                            if (abs(ZZflav)==11*11*11*11 or abs(ZZflav)==2*11*11*11*11 or abs(ZZflav)==2*11*11*2*11*11): const2 = DbkgjjEWQCDSpline4lJJVBF.Eval(M)
                            elif (abs(ZZflav)==11*11*13*13 or abs(ZZflav)==2*11*11*13*13 or abs(ZZflav)==2*11*11*2*13*13): const2 = DbkgjjEWQCDSpline2l2lJJVBF.Eval(M)
                            elif (abs(ZZflav)==13*13*13*13 or abs(ZZflav)==2*13*13*13*13 or abs(ZZflav)==2*13*13*2*13*13): const2 = DbkgjjEWQCDSpline4lJJVBF.Eval(M)
                            else: 
                                branchdict["Dbkg"].append(-999)
                                branchdict["Dbsi"].append(-999)
                                break


                        var = [t.p_JJVBF_S_SIG_ghv1_1_MCFM_JECNominal, t.p_HadZH_S_SIG_ghz1_1_MCFM_JECNominal, t.p_HadWH_S_SIG_ghw1_1_MCFM_JECNominal, t.p_JJVBF_BKG_MCFM_JECNominal, t.p_HadZH_BKG_MCFM_JECNominal, t.p_HadWH_BKG_MCFM_JECNominal, t.p_JJQCD_BKG_MCFM_JECNominal, t.p_HadZH_mavjj_JECNominal, t.p_HadZH_mavjj_true_JECNominal, t.p_HadWH_mavjj_JECNominal, t.p_HadWH_mavjj_true_JECNominal, t.pConst_JJVBF_S_SIG_ghv1_1_MCFM_JECNominal, t.pConst_HadZH_S_SIG_ghz1_1_MCFM_JECNominal, t.pConst_HadWH_S_SIG_ghw1_1_MCFM_JECNominal, t.pConst_JJVBF_BKG_MCFM_JECNominal, t.pConst_HadZH_BKG_MCFM_JECNominal, t.pConst_HadWH_BKG_MCFM_JECNominal, t.pConst_JJQCD_BKG_MCFM_JECNominal, t.p_JJVBF_S_BSI_ghv1_1_MCFM_JECNominal, t.p_HadZH_S_BSI_ghz1_1_MCFM_JECNominal, t.p_HadWH_S_BSI_ghw1_1_MCFM_JECNominal]

                        if any(v == 0 for v in [var[11], var[12], var[13], var[14], var[15], var[16], var[17], var[8], var[10]]) or any(v < 0 for v in var): 
                            D2 = -999

                        else:
                            vbf = var[0]/var[11]
                            zh = var[1]/var[12]
                            wh = var[2]/var[13]
                            constA = 1./(1./var[11]+1./var[12]+1./var[13])

                            vbs = var[3]/var[14]
                            zzz = var[4]/var[15]
                            wzz = var[5]/var[16]
                            qcdzz = var[6]/var[17]
                            constB = 1./(1./var[14]+1./var[15]+1./var[16]+1./var[17])

                            vbf_vbs_int = var[18]*(1./var[11]+1./var[14]) - vbf - vbs
                            zh_zzz_int = var[19]*(1./var[12]+1./var[15]) - zh - zzz
                            wh_wzz_int = var[20]*(1./var[13]+1./var[16]) - wh - wzz

                            scale_Pmjj_vb=1
                            scale_Pmjj_z = var[7]/var[8]
                            scale_Pmjj_w = var[9]/var[10]

                            vbf *= scale_Pmjj_vb
                            vbs *= scale_Pmjj_vb
                            vbf_vbs_int *= scale_Pmjj_vb

                            zh *= scale_Pmjj_z
                            zzz *= scale_Pmjj_z
                            zh_zzz_int *= scale_Pmjj_z

                            wh *= scale_Pmjj_w
                            wzz *= scale_Pmjj_w
                            wh_wzz_int *= scale_Pmjj_w

                            PA = (vbf + zh + wh)*constA
                            PB = (vbs + zzz + wzz + qcdzz)*constB
                            d = (PA+const2*PB)
                            if (d != 0) and (constA*constB >= 0) and (const2 >= 0):
                                Pint = (vbf_vbs_int + zh_zzz_int + wh_wzz_int)*sqrt(constA*constB)
                                D2 = Pint*sqrt(const2)/d
                            else:
                                D2 = -999

                    #================ Calculating gg discriminants ================

                    elif tag == "none":

                        if (abs(ZZflav)==11*11*11*11 or abs(ZZflav)==2*11*11*11*11 or abs(ZZflav)==2*11*11*2*11*11): const1 = DbkgkinSpline4e.Eval(M)
                        elif (abs(ZZflav)==11*11*13*13 or abs(ZZflav)==2*11*11*13*13 or abs(ZZflav)==2*11*11*2*13*13): const1 = DbkgkinSpline2e2mu.Eval(M)
                        elif (abs(ZZflav)==13*13*13*13 or abs(ZZflav)==2*13*13*13*13 or abs(ZZflav)==2*13*13*2*13*13): const1 = DbkgkinSpline4mu.Eval(M)
                        else: 
                            branchdict["Dbkg"].append(-999)
                            branchdict["Dbsi"].append(-999)
                            break

                        var = [t.p_GG_SIG_ghg2_1_ghz1_1_JHUGen, t.p_QQB_BKG_MCFM]
                        if any(v < 0 for v in var): 
                            D1 = -999

                        else:
                            d = (var[0]+const1*var[1])
                            if d != 0:
                                D1 = var[0]/d
                            else:
                                D1 = -999

                        if (abs(ZZflav)==11*11*11*11 or abs(ZZflav)==2*11*11*11*11 or abs(ZZflav)==2*11*11*2*11*11): const2 = DggbkgkinSpline4e.Eval(M)
                        elif (abs(ZZflav)==11*11*13*13 or abs(ZZflav)==2*11*11*13*13 or abs(ZZflav)==2*11*11*2*13*13): const2 = DggbkgkinSpline2e2mu.Eval(M)
                        elif (abs(ZZflav)==13*13*13*13 or abs(ZZflav)==2*13*13*13*13 or abs(ZZflav)==2*13*13*2*13*13): const2 = DggbkgkinSpline4mu.Eval(M)
                        else: 
                                branchdict["Dbkg"].append(-999)
                                branchdict["Dbsi"].append(-999)
                                break


                        var = [t.p_GG_SIG_kappaTopBot_1_ghz1_1_MCFM, t.p_GG_BKG_MCFM, t.p_GG_BSI_kappaTopBot_1_ghz1_1_MCFM, t.pConst_GG_SIG_kappaTopBot_1_ghz1_1_MCFM, t.pConst_GG_BKG_MCFM]
                        if any(v == 0 for v in var[3:]) or any(v < 0 for v in var[:3]): 
                            D2 = -999

                        else:
                            d = (var[0]+const2*var[1])
                            if (d != 0) and (var[3]*var[4]*const2 >= 0):
                                D2 = (var[2]*(1./var[3]+1./var[4])-var[0]/var[3]-var[1]/var[4])*sqrt(var[3]*var[4]*const2)/d
                            else:
                                D2 = -999

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

        mergecmd = "hadd -f {}".format(tagtreefilename)

        for i in range(len(treenames)):
            mergecmd = mergecmd + " {}".format(tagtreefilename.replace(".root", "_subtree"+str(i)+".root"))
        
        process = subprocess.Popen(mergecmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        process.communicate()

        print("Merged eventTree written to '{}' with return code {}\n".format(tagtreefilename, process.returncode))

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
