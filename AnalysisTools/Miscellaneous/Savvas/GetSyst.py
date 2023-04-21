import ROOT

def getsyst(syst_name,category,year,MZZ) : 
   #syst_list_ggh = ["qcd_ren","qcd_fact","pdf","a_strong"]

   weightup = 1.0
   weightdn = 1.0

   hreadname = ""

   if category == 0 : cat = "Untagged"
   if category == 1 : cat = "VBF"
   if category == 2 : cat = "VH"
  
   if syst_name == "qcdren" : hreadname =  "qcdrenom"
   if syst_name == "qcdfac" : hreadname =  "qcdfact"
   if syst_name == "pdf" : hreadname = "pdf"
   if syst_name == "astrong" : hreadname = "astrong"


   if syst_name == "kfqcd" : hreadname =  "QCDScale"
   if syst_name == "kfpdf" : hreadname =  "PDFScale"
   if syst_name == "kfas"  : hreadname =  "As"
   if syst_name == "kfnnqcd" : hreadname =  "QCDScale"
   if syst_name == "kfnnpdf" : hreadname =  "PDFScale"
   if syst_name == "kfnnas"  : hreadname =  "As"


   if hreadname == "": 
      
      weightup = 1.05
      weightdn = 0.95
   else : 
      fname = ""
      if "kf" in syst_name and "kfnn" not in syst_name : 
         fname = "/afs/cern.ch/work/s/skyriaco/CJLSTUL/CMSSW_10_6_26/src/ZZAnalysis/AnalysisStep/data/kfactors/Kfactor_Collected_ggHZZ_2l2l_NLO_NNPDF_NarrowWidth_13TeV.root"
         hnameup = "sp_kfactor_"+hreadname+"Up"
         hnamedn = "sp_kfactor_"+hreadname+"Dn"


      elif "kfnn" in systname :
         fname = "/afs/cern.ch/work/s/skyriaco/CJLSTUL/CMSSW_10_6_26/src/ZZAnalysis/AnalysisStep/data/kfactors/Kfactor_Collected_ggHZZ_2l2l_NNLO_NNPDF_NarrowWidth_13TeV.root"
         hnameup = "sp_kfactor_"+hreadname+"Up"
         hnamedn = "sp_kfactor_"+hreadname+"Dn"

      else  : 
   
         fname = "Theory_gg_syst_ratio_"+cat+".root"
         hnameup = "ratio_"+hreadname+"_up"
         hnamedn = "ratio_"+hreadname+"_dn"

      fin =  ROOT.TFile(fname)

      if not "kf" in syst_name: 
         htup = fin.Get(hnameup)
         binn = htup.GetXaxis().FindBin(MZZ)
         weightup = htup.GetBinContent(binn)
         htdn = fin.Get(hnamedn)
         binn = htdn.FindBin(MZZ)
         weightdn = htdn.GetBinContent(binn)
      else : 
         htup = fin.Get(hnameup)
         weightup = htup.Eval(MZZ) 
         htdn = fin.Get(hnamedn)
         weightdn = htdn.Eval(MZZ)
          
         
   
   syst_w = (weightup,weightdn)


   return syst_w
