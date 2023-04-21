#!/usr/bin/python3

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
from AnalysisTools.data import gConstants as gConstants
from AnalysisTools.data import cConstants as cConstants
from AnalysisTools.Utils import Config as Config
from AnalysisTools.Utils import OnShell_Category as OnShell_Category
from AnalysisTools.Utils import Discriminants as Discriminants
from AnalysisTools.Utils import OnShell_Help as OnShell_Help

def main(argv):
    inputfile = ''
    outputdir = ''
    branchfile = ''
    isData = False 
    try:
        opts, args = getopt.getopt(argv,"hi:o:b:d:",["ifile=","ofile=","bfile=","dfile="])
    except getopt.GetoptError:
        print('batchTreeTagger.py -i <inputfile> -o <outputdir> -b <branchfile> -d <isData>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('batchTreeTagger.py -i <inputfile> -o <outputdir> -b <branchfile> -d <isData>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputdir = arg
        elif opt in ("-b", "--bfile"):
            branchfile = arg
        elif opt in ("-d", "--dfile"):
            isData = arg
    if not all([inputfile, outputdir, branchfile, isData]):
        print('batchTreeTagger.py -i <inputfile> -o <outputdir> -b <branchfile> -d <isData>')
        sys.exit(2)

    if not outputdir.endswith("/"):
        outputdir = outputdir+"/"
    if arg.upper()=="TRUE":
        isData = True
    elif arg.upper()=="FALSE":
        isData = False
    print("\n================ Reading user input ================\n")

    print("Input CJLST TTree is '{}'".format(inputfile))
    print("Output directory is '{}'".format(outputdir))
    print("Branch list file is '{}'".format(branchfile))
    print("Treat as data: '{}'".format(isData))
    print("\n================ Processing user input ================\n")

    #=============== Load the Analysis Config =================
    cConstants_list = cConstants.init_cConstants()
    gConstants_list = gConstants.init_gConstants()
    #Analysis_Config = Config.Analysis_Config("OnShell_HVV_Photons_2021")
    Analysis_Config = Config.Analysis_Config("gammaH_Photons_Decay_Only")

    #================ Set input file path and output file path ================
    
    filename = inputfile
    branchlistpath = branchfile
    tagtreepath = outputdir

    ind = filename.split("/").index(Analysis_Config.TreeFile)

    tagtreefile = "/".join(filename.split("/")[ind:])
    tagtreefilename = tagtreepath+tagtreefile

    print("Read '"+filename+"'\n")
    print("Write '"+tagtreefilename+"'\n")

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

        if Analysis_Config.Save_Failed:
          treenames = ["candTree", "candTree_failed"]
        else:
          treenames = ["candTree"]
        #================ Loop over target trees ================

        for tind, tree in enumerate(treenames):
            ftemptree = ROOT.TFile(tagtreefilename.replace(".root", "_subtree"+str(tind)+".root"), "CREATE")

            print("\n================ Reading events from '" + tree + "' and calculating new branches ================\n")
            if not isData and "AllData" in tagtreefilename:
              print("here")
              t = f.Get("CRZLLTree/"+tree)
            else:
              t = f.Get("ZZTree/"+tree)

            treebranches = [ x.GetName() for x in t.GetListOfBranches() ]

            branchdict = {}
            signfixdict = {}
            # Save any Branch with p_ in the name. This allows for variable branch names in different samples #
            if Analysis_Config.Save_p == True:
              for branch in treebranches: 
                if 'p_' in branch:
                  branchlist.append(branch)
            for branch in branchlist:
                if "-" in branch and branch in treebranches:
                    signfixdict[branch.replace("-", "m")] = array('f',[0])
                    t.SetBranchAddress(branch, signfixdict[branch.replace("-", "m")])
                    branchdict[branch.replace("-", "m")] = [] 
                elif branch not in treebranches:
                    branchdict[branch.replace("-", "m")] = [-999] * t.GetEntries()
	   
            branchdict["EventTag"] = []
            branchdict["Bin40"] = []
            
            # Load the Disriminants to be saved as branches #
            for name in Analysis_Config.Discriminants_To_Calculate:
              branchdict[name] = []
            #for ent in trange(t.GetEntries()):
            for ent in trange(t.GetEntries()):

                #================ Loop over events ================

                while t.GetEntry(ent):

                    #================ Fill failed events with dummy and skip to loop over branches ================

                    branchdict["Bin40"].append(f.Get("ZZTree/Counters").GetBinContent(40))
                    if tree == "candTree_failed":
                        branchdict["EventTag"].append(-999)
                        for name in Analysis_Config.Discriminants_To_Calculate:
                          branchdict[name].append(-999)
                        for key in signfixdict.keys():
                            branchdict[key].append(signfixdict[key][0])
                        break
            
                    #================ Tagging event by category ================				
                    if Analysis_Config.TaggingProcess == "Tag_AC_19_Scheme_2":
                      Protect = OnShell_Category.Protect_Category_Against_NAN(t.pConst_JJVBF_S_SIG_ghv1_1_MCFM_JECNominal,
                                 t.pConst_HadZH_S_SIG_ghz1_1_MCFM_JECNominal,
                                 t.pConst_HadWH_S_SIG_ghw1_1_MCFM_JECNominal,
                                 t.pConst_JJVBF_BKG_MCFM_JECNominal,
                                 t.pConst_HadZH_BKG_MCFM_JECNominal,
                                 t.pConst_HadWH_BKG_MCFM_JECNominal,
                                 t.pConst_JJQCD_BKG_MCFM_JECNominal,
                                 t.p_HadZH_mavjj_true_JECNominal,
                                 t.p_HadWH_mavjj_true_JECNominal,
                                 t.p_JVBF_SIG_ghv1_1_JHUGen_JECNominal,
                                 t.pAux_JVBF_SIG_ghv1_1_JHUGen_JECNominal,
                                 t.p_HadWH_mavjj_JECNominal,
                                 t.p_HadWH_SIG_ghw1_1_JHUGen_JECNominal,
                                 t.p_HadZH_mavjj_JECNominal,
                                 t.p_HadZH_SIG_ghz1_1_JHUGen_JECNominal)
                      if Protect:
                        branchdict["EventTag"].append(-999)
                      else:
                        tag = OnShell_Category.Tag_AC_19_Scheme_2( t.nExtraLep,  
                                                   t.nExtraZ,
                                                   t.nCleanedJetsPt30,
                                                   t.nCleanedJetsPt30BTagged_bTagSF,  
                                                   t.JetQGLikelihood, 
                                                   t.p_JJQCD_SIG_ghg2_1_JHUGen_JECNominal,  
                                                   t.p_JQCD_SIG_ghg2_1_JHUGen_JECNominal,
                                                   t.p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal, 
                                                   t.p_JJVBF_SIG_ghv2_1_JHUGen_JECNominal,
                                                   t.p_JJVBF_SIG_ghv4_1_JHUGen_JECNominal,
                                                   t.p_JJVBF_SIG_ghv1prime2_1E4_JHUGen_JECNominal,
                                                   t.p_JJVBF_SIG_ghza1prime2_1E4_JHUGen_JECNominal,
                                                   t.p_JVBF_SIG_ghv1_1_JHUGen_JECNominal,
                                                   t.pAux_JVBF_SIG_ghv1_1_JHUGen_JECNominal,  
                                                   t.p_HadWH_SIG_ghw1_1_JHUGen_JECNominal,  
                                                   t.p_HadWH_SIG_ghw2_1_JHUGen_JECNominal,  
                                                   t.p_HadWH_SIG_ghw4_1_JHUGen_JECNominal,  
                                                   t.p_HadWH_SIG_ghw1prime2_1E4_JHUGen_JECNominal,  
                                                   t.p_HadZH_SIG_ghz1_1_JHUGen_JECNominal,
                                                   t.p_HadZH_SIG_ghz2_1_JHUGen_JECNominal,   
                                                   t.p_HadZH_SIG_ghz4_1_JHUGen_JECNominal,   
                                                   t.p_HadZH_SIG_ghz1prime2_1E4_JHUGen_JECNominal,   
                                                   t.p_HadZH_SIG_ghza1prime2_1E4_JHUGen_JECNominal,  
                                                   t.p_HadWH_mavjj_JECNominal,  
                                                   t.p_HadWH_mavjj_true_JECNominal,  
                                                   t.p_HadZH_mavjj_JECNominal,
                                                   t.p_HadZH_mavjj_true_JECNominal,  
                                                   t.JetPhi,  
                                                   t.ZZMass,  
                                                   t.ZZPt,  
                                                   t.PFMET,  
                                                   t.PhotonIsCutBasedLooseID, 
                                                   t.PhotonPt, 
                                                   Analysis_Config.useVHMETTagged,  
                                                   Analysis_Config.useQGTagging, 
                                                   cConstants_list, 
                                                   gConstants_list)
                    #================ Saving category tag ================
                        branchdict["EventTag"].append(tag)
                    elif Analysis_Config.TaggingProcess == "Tag_Untagged_and_gammaH":
                      tag = OnShell_Category.Tag_Untagged_and_gammaH(t.PhotonPt,t.PhotonIsCutBasedLooseID)
                      branchdict["EventTag"].append(tag)
                    #============= Save pt_4l discriminants ==============
                    if "Pt4l" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["Pt4l"].append(t.ZZPt)
                    #===== Calculating Useful Info for OnShell Discriminants ======
                    notdijet = OnShell_Help.notdijet(t.p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal)
                    #================ Calculating AC discriminants ================
                    if "D_0minus_decay" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_0minus_decay"].append(Discriminants.D_0minus_decay(t.p_GG_SIG_ghg2_1_ghz1_1_JHUGen,t.p_GG_SIG_ghg2_1_ghz4_1_JHUGen,t.ZZMass,gConstants_list))
                    if "D_CP_decay" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_CP_decay"].append(Discriminants.D_CP_decay(t.p_GG_SIG_ghg2_1_ghz1_1_ghz4_1_JHUGen,t.p_GG_SIG_ghg2_1_ghz1_1_JHUGen,t.p_GG_SIG_ghg2_1_ghz4_1_JHUGen,t.ZZMass,gConstants_list))
                    if "D_0hplus_decay" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_0hplus_decay"].append(Discriminants.D_0hplus_decay(t.p_GG_SIG_ghg2_1_ghz1_1_JHUGen,t.p_GG_SIG_ghg2_1_ghz1_1_ghz2_1_JHUGen,t.ZZMass,gConstants_list))
                    if "D_int_decay" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_int_decay"].append(Discriminants.D_int_decay(t.p_GG_SIG_ghg2_1_ghz1_1_ghz2_1_JHUGen,t.p_GG_SIG_ghg2_1_ghz1_1_JHUGen,t.p_GG_SIG_ghg2_1_ghz2_1_JHUGen,t.ZZMass,gConstants_list))
                    if "D_L1_decay" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_L1_decay"].append(Discriminants.D_L1_decay(t.p_GG_SIG_ghg2_1_ghz1_1_JHUGen,t.p_GG_SIG_ghg2_1_ghz1prime2_1E4_JHUGen,t.ZZMass,gConstants_list))
                    if "D_L1int_decay" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_L1int_decay"].append(Discriminants.D_L1int_decay(t.p_GG_SIG_ghg2_1_ghz1_1_ghz1prime2_1E4_JHUGen,t.p_GG_SIG_ghg2_1_ghz1_1_JHUGen,t.p_GG_SIG_ghg2_1_ghz1prime2_1E4_JHUGen,t.ZZMass,gConstants_list))
                    if "D_L1Zg_decay" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_L1Zg_decay"].append(Discriminants.D_L1Zg_decay(t.p_GG_SIG_ghg2_1_ghz1_1_JHUGen,t.p_GG_SIG_ghg2_1_ghza1prime2_1E4_JHUGen,t.ZZMass,gConstants_list))
                    if "D_L1Zgint_decay" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_L1Zgint_decay"].append(Discriminants.D_L1Zgint_decay(t.p_GG_SIG_ghg2_1_ghz1_1_ghza1prime2_1E4_JHUGen,t.p_GG_SIG_ghg2_1_ghz1_1_JHUGen,t.p_GG_SIG_ghg2_1_ghza1prime2_1E4_JHUGen,t.ZZMass,gConstants_list))
                    if "D_L1L1Zg_decay" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_L1L1Zg_decay"].append(Discriminants.D_L1L1Zg_decay(t.p_GG_SIG_ghg2_1_ghz1prime2_1E4_JHUGen, t.p_GG_SIG_ghg2_1_ghza1prime2_1E4_JHUGen,t.ZZMass,gConstants_list))
                    if "D_L1L1Zgint_decay" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_L1L1Zgint_decay"].append(Discriminants.D_L1L1Zgint_decay(t.p_GG_SIG_ghg2_1_ghz1prime2_1E4_ghza1prime2_1E4_JHUGen,t.p_GG_SIG_ghg2_1_ghz1prime2_1E4_JHUGen,t.p_GG_SIG_ghg2_1_ghza1prime2_1E4_JHUGen,t.ZZMass,gConstants_list))
                    if "D_0minus_Zg_decay" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_0minus_Zg_decay"].append(Discriminants.D_0minus_Zg_decay(t.p_GG_SIG_ghg2_1_ghz1_1_JHUGen,t.p_GG_SIG_ghg2_1_ghza4_1_JHUGen,t.ZZMass,gConstants_list))
                    if "D_CP_Zg_decay" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_CP_Zg_decay"].append(Discriminants.D_CP_Zg_decay(t.p_GG_SIG_ghg2_1_ghz1_1_ghza4_1_JHUGen,t.p_GG_SIG_ghg2_1_ghz1_1_JHUGen,t.p_GG_SIG_ghg2_1_ghza4_1_JHUGen,t.ZZMass,gConstants_list))
                    if "D_0hplus_Zg_decay" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_0hplus_Zg_decay"].append(Discriminants.D_0hplus_Zg_decay(t.p_GG_SIG_ghg2_1_ghz1_1_JHUGen,t.p_GG_SIG_ghg2_1_ghza2_1_JHUGen,t.ZZMass,gConstants_list))
                    if "D_int_Zg_decay" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_int_Zg_decay"].append(Discriminants.D_int_Zg_decay(t.p_GG_SIG_ghg2_1_ghz1_1_ghza2_1_JHUGen,t.p_GG_SIG_ghg2_1_ghz1_1_JHUGen,t.p_GG_SIG_ghg2_1_ghza2_1_JHUGen,t.ZZMass,gConstants_list))
                    if "D_0minus_gg_decay" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_0minus_gg_decay"].append(Discriminants.D_0minus_gg_decay(t.p_GG_SIG_ghg2_1_ghz1_1_JHUGen,t.p_GG_SIG_ghg2_1_gha4_1_JHUGen,t.ZZMass,gConstants_list))
                    if "D_CP_gg_decay" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_CP_gg_decay"].append(Discriminants.D_CP_gg_decay(t.p_GG_SIG_ghg2_1_ghz1_1_gha4_1_JHUGen,t.p_GG_SIG_ghg2_1_ghz1_1_JHUGen,t.p_GG_SIG_ghg2_1_gha4_1_JHUGen,t.ZZMass,gConstants_list))
                    if "D_0hplus_gg_decay" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_0hplus_gg_decay"].append(Discriminants.D_0hplus_gg_decay(t.p_GG_SIG_ghg2_1_ghz1_1_JHUGen,t.p_GG_SIG_ghg2_1_gha2_1_JHUGen,t.ZZMass,gConstants_list))
                    #=============== Calculating VBF Discriminants ================
                    if "D_0minus_VBF" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_0minus_VBF"].append(Discriminants.D_0minus_VBF(t.p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal,t.p_JJVBF_SIG_ghv4_1_JHUGen_JECNominal,notdijet,t.ZZMass,gConstants_list))
                    if "D_CP_VBF" in Analysis_Config.Discriminants_To_Calculate:
                     branchdict["D_CP_VBF"].append(Discriminants.D_CP_VBF(t.p_JJVBF_SIG_ghv1_1_ghv4_1_JHUGen_JECNominal,t.p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal,t.p_JJVBF_SIG_ghv4_1_JHUGen_JECNominal,notdijet,t.ZZMass,gConstants_list))
                    if "D_0hplus_VBF" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_0hplus_VBF"].append(Discriminants.D_0hplus_VBF(t.p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal,t.p_JJVBF_SIG_ghv2_1_JHUGen_JECNominal,notdijet,t.ZZMass,gConstants_list))
                    if "D_int_VBF" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_int_VBF"].append(Discriminants.D_int_VBF(t.p_JJVBF_SIG_ghv1_1_ghv2_1_JHUGen_JECNominal,t.p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal,t.p_JJVBF_SIG_ghv2_1_JHUGen_JECNominal,notdijet,t.ZZMass,gConstants_list))
                    if "D_L1_VBF" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_L1_VBF"].append(Discriminants.D_L1_VBF(t.p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal,t.p_JJVBF_SIG_ghv1prime2_1E4_JHUGen_JECNominal,notdijet,t.ZZMass,gConstants_list))
                    if "D_L1int_VBF" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_L1int_VBF"].append(Discriminants.D_L1int_VBF(t.p_JJVBF_SIG_ghv1_1_ghv1prime2_1E4_JHUGen_JECNominal,t.p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal,t.p_JJVBF_SIG_ghv1prime2_1E4_JHUGen_JECNominal,notdijet,t.ZZMass,gConstants_list))
                    if "D_L1Zg_VBF" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_L1Zg_VBF"].append(Discriminants.D_L1Zg_VBF(t.p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal,t.p_JJVBF_SIG_ghza1prime2_1E4_JHUGen_JECNominal,notdijet,t.ZZMass,gConstants_list))
                    if "D_L1Zgint_VBF" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_L1Zgint_VBF"].append(Discriminants.D_L1Zgint_VBF(t.p_JJVBF_SIG_ghv1_1_ghza1prime2_1E4_JHUGen_JECNominal,t.p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal,t.p_JJVBF_SIG_ghza1prime2_1E4_JHUGen_JECNominal,notdijet,t.ZZMass,gConstants_list))
                    if "D_0minus_Zg_VBF" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_0minus_Zg_VBF"].append(Discriminants.D_0minus_Zg_VBF(t.p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal,t.p_JJVBF_SIG_ghza4_1_JHUGen_JECNominal,notdijet,t.ZZMass,gConstants_list))
                    if "D_CP_Zg_VBF" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_CP_Zg_VBF"].append(Discriminants.D_CP_Zg_VBF(t.p_JJVBF_SIG_ghv1_1_ghza4_1_JHUGen_JECNominal,t.p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal,t.p_JJVBF_SIG_ghza4_1_JHUGen_JECNominal,notdijet,t.ZZMass,gConstants_list))
                    if "D_0hplus_Zg_VBF" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_0hplus_Zg_VBF"].append(Discriminants.D_0hplus_Zg_VBF(t.p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal,t.p_JJVBF_SIG_ghza2_1_JHUGen_JECNominal,notdijet,t.ZZMass,gConstants_list))
                    if "D_int_Zg_VBF" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_int_Zg_VBF"].append(Discriminants.D_int_Zg_VBF(t.p_JJVBF_SIG_ghv1_1_ghza2_1_JHUGen_JECNominal,t.p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal,t.p_JJVBF_SIG_ghza2_1_JHUGen_JECNominal,notdijet,t.ZZMass,gConstants_list))
                    #=============== Calculating VBF with Decay Discriminants ================
                    if "D_0minus_VBFdecay" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_0minus_VBFdecay"].append(Discriminants.D_0minus_VBFdecay(t.p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal,t.p_GG_SIG_ghg2_1_ghz1_1_JHUGen,t.p_JJVBF_SIG_ghv4_1_JHUGen_JECNominal,t.p_GG_SIG_ghg2_1_ghz4_1_JHUGen,notdijet,t.ZZMass,gConstants_list))
                    if "D_0hplus_VBFdecay" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_0hplus_VBFdecay"].append(Discriminants.D_0hplus_VBFdecay(t.p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal,t.p_GG_SIG_ghg2_1_ghz1_1_JHUGen,t.p_JJVBF_SIG_ghv2_1_JHUGen_JECNominal,t.p_GG_SIG_ghg2_1_ghz2_1_JHUGen,notdijet,t.ZZMass,gConstants_list))
                    if "D_L1_VBFdecay" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_L1_VBFdecay"].append(Discriminants.D_L1_VBFdecay(t.p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal,t.p_GG_SIG_ghg2_1_ghz1_1_JHUGen,t.p_JJVBF_SIG_ghv1prime2_1E4_JHUGen_JECNominal,t.p_GG_SIG_ghg2_1_ghz1prime2_1E4_JHUGen,notdijet,t.ZZMass,gConstants_list))
                    if "D_L1Zg_VBFdecay" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_L1Zg_VBFdecay"].append(Discriminants.D_L1Zg_VBFdecay(t.p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal,t.p_GG_SIG_ghg2_1_ghz1_1_JHUGen,t.p_JJVBF_SIG_ghza1prime2_1E4_JHUGen_JECNominal,t.p_GG_SIG_ghg2_1_ghza1prime2_1E4_JHUGen,notdijet,t.ZZMass,gConstants_list))
                    if "D_0minus_Zg_VBFdecay" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_0minus_Zg_VBFdecay"].append(Discriminants.D_0minus_Zg_VBFdecay(t.p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal,t.p_GG_SIG_ghg2_1_ghz1_1_JHUGen,t.p_JJVBF_SIG_ghza4_1_JHUGen_JECNominal,t.p_GG_SIG_ghg2_1_ghza4_1_JHUGen,notdijet,t.ZZMass,gConstants_list))
                    if "D_0hplus_Zg_VBFdecay" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_0hplus_Zg_VBFdecay"].append(Discriminants.D_0hplus_Zg_VBFdecay(t.p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal,t.p_GG_SIG_ghg2_1_ghz1_1_JHUGen,t.p_JJVBF_SIG_ghza2_1_JHUGen_JECNominal,t.p_GG_SIG_ghg2_1_ghza2_1_JHUGen,notdijet,t.ZZMass,gConstants_list))
                    if "D_0minus_gg_VBFdecay" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_0minus_gg_VBFdecay"].append(Discriminants.D_0minus_gg_VBFdecay(t.p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal,t.p_GG_SIG_ghg2_1_ghz1_1_JHUGen,t.p_JJVBF_SIG_gha4_1_JHUGen_JECNominal,t.p_GG_SIG_ghg2_1_gha4_1_JHUGen,notdijet,t.ZZMass,gConstants_list))
                    if "D_0hplus_gg_VBFdecay" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_0hplus_gg_VBFdecay"].append(Discriminants.D_0hplus_gg_VBFdecay(t.p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal,t.p_GG_SIG_ghg2_1_ghz1_1_JHUGen,t.p_JJVBF_SIG_gha2_1_JHUGen_JECNominal,t.p_GG_SIG_ghg2_1_gha2_1_JHUGen,notdijet,t.ZZMass,gConstants_list))
                    #=========== Calculating VH Hadronic Discriminants ============
                    WH_scale = OnShell_Help.HadWH_Scale_Nominal(t.p_HadWH_mavjj_JECNominal,t.p_HadWH_mavjj_true_JECNominal,t.pConst_HadWH_SIG_ghw1_1_JHUGen_JECNominal)
                    ZH_scale = OnShell_Help.HadZH_Scale_Nominal(t.p_HadZH_mavjj_JECNominal,t.p_HadZH_mavjj_true_JECNominal,t.pConst_HadZH_SIG_ghz1_1_JHUGen_JECNominal)
                    if "D_0minus_HadVH" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_0minus_HadVH"].append(Discriminants.D_0minus_HadVH(t.p_HadWH_SIG_ghw1_1_JHUGen_JECNominal,t.p_HadZH_SIG_ghz1_1_JHUGen_JECNominal,t.p_HadWH_SIG_ghw4_1_JHUGen_JECNominal,t.p_HadZH_SIG_ghz4_1_JHUGen_JECNominal,WH_scale,ZH_scale,notdijet,t.ZZMass,gConstants_list))
                    if "D_CP_HadVH" in Analysis_Config.Discriminants_To_Calculate:
                     branchdict["D_CP_HadVH"].append(Discriminants.D_CP_HadVH(t.p_HadZH_SIG_ghz1_1_ghz4_1_JHUGen_JECNominal,t.p_HadWH_SIG_ghw1_1_JHUGen_JECNominal,t.p_HadWH_SIG_ghw4_1_JHUGen_JECNominal,t.p_HadZH_SIG_ghz1_1_JHUGen_JECNominal,t.p_HadZH_SIG_ghz4_1_JHUGen_JECNominal,WH_scale,ZH_scale,notdijet))
                    if "D_0hplus_HadVH" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_0hplus_HadVH"].append(Discriminants.D_0hplus_HadVH(t.p_HadWH_SIG_ghw1_1_JHUGen_JECNominal,t.p_HadZH_SIG_ghz1_1_JHUGen_JECNominal,t.p_HadWH_SIG_ghw2_1_JHUGen_JECNominal,t.p_HadZH_SIG_ghz2_1_JHUGen_JECNominal,WH_scale,ZH_scale,notdijet,t.ZZMass,gConstants_list))
                    if "D_int_HadVH" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_int_HadVH"].append(Discriminants.D_int_HadVH(t.p_HadZH_SIG_ghz1_1_ghz2_1_JHUGen_JECNominal,t.p_HadWH_SIG_ghw1_1_JHUGen_JECNominal,t.p_HadWH_SIG_ghw2_1_JHUGen_JECNominal,t.p_HadZH_SIG_ghz1_1_JHUGen_JECNominal,t.p_HadWH_SIG_ghw2_1_JHUGen_JECNominal,WH_scale,ZH_scale,notdijet))
                    if "D_L1_HadVH" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_L1_HadVH"].append(Discriminants.D_L1_HadVH(t.p_HadWH_SIG_ghw1_1_JHUGen_JECNominal,t.p_HadZH_SIG_ghz1_1_JHUGen_JECNominal,t.p_HadWH_SIG_ghw1prime2_1E4_JHUGen_JECNominal,t.p_HadZH_SIG_ghz1prime2_1E4_JHUGen_JECNominal,WH_scale,ZH_scale,notdijet,t.ZZMass,gConstants_list))
                    if "D_L1int_HadVH" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_L1int_HadVH"].append(Discriminants.D_L1int_HadVH(t.p_HadWH_SIG_ghw1_1_ghw1prime2_1E4_JHUGen_JECNominal,t.p_HadWH_SIG_ghw1_1_JHUGen_JECNominal,t.p_HadWH_SIG_ghw1prime2_1E4_JHUGen_JECNominal,t.p_HadZH_SIG_ghz1_1_ghz1prime2_1E4_JHUGen_JECNominal,t.p_HadZH_SIG_ghz1_1_JHUGen_JECNominal,t.p_HadZH_SIG_ghz1prime2_1E4_JHUGen_JECNominal,WH_scale,ZH_scale,notdijet,t.ZZMass,gConstants_list))
                    if "D_L1Zg_HadVH" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_L1Zg_HadVH"].append(Discriminants.D_L1Zg_HadVH(t.p_HadWH_SIG_ghw1_1_JHUGen_JECNominal,t.p_HadZH_SIG_ghz1_1_JHUGen_JECNominal,0,t.p_HadZH_SIG_ghza1prime2_1E4_JHUGen_JECNominal,WH_scale,ZH_scale,notdijet,t.ZZMass,gConstants_list))
                    if "D_L1Zgint_HadVH" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_L1Zgint_HadVH"].append(Discriminants.D_L1Zgint_HadVH(t.p_HadZH_SIG_ghz1_1_ghz1prime2_1E4_JHUGen_JECNominal,t.p_HadZH_SIG_ghz1_1_JHUGen_JECNominal,t.p_HadZH_SIG_ghza1prime2_1E4_JHUGen_JECNominal,WH_scale,ZH_scale,notdijet,t.ZZMass,gConstants_list))
                    if "D_0minus_Zg_HadVH" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_0minus_Zg_HadVH"].append(Discriminants.D_0minus_Zg_HadVH(t.p_HadWH_SIG_ghw1_1_JHUGen_JECNominal,t.p_HadZH_SIG_ghz1_1_JHUGen_JECNominal,0,t.p_HadZH_SIG_ghza4_1_JHUGen_JECNominal,WH_scale,ZH_scale,notdijet,t.ZZMass,gConstants_list))
                    if "D_CP_Zg_HadVH" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_CP_Zg_HadVH"].append(Discriminants.D_CP_Zg_HadVH(t.p_HadZH_SIG_ghz1_1_ghza4_1_JHUGen_JECNominal,t.p_HadZH_SIG_ghz1_1_JHUGen_JECNominal,t.p_HadZH_SIG_ghza4_1_JHUGen_JECNominal,WH_scale,ZH_scale,notdijet))
                    if "D_0hplus_Zg_HadVH" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_0hplus_Zg_HadVH"].append(Discriminants.D_0hplus_Zg_HadVH(t.p_HadWH_SIG_ghw1_1_JHUGen_JECNominal,t.p_HadZH_SIG_ghz1_1_JHUGen_JECNominal,0,t.p_HadZH_SIG_ghza2_1_JHUGen_JECNominal,WH_scale,ZH_scale,notdijet,t.ZZMass,gConstants_list))
                    if "D_int_Zg_HadVH" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_int_Zg_HadVH"].append(Discriminants.D_int_Zg_HadVH(t.p_HadZH_SIG_ghz1_1_ghza2_1_JHUGen_JECNominal,t.p_HadZH_SIG_ghz1_1_JHUGen_JECNominal,t.p_HadZH_SIG_ghza2_1_JHUGen_JECNominal,WH_scale,ZH_scale,notdijet,t.ZZMass,gConstants_list))
                    if "D_0minus_gg_HadVH" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_0minus_gg_HadVH"].append(Discriminants.D_0minus_gg_HadVH(t.p_HadWH_SIG_ghw1_1_JHUGen_JECNominal,t.p_HadZH_SIG_ghz1_1_JHUGen_JECNominal,0,t.p_HadZH_SIG_gha4_1_JHUGen_JECNominal,WH_scale,ZH_scale,notdijet,t.ZZMass,gConstants_list))
                    if "D_CP_gg_HadVH" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_CP_gg_HadVH"].append(Discriminants.D_CP_gg_HadVH(t.p_HadZH_SIG_ghz1_1_gha4_1_JHUGen_JECNominal,t.p_HadZH_SIG_ghz1_1_JHUGen_JECNominal,t.p_HadZH_SIG_gha4_1_JHUGen_JECNominal,WH_scale,ZH_scale,notdijet))
                    if "D_0hplus_gg_HadVH" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_0hplus_gg_HadVH"].append(Discriminants.D_0hplus_gg_HadVH(t.p_HadWH_SIG_ghw1_1_JHUGen_JECNominal,t.p_HadZH_SIG_ghz1_1_JHUGen_JECNominal,0,t.p_HadZH_SIG_gha2_1_JHUGen_JECNominal,WH_scale,ZH_scale,notdijet,t.ZZMass,gConstants_list))
                    if "D_int_gg_HadVH" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_int_gg_HadVH"].append(Discriminants.D_int_gg_HadVH(t.p_HadZH_SIG_ghz1_1_gha2_1_JHUGen_JECNominal,t.p_HadZH_SIG_ghz1_1_JHUGen_JECNominal,t.p_HadZH_SIG_gha2_1_JHUGen_JECNominal,WH_scale,ZH_scale,notdijet,t.ZZMass,gConstants_list))
                    #============== Calculating VH Decay Discriminants ============
                    if "D_0minus_HadVHdecay" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_0minus_HadVHdecay"].append(Discriminants.D_0minus_HadVHdecay(t.p_HadWH_SIG_ghw1_1_JHUGen_JECNominal,t.p_HadZH_SIG_ghz1_1_JHUGen_JECNominal,t.p_GG_SIG_ghg2_1_ghz1_1_JHUGen,t.p_HadWH_SIG_ghw4_1_JHUGen_JECNominal,t.p_HadZH_SIG_ghz4_1_JHUGen_JECNominal,t.p_GG_SIG_ghg2_1_ghz4_1_JHUGen,WH_scale,ZH_scale,notdijet,t.ZZMass,gConstants_list))
                    if "D_0hplus_HadVHdecay" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_0hplus_HadVHdecay"].append(Discriminants.D_0hplus_HadVHdecay(t.p_HadWH_SIG_ghw1_1_JHUGen_JECNominal,t.p_HadZH_SIG_ghz1_1_JHUGen_JECNominal,t.p_GG_SIG_ghg2_1_ghz1_1_JHUGen,t.p_HadWH_SIG_ghw2_1_JHUGen_JECNominal,t.p_HadZH_SIG_ghz2_1_JHUGen_JECNominal,t.p_GG_SIG_ghg2_1_ghz2_1_JHUGen,WH_scale,ZH_scale,notdijet,t.ZZMass,gConstants_list))
                    if "D_L1_HadVHdecay" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_L1_HadVHdecay"].append(Discriminants.D_L1_HadVHdecay(t.p_HadWH_SIG_ghw1_1_JHUGen_JECNominal,t.p_HadZH_SIG_ghz1_1_JHUGen_JECNominal,t.p_GG_SIG_ghg2_1_ghz1_1_JHUGen,t.p_HadWH_SIG_ghw1prime2_1E4_JHUGen_JECNominal,t.p_HadZH_SIG_ghz1prime2_1E4_JHUGen_JECNominal,t.p_GG_SIG_ghg2_1_ghz1prime2_1E4_JHUGen,WH_scale,ZH_scale,notdijet,t.ZZMass,gConstants_list))
                    if "D_L1Zg_HadVHdecay" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_L1Zg_HadVHdecay"].append(Discriminants.D_L1Zg_HadVHdecay(t.p_HadWH_SIG_ghw1_1_JHUGen_JECNominal,t.p_HadZH_SIG_ghz1_1_JHUGen_JECNominal,t.p_GG_SIG_ghg2_1_ghz1_1_JHUGen,t.p_HadZH_SIG_ghza1prime2_1E4_JHUGen_JECNominal,t.p_GG_SIG_ghg2_1_ghza1prime2_1E4_JHUGen,WH_scale,ZH_scale,notdijet,t.ZZMass,gConstants_list))
                    if "D_0minus_Zg_HadVHdecay" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_0minus_Zg_HadVHdecay"].append(Discriminants.D_0minus_Zg_HadVHdecay(t.p_HadWH_SIG_ghw1_1_JHUGen_JECNominal,t.p_HadZH_SIG_ghz1_1_JHUGen_JECNominal,t.p_GG_SIG_ghg2_1_ghz1_1_JHUGen,t.p_HadZH_SIG_ghza4_1_JHUGen_JECNominal,t.p_GG_SIG_ghg2_1_ghza4_1_JHUGen,WH_scale,ZH_scale,notdijet,t.ZZMass,gConstants_list))
                    if "D_0hplus_Zg_HadVHdecay" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_0hplus_Zg_HadVHdecay"].append(Discriminants.D_0hplus_Zg_HadVHdecay(t.p_HadWH_SIG_ghw1_1_JHUGen_JECNominal,t.p_HadZH_SIG_ghz1_1_JHUGen_JECNominal,t.p_GG_SIG_ghg2_1_ghz1_1_JHUGen,t.p_HadZH_SIG_ghza2_1_JHUGen_JECNominal,t.p_GG_SIG_ghg2_1_ghza2_1_JHUGen,WH_scale,ZH_scale,notdijet,t.ZZMass,gConstants_list))
                    if "D_0minus_gg_HadVHdecay" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_0minus_gg_HadVHdecay"].append(Discriminants.D_0minus_gg_HadVHdecay(t.p_HadWH_SIG_ghw1_1_JHUGen_JECNominal,t.p_HadZH_SIG_ghz1_1_JHUGen_JECNominal,t.p_GG_SIG_ghg2_1_ghz1_1_JHUGen,t.p_HadZH_SIG_gha4_1_JHUGen_JECNominal,t.p_GG_SIG_ghg2_1_gha4_1_JHUGen,WH_scale,ZH_scale,notdijet,t.ZZMass,gConstants_list))
                    if "D_0hplus_gg_HadVHdecay" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_0hplus_gg_HadVHdecay"].append(Discriminants.D_0hplus_gg_HadVHdecay(t.p_HadWH_SIG_ghw1_1_JHUGen_JECNominal,t.p_HadZH_SIG_ghz1_1_JHUGen_JECNominal,t.p_GG_SIG_ghg2_1_ghz1_1_JHUGen,t.p_HadZH_SIG_gha2_1_JHUGen_JECNominal,t.p_GG_SIG_ghg2_1_gha2_1_JHUGen,WH_scale,ZH_scale,notdijet,t.ZZMass,gConstants_list))
                    #================ Calculating BKG discriminants ===============
                    ZZFlav=t.Z1Flav*t.Z2Flav
                    if "D_bkg" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_bkg"].append(Discriminants.D_bkg(t.p_GG_SIG_ghg2_1_ghz1_1_JHUGen,t.p_m4l_SIG,t.p_QQB_BKG_MCFM,t.p_m4l_BKG,cConstants_list,ZZFlav,t.ZZMass))
                    if "D_bkg_VBFdecay" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_bkg_VBFdecay"].append(Discriminants.D_bkg_VBFdecay(t.p_JJVBF_S_SIG_ghv1_1_MCFM_JECNominal,t.p_HadZH_S_SIG_ghz1_1_MCFM_JECNominal,t.p_HadWH_S_SIG_ghw1_1_MCFM_JECNominal,t.p_JJVBF_BKG_MCFM_JECNominal,t.p_HadZH_BKG_MCFM_JECNominal,t.p_HadWH_BKG_MCFM_JECNominal,t.p_JJQCD_BKG_MCFM_JECNominal,t.p_HadZH_mavjj_JECNominal,t.p_HadZH_mavjj_true_JECNominal,t.p_HadWH_mavjj_JECNominal,t.p_HadWH_mavjj_true_JECNominal,t.pConst_JJVBF_S_SIG_ghv1_1_MCFM_JECNominal,t.pConst_HadZH_S_SIG_ghz1_1_MCFM_JECNominal,t.pConst_HadWH_S_SIG_ghw1_1_MCFM_JECNominal,t.pConst_JJVBF_BKG_MCFM_JECNominal,t.pConst_HadZH_BKG_MCFM_JECNominal,t.pConst_HadWH_BKG_MCFM_JECNominal,t.pConst_JJQCD_BKG_MCFM_JECNominal,cConstants_list,ZZFlav,t.ZZMass,t.p_m4l_BKG,t.p_m4l_SIG,notdijet))
                    if "D_bkg_HadVHdecay" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_bkg_HadVHdecay"].append(Discriminants.D_bkg_HadVHdecay(t.p_JJVBF_S_SIG_ghv1_1_MCFM_JECNominal,t.p_HadZH_S_SIG_ghz1_1_MCFM_JECNominal,t.p_HadWH_S_SIG_ghw1_1_MCFM_JECNominal,t.p_JJVBF_BKG_MCFM_JECNominal,t.p_HadZH_BKG_MCFM_JECNominal,t.p_HadWH_BKG_MCFM_JECNominal,t.p_JJQCD_BKG_MCFM_JECNominal,t.p_HadZH_mavjj_JECNominal,t.p_HadZH_mavjj_true_JECNominal,t.p_HadWH_mavjj_JECNominal,t.p_HadWH_mavjj_true_JECNominal,t.pConst_JJVBF_S_SIG_ghv1_1_MCFM_JECNominal,t.pConst_HadZH_S_SIG_ghz1_1_MCFM_JECNominal,t.pConst_HadWH_S_SIG_ghw1_1_MCFM_JECNominal,t.pConst_JJVBF_BKG_MCFM_JECNominal,t.pConst_HadZH_BKG_MCFM_JECNominal,t.pConst_HadWH_BKG_MCFM_JECNominal,t.pConst_JJQCD_BKG_MCFM_JECNominal,cConstants_list,ZZFlav,t.ZZMass,t.p_m4l_BKG,t.p_m4l_SIG,notdijet))

                    #================ Calculating EW discriminants ================
                    
                    #================ Calculating gg discriminants ================

                    #================ Saving calculated discriminants ================

                    #================ Saving signed branches ================

                    for key in signfixdict.keys():
                        branchdict[key].append(signfixdict[key][0])
                    break

            print("\n================ Selecting and cloning branches from '"+tree+"' ================\n")

            for i in trange(len(treebranches)):
                branch = treebranches[i]
                if branch not in branchlist or "-" in branch:
                    t.SetBranchStatus(branch, 0)

            exec("new{} = t.CloneTree()".format(tree))

            for key in branchdict.keys():
                exec("array2tree(np.array(branchdict['{}'], dtype=[('{}', float)]), tree=new{})".format(key, key, tree))

            print("\n================ Saving processed '"+tree+"' ================\n")

            exec("new{}.SetName('eventTree')".format(tree))
            exec("new{}.Write()".format(tree))

            ftemptree.Close()

            print("Modified '{}' written to '{}'".format(tree, tagtreefilename.replace(".root", "_subtree"+str(tind)+".root")))

        f.Close()

        print("\n================ Building and saving final merged eventTree ================\n")

        chain = ROOT.TChain("eventTree")
        
        for i in range(len(treenames)):
            chain.Add(tagtreefilename.replace(".root", "_subtree"+str(i)+".root"))

        chain.Merge(tagtreefilename)
        
        print("Merged eventTree written to '{}'\n".format(tagtreefilename))

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
