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
def main(argv):
    inputfile = ''
    outputdir = ''
    branchfile = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:b:",["ifile=","ofile=","bfile="])
    except getopt.GetoptError:
        print('batchTreeTagger.py -i <inputfile> -o <outputdir> -b <branchfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('batchTreeTagger.py -i <inputfile> -o <outputdir> -b <branchfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputdir = arg
        elif opt in ("-b", "--bfile"):
            branchfile = arg
    
    if not all([inputfile, outputdir, branchfile]):
        print('batchTreeTagger.py -i <inputfile> -o <outputdir> -b <branchfile>')
        sys.exit(2)

    if not outputdir.endswith("/"):
        outputdir = outputdir+"/"

    print("\n================ Reading user input ================\n")

    print("Input CJLST TTree is '{}'".format(inputfile))
    print("Output directory is '{}'".format(outputdir))
    print("Branch list file is '{}'".format(branchfile))

    print("\n================ Processing user input ================\n")

    #=============== Load the Analysis Config =================
    cConstants_list = cConstants.init_cConstants()
    gConstants_list = gConstants.init_gConstants()
    Analysis_Config = Config.Analysis_Config("OnShell_HVV_Photons_2021")

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

            t = f.Get("ZZTree/"+tree)

            treebranches = [ x.GetName() for x in t.GetListOfBranches() ]

            branchdict = {}
            signfixdict = {}

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
            for ent in trange(1000):

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
                    #================ Calculating AC discriminants ================
                    if "D_0minus_decay" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_0minus_decay"].append(Discriminants.D_0minus_decay(t.p_GG_SIG_ghg2_1_ghz1_1_JHUGen,t.p_GG_SIG_ghg2_1_ghz4_1_JHUGen,t.ZZMass,gConstants_list))
                    if "D_CP_decay" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_CP_decay"].append(Discriminants.D_CP_decay(t.p_GG_SIG_ghg2_1_ghz1_1_ghz4_1_JHUGen,t.p_GG_SIG_ghg2_1_ghz1_1_JHUGen,t.p_GG_SIG_ghg2_1_ghz4_1_JHUGen,t.ZZMass,gConstants_list))
                    if "D_0hplus_decay" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_0hplus_decay"].append(Discriminants.D_0hplus_decay(t.p_GG_SIG_ghg2_1_ghz1_1_JHUGen,t.p_GG_SIG_ghg2_1_ghz1_1_ghz2_1_JHUGen,t.ZZMass,gConstants_list))
                    if "D_int_decay" in Analysis_Config.Discriminants_To_Calculate:
                      branchdict["D_int_decay"].append(Discriminants.D_int_decay(t.p_GG_SIG_ghg2_1_ghz1_1_ghz2_1_JHUGen,t.p_GG_SIG_ghg2_1_ghz1_1_JHUGen,t.ZZMass,gConstants_list))
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
