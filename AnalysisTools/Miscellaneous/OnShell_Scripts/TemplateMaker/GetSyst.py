import ROOT

def getsyst(syst_name,category,year,MZZ) : 
   #syst_list_ggh = ["qcd_ren","qcd_fact","pdf","a_strong"]

   weightup = 1.0
   weightdn = 1.0

   if category == 0 : cat = "Untagged"
   if category == 1 : cat = "VBF"
   if category == 2 : cat = "VH"
  
   if syst_name == "qcdren" : hreadname =  "qcdrenom"
   if syst_name == "qcdfac" : hreadname =  "qcdfact"
   if syst_name == "pdf" : hreadname = "pdf"
   if syst_name == "a_strong" : hreadname = "astrong"

   if hreadname == "": 
      
      weightup = 1.05
      weightdn = 0.95
   else : 
      fname = "Theory_gg_syst_ratio_"+cat+".root"
      fin =  ROOT.TFile(fname)

      hnameup = "ratio_"+hreadname+"_up"
      htup = fin.Get(hnameup)
      binn = htup.GetXaxis().FindBin(MZZ)
      weightup = htup.GetBinContent(binn)
      
      hnamedn = "ratio_"+hreadname+"_dn"
      htdn = fin.Get(hnamedn)
      binn = htdn.FindBin(MZZ)
      weightdn = htdn.GetBinContent(binn)

   syst_w = (weightup,weightdn)


   return syst_w
