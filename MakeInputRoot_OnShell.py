import os
import sys
import ROOT
import copy

# What this script does is trim and rename the template files and prepare them for the datacards.
# The expected input is a list of templates that would belong to the sample datacard.

#========================== How to run this ===========================
# 1. First argument is the name of the template you want to create

# 2. The next arguments are all of the input root files with the histrograms needed

OutName = sys.argv[1] # Output Root File Name
names = sys.argv[2:] # Input Root Files 

hists = [] # Holds the histograms to add to the final TFile
used_names = [] # Stores the names of the histrograms 

for nm in names:
  fin = ROOT.TFile.Open(nm)
  for key in fin.GetListOfKeys():
    if "TH1F" in key.GetClassName():
        h_name = key.GetName()
        h_temp = fin.Get(h_name)
        h_temp.SetDirectory(0)
        if h_name not in used_names:
          hists.append(h_temp)
          used_names.append(h_name)
  fin.Close()

# Make a fake data histogram #

Fake_Data = []
for hist in hists:
  h_name = hist.GetName()
  if "0PM" in h_name:
    Fake_Data.append(hist)
  if "bkg" in h_name:
    Fake_Data.append(hist)

for i in range(1,len(Fake_Data)):
  Fake_Data[0].Add(Fake_Data[i])



fout =  ROOT.TFile.Open(OutName,"recreate")
fout.cd()

Fake_Data[0].Write("data_obs")

for hist in hists:
  hist.Write()
print(OutName)
'''            
chanell = nm.replace(".root","")    
n_fout  = chanell+".input.root"
data_obs = copy.deepcopy(hists[0])
data_obs.SetName("data_obs")
for i,hist in enumerate(hists):
    if i > 1 : 
      data_obs.Add(hist)
for his in hists:
    
    hns = his.GetName()
    hns = hns.replace("_up","Up")    
    hns = hns.replace("_dn","Down")    
    his.SetName(hns)
    print fout.GetName(),"writing ",his.GetName()," ",his.Integral()
    his.Write()
     
data_obs.Write()

fout.Close()
totyield = data_obs.Integral()
'''            
