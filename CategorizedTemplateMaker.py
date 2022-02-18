#!/usr/bin/env python
# convert jupyter to python get_ipython().system('jupyter nbconvert --to script CategorizedTemplateMake-Parts.ipynb')

import os
import glob
import ROOT as ROOT
import ROOT 
from math import sqrt
import time
import getopt
#from pathlib import Path
import re
#from tqdm import trange, tqdm
import numpy as np
import copy
from array import *
from AnalysisTools.TemplateMaker.GetSyst import getsyst
from AnalysisTools.TemplateMaker.Sort_Category import sort_category
from AnalysisTools.Utils import Config as Config
#get_ipython().run_line_magic('jsroot', 'on')
import sys

def main(argv):
    treelistpath = ''
    production = ''
    category = ''
    try:
        opts, args = getopt.getopt(argv,"hi:p:c:",["ifile=","pfile=","cfile="])
    except getopt.GetoptError:
        print('CategorizedTemplateMaker.py -i <treelistpath> -p <production> -c <category>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('CategorizedTemplateMaker.py -i <treelistpath> -p <production> -c <category>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            treelistpath = arg
        elif opt in ("-p", "--pfile"):
            production = arg
        elif opt in ("-c", "--cfile"):
            category = arg

    if not all([treelistpath, production, category]):
        print('CategorizedTemplateMaker.py -i <treelistpath> -p <production> -c <category>')
        sys.exit(2)

    print("\n================ Reading user input ================\n")

    print("Input CJLST TTree is '{}'".format(treelistpath))
    print("Production mode is '{}'".format(production))
    print("Category is '{}'".format(category))

    print("\n================ Processing user input ================\n")

    print("\n=============== Loading Analysis Config ===============\n")
    #====== Load Analysis Config =====#
    Analysis_Config = Config.Analysis_Config("OnShell_HVV_Photons_2021")


    lumi = Analysis_Config.lumi



    if Analysis_Config.Variable_Edges == True:
      medges = Analysis_Config.medges  
      d1edges = Analysis_Config.d1edges
      d2edges = ReweightingSamplePlus
      print("medges", len(medges))
      print("medges", (medges))
      print("d1edges", len(d1edges))
      print("d1edges", (d1edges))
      print("d2edges", len(d2edges))
      print("d2edges", (d2edges))



    treelist = []

    with open(treelistpath) as f:
      llist = [line.rstrip() for line in f]
        
    for line in llist:
      if os.path.exists(line): 
        treelist.append(line)

    yeardict = {}

    for numfile in range(0,len(treelist)):
      filename = treelist[numfile]
      ind = filename.split("/").index(Analysis_Config.TreeFile) # ex 200205_CutBased set in Config #
      year = filename.split("/")[ind:][1]
      ## Allow for strings in the year##
      if "2016" in year:
        year = "2016"
      elif "2017" in year:
        year = "2017"
      elif "2018" in year:
        year = "2018"
      if year not in yeardict.keys():
        yeardict[year] = {}
      # Set the Production Method #
      prod = filename.split("/")[ind:][2]
      prod, p_sorted = sort_category(Analysis_Config,prod)
      if prod not in yeardict[year] and p_sorted:
          yeardict[year][prod] = [[]]   #, [], []]
      try:
        yeardict[year][prod][0].append(filename)
      except:
        print("ERROR: Cannot recognize production mode of " + filename + "! Tree not sorted!")
    print(yeardict)

# ### Check organized trees
#print (yeardict)

refsam4l = ["VBFToContinToZZTo4l", "VBFToHiggs0L1ContinToZZTo4l", "VBFToHiggs0L1f025ph0ToZZTo4l", "VBFToHiggs0L1f05ph0ContinToZZTo4l", "VBFToHiggs0L1f05ph0ToZZTo4l", "VBFToHiggs0L1f075ph0ToZZTo4l", "VBFToHiggs0L1ToZZTo4l", "VBFToHiggs0MContinToZZTo4l", "VBFToHiggs0Mf025ph0ToZZTo4l", "VBFToHiggs0Mf05ph0ContinToZZTo4l", "VBFToHiggs0Mf05ph0ToZZTo4l", "VBFToHiggs0Mf075ph0ToZZTo4l", "VBFToHiggs0MToZZTo4l", "VBFToHiggs0PHContinToZZTo4l", "VBFToHiggs0PHf025ph0ToZZTo4l", "VBFToHiggs0PHf05ph0ContinToZZTo4l", "VBFToHiggs0PHf05ph0ToZZTo4l", "VBFToHiggs0PHf075ph0ToZZTo4l", "VBFToHiggs0PHToZZTo4l", "VBFToHiggs0PMContinToZZTo4l", "VBFToHiggs0PMToZZTo4l"]
refmel = ["p_Gen_JJEW_BKG_MCFM", "p_Gen_JJEW_BSI_ghv1_0_ghv1prime2_m1549p165_MCFM", "p_Gen_JJEW_SIG_ghv1_1_ghv1prime2_m1177p11_MCFM", "p_Gen_JJEW_BSI_ghv1_1_ghv1prime2_m1549p165_MCFM", "p_Gen_JJEW_SIG_ghv1_1_ghv1prime2_m1549p165_MCFM", "p_Gen_JJEW_SIG_ghv1_1_ghv1prime2_m2038p82_MCFM", "p_Gen_JJEW_SIG_ghv1_0_ghv1prime2_m1549p165_MCFM", "p_Gen_JJEW_BSI_ghv1_0_ghv4_0p216499_MCFM", "p_Gen_JJEW_SIG_ghv1_1_ghv4_0p164504_MCFM", "p_Gen_JJEW_BSI_ghv1_1_ghv4_0p216499_MCFM", "p_Gen_JJEW_SIG_ghv1_1_ghv4_0p216499_MCFM", "p_Gen_JJEW_SIG_ghv1_1_ghv4_0p284929_MCFM", "p_Gen_JJEW_SIG_ghv1_0_ghv4_0p216499_MCFM", "p_Gen_JJEW_BSI_ghv1_0_ghv2_0p207049_MCFM", "p_Gen_JJEW_SIG_ghv1_1_ghv2_0p157323_MCFM", "p_Gen_JJEW_BSI_ghv1_1_ghv2_0p207049_MCFM", "p_Gen_JJEW_SIG_ghv1_1_ghv2_0p207049_MCFM", "p_Gen_JJEW_SIG_ghv1_1_ghv2_0p272492_MCFM", "p_Gen_JJEW_SIG_ghv1_0_ghv2_0p207049_MCFM", "p_Gen_JJEW_BSI_ghv1_1_MCFM", "p_Gen_JJEW_SIG_ghv1_1_MCFM"]

refden = dict(zip(refsam4l, refmel))

hlist = ['ggH SIG', 'ggH BSI', 'ggH BKG', 'qqbar BKG']

finalstate = {"4e": "121*121", "4mu": "169*169", "2e2mu": "121*169"}
proc = ["ggH_0PM", "ggH_g11g21_negative", "ggH_g11g21_positive", "back_ggZZ", "back_qqZZ", "data_obs"]

#configure what you would like to run

ltargetyear = ["MC_2017","MC_2016_CorrectBTag","MC_2018"]
ltargetprod = ["gg","VBF","ZZTo4l"]
ltargetstate = ["4mu","4e","2e2mu"]
ltargetcomp = [0,1,2]    # SIG=0 BSI=1 BKG=2    (for the qqbar bkg events in 'ZZTo4l' this choice does not matter as you can see above)
if production == "ZZTo4l" : 
    ltargetcomp = [0]
ltargetcateg = [0,1,2]  # Untag=0 VBF=1 VH=2




if __name__ == "__main__":
    main(sys.argv[1:])
