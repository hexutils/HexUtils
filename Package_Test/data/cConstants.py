import ROOT

def init_cConstants():
  D2jetZHSpline = ROOT.TFile("cconstants/SmoothKDConstant_m4l_DjjZH_13TeV.root").Get("sp_gr_varReco_Constant_Smooth")
  D2jetWHSpline = ROOT.TFile("cconstants/SmoothKDConstant_m4l_DjjWH_13TeV.root").Get("sp_gr_varReco_Constant_Smooth")
  D2jetVBFSpline = ROOT.TFile("cconstants/SmoothKDConstant_m4l_DjjVBF_13TeV.root").Get("sp_gr_varReco_Constant_Smooth")
  D1jetVBFSpline = ROOT.TFile("cconstants/SmoothKDConstant_m4l_DjVBF_13TeV.root").Get("sp_gr_varReco_Constant_Smooth")
  DbkgkinSpline4e = ROOT.TFile("cconstants/SmoothKDConstant_m4l_Dbkgkin_4e_13TeV.root").Get("sp_gr_varReco_Constant_Smooth")
  DbkgkinSpline4mu = ROOT.TFile("cconstants/SmoothKDConstant_m4l_Dbkgkin_4mu_13TeV.root").Get("sp_gr_varReco_Constant_Smooth")
  DbkgkinSpline2e2mu = ROOT.TFile("cconstants/SmoothKDConstant_m4l_Dbkgkin_2e2mu_13TeV.root").Get("sp_gr_varReco_Constant_Smooth")
  DbkgjjEWQCDSpline4lHadVH = ROOT.TFile("cconstants/SmoothKDConstant_m4l_DbkgjjEWQCD_4l_HadVHTagged_13TeV.root").Get("sp_gr_varReco_Constant_Smooth")
  DbkgjjEWQCDSpline2l2lHadVH = ROOT.TFile("cconstants/SmoothKDConstant_m4l_DbkgjjEWQCD_2l2l_HadVHTagged_13TeV.root").Get("sp_gr_varReco_Constant_Smooth")
  DbkgjjEWQCDSpline4lJJVBF = ROOT.TFile("cconstants/SmoothKDConstant_m4l_DbkgjjEWQCD_4l_JJVBFTagged_13TeV.root").Get("sp_gr_varReco_Constant_Smooth")
  DbkgjjEWQCDSpline2l2lJJVBF = ROOT.TFile("cconstants/SmoothKDConstant_m4l_DbkgjjEWQCD_2l2l_JJVBFTagged_13TeV.root").Get("sp_gr_varReco_Constant_Smooth")
  DggbkgkinSpline4e = ROOT.TFile("cconstants/SmoothKDConstant_m4l_Dggbkgkin_4e_13TeV.root").Get("sp_gr_varReco_Constant_Smooth")
  DggbkgkinSpline4mu = ROOT.TFile("cconstants/SmoothKDConstant_m4l_Dggbkgin_4mu_13TeV.root").Get("sp_gr_varReco_Constant_Smooth")
  DggbkgkinSpline2e2mu = ROOT.TFile("cconstants/SmoothKDConstant_m4l_Dggbkgin_2e2mu_13TeV.root").Get("sp_gr_varReco_Constant_Smooth")

  cConstant_Dictionary = {
  	"D2jetZHSpline": D2jetZHSpline,
  	"D2jetWHSpline": D2jetZHSpline,
  	"D2jetVBFSpline": D2jetZHSpline,
  	"D1jetVBFSpline": D2jetZHSpline,
  	"DbkgkinSpline4e": DbkgkinSpine4e,
  	"DbkgkinSpline4mu": DbkgkinSpine4mu,
  	"DbkgkinSpline2e2mu": DbkgkinSpine2e2mu,
  	"DbkgjjEWQCDSpline4lHadVH": DbkgjjEWQCDSpline4lHadVH,
   	"DbkgjjEWQCDSpline2l2lHadVH": DbkgjjEWQCDSpline2l2lHadVH,
   	"DbkgjjEWQCDSpline4lJJVBF": DbkgjjEWQCDSpline4lJJVBF,
   	"DbkgjjEWQCDSpline2l2lJJVBF": DbkgjjEWQCDSpline2l2lJJVBF
	"DggbkgkinSpline4e" = DggbkgkinSpline4e
        "DggbkgkinSpline4mu" = DggbkgkinSpline4mu
        "DggbkgkinSpline2e2mu" = DggbkgkinSpline2e2mu
        }
  return cConstant_Dictionary 

