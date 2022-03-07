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
from AnalysisTools.TemplateMaker.OnShell_Template import FillHistOnShellNoSyst
from AnalysisTools.TemplateMaker.Unroll_gen import Unroll_2D_OnShell, Unroll_3D_OnShell
from AnalysisTools.Utils import Config as Config
#get_ipython().run_line_magic('jsroot', 'on')
import sys

def main(argv):
    treelistpath = ''
    production = ''
    category = ''
    year = ''
    outputdir = ''
    try:
        opts, args = getopt.getopt(argv,"hi:p:c:y:o:",["ifile=","pfile=","cfile=","yfile=","ofile="])
    except getopt.GetoptError:
        print('CategorizedTemplateMaker.py -i <treelistpath> -p <production> -c <category> -y <year> -o <output_directory>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('CategorizedTemplateMaker.py -i <treelistpath> -p <production> -c <category> -y <year> -o <output_directory>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            treelistpath = arg
        elif opt in ("-p", "--pfile"):
            production = arg
        elif opt in ("-c", "--cfile"):
            category = arg
        elif opt in ("-y", "--yfile"):
            year = arg
        elif opt in ("-o", "--ofile"):
            outputdir = arg
    if not all([treelistpath, production, category, year, outputdir]):
        print('CategorizedTemplateMaker.py -i <treelistpath> -p <production> -c <category> -y <year> -o <output_dir>')
        sys.exit(2)
    if not outputdir.endswith("/"):
        outputdir = outputdir+"/"

    print("\n================ Reading user input ================\n")

    print("Input CJLST TTree is '{}'".format(treelistpath))
    print("Production mode is '{}'".format(production))
    print("Category is '{}'".format(category))
    print("Year is '{}'".format(year))
    print("Output Directory is '{}'".format(outputdir))

    print("\n================ Processing user input ================\n")
    
    os.mkdir(outputdir)
    unrolled_dir = outputdir+"unrolled/"
    rolled_dir = outputdir+"rolled/"
    os.mkdir(unrolled_dir)
    os.mkdir(rolled_dir)


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
      print(filename)
      ind = filename.split("/").index(Analysis_Config.TreeFile) # ex 200205_CutBased set in Config #
      year = filename.split("/")[ind:][1]
      ## Allow for strings in the year##
      if "16" in year:
        year = "2016"
      elif "17" in year:
        year = "2017"
      elif "18" in year:
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

    hlist = []
    foutName = FillHistOnShellNoSyst(production,category,hlist,yeardict,Analysis_Config,year) # Store the Histrograms before unrolling
    fout = ROOT.TFile(rolled_dir+foutName,"recreate")
    fout.cd()

    print  ("here")
    for hist in hlist: 
      print ("writing :",hist.GetName(),hist.Integral())
      hist.Write()
    fout.Close()

    fout = ROOT.TFile(unrolled_dir+foutName,"recreate")
    fout.cd()
    # Unroll and save the unrolled histograms #
     
    for hist in hlist:
      if type(hist) == type(ROOT.TH3F()):
        Temp_Neg, Temp_Pos = Unroll_3D_OnShell(hist)
        Temp_Neg.Write()
        Temp_Pos.Write()
      if type(hist) == type(ROOT.TH2F()):
        Temp_Neg, Temp_Pos = Unroll_2D_OnShell(hist)
        Temp_Neg.Write()
        Temp_Pos.Write()

if __name__ == "__main__":
    main(sys.argv[1:])
