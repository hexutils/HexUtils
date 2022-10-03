import ROOT
import os
def init_FakeRates():
  Path_To_This_File = os.path.abspath(__file__)
  Path_To_This_Directory = os.path.split(Path_To_This_File)[0]
  Relative_Path_To_Splines ="FakeRates/"
  PathToSpline = os.path.join(Path_To_This_Directory, Relative_Path_To_Splines)
  FakeRates_OS_2016 = ROOT.TFile(PathToSpline+"/FakeRates_OS_2016.root")
  FakeRates_OS_2017 = ROOT.TFile(PathToSpline+"/FakeRates_OS_2017.root")
  FakeRates_OS_2018 = ROOT.TFile(PathToSpline+"/FakeRates_OS_2018.root")
  FakeRates_SS_2016 = ROOT.TFile(PathToSpline+"/FakeRates_SS_2016.root")
  FakeRates_SS_2017 = ROOT.TFile(PathToSpline+"/FakeRates_SS_2017.root")
  FakeRates_SS_2018 = ROOT.TFile(PathToSpline+"/FakeRates_SS_2018.root")
  newData_FakeRates_OS_2016 = ROOT.TFile(PathToSpline+"/newData_FakeRates_OS_2016.root")
  newData_FakeRates_OS_2017 = ROOT.TFile(PathToSpline+"/newData_FakeRates_OS_2017.root")
  newData_FakeRates_OS_2018 = ROOT.TFile(PathToSpline+"/newData_FakeRates_OS_2018.root")
  newData_FakeRates_SS_2016 = ROOT.TFile(PathToSpline+"/newData_FakeRates_SS_2016.root")
  newData_FakeRates_SS_2017 = ROOT.TFile(PathToSpline+"/newData_FakeRates_SS_2017.root")
  newData_FakeRates_SS_2018 = ROOT.TFile(PathToSpline+"/newData_FakeRates_SS_2018.root")

  FakeRate_Dict = {"FakeRates_OS_2016":FakeRates_OS_2016,
                   "FakeRates_OS_2017":FakeRates_OS_2017,
                   "FakeRates_OS_2018":FakeRates_OS_2018,
                   "FakeRates_SS_2016":FakeRates_SS_2016,
                   "FakeRates_SS_2017":FakeRates_SS_2017,
                   "FakeRates_SS_2018":FakeRates_SS_2018,
                   "newData_FakeRates_OS_2016":newData_FakeRates_OS_2016,
                   "newData_FakeRates_OS_2017":newData_FakeRates_OS_2017,
                   "newData_FakeRates_OS_2018":newData_FakeRates_OS_2018,
                   "newData_FakeRates_SS_2016":newData_FakeRates_SS_2016,
                   "newData_FakeRates_SS_2017":newData_FakeRates_SS_2017,
                   "newData_FakeRates_SS_2018":newData_FakeRates_SS_2018
  }
  return FakeRate_Dict

def init_FakeRates_SS():
  Path_To_This_File = os.path.abspath(__file__)
  Path_To_This_Directory = os.path.split(Path_To_This_File)[0]
  Relative_Path_To_Splines ="FakeRates/"
  PathToSpline = os.path.join(Path_To_This_Directory, Relative_Path_To_Splines)
  FakeRates_SS_2016 = ROOT.TFile(PathToSpline+"/FakeRates_SS_2016.root")
  FakeRates_SS_2017 = ROOT.TFile(PathToSpline+"/FakeRates_SS_2017.root")
  FakeRates_SS_2018 = ROOT.TFile(PathToSpline+"/FakeRates_SS_2018.root")
  newData_FakeRates_SS_2016 = ROOT.TFile(PathToSpline+"/newData_FakeRates_SS_2016.root")
  newData_FakeRates_SS_2017 = ROOT.TFile(PathToSpline+"/newData_FakeRates_SS_2017.root")
  newData_FakeRates_SS_2018 = ROOT.TFile(PathToSpline+"/newData_FakeRates_SS_2018.root")
  FakeRate_Dict = {(2016, False):FakeRates_SS_2016,
                   (2017, False):FakeRates_SS_2017,
                   (2018, False):FakeRates_SS_2018,
                   (2016, True):newData_FakeRates_SS_2016,
                   (2017, True):newData_FakeRates_SS_2017,
                   (2018, True):newData_FakeRates_SS_2018
  }
  return FakeRate_Dict

def init_FakeRates_OS():
  Path_To_This_File = os.path.abspath(__file__)
  Path_To_This_Directory = os.path.split(Path_To_This_File)[0]
  Relative_Path_To_Splines ="FakeRates/"
  PathToSpline = os.path.join(Path_To_This_Directory, Relative_Path_To_Splines)
  FakeRates_OS_2016 = ROOT.TFile(PathToSpline+"/FakeRates_OS_2016.root")
  FakeRates_OS_2017 = ROOT.TFile(PathToSpline+"/FakeRates_OS_2017.root")
  FakeRates_OS_2018 = ROOT.TFile(PathToSpline+"/FakeRates_OS_2018.root")
  newData_FakeRates_OS_2016 = ROOT.TFile(PathToSpline+"/newData_FakeRates_OS_2016.root")
  newData_FakeRates_OS_2017 = ROOT.TFile(PathToSpline+"/newData_FakeRates_OS_2017.root")
  newData_FakeRates_OS_2018 = ROOT.TFile(PathToSpline+"/newData_FakeRates_OS_2018.root")
 
  FakeRate_Dict = {(2016, False):FakeRates_OS_2016,
                   (2017, False):FakeRates_OS_2017,
                   (2018, False):FakeRates_OS_2018,
                   (2016, True):newData_FakeRates_OS_2016,
                   (2017, True):newData_FakeRates_OS_2017,
                   (2018, True):newData_FakeRates_OS_2018
  }
  return FakeRate_Dict

def get_Fake_Rate_From_File(FakeRate_Root_File,lep_Pt,lep_eta,lep_ID):
   if "_SS_" in FakeRate_Root_File.GetName():
     g_FR_mu_EB = FakeRate_Root_File.Get("FR_SS_muon_EB")
     g_FR_mu_EE = FakeRate_Root_File.Get("FR_SS_muon_EE")
     g_FR_e_EB  = FakeRate_Root_File.Get("FR_SS_electron_EB")
     g_FR_e_EE  = FakeRate_Root_File.Get("FR_SS_electron_EE")
   elif "_OS_" in FakeRate_Root_File.GetName():
     g_FR_mu_EB = FakeRate_Root_File.Get("FR_OS_muon_EB");
     g_FR_mu_EE = FakeRate_Root_File.Get("FR_OS_muon_EE");
     g_FR_e_EB  = FakeRate_Root_File.Get("FR_OS_electron_EB");
     g_FR_e_EE  = FakeRate_Root_File.Get("FR_OS_electron_EE");
   # Pull the correct histograms from the root file #

   if lep_Pt >= 80:
     my_lep_Pt = 79
   else:
     my_lep_Pt = lep_Pt
   
   my_lep_ID = abs(lep_ID)

   nbin = 0
   if ( my_lep_Pt > 5 and my_lep_Pt <= 7 ): nbin = 0
   elif ( my_lep_Pt >  7 and my_lep_Pt <= 10 ): nbin = 1
   elif ( my_lep_Pt > 10 and my_lep_Pt <= 20 ): nbin = 2
   elif ( my_lep_Pt > 20 and my_lep_Pt <= 30 ): nbin = 3
   elif ( my_lep_Pt > 30 and my_lep_Pt <= 40 ): nbin = 4
   elif ( my_lep_Pt > 40 and my_lep_Pt <= 50 ): nbin = 5
   elif ( my_lep_Pt > 50 and my_lep_Pt <= 80 ): nbin = 6
   
   if ( abs(my_lep_ID) == 11 ): nbin = nbin-1 # there is no [5, 7] bin in the electron fake rate

   if ( my_lep_ID == 11 ):
      if ( abs(lep_eta) < 1.479 ):
         return (g_FR_e_EB.GetY())[nbin]
      else:
         return (g_FR_e_EE.GetY())[nbin]
   elif ( my_lep_ID == 13 ):
      if ( abs(lep_eta) < 1.2 ):
         return (g_FR_mu_EB.GetY())[nbin]
      else:
         return (g_FR_mu_EE.GetY())[nbin];
   else:
      print("[ERROR] Wrong lepton ID: " + my_lep_ID + "\n")
      return 0

def getFakeRate(fakeRateDict, year, usenewobjects, leppt, lepeta, leplepid):
   return get_Fake_Rate_From_File(fakeRateDict[year,usenewobjects],leppt,lepeta,leplepid)
     

def ratio_combination_over_SS_new(year, flavor):
    el = 11**2
    mu = 13**2
    return {
      2016: {
        -mu*mu: 0.9504,
        -el*el: 1.2379,
        -el*mu: 1.0709,
      },
      2017: {
        -mu*mu: 0.9875,
        -el*el: 1.1870,
        -el*mu: 1.0510,
      },
      2018: {
        -mu*mu: 0.9722,
        -el*el: 1.2145,
        -el*mu: 1.05088,
      },
    }[year][flavor]

def ratio_combination_over_SS_old(year, flavor):
   el = 11**2
   mu = 13**2
   txtfileold = """
******************************************************************************
2016		SS		OS	
4mu		26.5 +/- 8.1	25.7 +/- 8.2
4e		13.1 +/- 5.5	20.2 +/- 6.2
2e2mu		21.6 +/- 6.6	23.6 +/- 7.5
2mu2e		16.8 +/- 7.0	23.5 +/- 7.2
2e2mu_Combined	38.5 +/- 9.7	47.1 +/- 10.3
				
SS-OS Combination	Yield	
4mu			26.1	
4e			16.2	
2e2mu			42.5	
				
******************************************************************************
2017		SS		OS	
4mu		30.0 +/- 9.2	31.9 +/- 10.0
4e		10.8 +/- 4.1	16.1 +/- 4.9
2e2mu		23.2 +/- 7.1	22.3 +/- 7.1
2mu2e		14.7 +/- 5.5	20.9 +/- 6.4
2e2mu_Combined 	37.9 +/- 9.0	43.1 +/- 9.5
				
SS-OS Combination	Yield	
4mu			30.9	
4e			13.0	
2e2mu			40.4	
******************************************************************************
2018		SS		OS		
4mu		49.9 +/- 15.2	47.7 +/- 14.8
4e		16.2 +/- 5.9	25.4 +/- 7.7
2e2mu		35.9 +/- 10.9	33.7 +/- 10.6
2mu2e		23.6 +/- 8.5	33.5 +/- 10.1
2e2mu_Combined	59.5 +/- 13.8	67.2 +/- 14.6
				
SS-OS Combination	Yield	
4mu			48.8	
4e			19.6	
2e2mu			63.1	
******************************************************************************
  """

   txtfilenew = """
SS	2016	2017	2018	Full Run 2
4mu	9.48	10.94	16.87	37.29		
4e	2.67	2.63	4.10	9.40
2e2mu	8.26	8.18	13.26	29.70
2mu2e	3.46	3.52	5.55	12.53
TOT	23.87	25.27	39.78	88.92
OS	2016	2017	2018	Full Run 2
4mu	8.37	8.58	14.11	31.06		
4e	5.33	3.85	6.53	15.71
2e2mu	7.68	7.59	11.05	26.32
2mu2e	5.67	6.39	8.68	20.74
TOT	27.05	26.41	40.37	93.83
COMB	2016	2017	2018	Full Run 2
4mu	8.94	9.66	15.37	33.97		
4e	3.43	3.07	4.88	11.38
2e2mu	12.43	12.63	19.25	44.31
TOT	24.8	25.36	39.5	89.66
  """
  
   lines = iter(txtfileold.split("\n"))
   for line in lines:
     if line.startswith(str(year)): break
   for line in lines:
     if line.startswith("201"): assert False
     if line.startswith({-el*el: "4e", -mu*mu: "4mu", -el*mu: "2e2mu_Combined"}[flavor]):
       SS = float(line.split()[1])
       break
   for line in lines:
      if line.startswith("201"): assert False
      if line.startswith("SS-OS Combination"): break
   for line in lines:
     if line.startswith("201"): assert False
     if line.startswith({-el*el: "4e", -mu*mu: "4mu", -el*mu: "2e2mu"}[flavor]):
       combination = float(line.split()[1])
       break
   return combination / SS

def Normalize_ZX(year, usenewobject, Z1Flav, Z2Flav): # This is the way it was done in HIG 19 009 
  if usenewobject:
    return ratio_combination_over_SS_new(year,-Z1Flav*Z2Flav)
  else:
    return ratio_combination_over_SS_old(year,-Z1Flav*Z2Flav)
