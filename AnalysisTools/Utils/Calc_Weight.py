import ROOT
import sys 
from ..data.Lep_Scale_Factor import *
from ..data.Fake_Rates import init_FakeRates_OS, init_FakeRates_SS, getFakeRate, Normalize_ZX
from .Fix_Xsec import *
from root_numpy import array2tree, tree2array
import numpy as np

def Calc_Event_Weight_200205(t,name): #Tree input as t and the name of the tree should have all info included#
        doSIP = False
        doL1prefiringweight = True
        doleptonSF = True
        doZ2Mass = False
        useJEC = False
        useJES = True
        useJER = False

        pb_to_fb = 1000
        nEntries=t.GetEntries()

	#==============Calculate the event scale per event array===============================#
        scale = np.ones(nEntries)
        if doL1prefiringweight:
          L1_Prefiring = tree2array(tree=t,branches=["L1prefiringWeight"]).astype(float)
          scale = scale * L1_Prefiring
        if doleptonSF:
          year = 0
          if "2016" in name:
            year = 2016
          elif "2017" in name:
            year = 2017 
          elif "2018" in name:
            year = 2018

          LepLepId = tree2array(tree=t,branches=["LepLepId"])
          LepPt = tree2array(tree=t,branches=["LepPt"])
          LepEta = tree2array(tree=t,branches=["LepEta"])
          dataMCWeight = tree2array(tree=t,branches=["dataMCWeight"])
          LepScale = []
          # Load up the LeptonScale Factors#
          LepSF = init_LEPSF()
          for i in range(nEntries):
            LepScale.append(fixleptonscalefactor(int(year),LepLepId[i][0],LepPt[i][0],LepEta[i][0],dataMCWeight[i][0],LepSF))
          scale = scale * LepScale
        if any( x in ["ggH","VBF","ZH","WH","VH","ttH","bbH","tqH","WplusH","WminusH","VBFbkg","TTZZ","ZZZ","WZZ","WWZ","TTWW","TTZJets_M10_MLM","TTZToLLNuNu_M10","TTZToLL_M1to10_MLM"] for x in name):
          scale = scale * 1.
        elif "ggZZ" in name: #or self.isggZZoffshell: 
          KFactor_QCD_ggZZ_Nominal = tree2array(tree=t,branches=["KFactor_QCD_ggZZ_Nominal"]).astype(float)
          scale = scale * KFactor_QCD_ggZZ_Nominal
        if "ggH" in name:
          ggH_NNLOPS_weight = tree2array(tree=t,branches=["ggH_NNLOPS_weight"]).astype(float)
          scale = scale * ggH_NNLOPS_weight
        elif "qqZZ" in name:
            if "GEN" in name: #Must check this later # 
              scale = scale * 1
            else:
              KFactor_EW_qqZZ = tree2array(tree=t,branches=["KFactor_EW_qqZZ"]).astype(float)
              KFactor_QCD_qqZZ_M = tree2array(tree=t,branches=["KFactor_QCD_qqZZ_M"]).astype(float)
              scale = scale * KFactor_EW_qqZZ * KFactor_QCD_qqZZ_M
        #===================================Make an array of each event weight===========================================#

        # Need to add Z + X stuff here at some point #

        print(scale)

        return tree2array(tree=t,branches=["genxsec*genBR*overallEventWeight*xsec/(genxsec*genBR)/Bin40"]).astype(float) * scale * pb_to_fb 

def Calc_Tree_Weight_2021_gammaH(t,name,DoMassFilter): #Tree input as t and the name of the tree should have all info included#
        doleptonSF=True
        pb_to_fb =1000
        nEntries=t.GetEntries()
        #==============Calculate the event scale per event array===============================#
        scale = np.ones(nEntries)
        year = 0
        if "2016" in name:
          year = 2016
        elif "2017" in name:
          year = 2017 
        elif "2018" in name:
          year = 2018
        if doleptonSF and not "ZX" in name:
          LepLepId = tree2array(tree=t,branches=["LepLepId"])
          LepPt = tree2array(tree=t,branches=["LepPt"])
          LepEta = tree2array(tree=t,branches=["LepEta"])
          dataMCWeight = tree2array(tree=t,branches=["dataMCWeight"])
          LepScale = []
          # Load up the LeptonScale Factors#
          LepSF = init_LEPSF()
          for i in range(nEntries):
            LepScale.append(fixleptonscalefactor(int(year),LepLepId[i][0],LepPt[i][0],LepEta[i][0],dataMCWeight[i][0],LepSF))
          scale = scale * LepScale
        if any( x in ["ggH","VBF","ZH","WH","ttH","bbH","tqH","WplusH","WminusH","VBFbkg","TTZZ","ZZZ","WZZ","WWZ","TTWW","TTZJets_M10_MLM","TTZToLLNuNu_M10","TTZToLL_M1to10_MLM"] for x in name):
          scale = scale * 1.
        if "ggH" in name:
          ggH_NNLOPS_weight = tree2array(tree=t,branches=["ggH_NNLOPS_weight"]).astype(float)
          scale = scale * ggH_NNLOPS_weight
        elif "ggZZ" in name: #or self.isggZZoffshell: 
          KFactor_QCD_ggZZ_Nominal = tree2array(tree=t,branches=["KFactor_QCD_ggZZ_Nominal"]).astype(float)
          scale = scale * KFactor_QCD_ggZZ_Nominal
        elif "qqZZ" in name:
            if "GEN" in name: #Must check this later # 
              scale = scale * 1
            else:
              print(name)
              KFactor_EW_qqZZ = tree2array(tree=t,branches=["KFactor_EW_qqZZ"]).astype(float)
              KFactor_QCD_qqZZ_M = tree2array(tree=t,branches=["KFactor_QCD_qqZZ_M"]).astype(float)
              scale = scale * KFactor_EW_qqZZ * KFactor_QCD_qqZZ_M
        elif "ZX" in name or "data" in name:
          if "data" in name:
            return np.ones(nEntries)
          elif "ZX" in name:
            # Load up the ZX dictionaries #
            SSFR = init_FakeRates_SS()
            OSFR = init_FakeRates_OS()
            #=============================#
            LepLepId = tree2array(tree=t,branches=["LepLepId"])
            LepPt = tree2array(tree=t,branches=["LepPt"])
            LepEta = tree2array(tree=t,branches=["LepEta"])
            Z1Flav = tree2array(tree=t,branches=["Z1Flav"])
            Z2Flav = tree2array(tree=t,branches=["Z2Flav"])
            ZZMass = tree2array(tree=t,branches=["ZZMass"]).astype(float)
            ZX_Weight = []
            for i in range(nEntries):
              if 105 < ZZMass[i] < 140:
                if (Z1Flav[i][0] < 0 and Z2Flav[i][0] < 0) or (Z1Flav[i][0] > 0 and Z2Flav[i][0] > 0):
                  #ZX_Norm = 0
                  ZX_Norm = Normalize_ZX(year, True, Z1Flav[i][0], Z2Flav[i][0]) 
                  ZX_Lep3FR = getFakeRate(SSFR, year, True, LepPt[i][0][2], LepEta[i][0][2], LepLepId[i][0][2]) 
                  ZX_Lep4FR = getFakeRate(SSFR, year, True, LepPt[i][0][3], LepEta[i][0][3], LepLepId[i][0][3])
                  ZX_Weight.append(ZX_Norm * ZX_Lep3FR * ZX_Lep4FR)
                else:
                  ZX_Norm = 0
                  #ZX_Norm = Normalize_ZX(year, False, Z1Flav[i][0], Z2Flav[i][0]) 
                  ZX_Lep3FR = getFakeRate(OSFR, year, False, LepPt[i][0][2], LepEta[i][0][2], LepLepId[i][0][2]) 
                  ZX_Lep4FR = getFakeRate(OSFR, year, False, LepPt[i][0][3], LepEta[i][0][3], LepLepId[i][0][3])
                  ZX_Weight.append(ZX_Norm * ZX_Lep3FR * ZX_Lep4FR)
              else: ZX_Weight.append(0)
            return ZX_Weight
        # Filter out by mass THIS is not done for data like in ZX and DATA#
        if DoMassFilter:
          m4l = tree2array(tree=t,branches=["ZZMass"]).astype(float)
          for i in range(len(m4l)):
            if not (105<=m4l[i]<=140):
              scale[i] = 0
        #===================================Make an array of each event weight===========================================#

        # Need to add Z + X stuff here at some point #

        # Grab the cross section form the tree #
        new_xsec = update_xsec(name,tree2array(tree=t,branches=["xsec"]).astype(float)[0])
        #print ((tree2array(tree=t,branches=["Bin40"]).astype(float)[0]),np.sum(tree2array(tree=t,branches=["xsec"]).astype(float)[0]))

        # Check to update the cross_sections to match YR_4 report#

        #return tree2array(tree=t,branches=["overallEventWeight*genBR*(genxsec/xsec)*L1prefiringWeight/Bin40"]).astype(float) * scale * new_xsec * pb_to_fb
        #return tree2array(tree=t,branches=["xsec*overallEventWeight*L1prefiringWeight/Bin40"]).astype(float) * scale  * pb_to_fb
        #print tree2array(tree=t,branches=["Bin40"])[0][0],name
        return tree2array(tree=t,branches=["overallEventWeight*L1prefiringWeight/Bin40"]).astype(float) * new_xsec * scale  * pb_to_fb
        #return tree2array(tree=t,branches=["overallEventWeight/Bin40"]).astype(float) * new_xsec * scale  * pb_to_fb

def Calc_Event_Weight_2021_gammaH(event,name): #Tree input as t and the name of the tree should have all info included#
        doleptonSF=True
        pb_to_fb =1000
        #==============Calculate the event scale per event array===============================#
        scale = 1
        if doleptonSF:
          year = 0
          if "2016" in name:
            year = 2016
          elif "2017" in name:
            year = 2017
          elif "2018" in name:
            year = 2018

          LepLepId = event.LepLepId
          LepPt = event.LepPt
          LepEta = event.LepEta
          dataMCWeight = event.dataMCWeight
          LepScale = []
          # Load up the LeptonScale Factors#
          LepSF = init_LEPSF()
          LepScale = fixleptonscalefactor(int(year),LepLepId,LepPt,LepEta,dataMCWeight,LepSF)
          scale = scale * LepScale
        if any( x in ["ggH","VBF","ZH","WH","ttH","bbH","tqH","WplusH","WminusH","VBFbkg","TTZZ","ZZZ","WZZ","WWZ","TTWW","TTZJets_M10_MLM","TTZToLLNuNu_M10","TTZToLL_M1to10_MLM"] for x in name):
          scale = scale * 1.
        if "ggH" in name:
          ggH_NNLOPS_weight = event.ggH_NNLOPS_weight
          scale = scale * ggH_NNLOPS_weight
        elif "ggZZ" in name: #or self.isggZZoffshell:
          LepLepId = event.KFactor_QCD_ggZZ_Nominal
          scale = scale * event.KFactor_QCD_ggZZ_Nominal
        elif "qqZZ" in name:
            if "GEN" in name: #Must check this later #
              scale = scale * 1
            else:
              KFactor_EW_qqZZ = event.KFactor_EW_qqZZ
              KFactor_EW_qqZZ = event.KFactor_QCD_qqZZ_M
              scale = scale * KFactor_EW_qqZZ * KFactor_QCD_qqZZ_M
        elif "ZX" in name or "data" in name:
          if "data" in name:
            return 1
          elif "ZX" in name:
            LepLepId = event.LepLepId
            LepPt = event.LepPt
            LepEta = event.LepEta
            ZX_Weight = 0
            ZX_Norm = FakeRate.normalizeZX(self.year, self.usenewobjects, self.tree.Z1Flav, self.tree.Z2Flav)
            ZX_Lep2FR = ZX.getfakerate(self.year, self.usenewobjects, LepPt[2], LepEta[2], LepLepId[2])
            ZX_Lep3FR = ZX.getfakerate(self.year, self.usenewobjects, LepPt[3], LepEta[3], LepLepId[3])
            ZX_Weight.append(ZX_Norm * ZX_Lep2FR * ZX_Lep3FR)
            return ZX_Weight

        #===================================Make an array of each event weight===========================================#

        # Need to add Z + X stuff here at some point #

        # Grab the cross section form the tree #
        new_xsec = update_xsec(name,event.xsec)
        #print ((tree2array(tree=t,branches=["Bin40"]).astype(float)[0]),np.sum(tree2array(tree=t,branches=["xsec"]).astype(float)[0]))

        # Check to update the cross_sections to match YR_4 report#

        return event.overallEventWeight*event.L1prefiringWeight/event.Bin40 * new_xsec * scale  * pb_to_fb
