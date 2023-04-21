#! /cvmfs/sft.cern.ch/lcg/views/LCG_102b_cuda/x86_64-centos7-gcc8-opt/bin/python3

"""
run 'cmsenv' then run 'source /cvmfs/sft.cern.ch/lcg/views/LCG_102b_cuda/x86_64-centos7-gcc8-opt/setup.sh' then './TreeTagger.py'
"""

import re
import time
import glob
import subprocess
import os, sys, getopt
from pathlib import Path

import ROOT
import numpy as np
import uproot as up
import pandas as pd
import awkward as ak
import vector as vec

from scipy import stats
from itertools import chain
import pyarrow.parquet as pq
from collections import Counter
from tqdm import trange, tqdm

import mplhep as hep
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt

pd.set_option('display.min_rows', pd.options.display.max_rows)

sns.set(rc={"figure.figsize": (24, 15)})
sns.set_context("poster")
sns.set_style("whitegrid")
sns.reset_orig()

plt.style.use(hep.style.CMS)
# plt.style.use(hep.style.CMSTex)
# hep.style.use("CMS")
# hep.style.use("CMSTex")

print(ROOT.__version__)

ROOT.gInterpreter.Declare('''
template<typename T>
ROOT::RDF::RNode AddArray(ROOT::RDF::RNode df, ROOT::RVec<T> &v, const std::string &name) {
    return df.Define(name, [&](ULong64_t e) { return v[e]; }, {"rdfentry_"});
}

template<typename T>
ROOT::RDF::RNode FixRVec(ROOT::RDF::RNode df, const std::string &name) {
    return df.Redefine(name, [](const ROOT::VecOps::RVec<T> &v) { return std::vector<T>(v.begin(), v.end()); }, {name});
}
''')

sys.path.append(os.getcwd() + '/..')

from AnalysisTools.data import gConstants as gConstants
from AnalysisTools.data import cConstants as cConstants
from AnalysisTools.Utils.Discriminants import *

print('finished imports and definitions')

def main(argv):
    inputfile = ''
    pthsubdir = ''
    outputdir = ''
    branchfile = ''
    removesubtrees = ''
    try:
        opts, args = getopt.getopt(argv,"hi:s:o:b:c:",["ifile=","subdr=","outdr=","bfile=","clean="])
    except getopt.GetoptError:
        print('\nTreeTagger.py -i <inputfile> -s <subdirectory> -o <outputdir> -b <branchfile> (-c <removesubtrees>)\n')
        exit()
    for opt, arg in opts:
        if opt == '-h' or opt == '--help':
            print('\nTreeTagger.py -i <inputfile> -s <subdirectory> -o <outputdir> -b <branchfile> (-c <removesubtrees>)\n')
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
        print('\nTreeTagger.py -i <inputfile> -s <subdirectory> -o <outputdir> -b <branchfile> (-c <removesubtrees>)\n')
        exit()

    if not outputdir.endswith("/"):
        outputdir = outputdir+"/"

    if not pthsubdir.endswith("/"):
        pthsubdir = pthsubdir+"/"

    pthsubdir = pthsubdir.split("/")[-2]

    removesubtrees = removesubtrees.replace(" ", "").capitalize()

    if not os.path.exists(inputfile):
        print("\nERROR: \tROOT file '" + inputfile + "' cannot be located. Please try again with valid input.\n")
        print('TreeTagger.py -i <inputfile> -s <subdirectory> -o <outputdir> -b <branchfile> (-c <removesubtrees>)\n')
        exit()

    if not os.path.exists(branchfile):
        print("\nERROR: \tBranches list '" + branchfile + "' cannot be located. Please try again with valid input.\n")
        print('TreeTagger.py -i <inputfile> -s <subdirectory> -o <outputdir> -b <branchfile> (-c <removesubtrees>)\n')
        exit()

    if pthsubdir not in inputfile:
        print("\nERROR: \tSubdirectory '" + pthsubdir + "' is not in the input path. Please try again with valid input.\n")
        print('TreeTagger.py -i <inputfile> -s <subdirectory> -o <outputdir> -b <branchfile> (-c <removesubtrees>)\n')
        exit()

    if len(removesubtrees) > 0:
        if removesubtrees not in ["True", "False"]:
            print("\nERROR: \tOption '-c' is expected to be True or False. Please try again with valid input.\n")
            print('TreeTagger.py -i <inputfile> -s <subdirectory> -o <outputdir> -b <branchfile> (-c <removesubtrees>)\n')
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
    
    ind = inputfile.split("/").index(pthsubdir)

    tagtreename = "/".join(inputfile.split("/")[ind:])
    tagtreepath = outputdir+tagtreename

    print("Read '"+inputfile+"'\n")
    print("Write '"+tagtreepath+"'\n")

    #================ Check existence of output and set up target branches ================

    cConstants_list = cConstants.init_cConstants()
    gConstants_list = gConstants.init_gConstants()

    useQGTagging = False

    print("================ Check output location and set up branches ================\n")

    if not os.path.exists(inputfile):
        print("ERROR: \t'" + inputfile + "' does not exist!\n")
        exit()

    elif os.path.exists(tagtreepath) or glob.glob(tagtreepath.replace(".root", "_subtree*.root")):
        print("ERROR: \t'" + tagtreepath + "' or parts of it already exist!\n\tNote that part to all of the final eventTree can be reconstructed from its subtree files if necessary.\n")
        exit()

    else:
        print("Pre-existing output TTree not found --- safe to proceed")
        if not os.path.exists("/".join(tagtreepath.split("/")[:-1])):
            Path("/".join(tagtreepath.split("/")[:-1])).mkdir(parents=True, exist_ok=True)

        branchlist = []

        with open(branchfile) as f:
            blist = [line.rstrip() for line in f]
            for branch in blist:
                if branch: branchlist.append(branch)

        treenames = ["candTree", "candTree_failed"]
        #treenames = ["candTree"]

        #================ Loop over target trees ================

        for tind, tree in enumerate(treenames):
            FixRVec = []
            FixRVec_br = []
            FixRVec_ty = []
            with up.open(inputfile) as f:
                if not any(tree in key for key in f.keys()): 
                    print(f.keys())
                    print("ERROR: '"+tree+"' not found\n")
                    continue
                t = f['ZZTree/'+tree]
                for brn, typ in t.typenames().items():
                    if 'vector' in typ: #ROOT::VecOps::RVec
                        if brn in branchlist:
                            FixRVec_br.append(brn)
                            FixRVec_ty.append(re.split('<|>', typ)[-2])
            FixRVec_ty = ['int16_t' if re.match('short', s) else s for s in FixRVec_ty]
            FixRVec = dict(zip(FixRVec_br, FixRVec_ty))
            print(FixRVec)
            
            f = ROOT.TFile(inputfile, 'READ')
            
            print("\n================ Reading events from '" + tree + "' and calculating new branches ================\n")

            t = f.Get('ZZTree/'+tree)

            treebranches = [ x.GetName() for x in t.GetListOfBranches() ]

            branchdict = {}
            signfixdict = {}

            for branch in branchlist:
                if "-" in branch and branch in treebranches:
                    signfixdict[branch.replace("-", "m")] = array('f',[0])
                    t.SetBranchAddress(branch, signfixdict[branch.replace("-", "m")])
                    branchdict[branch.replace("-", "m")] = []

            newbranches = ['EventTag', 'Dbkg', 'Dbsi', 'Bin40', 'D2jVBF', 'D2jZH', 'D2jWH']
    
            for newb in newbranches:
                exec('branchdict["{}"] = []'.format(newb))

            for ent in trange(t.GetEntries()):

                #================ Loop over events ================

                while t.GetEntry(ent):

                    #================ Fill failed events with dummy and skip to loop over branches ================

                    branchdict["Bin40"].append(f.Get("ZZTree/Counters").GetBinContent(40))
                    if tree == "candTree_failed":
                        for newb in newbranches:
                            exec('branchdict["{}"].append(-999)'.format(newb))
                        for key in signfixdict.keys():
                            branchdict[key].append(signfixdict[key][0])
                        break

                    #================ Tagging event by category ================

                    ZZMass = t.ZZMass
                    ZZFlav = t.Z1Flav * t.Z2Flav

                    tag = "none"

                    if( t.nCleanedJetsPt30 < 2 ):
                    
                        tag = "non2j"

                        branchdict["D2jVBF"].append(-999)
                        branchdict["D2jWH"].append(-999)
                        branchdict["D2jZH"].append(-999)

                    else:

                        D_VBF2j = DVBF2j_ME(t.p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal, t.p_JJQCD_SIG_ghg2_1_JHUGen_JECNominal, ZZMass, cConstants_list)
                        WP_VBF2j = getDVBF2jetsWP(ZZMass, useQGTagging)

                        D_WHh = DWHh_ME(t.p_HadWH_SIG_ghw1_1_JHUGen_JECNominal, t.p_JJQCD_SIG_ghg2_1_JHUGen_JECNominal, t.p_HadWH_mavjj_JECNominal, t.p_HadWH_mavjj_true_JECNominal, ZZMass, cConstants_list)
                        WP_WHh = getDWHhWP(ZZMass, useQGTagging)

                        D_ZHh = DZHh_ME(t.p_HadZH_SIG_ghz1_1_JHUGen_JECNominal, t.p_JJQCD_SIG_ghg2_1_JHUGen_JECNominal, t.p_HadZH_mavjj_JECNominal, t.p_HadZH_mavjj_true_JECNominal, ZZMass, cConstants_list)
                        WP_ZHh = getDZHhWP(ZZMass, useQGTagging)
                    
                        if( t.nExtraLep==0 and (((t.nCleanedJetsPt30==2 or t.nCleanedJetsPt30==3) and t.nCleanedJetsPt30BTagged_bTagSF<=1) or (t.nCleanedJetsPt30>=4 and t.nCleanedJetsPt30BTagged_bTagSF==0)) and D_VBF2j>WP_VBF2j ):
                            tag = "VBF"
                        
                        elif( t.nExtraLep==0 and (t.nCleanedJetsPt30==2 or t.nCleanedJetsPt30==3 or (t.nCleanedJetsPt30>=4 and t.nCleanedJetsPt30BTagged_bTagSF==0)) and (D_WHh>WP_WHh or D_ZHh>WP_ZHh) ):
                            tag = "VH"

                        branchdict["D2jVBF"].append(D_VBF2j)
                        branchdict["D2jWH"].append(D_WHh)
                        branchdict["D2jZH"].append(D_ZHh)

                    #================ Saving category tag ================

                    #if tag == "non2j": branchdict["EventTag"].append(-1)
                    if tag == "VBF": branchdict["EventTag"].append(1)
                    elif tag == "VH": branchdict["EventTag"].append(2)
                    else: branchdict["EventTag"].append(0)

                    #================ Calculating EW discriminants ================

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
            
            print("\n================ Cloning '"+tree+"' ================\n")

            print("Modified '{}' written to '{}'".format(tree, tagtreepath.replace(".root", "_subtree"+str(tind)+".root")))

            #exit()

            ftemppath = tagtreepath.replace(".root", "_subtree"+str(tind)+".root")

            ftemptree = ROOT.TFile(ftemppath, "CREATE")
            newTree = t.CloneTree(-1, 'fast')
            newTree.SetName('eventTree')
            newTree.Write()
            ftemptree.Close()
            
            f.Close()
            
            print('Saving new branches to cloned tree')

            df = ROOT.RDataFrame('eventTree', ftemppath)
            for key in branchdict.keys():
                exec('rvec_{} = ROOT.VecOps.AsRVec(np.asarray(branchdict["{}"]))'.format(key, key))
                exec('df = ROOT.AddArray(ROOT.RDF.AsRNode(df), rvec_{}, "{}")'.format(key, key))
            for fixb, fixt in FixRVec.items():
                exec('df = ROOT.FixRVec["{}"](ROOT.RDF.AsRNode(df), "{}")'.format(fixt, fixb))
            df.Snapshot('eventTree', ftemppath)
            
            print("Modified '{}' written to '{}'".format(tree, ftemppath))

        print("\n================ Building and saving final merged eventTree ================\n")

        mergecmd = "hadd -O {}".format(tagtreepath)

        for i in range(len(treenames)):
            if os.path.exists(tagtreepath.replace(".root", "_subtree"+str(i)+".root")):
                mergecmd = mergecmd + " {}".format(tagtreepath.replace(".root", "_subtree"+str(i)+".root"))
        
        process = subprocess.Popen(mergecmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        process.communicate()

        print("Merged eventTree written to '{}'\n".format(tagtreepath))

        if removesubtrees:
            for i in range(len(treenames)):
                if os.path.exists(tagtreepath.replace(".root", "_subtree"+str(i)+".root")):
                    os.remove(tagtreepath.replace(".root", "_subtree"+str(i)+".root"))

        f = ROOT.TFile(tagtreepath, 'READ')
        t = f.Get("eventTree")
        t.Print()
        f.Close()
        print("")

if __name__ == "__main__":
    main(sys.argv[1:])

