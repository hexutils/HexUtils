import numpy as np
import ROOT
from Discriminants import *
import gConstants

# This initializes discriminat splines for categorizations #
def init_spline():
  wkdir = "/afs/cern.ch/work/j/jejeffre/public/HEP_Ex_Tools/HepExUtils/OnShell_Utils/"
  D2jetZHSpline = ROOT.TFile(wkdir+"Discriminants/SmoothKDConstant_m4l_DjjZH13TeV.root").Get("sp_gr_varReco_Constant_Smooth")
  D2jetWHSpline = ROOT.TFile(wkdir+"Discriminants/SmoothKDConstant_m4l_DjjWH13TeV.root").Get("sp_gr_varReco_Constant_Smooth")
  D2jetVBFSpline = ROOT.TFile(wkdir+"Discriminants/SmoothKDConstant_m4l_DjjVBF13TeV.root").Get("sp_gr_varReco_Constant_Smooth")
  D1jetVBFSpline = ROOT.TFile(wkdir+"Discriminants/SmoothKDConstant_m4l_DjVBF13TeV.root").Get("sp_gr_varReco_Constant_Smooth")
  DbkgkinSpline4e = ROOT.TFile(wkdir+"Discriminants/SmoothKDConstant_m4l_Dbkgkin_4e13TeV.root").Get("sp_gr_varReco_Constant_Smooth")
  DbkgkinSpline4mu = ROOT.TFile(wkdir+"Discriminants/SmoothKDConstant_m4l_Dbkgkin_4mu13TeV.root").Get("sp_gr_varReco_Constant_Smooth")
  DbkgkinSpline2e2mu = ROOT.TFile(wkdir+"Discriminants/SmoothKDConstant_m4l_Dbkgkin_2e2mu13TeV.root").Get("sp_gr_varReco_Constant_Smooth")
  DbkgjjEWQCDSpline4lHadVH = ROOT.TFile(wkdir+"Discriminants/SmoothKDConstant_m4l_DbkgjjEWQCD_4l_HadVHTagged_13TeV.root").Get("sp_gr_varReco_Constant_Smooth")
  DbkgjjEWQCDSpline2l2lHadVH = ROOT.TFile(wkdir+"Discriminants/SmoothKDConstant_m4l_DbkgjjEWQCD_2l2l_HadVHTagged_13TeV.root").Get("sp_gr_varReco_Constant_Smooth")
  DbkgjjEWQCDSpline4lJJVBF = ROOT.TFile(wkdir+"Discriminants/SmoothKDConstant_m4l_DbkgjjEWQCD_4l_JJVBFTagged_13TeV.root").Get("sp_gr_varReco_Constant_Smooth")
  DbkgjjEWQCDSpline2l2lJJVBF = ROOT.TFile(wkdir+"Discriminants/SmoothKDConstant_m4l_DbkgjjEWQCD_2l2l_JJVBFTagged_13TeV.root").Get("sp_gr_varReco_Constant_Smooth")
  array_splines=[D2jetZHSpline,D2jetWHSpline,D2jetVBFSpline,D1jetVBFSpline,DbkgkinSpline4e,DbkgkinSpline4mu,DbkgkinSpline2e2mu,DbkgjjEWQCDSpline4lHadVH,DbkgjjEWQCDSpline2l2lHadVH,DbkgjjEWQCDSpline4lJJVBF,DbkgjjEWQCDSpline2l2lJJVBF]
  return array_splines

def Tag_MOR18( nExtraLep,  nExtraZ,  nCleanedJetsPt30,  nCleanedJetsPt30BTagged_bTagSF,  jetQGLikelihood, p_JJQCD_SIG_ghg2_1_JHUGen_JECNominal,  p_JQCD_SIG_ghg2_1_JHUGen_JECNominal,  p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal,  p_JVBF_SIG_ghv1_1_JHUGen_JECNominal,  pAux_JVBF_SIG_ghv1_1_JHUGen_JECNominal,  p_HadWH_SIG_ghw1_1_JHUGen_JECNominal,  p_HadZH_SIG_ghz1_1_JHUGen_JECNominal,  p_HadWH_mavjj_JECNominal,  p_HadWH_mavjj_true_JECNominal,  p_HadZH_mavjj_JECNominal,  p_HadZH_mavjj_true_JECNominal,  jetPhi,  ZZMass,  ZZPt,  PFMET,  useVHMETTagged,  useQGTagging , spline_list):

  # Load all of the spline names from the given init spline # 
 
  DZHhSpline=spline_list[0]
  DWHhSpline=spline_list[1]
  DVBF2jetSpline=spline_list[2]
  DVBF1jetSpline=spline_list[3]
  DbkgkinSpline4e=spline_list[4]
  DbkgkinSpline4mu=spline_list[5]
  DbkgkinSpline2e2mu=spline_list[6]
  DbkgjjEWQCDSpline4lHadVH=spline_list[7]
  DbkgjjEWQCDSpline2l2lHadVH=spline_list[8]
  DbkgjjEWQCDSpline4lJJVBF=spline_list[9]
  DbkgjjEWQCDSpline2l2lJJVBF=spline_list[10]


  # Num for each category #
  Untagged      = 0
  VBF1jTagged   = 1
  VBF2jTagged   = 2
  VHLeptTagged  = 3
  VHHadrTagged  = 4
  ttHLeptTagged = 5
  ttHHadrTagged = 6
  VHMETTagged   = 7
  Boosted       = 8
  gammaHTagged  = 9
  Failed = -999
  
  D_VBF2j = -2
  D_VBF1j = -2
  D_WHh   = -2
  D_ZHh   = -2
 
  if(useQGTagging):
    if(nCleanedJetsPt30==1):
      D_VBF1j = DVBF1j_ME_QG(p_JVBF_SIG_ghv1_1_JHUGen_JECNominal, pAux_JVBF_SIG_ghv1_1_JHUGen_JECNominal, p_JQCD_SIG_ghg2_1_JHUGen_JECNominal, ZZMass, jetQGLikelihood, jetPhi)
    elif(nCleanedJetsPt30>=2):
      D_VBF2j = DVBF2j_ME_QG(p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal, p_JJQCD_SIG_ghg2_1_JHUGen_JECNominal, ZZMass, jetQGLikelihood, jetPhi)
      D_WHh   = DWHh_ME_QG(p_HadWH_SIG_ghw1_1_JHUGen_JECNominal, p_JJQCD_SIG_ghg2_1_JHUGen_JECNominal, p_HadWH_mavjj_JECNominal, p_HadWH_mavjj_true_JECNominal, ZZMass, jetQGLikelihood, jetPhi)
      D_ZHh   = DZHh_ME_QG(p_HadZH_SIG_ghz1_1_JHUGen_JECNominal, p_JJQCD_SIG_ghg2_1_JHUGen_JECNominal, p_HadZH_mavjj_JECNominal, p_HadZH_mavjj_true_JECNominal, ZZMass, jetQGLikelihood, jetPhi)
    
  else:
    if(nCleanedJetsPt30==1):
      D_VBF1j = DVBF1j_ME(p_JVBF_SIG_ghv1_1_JHUGen_JECNominal, pAux_JVBF_SIG_ghv1_1_JHUGen_JECNominal, p_JQCD_SIG_ghg2_1_JHUGen_JECNominal, ZZMass, DVBF1jetSpline)
    elif(nCleanedJetsPt30>=2):
      D_VBF2j = DVBF2j_ME(p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal, p_JJQCD_SIG_ghg2_1_JHUGen_JECNominal, ZZMass, DVBF2jetSpline)
      D_WHh   = DWHh_ME(p_HadWH_SIG_ghw1_1_JHUGen_JECNominal, p_JJQCD_SIG_ghg2_1_JHUGen_JECNominal, p_HadWH_mavjj_JECNominal, p_HadWH_mavjj_true_JECNominal, ZZMass, DWHhSpline)
      D_ZHh   = DZHh_ME(p_HadZH_SIG_ghz1_1_JHUGen_JECNominal, p_JJQCD_SIG_ghg2_1_JHUGen_JECNominal, p_HadZH_mavjj_JECNominal, p_HadZH_mavjj_true_JECNominal, ZZMass, DZHhSpline)

  WP_VBF2j = getDVBF2jetsWP(ZZMass, useQGTagging)
  WP_VBF1j = getDVBF1jetWP(ZZMass, useQGTagging)
  WP_WHh = getDWHhWP(ZZMass, useQGTagging)
  WP_ZHh = getDZHhWP(ZZMass, useQGTagging)
  
  if( nExtraLep==0 and (((nCleanedJetsPt30==2 or nCleanedJetsPt30==3) and nCleanedJetsPt30BTagged_bTagSF<=1) or (nCleanedJetsPt30>=4 and nCleanedJetsPt30BTagged_bTagSF==0)) and D_VBF2j>WP_VBF2j ):
    return VBF2jTagged

  elif( nExtraLep==0 and (nCleanedJetsPt30==2 or nCleanedJetsPt30==3 or (nCleanedJetsPt30>=4 and nCleanedJetsPt30BTagged_bTagSF==0)) and (D_WHh>WP_WHh or D_ZHh>WP_ZHh)):

    return VHHadrTagged

  elif( (nCleanedJetsPt30<=3 and nCleanedJetsPt30BTagged_bTagSF==0 and (nExtraLep==1 or nExtraZ>=1)) or  ( nCleanedJetsPt30==0 and nExtraLep>=1 )):

    return VHLeptTagged

  elif( nCleanedJetsPt30>=4 and nCleanedJetsPt30BTagged_bTagSF>=1 and nExtraLep ==0):

    return ttHHadrTagged
  
  elif( nExtraLep>=1 ):
  
    return ttHLeptTagged
	
  elif( useVHMETTagged and nExtraLep==0 and (nCleanedJetsPt30==0 or nCleanedJetsPt30==1) and PFMET>100 ):

    return VHMETTagged

  elif(nExtraLep==0 and nCleanedJetsPt30==1 and D_VBF1j>WP_VBF1j):
    
    return VBF1jTagged
  
  else:
   
    return Untagged

def Tag_AC_19_Scheme_1( nExtraLep,  nExtraZ,  nCleanedJetsPt30,  nCleanedJetsPt30BTagged_bTagSF,  jetQGLikelihood, p_JJQCD_SIG_ghg2_1_JHUGen_JECNominal,  p_JQCD_SIG_ghg2_1_JHUGen_JECNominal,  p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal,  p_JVBF_SIG_ghv1_1_JHUGen_JECNominal,  pAux_JVBF_SIG_ghv1_1_JHUGen_JECNominal,  p_HadWH_SIG_ghw1_1_JHUGen_JECNominal,  p_HadZH_SIG_ghz1_1_JHUGen_JECNominal,  p_HadWH_mavjj_JECNominal,  p_HadWH_mavjj_true_JECNominal,  p_HadZH_mavjj_JECNominal,  p_HadZH_mavjj_true_JECNominal,  jetPhi,  ZZMass,  ZZPt,  PFMET,  PhotonIsCutBasedLooseID, PhotonPt, useVHMETTagged,  useQGTagging , spline_list):

  Untagged      = 0
  VBF1jTagged   = 1
  VBF2jTagged   = 2
  VHLeptTagged  = 3
  VHHadrTagged  = 4
  ttHLeptTagged = 5
  ttHHadrTagged = 6
  VHMETTagged   = 7
  Boosted       = 8
  gammaHTagged  = 9
  Failed = -999

  # Apply Hard Gamma H Cut befor everything #

  Photon_Pt_Cut=400
  
  if(len(PhotonIsCutBasedLooseID)!=0 and PhotonPt[0]>Photon_Pt_Cut):
    return gammaHTagged

  c = Tag_MOR18( nExtraLep,  nExtraZ,  nCleanedJetsPt30,  nCleanedJetsPt30BTagged_bTagSF,  jetQGLikelihood, p_JJQCD_SIG_ghg2_1_JHUGen_JECNominal,  p_JQCD_SIG_ghg2_1_JHUGen_JECNominal,  p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal,  p_JVBF_SIG_ghv1_1_JHUGen_JECNominal,  pAux_JVBF_SIG_ghv1_1_JHUGen_JECNominal,  p_HadWH_SIG_ghw1_1_JHUGen_JECNominal,  p_HadZH_SIG_ghz1_1_JHUGen_JECNominal,  p_HadWH_mavjj_JECNominal,  p_HadWH_mavjj_true_JECNominal,  p_HadZH_mavjj_JECNominal,  p_HadZH_mavjj_true_JECNominal,  jetPhi,  ZZMass,  ZZPt,  PFMET, useVHMETTagged,  useQGTagging , spline_list)

  # Scheme 1 does not have a boosted category
  
  #if (c==VBF2jTagged or c==VHHadrTagged or c==VBF1jTagged or c==VHLeptTagged or c==ttHLeptTagged or c==ttHHadrTagged):
  #  return c 
  #elif (c==Untagged or c==VHMETTagged):
  #  if (ZZPt > 120):
  #    return Boosted
  
  return c
  
def Tag_AC_19_Scheme_2( nExtraLep,  nExtraZ,  nCleanedJetsPt30,  nCleanedJetsPt30BTagged_bTagSF,  jetQGLikelihood, p_JJQCD_SIG_ghg2_1_JHUGen_JECNominal,  p_JQCD_SIG_ghg2_1_JHUGen_JECNominal,  p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal, p_JJVBF_SIG_ghv2_1_JHUGen_JECNominal, p_JJVBF_SIG_ghv4_1_JHUGen_JECNominal, p_JJVBF_SIG_ghv1prime2_1E4_JHUGen_JECNominal, p_JJVBF_SIG_ghza1prime2_1E4_JHUGen_JECNominal, p_JVBF_SIG_ghv1_1_JHUGen_JECNominal, pAux_JVBF_SIG_ghv1_1_JHUGen_JECNominal,  p_HadWH_SIG_ghw1_1_JHUGen_JECNominal,  p_HadWH_SIG_ghw2_1_JHUGen_JECNominal,  p_HadWH_SIG_ghw4_1_JHUGen_JECNominal,  p_HadWH_SIG_ghw1prime2_1E4_JHUGen_JECNominal,  p_HadZH_SIG_ghz1_1_JHUGen_JECNominal,  p_HadZH_SIG_ghz2_1_JHUGen_JECNominal,   p_HadZH_SIG_ghz4_1_JHUGen_JECNominal,   p_HadZH_SIG_ghz1prime2_1E4_JHUGen_JECNominal,  p_HadZH_SIG_ghza1prime2_1E4_JHUGen_JECNominal, p_HadWH_mavjj_JECNominal,  p_HadWH_mavjj_true_JECNominal,  p_HadZH_mavjj_JECNominal,  p_HadZH_mavjj_true_JECNominal,  jetPhi,  ZZMass,  ZZPt,  PFMET,  PhotonIsCutBasedLooseID, PhotonPt, useVHMETTagged,  useQGTagging , spline_list, gConstant_list, conventions):

  ## The only thing different about this and scheme 1 is that ttH are added to Untagged ##
  
  Untagged      = 0
  VBF1jTagged   = 1
  VBF2jTagged   = 2
  VHLeptTagged  = 3
  VHHadrTagged  = 4
  ttHLeptTagged = 5
  ttHHadrTagged = 6
  VHMETTagged   = 7
  Boosted       = 8
  gammaHTagged  = 9
  Failed = -999

  # Apply Hard Gamma H Cut before everything #

  #Photon_Pt_Cut=400

  #if(len(PhotonIsCutBasedLooseID)!=0 and PhotonPt[0]>Photon_Pt_Cut):
  #  return gammaHTagged
  
  # Make Alternative Discriminants #
  # g2 
  p_JJVBF_SIG_ghv2_1_JHUGen_JECNominal = p_JJVBF_SIG_ghv2_1_JHUGen_JECNominal * gConstants.getvalue("g2","VBF",ZZMass,gConstant_list)**2 
  p_HadZH_SIG_ghz2_1_JHUGen_JECNominal = p_HadZH_SIG_ghz2_1_JHUGen_JECNominal * gConstants.getvalue("g2","ZH",ZZMass,gConstant_list)**2
  p_HadWH_SIG_ghw2_1_JHUGen_JECNominal = p_HadWH_SIG_ghw2_1_JHUGen_JECNominal * gConstants.getvalue("g2","WH",ZZMass,gConstant_list)**2
  # g1prime2 
  p_JJVBF_SIG_ghv1prime2_1E4_JHUGen_JECNominal = p_JJVBF_SIG_ghv1prime2_1E4_JHUGen_JECNominal * (gConstants.getvalue("L1","VBF",ZZMass,gConstant_list)/10000)**2 
  p_HadZH_SIG_ghz1prime2_1E4_JHUGen_JECNominal = p_HadZH_SIG_ghz1prime2_1E4_JHUGen_JECNominal * (gConstants.getvalue("L1","ZH",ZZMass,gConstant_list)/10000)**2 
  p_HadWH_SIG_ghw1prime2_1E4_JHUGen_JECNominal = p_HadWH_SIG_ghw1prime2_1E4_JHUGen_JECNominal * (gConstants.getvalue("L1","WH",ZZMass,gConstant_list)/10000)**2 
  # ghzgsprime1 
  p_JJVBF_SIG_ghza1prime2_1E4_JHUGen_JECNominal = p_JJVBF_SIG_ghza1prime2_1E4_JHUGen_JECNominal * (gConstants.getvalue("L1Zgs","VBF",ZZMass,gConstant_list)/10000)**2 
  p_HadZH_SIG_ghza1prime2_1E4_JHUGen_JECNominal = p_HadZH_SIG_ghza1prime2_1E4_JHUGen_JECNominal * (gConstants.getvalue("L1Zgs","ZH",ZZMass,gConstant_list)/10000)**2 
  p_HadWH_SIG_ghza1prime2_1E4_JHUGen_JECNominal = 0
  # g4 
  p_JJVBF_SIG_ghv4_1_JHUGen_JECNominal = p_JJVBF_SIG_ghv4_1_JHUGen_JECNominal * gConstants.getvalue("g4","VBF",ZZMass,gConstant_list)**2 
  p_HadZH_SIG_ghz4_1_JHUGen_JECNominal = p_HadZH_SIG_ghz4_1_JHUGen_JECNominal * gConstants.getvalue("g4","ZH",ZZMass,gConstant_list)**2 
  p_HadWH_SIG_ghw4_1_JHUGen_JECNominal = p_HadWH_SIG_ghw4_1_JHUGen_JECNominal * gConstants.getvalue("g4","WH",ZZMass,gConstant_list)**2 

  c_g1 = Tag_MOR18( nExtraLep,  nExtraZ,  nCleanedJetsPt30,  nCleanedJetsPt30BTagged_bTagSF,  jetQGLikelihood, p_JJQCD_SIG_ghg2_1_JHUGen_JECNominal,  p_JQCD_SIG_ghg2_1_JHUGen_JECNominal,  p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal,  p_JVBF_SIG_ghv1_1_JHUGen_JECNominal,  pAux_JVBF_SIG_ghv1_1_JHUGen_JECNominal,  p_HadWH_SIG_ghw1_1_JHUGen_JECNominal,  p_HadZH_SIG_ghz1_1_JHUGen_JECNominal,  p_HadWH_mavjj_JECNominal,  p_HadWH_mavjj_true_JECNominal,  p_HadZH_mavjj_JECNominal,  p_HadZH_mavjj_true_JECNominal,  jetPhi,  ZZMass,  ZZPt,  PFMET, useVHMETTagged,  useQGTagging , spline_list)

  c_g2 = Tag_MOR18( nExtraLep,  nExtraZ,  nCleanedJetsPt30,  nCleanedJetsPt30BTagged_bTagSF,  jetQGLikelihood, p_JJQCD_SIG_ghg2_1_JHUGen_JECNominal,  p_JQCD_SIG_ghg2_1_JHUGen_JECNominal,  p_JJVBF_SIG_ghv2_1_JHUGen_JECNominal,  p_JVBF_SIG_ghv1_1_JHUGen_JECNominal,  pAux_JVBF_SIG_ghv1_1_JHUGen_JECNominal,  p_HadWH_SIG_ghw2_1_JHUGen_JECNominal,  p_HadZH_SIG_ghz2_1_JHUGen_JECNominal,  p_HadWH_mavjj_JECNominal,  p_HadWH_mavjj_true_JECNominal,  p_HadZH_mavjj_JECNominal,  p_HadZH_mavjj_true_JECNominal,  jetPhi,  ZZMass,  ZZPt,  PFMET, useVHMETTagged,  useQGTagging , spline_list)

  c_g4 = Tag_MOR18( nExtraLep,  nExtraZ,  nCleanedJetsPt30,  nCleanedJetsPt30BTagged_bTagSF,  jetQGLikelihood, p_JJQCD_SIG_ghg2_1_JHUGen_JECNominal,  p_JQCD_SIG_ghg2_1_JHUGen_JECNominal,  p_JJVBF_SIG_ghv4_1_JHUGen_JECNominal,  p_JVBF_SIG_ghv1_1_JHUGen_JECNominal,  pAux_JVBF_SIG_ghv1_1_JHUGen_JECNominal,  p_HadWH_SIG_ghw4_1_JHUGen_JECNominal,  p_HadZH_SIG_ghz4_1_JHUGen_JECNominal,  p_HadWH_mavjj_JECNominal,  p_HadWH_mavjj_true_JECNominal,  p_HadZH_mavjj_JECNominal,  p_HadZH_mavjj_true_JECNominal,  jetPhi,  ZZMass,  ZZPt,  PFMET, useVHMETTagged,  useQGTagging , spline_list)

  c_g1prime2 = Tag_MOR18( nExtraLep,  nExtraZ,  nCleanedJetsPt30,  nCleanedJetsPt30BTagged_bTagSF,  jetQGLikelihood, p_JJQCD_SIG_ghg2_1_JHUGen_JECNominal,  p_JQCD_SIG_ghg2_1_JHUGen_JECNominal,  p_JJVBF_SIG_ghv1prime2_1E4_JHUGen_JECNominal,  p_JVBF_SIG_ghv1_1_JHUGen_JECNominal,  pAux_JVBF_SIG_ghv1_1_JHUGen_JECNominal,  p_HadWH_SIG_ghw1prime2_1E4_JHUGen_JECNominal,  p_HadZH_SIG_ghz1prime2_1E4_JHUGen_JECNominal,  p_HadWH_mavjj_JECNominal,  p_HadWH_mavjj_true_JECNominal,  p_HadZH_mavjj_JECNominal,  p_HadZH_mavjj_true_JECNominal,  jetPhi,  ZZMass,  ZZPt,  PFMET, useVHMETTagged,  useQGTagging , spline_list)

  c_ghza1prime2 = Tag_MOR18( nExtraLep,  nExtraZ,  nCleanedJetsPt30,  nCleanedJetsPt30BTagged_bTagSF,  jetQGLikelihood, p_JJQCD_SIG_ghg2_1_JHUGen_JECNominal,  p_JQCD_SIG_ghg2_1_JHUGen_JECNominal,  p_JJVBF_SIG_ghza1prime2_1E4_JHUGen_JECNominal,  p_JVBF_SIG_ghv1_1_JHUGen_JECNominal,  pAux_JVBF_SIG_ghv1_1_JHUGen_JECNominal,  p_HadWH_SIG_ghza1prime2_1E4_JHUGen_JECNominal,  p_HadZH_SIG_ghza1prime2_1E4_JHUGen_JECNominal,  p_HadWH_mavjj_JECNominal,  p_HadWH_mavjj_true_JECNominal,  p_HadZH_mavjj_JECNominal,  p_HadZH_mavjj_true_JECNominal,  jetPhi,  ZZMass,  ZZPt,  PFMET, useVHMETTagged,  useQGTagging , spline_list)
  
  categories = [c_g1,c_g2,c_g4,c_g1prime2,c_ghza1prime2]

  if (VBF2jTagged in categories):
    return VBF2jTagged
  if (VHHadrTagged in categories):
    return VHHadrTagged
  c = c_g1
  # Add ttH to the Untagged Category #
  if (c==ttHLeptTagged or c==ttHHadrTagged):
    return Untagged
  elif (c==VBF2jTagged or c==VHHadrTagged or c==VBF1jTagged or c==VHLeptTagged):
    return c
  elif (c==Untagged or c==VHMETTagged):
    if (ZZPt > 120): 
      return Boosted
  return c
  
