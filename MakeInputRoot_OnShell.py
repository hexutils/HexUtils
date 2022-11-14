import os, glob
import sys
import ROOT
import copy

# What this script does is trim and rename the template files and prepare them for the datacards.
# The expected input is a list of templates that would belong to the sample datacard.

#========================== How to run this ===========================
# 1. First argument is the name of the template you want to create

# 2. The next arguments are all of the input root files with the histrograms needed
def Make_Template_With_Fake_Data(OutName,names):
  # OutName = Output Root File Name
  # names = Input Root Files 

  hists = [] # Holds the histograms to add to the final TFile
  used_names = [] # Stores the names of the histrograms 

  for nm in names:
    fin = ROOT.TFile.Open(nm)
    for key in fin.GetListOfKeys():
      if "TH1" in key.GetClassName():
        h_name = key.GetName()
        h_temp = fin.Get(h_name)
        h_temp.SetDirectory(0)
        if h_name not in used_names:
          print(h_name)
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

  Fake_Data_Hist = Fake_Data[0].Clone("data_obs")
  for i in range(1,len(Fake_Data)):
    Fake_Data_Hist.Add(Fake_Data[i])

  fout =  ROOT.TFile.Open(OutName,"recreate")
  fout.cd()

  Fake_Data_Hist.Write("data_obs")

  for hist in hists:
    if ("bkg_ew_negative" not in hist.GetName()):
      if ("bkg_ew_positive" in hist.GetName()):
        hist.Write("bkg_ew")
      else:
        hist.Write()

  print(OutName)

def main():
  output_dir = sys.argv[2]
  if not os.path.exists(output_dir):
      os.mkdir(output_dir)
  output_dir = output_dir.strip("/")
  Input_Dir = sys.argv[1]
  for filename in glob.iglob(Input_Dir+'/**', recursive=True):
    if os.path.isfile(filename) and (".root" in filename):
      out_ext=filename
      if "/" in filename:
        out_ext = filename.split("/")[-1]
        out_ext = out_ext.split(".")[0]+".input."+out_ext.split(".")[1]
      Make_Template_With_Fake_Data(output_dir+"/"+out_ext,[filename]) 

if __name__ == "__main__":
    main()

