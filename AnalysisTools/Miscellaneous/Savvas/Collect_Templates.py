import os, glob
import sys 
import ROOT as ROOT 
from AnalysisTools.Utils import Config

# This script takes the output of the make all templates script as input
# The input should be a path to the directory which includes all Templates for each category and production mode
# Input will be parsed according to the event tag string in the filenames 

Input_Dir = sys.argv[1]
Output_Dir = sys.argv[2]

if not os.path.exists(Output_Dir):
  os.mkdir(Output_Dir)

# Make the output directory 
Input_Dir=Input_Dir.strip("/")
Output_Dir=Output_Dir.strip("/")
# Recursively look for all names with a given event tag by looping over each tag 
#Analysis_Config = Config.Analysis_Config("OnShell_HVV_Photons_2021")
Analysis_Config = Config.Analysis_Config("gammaH_Photons_Decay_Only")
Categories = Analysis_Config.Event_Categories
Coupling_Name = Analysis_Config.Coupling_Name
Final_States = Analysis_Config.Final_States
Years = Analysis_Config.Years
TreeFile = Analysis_Config.TreeFile

for Final_State in Final_States:
  for Year in Years:
    for cat in Categories:
      Temp_Hist_List = []
      used_names = []
      for filename in glob.iglob(Input_Dir+'/**', recursive=True):
        # Handle possible extenstions/ file paths with weird naming conventions
        root_name = filename.split("/")[-1]
        if os.path.isfile(filename) and (cat in root_name) and (Year in root_name) and (Final_State in root_name) and (TreeFile in root_name)  and ('unrolled' in filename): # filter dirs
          fin = ROOT.TFile(filename)
          for key in fin.GetListOfKeys():
            if "TH1F" in key.GetClassName():
              h_name = key.GetName()
              h_temp = fin.Get(h_name)
              h_temp.SetDirectory(0)
              if h_name not in used_names:
                Temp_Hist_List.append(h_temp)
                used_names.append(h_name)
              else: 
              # Find the name in the histogram
                Temp_Hist_List.append(h_temp)
          fin.Close()

      # After saving all relevant histograms #
      # Combine all histograms with the the same names #
      hist_combine = []
      for h_name in used_names:
        first = True
        h_temp = ROOT.TH1F()
        for h in Temp_Hist_List:
          if (h.GetName() == h_name) and (first):
            h_temp = h
            h_temp.SetDirectory(0)
            first = False
            print(h_name,h_temp.Integral())
          elif (h.GetName() == h_name) and not first:
            h_temp.Add(h)
            print(h_name,h_temp.Integral())
        hist_combine.append(h_temp)
      # Choose Naming Convntion for the combined templates

      fout = ROOT.TFile(Output_Dir+"/templates_combined_"+cat+"_"+Coupling_Name+"_"+Final_State+"_"+TreeFile+"_"+Year+".root","recreate")
      fout.cd()
      print("Saving: ",Output_Dir+"/templates_combined_"+cat+"_"+Coupling_Name+"_"+Final_State+"_"+TreeFile+"_"+Year+".root")
      for h in hist_combine:
        h.Write()
      fout.Close()
