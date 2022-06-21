import sys
import os, glob
import ROOT as ROOT
from AnalysisTools.Utils import Config

# This script takes the output of the make all templates script as input
# The input should be a path to the directory which includes all Templates for each category and production mode
# Input will be parsed according to the event tag string in the filenames 

Input_Dir = sys.argv[1]

# Make the output directory 
Input_Dir=Input_Dir.strip("/")

# Recursively look for all names with a given event tag by looping over each tag 
#Analysis_Config = Config.Analysis_Config("OnShell_HVV_Photons_2021")
Analysis_Config = Config.Analysis_Config("gammaH_Photons_Decay_Only")
Categories = Analysis_Config.Event_Categories

for filename in glob.iglob(Input_Dir+'/**', recursive=True):
  used_names = {}
  if os.path.isfile(filename):
    print(filename)
    fin = ROOT.TFile(filename,"update")
    for key in fin.GetListOfKeys():
      if "TH1F" in key.GetClassName():
        h_name = key.GetName()
        h_temp = fin.Get(h_name)
        h_temp.SetDirectory(0)
        #Check if there is a backup saved or not
        print(key,"Integral: ",h_temp.Integral())
        if h_name == used_names.keys():
          used_names[h_name] += 1
        else:
          used_names[h_name] = 1
    # Loop over used names and delete old cycles
    for name in used_names.keys():
      if used_names[name] != 1:
        for i in range(1, used_names[name]):
          del_string=name+";"+str(i)
          print(del_string)
          fin.Delete(del_string)
          ROOT.gDirectory.Delete(del_string)
    # Check to remove unsplit negative and positive histograms
    for name in used_names:
      if sum(name in i for i in used_names) > 1:
        print(name)
        del_string = name+";*"
        fin.Delete(del_string)
    fin.Close()
  print(used_names)

  # After saving all relevant histograms #
  # Combine all histograms with the the same names #
