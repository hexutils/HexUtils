import ROOT

def init_gConstants():
  gConstant_HZZ2e2mu_g2 = ROOT.TFile("/gConstants/gConstant_HZZ2e2mu_g2.root").Get("sp_tgfinal_HZZ2e2mu_SM_over_tgfinal_HZZ2e2mu_g2")
  gConstant_HZZ2e2mu_g4 = ROOT.TFile("/gConstants/gConstant_HZZ2e2mu_g4.root").Get("sp_tgfinal_HZZ2e2mu_SM_over_tgfinal_HZZ2e2mu_g4")
  gConstant_HZZ2e2mu_L1 = ROOT.TFile("/gConstants/gConstant_HZZ2e2mu_L1.root").Get("sp_tgfinal_HZZ2e2mu_SM_over_tgfinal_HZZ2e2mu_L1")
  gConstant_HZZ2e2mu_L1Zgs = ROOT.TFile("/gConstants/gConstant_HZZ2e2mu_L1Zgs.root").Get("sp_tgfinal_HZZ2e2mu_SM_photoncut_over_tgfinal_HZZ2e2mu_L1Zgs")
  gConstant_VBF_g2 = ROOT.TFile("/gConstants/gConstant_VBF_g2.root").Get("sp_tgfinal_VBF_SM_over_tgfinal_VBF_g2")
  gConstant_VBF_g4 = ROOT.TFile("/gConstants/gConstant_VBF_g4.root").Get("sp_tgfinal_VBF_SM_over_tgfinal_VBF_g4")
  gConstant_VBF_L1 = ROOT.TFile("/gConstants/gConstant_VBF_L1.root").Get("sp_tgfinal_VBF_SM_over_tgfinal_VBF_L1")
  gConstant_VBF_L1Zgs = ROOT.TFile("/gConstants/gConstant_VBF_L1Zgs.root").Get("sp_tgfinal_VBF_SM_photoncut_over_tgfinal_VBF_L1Zgs")
  gConstant_ZH_g2 = ROOT.TFile("/gConstants/gConstant_ZH_g2.root").Get("sp_tgfinal_ZH_SM_over_tgfinal_ZH_g2")
  gConstant_ZH_g4 = ROOT.TFile("/gConstants/gConstant_ZH_g4.root").Get("sp_tgfinal_ZH_SM_over_tgfinal_ZH_g4")
  gConstant_ZH_L1 = ROOT.TFile("/gConstants/gConstant_ZH_L1.root").Get("sp_tgfinal_ZH_SM_over_tgfinal_ZH_L1")
  gConstant_ZH_L1Zgs = ROOT.TFile("/gConstants/gConstant_ZH_L1Zgs.root").Get("sp_tgfinal_ZH_SM_photoncut_over_tgfinal_ZH_L1Zgs")
  gConstant_VH_g2 = ROOT.TFile("/gConstants/gConstant_VH_g2.root").Get("sp_tgfinal_ZH_SM_plus_tgfinal_WH_SM_over_tgfinal_ZH_g2_plus_tgfinal_WH_g2")
  gConstant_VH_g4 = ROOT.TFile("/gConstants/gConstant_VH_g4.root").Get("sp_tgfinal_ZH_SM_plus_tgfinal_WH_SM_over_tgfinal_ZH_g4_plus_tgfinal_WH_g4")
  gConstant_VH_L1 = ROOT.TFile("/gConstants/gConstant_VH_L1.root").Get("sp_tgfinal_ZH_SM_plus_tgfinal_WH_SM_over_tgfinal_ZH_L1_plus_tgfinal_WH_L1")
  gConstant_VH_L1Zgs = ROOT.TFile("/gConstants/gConstant_VH_L1Zgs.root").Get("sp_tgfinal_ZH_SM_photoncut_plus_tgfinal_WH_SM_over_tgfinal_ZH_L1Zgs")
  gConstant_WH_g2 = ROOT.TFile("/gConstants/gConstant_WH_g2.root").Get("sp_tgfinal_WH_SM_over_tgfinal_WH_g2")
  gConstant_WH_g4 = ROOT.TFile("/gConstants/gConstant_WH_g4.root").Get("sp_tgfinal_WH_SM_over_tgfinal_WH_g4")
  gConstant_WH_L1 = ROOT.TFile("/gConstants/gConstant_WH_L1.root").Get("sp_tgfinal_WH_SM_over_tgfinal_WH_L1")
  
  gConstant_Dictionary = {
  	"HZZ2e2mu_g2": gConstant_HZZ2e2mu_g2,
  	"HZZ2e2mu_g4": gConstant_HZZ2e2mu_g4,
  	"HZZ2e2mu_L1": gConstant_HZZ2e2mu_L1,
  	"HZZ2e2mu_L1Zgs": gConstant_HZZ2e2mu_L1Zgs,
	"VBF_g2": gConstant_VBF_g2,
	"VBF_g4": gConstant_VBF_g4,
	"VBF_L1": gConstant_VBF_L1,
	"VBF_L1Zgs": gConstant_VBF_L1Zgs,
	"ZH_g2": gConstant_ZH_g2,
	"ZH_g4": gConstant_ZH_g4,
	"ZH_L1": gConstant_ZH_L1,
	"ZH_L1Zgs": gConstant_ZH_L1Zgs,
	"VH_g2": gConstant_VH_g2,
	"VH_g4": gConstant_VH_g4,
	"VH_L1": gConstant_VH_L1,
	"VH_L1Zgs": gConstant_VH_L1Zgs,
	"WH_g2": gConstant_WH_g2,
	"WH_g4": gConstant_WH_g4,
	"WH_L1": gConstant_WH_L1
  }
  return gConstant_Dictionary 

# coupling hypothesis is hypothesis
# process is the production or decay mode you want
# m4l is self explanatory
# gConstants is the dictionary of g_Constants that init_gConstants returns
def getvalue(hypothesis,process,m4l,gConstants):
  if hypothesis == "g2":
    if process == "HZZ2e2mu": return gConstants["HZZ2e2mu_g2"].Eval(m4l)
    if process == "VH": return gConstants["VH_g2"].Eval(m4l)
    if process == "WH": return gConstants["WH_g2"].Eval(m4l)
    if process == "ZH": return gConstants["ZH_g2"].Eval(m4l)
    if process == "VBF": return gConstants["VBF_g2"].Eval(m4l)
    assert False, process
  if hypothesis == "g4":
    if process == "HZZ2e2mu": return gConstants["HZZ2e2mu_g4"].Eval(m4l)
    if process == "VH": return gConstants["VH_g4"].Eval(m4l)
    if process == "WH": return gConstants["WH_g4"].Eval(m4l)
    if process == "ZH": return gConstants["ZH_g4"].Eval(m4l)
    if process == "VBF": return gConstants["VBF_g4"].Eval(m4l)
    assert False, process
  if hypothesis == "L1":
    if process == "HZZ2e2mu": return gConstants["HZZ2e2mu_L1"].Eval(m4l)
    if process == "VH": return gConstants["VH_L1"].Eval(m4l)
    if process == "WH": return gConstants["WH_L1"].Eval(m4l)
    if process == "ZH": return gConstants["ZH_L1"].Eval(m4l)
    if process == "VBF": return gConstants["VBF_L1"].Eval(m4l)
    assert False, process
  if hypothesis == "L1Zgs":
    if process == "HZZ2e2mu": return gConstants["HZZ2e2mu_L1Zgs"].Eval(m4l)
    if process == "VH": return gConstants["VH_L1Zgs"].Eval(m4l)
    if process == "ZH": return gConstants["ZH_L1Zgs"].Eval(m4l)
    if process == "VBF": return gConstants["VBF_L1Zgs"].Eval(m4l)
    assert False, process
  if hypothesis == "g2Zg":
    #if self.process == "HZZ2e2mu": return 2.24e-3 ** 0.5  #table 1 in 14-018
    if process == "HZZ2e2mu": return 0.005226666666666666 ** 0.5  #from Savvas
    if process in ("VH", "ZH", "WH"): return 0.014778325123152709 ** 0.5 #from Savvas
    if process == "VBF": return 0.05263157894736842 ** .5
    assert False, process
  if hypothesis == "g4Zg":
    #if self.process == "HZZ2e2mu": return 2.72e-3 ** 0.5  #table 1 in 14-018
    if process == "HZZ2e2mu": return 0.01088 ** 0.5  #from Savvas
    if process in ("VH", "ZH", "WH"): return 0.017857142857142856 ** .5 #from Savvas
    if process == "VBF": return 0.05263157894736842 ** .5
    assert False, self.process
  if hypothesis == "g2gg":
    #if self.process == "HZZ2e2mu": return 2.82e-3 ** 0.5  #table 1 in 14-018
    if process == "HZZ2e2mu": return 0.005474117647058824 ** 0.5  #from Savvas
    if process in ("VH", "ZH", "WH"): return 1
    if process == "VBF": return 0.093567 ** .5
    assert False, process
  if hypothesis == "g4gg":
    #if self.process == "HZZ2e2mu": return 2.88e-3 ** 0.5  #table 1 in 14-018
    if process == "HZZ2e2mu": return 0.005590588235294118 ** 0.5  #from Savvas
    if process in ("VH", "ZH", "WH"): return 1
    if process == "VBF": return 0.093567 ** .5
    assert False, process
  raise NameError("gConstants: Please Choose Valid hypothesis")
