import os

class Analysis_Config:
  def __init__(self,name):
    if name == "OnShell_HVV_Photons_2021":
      self.useVHMETTagged = False
      self.useQGTagging = False
      self.TaggingProcess = "Tag_AC_19_Scheme_2"
      self.ReweightProcess = "Calc_Event_Weight_2021_gammaH"
      self.TreeFile = "200205_CutBased"
      self.Save_Failed = False
      self.Path_To_Utils = "/afs/cern.ch/work/j/jejeffre/public/HEP_Ex_Tools/HepExUtils/OnShell_Utils"
      self.Discriminants_To_Calculate = ["D_0minus_decay","D_CP_decay","D_0hplus_decay","D_int_decay","D_L1_decay","D_L1int_decay","D_L1Zg_decay","D_L1Zgint_decay","D_L1L1Zg_decay","D_L1L1Zgint_decay","D_0minus_Zg_decay","D_CP_Zg_decay","D_0hplus_Zg_decay","D_int_Zg_decay","D_0minus_gg_decay","D_CP_gg_decay","D_0hplus_gg_decay",
                                         "D_0minus_VBF","D_CP_VBF","D_0hplus_VBF","D_int_VBF","D_L1_VBF","D_L1int_VBF","D_L1Zg_VBF","D_L1Zgint_VBF","D_0minus_Zg_VBF","D_CP_Zg_VBF","D_0hplus_Zg_VBF","D_int_Zg_VBF",
                                         "D_0minus_VBFdecay","D_0hplus_VBFdecay","D_L1_VBFdecay","D_0minus_VBFdecay","D_0minus_Zg_VBFdecay","D_0hplus_Zg_VBFdecay","D_0minus_gg_VBFdecay", "D_0hplus_gg_VBFdecay",
                                         "D_0minus_HadVH","D_CP_HadVH","D_0hplus_HadVH","D_int_HadVH","D_L1_HadVH","D_L1int_HadVH","D_L1Zg_HadVH","D_L1Zgint_HadVH","D_0minus_Zg_HadVH", "D_CP_Zg_HadVH","D_0hplus_Zg_HadVH","D_int_Zg_HadVH", "D_0minus_gg_HadVH","D_CP_gg_HadVH","D_0hplus_gg_HadVH","D_int_gg_HadVH" ]

