import os

class Analysis_Config:
  def __init__(self,name):
    if name == "OnShell_HVV_Photons_2021": # HVV Couplings and Photons
      self.name = "OnShell_HVV_Photons_2021"
      self.useVHMETTagged = False
      self.useQGTagging = False
      self.TaggingProcess = "Tag_AC_19_Scheme_2"
      self.ReweightProcess = "Calc_Event_Weight_2021_gammaH"
      self.TreeFile = "200205_CutBased"
      self.Save_Failed = False
      self.Save_p = True
      self.Variable_Edges = False
      # Discriminants and couplings for OnShell Analysis #
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
      self.VBF1jTagged_Discriminants = {"D_bkg":[0,.33,.66,1],"Pt4l":[0,100,1000]}
      self.VBF2jTagged_Discriminants = {"D_bkg_VBFdecay":[0,.33,.66,1],"D_0hplus_VBFdecay":[0,.33,.66,1],"D_0minus_VBFdecay":[0,.33,.66,1],"D_L1_VBFdecay":[0,.33,.66,1],"D_L1Zg_VBFdecay":[0,.33,.66,1],"D_int_VBF":[-1,.33,.66,1],"D_CP_VBF":[0,.33,.66,1]}
      self.VHLeptTagged_Discriminants = {"D_bkg":[0,.33,.66,1],"Pt4l":[0,100,1000]}
      self.VHHadrTagged_Discriminants = {"D_bkg_HadVHdecay":[0,.33,.66,1],"D_0hplus_HadVHdecay":[0,.33,.66,1],"D_0minus_HadVHdecay":[0,.33,.66,1],"D_L1_HadVHdecay":[0,.33,.66,1],"D_L1Zg_HadVHdecay":[0,.33,.66,1],"D_int_HadVH":[-1,.33,.66,1],"D_CP_HadVH":[0,.33,.66,1]}
      self.ttHLeptTagged_Discriminants = {}
      self.ttHHadrTagged_Discriminants = {}
      self.VHMETTagged_Discriminants = {}
      self.Boosted_Discriminants = {"D_bkg":[0,.33,.66,1],"Pt4l":[0,100,1000]}
      self.Untagged_Discriminants = {"D_bkg":[0,.33,.66,1],"D_CP_decay":[-1,0,.66,1],"D_0hplus_decay":[0,.33,.66,1],"D_0minus_decay":[0,.33,.66,1],"D_L1_decay":[0,.33,.66,1],"D_L1Zg_decay":[0,.33,.66,1],"D_int_decay":[0,.33,.66,1]}
      # This section should be a list of tags and signal types to use to make cards #
      #self.Production_Modes=["ggH","VBF","Wplus","Wminus","ZH","bbH","ttH","tH"]
      self.Production_Modes=["WplusH","WminusH","bbH","ttH"]
      self.Event_Categories=["Untagged","VBF1jTagged","VBF2jTagged","VHLeptTagged","VHHadrTagged","Boosted"]
      self.Final_States=["4l"]
      self.Years=["2016"]

    if name == "gammaH_Photons_Decay_Only": # HVV Couplings and Photons
      self.name = "gammaH_Photons_Decay_Only"
      self.useVHMETTagged = False
      self.useQGTagging = False
      self.DoMassFilter = True
      self.TaggingProcess = "Tag_Untagged_and_gammaH"
      self.ReweightProcess = "Calc_Event_Weight_2021_gammaH"
      self.TreeFile = "200205_CutBased"
      self.Save_Failed = False
      self.Save_p = True
      self.Variable_Edges = False
      # Discriminants and couplings for OnShell Analysis #
      #self.Coupling_Name = 'a2a3L1L1Zg'
      self.Coupling_Name = 'a2a3L1'
      #self.Hypothesis_List = ['SM','g4','fa30.5-interf']
      self.Hypothesis_List = ['SM','g2','g4','L1','L1Zg','fa20.5-interf','fa30.5-interf','fL10.5-interf','fL1Zg0.5-interf']
      #self.Hypothesis_List = ['SM','g2','g4','L1','fa20.5-interf','fa30.5-interf','fL10.5-interf']
      self.Discriminants_To_Calculate = ["D_0minus_decay","D_CP_decay","D_0hplus_decay","D_int_decay","D_L1_decay","D_L1int_decay","D_L1Zg_decay","D_L1Zgint_decay","D_L1L1Zg_decay","D_L1L1Zgint_decay","D_0minus_Zg_decay","D_CP_Zg_decay","D_0hplus_Zg_decay","D_int_Zg_decay","D_0minus_gg_decay","D_CP_gg_decay","D_0hplus_gg_decay",
                                         "D_bkg",
                                         "Pt4l"]
      self.lumi = {'2016':35.9,'2017':41.5,'2018':59.7}
      self.gammaH_Discriminants = {"D_bkg":[0,.33,.66,1],"Pt4l":[0,100,200,300,400,500,600,700,1000]}
      #self.Untagged_Discriminants = {"D_bkg":[0,.33,.66,1],"D_CP_decay":[-1,0,.66,1],"D_0hplus_decay":[0,.33,.66,1],"D_0minus_decay":[0,.33,.66,1],"D_L1_decay":[0,.33,.66,1],"D_L1Zg_decay":[0,.33,.66,1],"D_int_decay":[0,.33,.66,1]}
      self.Untagged_Discriminants = {"D_bkg":[0,.2,.7,1],"D_CP_decay":[-1,0,1],"D_0hplus_decay":[0,.33,.66,1],"D_0minus_decay":[0,.33,.66,1],"D_L1_decay":[0,.55,.8,1],"D_L1Zg_decay":[0,.4,.55,1],"D_int_decay":[-1,.8,1]}
      # This section should be a list of tags and signal types to use to make cards #
      #self.Production_Modes=["ggH","VBF","Wplus","Wminus","ZH","bbH","ttH"]
      self.Production_Modes=["ggH"]
      self.Event_Categories=["Untagged","gammaH"]
      #self.Event_Categories=["gammaH"]
      self.Final_States=["4e","2e2mu","4mu"]
      #self.Final_States=["4l"]
      self.Years=["2016","2017","2018"]
      #self.Years=["2016"]
