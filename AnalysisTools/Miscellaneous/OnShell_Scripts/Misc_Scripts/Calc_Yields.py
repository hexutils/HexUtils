#!/usr/bin/env python

import sys, getopt
import os
import glob
import ROOT
from math import sqrt
import time
from os import path
#from pathlib import Path
import re
from root_numpy import array2tree, tree2array
from Calc_Weight import *
from Config import Analysis_Config
import numpy as np
from prettytable import PrettyTable
### 

def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print('Calc_Yields.py -i <inputdir> -o <outputfile> ')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('Calc_Yields.py -i <inputdir> -o <outputfile> ')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg   
    if not all([inputfile,outputfile]):
        print('Calc_Yields.py -i <inputfile> -o <outputfile> ')
        sys.exit(2)

    print("\n================ Reading user input ================\n")

    print('Input Directory is', inputfile)
    
    print("\n================ Processing user input ================\n")


    filename = inputfile #treelist[numfile]
        
    print(filename, "\n")
    
    # List the tags definitions #       
    Untagged      = 0
    VBF1jTagged   = 1
    VBF2jTagged   = 2
    VHLeptTagged  = 3
    VHHadrTagged  = 4
    ttHLeptTagged = 5
    ttHHadrTagged = 6
    VHMETTagged   = 7
    Boosted       = 8
    gammaHTagged  = 9
    
    # Dictionary for each production method and load configs #

    Yield_Per_Sample = dict([('ggH',0),('VBF',0),('WH',0),('ZH',0),('bbH',0),('ttH',0),('tH',0)])
    config = Analysis_Config("OnShell_HVV_Photons_2021")
    if config.TaggingProcess == "Tag_AC_19_Scheme_1":
      ggH=('ggH',0,0,0,0,0,0,0,0,0,0,0)
      VBF=('VBF',0,0,0,0,0,0,0,0,0,0,0)
      WH=('WH',0,0,0,0,0,0,0,0,0,0,0)
      ZH=('ZH',0,0,0,0,0,0,0,0,0,0,0)
      bbH=('bbH',0,0,0,0,0,0,0,0,0,0,0)
      ttH=('ttH',0,0,0,0,0,0,0,0,0,0,0)
      ktt=('ktt',0,0,0,0,0,0,0,0,0,0,0)
      tH=('tH',0,0,0,0,0,0,0,0,0,0,0)
      TotalSig=('Total Sig',0,0,0,0,0,0,0,0,0,0,0)
      qq4lBkg=('qq4l Bkg',0,0,0,0,0,0,0,0,0,0,0)
      gg4lBkg=('gg4l Bkg',0,0,0,0,0,0,0,0,0,0,0)
      EWBkg=('EW Bkg',0,0,0,0,0,0,0,0,0,0,0)
      ZXBkg=('Z+X Bkg',0,0,0,0,0,0,0,0,0,0,0)
      SigBkg=('Sig+Bkg',0,0,0,0,0,0,0,0,0,0,0)
      
      Tuple_List=[ggH,VBF,WH,ZH,bbH,ttH,tH,TotalSig,qq4lBkg,gg4lBkg,EWBkg,ZXBkg,SigBkg]

      Yields=np.array(Tuple_List,dtype=[('name','U10'),('Untagged','f4'),('VBF1jTagged','f4'),('VBF2jTagged','f4'),('VHLeptTagged','f4'),('VHHadrTagged','f4'),('ttHLeptTagged','f4'),('ttHHadrTagged','f4'),('VHMETTagged','f4'),('Boosted','f4'),('gammaHTagged','f4'),("Total",'f4')])
    elif config.TaggingProcess == "Tag_AC_19_Scheme_2":
      ggH=('ggH',0,0,0,0,0,0,0,0,0,0,0)
      VBF=('VBF',0,0,0,0,0,0,0,0,0,0,0)
      WH=('WH',0,0,0,0,0,0,0,0,0,0,0)
      ZH=('ZH',0,0,0,0,0,0,0,0,0,0,0)
      bbH=('bbH',0,0,0,0,0,0,0,0,0,0,0)
      ttH=('ttH',0,0,0,0,0,0,0,0,0,0,0)
      ktt=('ktt',0,0,0,0,0,0,0,0,0,0,0)
      tH=('tH',0,0,0,0,0,0,0,0,0,0,0)
      TotalSig=('Total Sig',0,0,0,0,0,0,0,0,0,0,0)
      qq4lBkg=('qq4l Bkg',0,0,0,0,0,0,0,0,0,0,0)
      gg4lBkg=('gg4l Bkg',0,0,0,0,0,0,0,0,0,0,0)
      EWBkg=('EW Bkg',0,0,0,0,0,0,0,0,0,0,0)
      ZXBkg=('Z+X Bkg',0,0,0,0,0,0,0,0,0,0,0)
      SigBkg=('Sig+Bkg',0,0,0,0,0,0,0,0,0,0,0)

      Tuple_List=[ggH,VBF,WH,ZH,bbH,ttH,tH,TotalSig,qq4lBkg,gg4lBkg,EWBkg,ZXBkg,SigBkg]

      Yields=np.array(Tuple_List,dtype=[('name','U10'),('Untagged','f4'),('VBF1jTagged','f4'),('VBF2jTagged','f4'),('VHLeptTagged','f4'),('VHHadrTagged','f4'),('ttHLeptTagged','f4'),('ttHHadrTagged','f4'),('VHMETTagged','f4'),('Boosted','f4'),('gammaHTagged','f4'),("Total",'f4')])


    print("\n================ Reading events from " + filename + " ================\n")
    
    # Open the output file #

    out = open(outputfile, 'a')

    # Load the array of total count of events #

    count=np.array([0,0,0,0,0,0,0,0,0,0])
    
    # Load luminosity variable #

    lumi_2016=35.9
    lumi_2017=41.5
    lumi_2018=59.7
        
    # Recursively Loop through directories
    for root, subdirs, files in os.walk(filename):
      #print('--\nroot = ' + root)
      list_file_path = os.path.join(root, 'ZZ4lAnalysis.root')
      if os.path.isfile(list_file_path):
        nUntagged      = 0.
        nVBF1jTagged   = 0.
        nVBF2jTagged   = 0.
        nVHLeptTagged  = 0.
        nVHHadrTagged  = 0.
        nttHLeptTagged = 0.
        nttHHadrTagged = 0.
        nVHMETTagged   = 0.
        nBoosted       = 0.
        ngammaHTagged  = 0.
        ntotal = 0.
        print('list_file_path = ' + list_file_path)
        f = ROOT.TFile.Open(list_file_path)
        t = f.Get('candTree')
        #t.Print()
        tag = tree2array(tree=t,branches=["tag"])
        tag = tag.astype(int)
        m4l = tree2array(tree=t,branches=["ZZMass"]).astype(float)
        # Calculate Weights according to custom #

        #eventweight = Calc_Event_Weight_200205(t,list_file_path)
        eventweight = Calc_Event_Weight_2021_gammaH(t,list_file_path)

        # ======== Choose Luminosity per year ==========#
        lumi = 0 
        if "2016" in list_file_path:
          lumi = lumi_2016
        elif "2017" in list_file_path:
          lumi = lumi_2017
        elif "2018" in list_file_path:
          lumi = lumi_2018
        # Sum up the event weights for each category #
        for i in range(len(tag)):
          # Tag the NP array based on Tag Scheme #
            if "H" in list_file_path or "ttH" in list_file_path:
              if m4l[i] <= 140 and m4l[i] >= 105:
                if tag[i] == Untagged:
                  nUntagged = nUntagged + eventweight[i] * lumi #/ weightsum
                if tag[i] == VBF1jTagged:
                  nVBF1jTagged = nVBF1jTagged + eventweight[i] * lumi #/ weightsum 
                if tag[i] == VBF2jTagged:
                  nVBF2jTagged = nVBF2jTagged + eventweight[i]  * lumi #/ weightsum
                if  tag[i] == VHLeptTagged:
                  nVHLeptTagged = nVHLeptTagged + eventweight[i] * lumi #/ weightsum
                if tag[i] == VHHadrTagged:
                  nVHHadrTagged = nVHHadrTagged + eventweight[i] * lumi #/ weightsum
                if tag[i] == ttHLeptTagged:
                  nttHLeptTagged = nttHLeptTagged + eventweight[i] * lumi #/ weightsum
                if tag[i] == ttHHadrTagged:
                  nttHHadrTagged = nttHHadrTagged + eventweight[i] * lumi #/ weightsum
                if tag[i] == VHMETTagged:
                  nVHMETTagged = nVHMETTagged + eventweight[i] * lumi #/ weightsum
                if tag[i] == Boosted:
                  nBoosted = nBoosted + eventweight[i] * lumi #/ weightsum
                if tag[i] == gammaHTagged:
                  ngammaHTagged = ngammaHTagged + eventweight[i] * lumi #/ weightsum
                ntotal = ntotal + eventweight[i] * lumi
            else:
              if tag[i] == Untagged:
                nUntagged = nUntagged + eventweight[i] * lumi #/ weightsum
              if tag[i] == VBF1jTagged:
                nVBF1jTagged = nVBF1jTagged + eventweight[i] * lumi #/ weightsum
              if tag[i] == VBF2jTagged:
                nVBF2jTagged = nVBF2jTagged + eventweight[i]  * lumi #/ weightsum
              if tag[i] == VHLeptTagged:
                nVHLeptTagged = nVHLeptTagged + eventweight[i] * lumi #/ weightsum
              if tag[i] == VHHadrTagged:
                nVHHadrTagged = nVHHadrTagged + eventweight[i] * lumi #/ weightsum
              if tag[i] == ttHLeptTagged:
                nttHLeptTagged = nttHLeptTagged + eventweight[i] * lumi #/ weightsum
              if tag[i] == ttHHadrTagged:
                nttHHadrTagged = nttHHadrTagged + eventweight[i] * lumi #/ weightsum
              if tag[i] == VHMETTagged:
                nVHMETTagged = nVHMETTagged + eventweight[i] * lumi #/ weightsum
              if tag[i] == Boosted:
                nBoosted = nBoosted + eventweight[i] * lumi #/ weightsum
              if tag[i] == gammaHTagged:
                ngammaHTagged = ngammaHTagged + eventweight[i] * lumi #/ weightsum
              ntotal = ntotal + eventweight[i] * lumi

        # Fill the NP Array up #
        if "ggH" in list_file_path:
          Yield_Per_Sample["ggH"]=Yield_Per_Sample["ggH"] + ntotal
          Yields["Untagged"][0] += nUntagged 
          Yields["VBF1jTagged"][0] += nVBF1jTagged 
          Yields["VBF2jTagged"][0] += nVBF2jTagged
          Yields["VHLeptTagged"][0] += nVHLeptTagged
          Yields["VHHadrTagged"][0] += nVHHadrTagged 
          Yields["ttHLeptTagged"][0] += nttHLeptTagged 
          Yields["ttHHadrTagged"][0] += nttHHadrTagged
          Yields["VHMETTagged"][0] += nVHMETTagged
          Yields["Boosted"][0] += nBoosted
          Yields["gammaHTagged"][0] += ngammaHTagged
          Yields["Total"][0] += nUntagged + nVBF1jTagged + nVBF2jTagged + nVHLeptTagged + nVHHadrTagged + nttHLeptTagged + nttHHadrTagged + nVHMETTagged + nBoosted + ngammaHTagged
        if "VBFH" in list_file_path:
          Yield_Per_Sample["VBF"]=Yield_Per_Sample["VBF"] + ntotal
          Yields["Untagged"][1] += nUntagged 
          Yields["VBF1jTagged"][1] += nVBF1jTagged 
          Yields["VBF2jTagged"][1] += nVBF2jTagged
          Yields["VHLeptTagged"][1] += nVHLeptTagged
          Yields["VHHadrTagged"][1] += nVHHadrTagged 
          Yields["ttHLeptTagged"][1] += nttHLeptTagged 
          Yields["ttHHadrTagged"][1] += nttHHadrTagged
          Yields["VHMETTagged"][1] += nVHMETTagged
          Yields["Boosted"][1] += nBoosted
          Yields["gammaHTagged"][1] += ngammaHTagged
          Yields["Total"][1] += nUntagged + nVBF1jTagged + nVBF2jTagged + nVHLeptTagged + nVHHadrTagged + nttHLeptTagged + nttHHadrTagged + nVHMETTagged + nBoosted + ngammaHTagged
        if ("WplusH" in list_file_path) or ("WminusH" in list_file_path):
          Yield_Per_Sample["WH"] = Yield_Per_Sample["WH"] + ntotal
          Yields["Untagged"][2] += nUntagged 
          Yields["VBF1jTagged"][2] += nVBF1jTagged 
          Yields["VBF2jTagged"][2] += nVBF2jTagged
          Yields["VHLeptTagged"][2] += nVHLeptTagged
          Yields["VHHadrTagged"][2] += nVHHadrTagged 
          Yields["ttHLeptTagged"][2] += nttHLeptTagged 
          Yields["ttHHadrTagged"][2] += nttHHadrTagged
          Yields["VHMETTagged"][2] += nVHMETTagged
          Yields["Boosted"][2] += nBoosted
          Yields["gammaHTagged"][2] += ngammaHTagged
          Yields["Total"][2] += nUntagged + nVBF1jTagged + nVBF2jTagged + nVHLeptTagged + nVHHadrTagged + nttHLeptTagged + nttHHadrTagged + nVHMETTagged + nBoosted + ngammaHTagged
        if "ZH" in list_file_path:
          Yield_Per_Sample["ZH"]=Yield_Per_Sample["ZH"] + ntotal
          Yields["Untagged"][3] += nUntagged 
          Yields["VBF1jTagged"][3] += nVBF1jTagged 
          Yields["VBF2jTagged"][3] += nVBF2jTagged
          Yields["VHLeptTagged"][3] += nVHLeptTagged
          Yields["VHHadrTagged"][3] += nVHHadrTagged 
          Yields["ttHLeptTagged"][3] += nttHLeptTagged 
          Yields["ttHHadrTagged"][3] += nttHHadrTagged
          Yields["VHMETTagged"][3] += nVHMETTagged
          Yields["Boosted"][3] += nBoosted
          Yields["gammaHTagged"][3] += ngammaHTagged
          Yields["Total"][3] += nUntagged + nVBF1jTagged + nVBF2jTagged + nVHLeptTagged + nVHHadrTagged + nttHLeptTagged + nttHHadrTagged + nVHMETTagged + nBoosted + ngammaHTagged
        if "bbH" in list_file_path:
          Yield_Per_Sample["bbH"]=Yield_Per_Sample["bbH"] + ntotal
          Yields["Untagged"][4] += nUntagged 
          Yields["VBF1jTagged"][4] += nVBF1jTagged 
          Yields["VBF2jTagged"][4] += nVBF2jTagged
          Yields["VHLeptTagged"][4] += nVHLeptTagged
          Yields["VHHadrTagged"][4] += nVHHadrTagged 
          Yields["ttHLeptTagged"][4] += nttHLeptTagged 
          Yields["ttHHadrTagged"][4] += nttHHadrTagged
          Yields["VHMETTagged"][4] += nVHMETTagged
          Yields["Boosted"][4] += nBoosted
          Yields["gammaHTagged"][4] += ngammaHTagged
          Yields["Total"][4] += nUntagged + nVBF1jTagged + nVBF2jTagged + nVHLeptTagged + nVHHadrTagged + nttHLeptTagged + nttHHadrTagged + nVHMETTagged + nBoosted + ngammaHTagged
        if "ttH" in list_file_path:
          Yield_Per_Sample["ttH"]=Yield_Per_Sample["ttH"] + ntotal
          Yields["Untagged"][5] += nUntagged 
          Yields["VBF1jTagged"][5] += nVBF1jTagged 
          Yields["VBF2jTagged"][5] += nVBF2jTagged
          Yields["VHLeptTagged"][5] += nVHLeptTagged
          Yields["VHHadrTagged"][5] += nVHHadrTagged 
          Yields["ttHLeptTagged"][5] += nttHLeptTagged 
          Yields["ttHHadrTagged"][5] += nttHHadrTagged
          Yields["VHMETTagged"][5] += nVHMETTagged
          Yields["Boosted"][5] += nBoosted
          Yields["gammaHTagged"][5] += ngammaHTagged
          Yields["Total"][5] += nUntagged + nVBF1jTagged + nVBF2jTagged + nVHLeptTagged + nVHHadrTagged + nttHLeptTagged + nttHHadrTagged + nVHMETTagged + nBoosted + ngammaHTagged
        if "tHW" in list_file_path or "tqH" in list_file_path:
          Yield_Per_Sample["tH"]=Yield_Per_Sample["tH"] + ntotal
          Yields["Untagged"][6] += nUntagged 
          Yields["VBF1jTagged"][6] += nVBF1jTagged 
          Yields["VBF2jTagged"][6] += nVBF2jTagged
          Yields["VHLeptTagged"][6] += nVHLeptTagged
          Yields["VHHadrTagged"][6] += nVHHadrTagged 
          Yields["ttHLeptTagged"][6] += nttHLeptTagged 
          Yields["ttHHadrTagged"][6] += nttHHadrTagged
          Yields["VHMETTagged"][6] += nVHMETTagged
          Yields["Boosted"][6] += nBoosted
          Yields["gammaHTagged"][6] += ngammaHTagged
          Yields["Total"][6] += nUntagged + nVBF1jTagged + nVBF2jTagged + nVHLeptTagged + nVHHadrTagged + nttHLeptTagged + nttHHadrTagged + nVHMETTagged + nBoosted + ngammaHTagged
        if any(x in list_file_path for x in ["ggH","VBFH","ZH","WplusH","WminusH","bbH","ttH","tHW","tqH"]):
          Yields["Untagged"][7] += nUntagged
          Yields["VBF1jTagged"][7] += nVBF1jTagged
          Yields["VBF2jTagged"][7] += nVBF2jTagged
          Yields["VHLeptTagged"][7] += nVHLeptTagged
          Yields["VHHadrTagged"][7] += nVHHadrTagged
          Yields["ttHLeptTagged"][7] += nttHLeptTagged
          Yields["ttHHadrTagged"][7] += nttHHadrTagged
          Yields["VHMETTagged"][7] += nVHMETTagged
          Yields["Boosted"][7] += nBoosted
          Yields["gammaHTagged"][7] += ngammaHTagged
          Yields["Total"][7] += nUntagged + nVBF1jTagged + nVBF2jTagged + nVHLeptTagged + nVHHadrTagged + nttHLeptTagged + nttHHadrTagged + nVHMETTagged + nBoosted + ngammaHTagged
        if any(x in list_file_path for x in ["TTZZ","TTWW","TTZJets_M10_MLM","TTZToLLNuNu_M10","TTZToLL_M1to10_MLM"]):
          Yields["Untagged"][8] += nUntagged
          Yields["VBF1jTagged"][8] += nVBF1jTagged
          Yields["VBF2jTagged"][8] += nVBF2jTagged
          Yields["VHLeptTagged"][8] += nVHLeptTagged
          Yields["VHHadrTagged"][8] += nVHHadrTagged
          Yields["ttHLeptTagged"][8] += nttHLeptTagged
          Yields["ttHHadrTagged"][8] += nttHHadrTagged
          Yields["VHMETTagged"][8] += nVHMETTagged
          Yields["Boosted"][8] += nBoosted
          Yields["gammaHTagged"][8] += ngammaHTagged
          Yields["Total"][8] += nUntagged + nVBF1jTagged + nVBF2jTagged + nVHLeptTagged + nVHHadrTagged + nttHLeptTagged + nttHHadrTagged + nVHMETTagged + nBoosted + ngammaHTagged
        count=count+[nUntagged,nVBF1jTagged,nVBF2jTagged,nVHLeptTagged,nVHHadrTagged,nttHLeptTagged,nttHHadrTagged,nVHMETTagged,nBoosted,ngammaHTagged]
        if any(x in list_file_path for x in ["WZZ","WWZ","WZZ"]):
          Yields["Untagged"][9] += nUntagged
          Yields["VBF1jTagged"][9] += nVBF1jTagged
          Yields["VBF2jTagged"][9] += nVBF2jTagged
          Yields["VHLeptTagged"][9] += nVHLeptTagged
          Yields["VHHadrTagged"][9] += nVHHadrTagged
          Yields["ttHLeptTagged"][9] += nttHLeptTagged
          Yields["ttHHadrTagged"][9] += nttHHadrTagged
          Yields["VHMETTagged"][9] += nVHMETTagged
          Yields["Boosted"][9] += nBoosted
          Yields["gammaHTagged"][9] += ngammaHTagged
          Yields["Total"][9] += nUntagged + nVBF1jTagged + nVBF2jTagged + nVHLeptTagged + nVHHadrTagged + nttHLeptTagged + nttHHadrTagged + nVHMETTagged + nBoosted + ngammaHTagged
        if any(x in list_file_path for x in ["VBFTo"]):
          Yields["Untagged"][10] += nUntagged
          Yields["VBF1jTagged"][10] += nVBF1jTagged
          Yields["VBF2jTagged"][10] += nVBF2jTagged
          Yields["VHLeptTagged"][10] += nVHLeptTagged
          Yields["VHHadrTagged"][10] += nVHHadrTagged
          Yields["ttHLeptTagged"][10] += nttHLeptTagged
          Yields["ttHHadrTagged"][10] += nttHHadrTagged
          Yields["VHMETTagged"][10] += nVHMETTagged
          Yields["Boosted"][10] += nBoosted
          Yields["gammaHTagged"][10] += ngammaHTagged
          Yields["Total"][10] += nUntagged + nVBF1jTagged + nVBF2jTagged + nVHLeptTagged + nVHHadrTagged + nttHLeptTagged + nttHHadrTagged + nVHMETTagged + nBoosted + ngammaHTagged
    #print(Yield_Per_Sample)     
    pt = PrettyTable(Yields.dtype.names)
    for row in Yields:
        pt.add_row(row)
    print(pt)
if __name__ == "__main__":
    main(sys.argv[1:])
