import os

class Analysis_Config:
  def __init__(self,name):
    if name == "OnShell_HVV_Photons_2021":
      self.name = "OnShell_HVV_Photons_2021"
      self.useVHMETTagged = False
      self.useQGTagging = False
      self.TaggingProcess = "Tag_AC_19_Scheme_2"
      self.ReweightProcess = "Calc_Event_Weight_2021_gammaH"
      self.TreeFile = "200205_CutBased"
      self.Save_Failed = False
      self.Save_p = True
      self.Variable_Edges = False
      self.Coupling_Name = 'a3'
      self.Hypothesis_List = ['SM','g4','fa30.5-interf']
      self.Discriminants_To_Calculate = ["D_0minus_decay","D_CP_decay","D_0hplus_decay","D_int_decay","D_L1_decay","D_L1int_decay","D_L1Zg_decay","D_L1Zgint_decay","D_L1L1Zg_decay","D_L1L1Zgint_decay","D_0minus_Zg_decay","D_CP_Zg_decay","D_0hplus_Zg_decay","D_int_Zg_decay","D_0minus_gg_decay","D_CP_gg_decay","D_0hplus_gg_decay",
                                         "D_0minus_VBF","D_CP_VBF","D_0hplus_VBF","D_int_VBF","D_L1_VBF","D_L1int_VBF","D_L1Zg_VBF","D_L1Zgint_VBF","D_0minus_Zg_VBF","D_CP_Zg_VBF","D_0hplus_Zg_VBF","D_int_Zg_VBF",
                                         "D_0minus_VBFdecay","D_0hplus_VBFdecay","D_L1_VBFdecay","D_L1Zg_VBFdecay","D_0minus_Zg_VBFdecay","D_0hplus_Zg_VBFdecay","D_0minus_gg_VBFdecay", "D_0hplus_gg_VBFdecay",
                                         "D_0minus_HadVHdecay","D_0hplus_HadVHdecay","D_L1_HadVHdecay","D_L1Zg_HadVHdecay","D_0minus_Zg_HadVHdecay","D_0hplus_Zg_HadVHdecay","D_0minus_gg_HadVHdecay", "D_0hplus_gg_HadVHdecay",
                                         "D_0minus_HadVH","D_CP_HadVH","D_0hplus_HadVH","D_int_HadVH","D_L1_HadVH","D_L1int_HadVH","D_L1Zg_HadVH","D_L1Zgint_HadVH","D_0minus_Zg_HadVH", "D_CP_Zg_HadVH","D_0hplus_Zg_HadVH","D_int_Zg_HadVH", "D_0minus_gg_HadVH","D_CP_gg_HadVH","D_0hplus_gg_HadVH","D_int_gg_HadVH",
                                         "D_bkg","D_bkg_VBFdecay","D_bkg_HadVHdecay",
                                         "Pt4l"]
      self.lumi = {'2016':35.9,'2017':41.5,'2018':59.7}
      self.VBF1jTagged_Discriminants = {"D_bkg":[0,.33,.66,1],"Pt4l":[0,100,200]}
      self.VBF2jTagged_Discriminants = {"D_bkg_VBFdecay":[0,.33,.66,1],"D_0hplus_VBFdecay":[0,.33,.66,1],"D_0minus_VBFdecay":[0,.33,.66,1],"D_L1_VBFdecay":[0,.33,.66,1],"D_L1Zg_VBFdecay":[0,.33,.66,1],"D_Int_VBF":[-1,.33,.66,1],"D_CP_VBF":[0,.33,.66,1]}
      self.VHLeptTagged_Discriminants = {"D_bkg":[0,.33,.66,1],"Pt4l":[0,100,200]}
      self.VHHadrTagged_Discriminants = {"D_bkg_HadVHdecay":[0,.33,.66,1],"D_0hplus_HadVHdecay":[0,.33,.66,1],"D_0minus_HadVHdecay":[0,.33,.66,1],"D_L1_HadVHdecay":[0,.33,.66,1],"D_L1Zg_HadVHdecay":[0,.33,.66,1],"D_Int_VH":[-1,.33,.66,1],"D_CP_VH":[0,.33,.66,1]}
      self.ttHLeptTagged_Discriminants = {}
      self.ttHHadrTagged_Discriminants = {}
      self.VHMETTagged_Discriminants = {}
      self.Boosted_Discriminants = {"D_bkg":[0,.33,.66,1],"Pt4l":[0,100,200]}
      self.Untagged_Discriminants = {"D_bkg":[0,.33,.66,1],"D_CP_decay":[-1,0,.66,1],"D_0hplus_decay":[0,.33,.66,1],"D_0minus_decay":[0,.33,.66,1],"D_L1_decay":[0,.33,.66,1],"D_L1Zg_decay":[0,.33,.66,1],"D_int_decay":[0,.33,.66,1]}

