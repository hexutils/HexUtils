import numpy as np
import ROOT
from .Discriminants import *
from ..data import gConstants as gConstants

def Protect_Category_Against_NAN(pConst_JJVBF_S_SIG_ghv1_1_MCFM_JECNominal,
				 pConst_HadZH_S_SIG_ghz1_1_MCFM_JECNominal,
				 pConst_HadWH_S_SIG_ghw1_1_MCFM_JECNominal,
				 pConst_JJVBF_BKG_MCFM_JECNominal,
				 pConst_HadZH_BKG_MCFM_JECNominal,
				 pConst_HadWH_BKG_MCFM_JECNominal,
				 pConst_JJQCD_BKG_MCFM_JECNominal,
				 p_HadZH_mavjj_true_JECNominal,
				 p_HadWH_mavjj_true_JECNominal,
				 p_JVBF_SIG_ghv1_1_JHUGen_JECNominal,
				 pAux_JVBF_SIG_ghv1_1_JHUGen_JECNominal,
				 p_HadWH_mavjj_JECNominal,
				 p_HadWH_SIG_ghw1_1_JHUGen_JECNominal,
				 p_HadZH_mavjj_JECNominal,
				 p_HadZH_SIG_ghz1_1_JHUGen_JECNominal):

  # This function returns true if one of the variables to be passed to the tagging funcion would cause it to return NaN and error out #

  # Signal VBF variables that will fail
  if pConst_JJVBF_S_SIG_ghv1_1_MCFM_JECNominal * pConst_HadZH_S_SIG_ghz1_1_MCFM_JECNominal * pConst_HadWH_S_SIG_ghw1_1_MCFM_JECNominal == 0:
    return True 
  # Bkg VBF variables that will fail
  elif pConst_JJVBF_BKG_MCFM_JECNominal * pConst_HadZH_BKG_MCFM_JECNominal * pConst_HadWH_BKG_MCFM_JECNominal * pConst_JJQCD_BKG_MCFM_JECNominal == 0:
    return True
  # QCD Scale variables that will fail #
  elif p_HadZH_mavjj_true_JECNominal * p_HadWH_mavjj_true_JECNominal == 0:
    return True
  # VBF 1 Jet and VBF 2 jet variables that will fail #
  elif p_JVBF_SIG_ghv1_1_JHUGen_JECNominal * pAux_JVBF_SIG_ghv1_1_JHUGen_JECNominal == 0:
    return True
  # WH and Vh variables that will fail #
  elif p_HadWH_mavjj_JECNominal * p_HadWH_SIG_ghw1_1_JHUGen_JECNominal * p_HadZH_mavjj_JECNominal * p_HadZH_SIG_ghz1_1_JHUGen_JECNominal == 0:
    return True
  else:
    return False
# Here we add the tagging functions #

def Tag_MOR18(  nExtraLep,  
	        nExtraZ,
		nCleanedJetsPt30,
		nCleanedJetsPt30BTagged_bTagSF,
		jetQGLikelihood, 
		p_JJQCD_SIG_ghg2_1_JHUGen_JECNominal,  
		p_JQCD_SIG_ghg2_1_JHUGen_JECNominal,  
		p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal,  
		p_JVBF_SIG_ghv1_1_JHUGen_JECNominal,  
		pAux_JVBF_SIG_ghv1_1_JHUGen_JECNominal,  
		p_HadWH_SIG_ghw1_1_JHUGen_JECNominal,  
		p_HadZH_SIG_ghz1_1_JHUGen_JECNominal,  
		p_HadWH_mavjj_JECNominal,  
		p_HadWH_mavjj_true_JECNominal,  
		p_HadZH_mavjj_JECNominal,  
		p_HadZH_mavjj_true_JECNominal,  
		jetPhi,  
		ZZMass,  
		ZZPt,  
		PFMET,  
		useVHMETTagged,  
		useQGTagging , 
		cConstants_list):

  # Moriond 2018 Categorization Algorithm # 

  # Load all of the spline names from the given init spline # 
 
  DZHhSpline=cConstants_list["D2jetZHSpline"]
  DWHhSpline=cConstants_list["D2jetWHSpline"]
  DVBF2jetSpline=cConstants_list["D2jetVBFSpline"]
  DVBF1jetSpline=cConstants_list["D1jetVBFSpline"]
  DbkgkinSpline4e=cConstants_list["DbkgkinSpline4e"]
  DbkgkinSpline4mu=cConstants_list["DbkgkinSpline4mu"]
  DbkgkinSpline2e2mu=cConstants_list["DbkgkinSpline2e2mu"]
  DbkgjjEWQCDSpline4lHadVH=cConstants_list["DbkgjjEWQCDSpline4lHadVH"]
  DbkgjjEWQCDSpline2l2lHadVH=cConstants_list["DbkgjjEWQCDSpline2l2lHadVH"]
  DbkgjjEWQCDSpline4lJJVBF=cConstants_list["DbkgjjEWQCDSpline4lJJVBF"]
  DbkgjjEWQCDSpline2l2lJJVBF=cConstants_list["DbkgjjEWQCDSpline2l2lJJVBF"]


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
  Failed = -999
  
  D_VBF2j = -2
  D_VBF1j = -2
  D_WHh   = -2
  D_ZHh   = -2
 
  if(useQGTagging):
    if(nCleanedJetsPt30==1):
      D_VBF1j = DVBF1j_ME_QG(p_JVBF_SIG_ghv1_1_JHUGen_JECNominal, pAux_JVBF_SIG_ghv1_1_JHUGen_JECNominal, p_JQCD_SIG_ghg2_1_JHUGen_JECNominal, ZZMass, jetQGLikelihood, jetPhi, cConstants_list)
    elif(nCleanedJetsPt30>=2):
      D_VBF2j = DVBF2j_ME_QG(p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal, p_JJQCD_SIG_ghg2_1_JHUGen_JECNominal, ZZMass, jetQGLikelihood, jetPhi, cConstants_list)
      D_WHh   = DWHh_ME_QG(p_HadWH_SIG_ghw1_1_JHUGen_JECNominal, p_JJQCD_SIG_ghg2_1_JHUGen_JECNominal, p_HadWH_mavjj_JECNominal, p_HadWH_mavjj_true_JECNominal, ZZMass, jetQGLikelihood, jetPhi, cConstants_list)
      D_ZHh   = DZHh_ME_QG(p_HadZH_SIG_ghz1_1_JHUGen_JECNominal, p_JJQCD_SIG_ghg2_1_JHUGen_JECNominal, p_HadZH_mavjj_JECNominal, p_HadZH_mavjj_true_JECNominal, ZZMass, jetQGLikelihood, jetPhi, cConstants_list)
    
  else:
    if(nCleanedJetsPt30==1):
      D_VBF1j = DVBF1j_ME(p_JVBF_SIG_ghv1_1_JHUGen_JECNominal, pAux_JVBF_SIG_ghv1_1_JHUGen_JECNominal, p_JQCD_SIG_ghg2_1_JHUGen_JECNominal, ZZMass, cConstants_list)
    elif(nCleanedJetsPt30>=2):
      D_VBF2j = DVBF2j_ME(p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal, p_JJQCD_SIG_ghg2_1_JHUGen_JECNominal, ZZMass, cConstants_list)
      D_WHh   = DWHh_ME(p_HadWH_SIG_ghw1_1_JHUGen_JECNominal, p_JJQCD_SIG_ghg2_1_JHUGen_JECNominal, p_HadWH_mavjj_JECNominal, p_HadWH_mavjj_true_JECNominal, ZZMass, cConstants_list)
      D_ZHh   = DZHh_ME(p_HadZH_SIG_ghz1_1_JHUGen_JECNominal, p_JJQCD_SIG_ghg2_1_JHUGen_JECNominal, p_HadZH_mavjj_JECNominal, p_HadZH_mavjj_true_JECNominal, ZZMass, cConstants_list)

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

def Tag_AC_19_Scheme_1( nExtraLep,
			nExtraZ,  
			nCleanedJetsPt30,  
			nCleanedJetsPt30BTagged_bTagSF,  
			jetQGLikelihood, 
			p_JJQCD_SIG_ghg2_1_JHUGen_JECNominal,  
			p_JQCD_SIG_ghg2_1_JHUGen_JECNominal,  
			p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal,  
			p_JVBF_SIG_ghv1_1_JHUGen_JECNominal,  
			pAux_JVBF_SIG_ghv1_1_JHUGen_JECNominal,  
			p_HadWH_SIG_ghw1_1_JHUGen_JECNominal,  
			p_HadZH_SIG_ghz1_1_JHUGen_JECNominal,  
			p_HadWH_mavjj_JECNominal,  
			p_HadWH_mavjj_true_JECNominal,  
			p_HadZH_mavjj_JECNominal,  
			p_HadZH_mavjj_true_JECNominal,  
			jetPhi,  
			ZZMass,  
			ZZPt,  
			PFMET,  
			PhotonIsCutBasedLooseID, 
			PhotonPt, 
			useVHMETTagged,  
			useQGTagging , 
			cConstant_list):

  #Higgs 19-009 Categorization Scheme 1, Not Complete/Exactly as described in paper #

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

  c = Tag_MOR18( nExtraLep,  nExtraZ,  nCleanedJetsPt30,  nCleanedJetsPt30BTagged_bTagSF,  jetQGLikelihood, p_JJQCD_SIG_ghg2_1_JHUGen_JECNominal,  p_JQCD_SIG_ghg2_1_JHUGen_JECNominal,  p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal,  p_JVBF_SIG_ghv1_1_JHUGen_JECNominal,  pAux_JVBF_SIG_ghv1_1_JHUGen_JECNominal,  p_HadWH_SIG_ghw1_1_JHUGen_JECNominal,  p_HadZH_SIG_ghz1_1_JHUGen_JECNominal,  p_HadWH_mavjj_JECNominal,  p_HadWH_mavjj_true_JECNominal,  p_HadZH_mavjj_JECNominal,  p_HadZH_mavjj_true_JECNominal,  jetPhi,  ZZMass,  ZZPt,  PFMET, useVHMETTagged,  useQGTagging , cConstant_list)

  # Scheme 1 does not have a boosted category
  
  return c
  
def Tag_AC_19_Scheme_2( nExtraLep,
			nExtraZ,  
			nCleanedJetsPt30,  
			nCleanedJetsPt30BTagged_bTagSF,  
			jetQGLikelihood, 
			p_JJQCD_SIG_ghg2_1_JHUGen_JECNominal,  
			p_JQCD_SIG_ghg2_1_JHUGen_JECNominal,  
			p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal, 
			p_JJVBF_SIG_ghv2_1_JHUGen_JECNominal, 
			p_JJVBF_SIG_ghv4_1_JHUGen_JECNominal,
			p_JJVBF_SIG_ghv1prime2_1E4_JHUGen_JECNominal, 
			p_JJVBF_SIG_ghza1prime2_1E4_JHUGen_JECNominal, 
			p_JVBF_SIG_ghv1_1_JHUGen_JECNominal, 
			pAux_JVBF_SIG_ghv1_1_JHUGen_JECNominal,  
			p_HadWH_SIG_ghw1_1_JHUGen_JECNominal,  
			p_HadWH_SIG_ghw2_1_JHUGen_JECNominal,  
			p_HadWH_SIG_ghw4_1_JHUGen_JECNominal,  
			p_HadWH_SIG_ghw1prime2_1E4_JHUGen_JECNominal,  
			p_HadZH_SIG_ghz1_1_JHUGen_JECNominal,  
			p_HadZH_SIG_ghz2_1_JHUGen_JECNominal,   
			p_HadZH_SIG_ghz4_1_JHUGen_JECNominal,   
			p_HadZH_SIG_ghz1prime2_1E4_JHUGen_JECNominal,  
			p_HadZH_SIG_ghza1prime2_1E4_JHUGen_JECNominal, 
			p_HadWH_mavjj_JECNominal,  
			p_HadWH_mavjj_true_JECNominal,  
			p_HadZH_mavjj_JECNominal, 
		 	p_HadZH_mavjj_true_JECNominal,  
			jetPhi,  
			ZZMass,  
			ZZPt,  
			PFMET,  
			PhotonIsCutBasedLooseID, 
			PhotonPt, 
			useVHMETTagged,  
			useQGTagging , 	
			cConstant_list, 
			gConstant_list):

  ## This is the scheme used for the HIG-19-009 analysis scheme 2
  
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
  p_JJVBF_SIG_ghza1prime2_1E4_JHUGen_JECNominal = p_JJVBF_SIG_ghza1prime2_1E4_JHUGen_JECNominal * (gConstants.getvalue("L1Zg","VBF",ZZMass,gConstant_list)/10000)**2 
  p_HadZH_SIG_ghza1prime2_1E4_JHUGen_JECNominal = p_HadZH_SIG_ghza1prime2_1E4_JHUGen_JECNominal * (gConstants.getvalue("L1Zg","ZH",ZZMass,gConstant_list)/10000)**2 
  p_HadWH_SIG_ghza1prime2_1E4_JHUGen_JECNominal = 0
  # g4 
  p_JJVBF_SIG_ghv4_1_JHUGen_JECNominal = p_JJVBF_SIG_ghv4_1_JHUGen_JECNominal * gConstants.getvalue("g4","VBF",ZZMass,gConstant_list)**2 
  p_HadZH_SIG_ghz4_1_JHUGen_JECNominal = p_HadZH_SIG_ghz4_1_JHUGen_JECNominal * gConstants.getvalue("g4","ZH",ZZMass,gConstant_list)**2 
  p_HadWH_SIG_ghw4_1_JHUGen_JECNominal = p_HadWH_SIG_ghw4_1_JHUGen_JECNominal * gConstants.getvalue("g4","WH",ZZMass,gConstant_list)**2 

  c_g1 = Tag_MOR18( nExtraLep,  nExtraZ,  nCleanedJetsPt30,  nCleanedJetsPt30BTagged_bTagSF,  jetQGLikelihood, p_JJQCD_SIG_ghg2_1_JHUGen_JECNominal,  p_JQCD_SIG_ghg2_1_JHUGen_JECNominal,  p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal,  p_JVBF_SIG_ghv1_1_JHUGen_JECNominal,  pAux_JVBF_SIG_ghv1_1_JHUGen_JECNominal,  p_HadWH_SIG_ghw1_1_JHUGen_JECNominal,  p_HadZH_SIG_ghz1_1_JHUGen_JECNominal,  p_HadWH_mavjj_JECNominal,  p_HadWH_mavjj_true_JECNominal,  p_HadZH_mavjj_JECNominal,  p_HadZH_mavjj_true_JECNominal,  jetPhi,  ZZMass,  ZZPt,  PFMET, useVHMETTagged,  useQGTagging , cConstant_list)

  c_g2 = Tag_MOR18( nExtraLep,  nExtraZ,  nCleanedJetsPt30,  nCleanedJetsPt30BTagged_bTagSF,  jetQGLikelihood, p_JJQCD_SIG_ghg2_1_JHUGen_JECNominal,  p_JQCD_SIG_ghg2_1_JHUGen_JECNominal,  p_JJVBF_SIG_ghv2_1_JHUGen_JECNominal,  p_JVBF_SIG_ghv1_1_JHUGen_JECNominal,  pAux_JVBF_SIG_ghv1_1_JHUGen_JECNominal,  p_HadWH_SIG_ghw2_1_JHUGen_JECNominal,  p_HadZH_SIG_ghz2_1_JHUGen_JECNominal,  p_HadWH_mavjj_JECNominal,  p_HadWH_mavjj_true_JECNominal,  p_HadZH_mavjj_JECNominal,  p_HadZH_mavjj_true_JECNominal,  jetPhi,  ZZMass,  ZZPt,  PFMET, useVHMETTagged,  useQGTagging , cConstant_list)

  c_g4 = Tag_MOR18( nExtraLep,  nExtraZ,  nCleanedJetsPt30,  nCleanedJetsPt30BTagged_bTagSF,  jetQGLikelihood, p_JJQCD_SIG_ghg2_1_JHUGen_JECNominal,  p_JQCD_SIG_ghg2_1_JHUGen_JECNominal,  p_JJVBF_SIG_ghv4_1_JHUGen_JECNominal,  p_JVBF_SIG_ghv1_1_JHUGen_JECNominal,  pAux_JVBF_SIG_ghv1_1_JHUGen_JECNominal,  p_HadWH_SIG_ghw4_1_JHUGen_JECNominal,  p_HadZH_SIG_ghz4_1_JHUGen_JECNominal,  p_HadWH_mavjj_JECNominal,  p_HadWH_mavjj_true_JECNominal,  p_HadZH_mavjj_JECNominal,  p_HadZH_mavjj_true_JECNominal,  jetPhi,  ZZMass,  ZZPt,  PFMET, useVHMETTagged,  useQGTagging , cConstant_list)

  c_g1prime2 = Tag_MOR18( nExtraLep,  nExtraZ,  nCleanedJetsPt30,  nCleanedJetsPt30BTagged_bTagSF,  jetQGLikelihood, p_JJQCD_SIG_ghg2_1_JHUGen_JECNominal,  p_JQCD_SIG_ghg2_1_JHUGen_JECNominal,  p_JJVBF_SIG_ghv1prime2_1E4_JHUGen_JECNominal,  p_JVBF_SIG_ghv1_1_JHUGen_JECNominal,  pAux_JVBF_SIG_ghv1_1_JHUGen_JECNominal,  p_HadWH_SIG_ghw1prime2_1E4_JHUGen_JECNominal,  p_HadZH_SIG_ghz1prime2_1E4_JHUGen_JECNominal,  p_HadWH_mavjj_JECNominal,  p_HadWH_mavjj_true_JECNominal,  p_HadZH_mavjj_JECNominal,  p_HadZH_mavjj_true_JECNominal,  jetPhi,  ZZMass,  ZZPt,  PFMET, useVHMETTagged,  useQGTagging , cConstant_list)

  c_ghza1prime2 = Tag_MOR18( nExtraLep,  nExtraZ,  nCleanedJetsPt30,  nCleanedJetsPt30BTagged_bTagSF,  jetQGLikelihood, p_JJQCD_SIG_ghg2_1_JHUGen_JECNominal,  p_JQCD_SIG_ghg2_1_JHUGen_JECNominal,  p_JJVBF_SIG_ghza1prime2_1E4_JHUGen_JECNominal,  p_JVBF_SIG_ghv1_1_JHUGen_JECNominal,  pAux_JVBF_SIG_ghv1_1_JHUGen_JECNominal,  p_HadWH_SIG_ghza1prime2_1E4_JHUGen_JECNominal,  p_HadZH_SIG_ghza1prime2_1E4_JHUGen_JECNominal,  p_HadWH_mavjj_JECNominal,  p_HadWH_mavjj_true_JECNominal,  p_HadZH_mavjj_JECNominal,  p_HadZH_mavjj_true_JECNominal,  jetPhi,  ZZMass,  ZZPt,  PFMET, useVHMETTagged,  useQGTagging , cConstant_list)
  
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
  
def Tag_AC_19_Scheme_2_gammaH( nExtraLep,  nExtraZ,  nCleanedJetsPt30,  nCleanedJetsPt30BTagged_bTagSF,  jetQGLikelihood, p_JJQCD_SIG_ghg2_1_JHUGen_JECNominal,  p_JQCD_SIG_ghg2_1_JHUGen_JECNominal,  p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal, p_JJVBF_SIG_ghv2_1_JHUGen_JECNominal, p_JJVBF_SIG_ghv4_1_JHUGen_JECNominal, p_JJVBF_SIG_ghv1prime2_1E4_JHUGen_JECNominal, p_JJVBF_SIG_ghza1prime2_1E4_JHUGen_JECNominal, p_JVBF_SIG_ghv1_1_JHUGen_JECNominal, pAux_JVBF_SIG_ghv1_1_JHUGen_JECNominal,  p_HadWH_SIG_ghw1_1_JHUGen_JECNominal,  p_HadWH_SIG_ghw2_1_JHUGen_JECNominal,  p_HadWH_SIG_ghw4_1_JHUGen_JECNominal,  p_HadWH_SIG_ghw1prime2_1E4_JHUGen_JECNominal,  p_HadZH_SIG_ghz1_1_JHUGen_JECNominal,  p_HadZH_SIG_ghz2_1_JHUGen_JECNominal,   p_HadZH_SIG_ghz4_1_JHUGen_JECNominal,   p_HadZH_SIG_ghz1prime2_1E4_JHUGen_JECNominal,  p_HadZH_SIG_ghza1prime2_1E4_JHUGen_JECNominal, p_HadWH_mavjj_JECNominal,  p_HadWH_mavjj_true_JECNominal,  p_HadZH_mavjj_JECNominal,  p_HadZH_mavjj_true_JECNominal,  jetPhi,  ZZMass,  ZZPt,  PFMET,  PhotonIsCutBasedLooseID, PhotonPt, useVHMETTagged,  useQGTagging , cConstant_list, gConstant_list):

  ## This is the scheme used for the HIG-19-009 analysis scheme 2 but with a gammaH category on top ##
  
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

  Photon_Pt_Cut=400

  if(len(PhotonIsCutBasedLooseID)!=0 and PhotonPt[0]>Photon_Pt_Cut):
    return gammaHTagged
  
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
  p_JJVBF_SIG_ghza1prime2_1E4_JHUGen_JECNominal = p_JJVBF_SIG_ghza1prime2_1E4_JHUGen_JECNominal * (gConstants.getvalue("L1Zg","VBF",ZZMass,gConstant_list)/10000)**2 
  p_HadZH_SIG_ghza1prime2_1E4_JHUGen_JECNominal = p_HadZH_SIG_ghza1prime2_1E4_JHUGen_JECNominal * (gConstants.getvalue("L1Zg","ZH",ZZMass,gConstant_list)/10000)**2 
  p_HadWH_SIG_ghza1prime2_1E4_JHUGen_JECNominal = 0
  # g4 
  p_JJVBF_SIG_ghv4_1_JHUGen_JECNominal = p_JJVBF_SIG_ghv4_1_JHUGen_JECNominal * gConstants.getvalue("g4","VBF",ZZMass,gConstant_list)**2 
  p_HadZH_SIG_ghz4_1_JHUGen_JECNominal = p_HadZH_SIG_ghz4_1_JHUGen_JECNominal * gConstants.getvalue("g4","ZH",ZZMass,gConstant_list)**2 
  p_HadWH_SIG_ghw4_1_JHUGen_JECNominal = p_HadWH_SIG_ghw4_1_JHUGen_JECNominal * gConstants.getvalue("g4","WH",ZZMass,gConstant_list)**2 

  c_g1 = Tag_MOR18( nExtraLep,  nExtraZ,  nCleanedJetsPt30,  nCleanedJetsPt30BTagged_bTagSF,  jetQGLikelihood, p_JJQCD_SIG_ghg2_1_JHUGen_JECNominal,  p_JQCD_SIG_ghg2_1_JHUGen_JECNominal,  p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal,  p_JVBF_SIG_ghv1_1_JHUGen_JECNominal,  pAux_JVBF_SIG_ghv1_1_JHUGen_JECNominal,  p_HadWH_SIG_ghw1_1_JHUGen_JECNominal,  p_HadZH_SIG_ghz1_1_JHUGen_JECNominal,  p_HadWH_mavjj_JECNominal,  p_HadWH_mavjj_true_JECNominal,  p_HadZH_mavjj_JECNominal,  p_HadZH_mavjj_true_JECNominal,  jetPhi,  ZZMass,  ZZPt,  PFMET, useVHMETTagged,  useQGTagging , cConstant_list)

  c_g2 = Tag_MOR18( nExtraLep,  nExtraZ,  nCleanedJetsPt30,  nCleanedJetsPt30BTagged_bTagSF,  jetQGLikelihood, p_JJQCD_SIG_ghg2_1_JHUGen_JECNominal,  p_JQCD_SIG_ghg2_1_JHUGen_JECNominal,  p_JJVBF_SIG_ghv2_1_JHUGen_JECNominal,  p_JVBF_SIG_ghv1_1_JHUGen_JECNominal,  pAux_JVBF_SIG_ghv1_1_JHUGen_JECNominal,  p_HadWH_SIG_ghw2_1_JHUGen_JECNominal,  p_HadZH_SIG_ghz2_1_JHUGen_JECNominal,  p_HadWH_mavjj_JECNominal,  p_HadWH_mavjj_true_JECNominal,  p_HadZH_mavjj_JECNominal,  p_HadZH_mavjj_true_JECNominal,  jetPhi,  ZZMass,  ZZPt,  PFMET, useVHMETTagged,  useQGTagging , cConstant_list)

  c_g4 = Tag_MOR18( nExtraLep,  nExtraZ,  nCleanedJetsPt30,  nCleanedJetsPt30BTagged_bTagSF,  jetQGLikelihood, p_JJQCD_SIG_ghg2_1_JHUGen_JECNominal,  p_JQCD_SIG_ghg2_1_JHUGen_JECNominal,  p_JJVBF_SIG_ghv4_1_JHUGen_JECNominal,  p_JVBF_SIG_ghv1_1_JHUGen_JECNominal,  pAux_JVBF_SIG_ghv1_1_JHUGen_JECNominal,  p_HadWH_SIG_ghw4_1_JHUGen_JECNominal,  p_HadZH_SIG_ghz4_1_JHUGen_JECNominal,  p_HadWH_mavjj_JECNominal,  p_HadWH_mavjj_true_JECNominal,  p_HadZH_mavjj_JECNominal,  p_HadZH_mavjj_true_JECNominal,  jetPhi,  ZZMass,  ZZPt,  PFMET, useVHMETTagged,  useQGTagging , cConstant_list)

  c_g1prime2 = Tag_MOR18( nExtraLep,  nExtraZ,  nCleanedJetsPt30,  nCleanedJetsPt30BTagged_bTagSF,  jetQGLikelihood, p_JJQCD_SIG_ghg2_1_JHUGen_JECNominal,  p_JQCD_SIG_ghg2_1_JHUGen_JECNominal,  p_JJVBF_SIG_ghv1prime2_1E4_JHUGen_JECNominal,  p_JVBF_SIG_ghv1_1_JHUGen_JECNominal,  pAux_JVBF_SIG_ghv1_1_JHUGen_JECNominal,  p_HadWH_SIG_ghw1prime2_1E4_JHUGen_JECNominal,  p_HadZH_SIG_ghz1prime2_1E4_JHUGen_JECNominal,  p_HadWH_mavjj_JECNominal,  p_HadWH_mavjj_true_JECNominal,  p_HadZH_mavjj_JECNominal,  p_HadZH_mavjj_true_JECNominal,  jetPhi,  ZZMass,  ZZPt,  PFMET, useVHMETTagged,  useQGTagging , cConstant_list)

  c_ghza1prime2 = Tag_MOR18( nExtraLep,  nExtraZ,  nCleanedJetsPt30,  nCleanedJetsPt30BTagged_bTagSF,  jetQGLikelihood, p_JJQCD_SIG_ghg2_1_JHUGen_JECNominal,  p_JQCD_SIG_ghg2_1_JHUGen_JECNominal,  p_JJVBF_SIG_ghza1prime2_1E4_JHUGen_JECNominal,  p_JVBF_SIG_ghv1_1_JHUGen_JECNominal,  pAux_JVBF_SIG_ghv1_1_JHUGen_JECNominal,  p_HadWH_SIG_ghza1prime2_1E4_JHUGen_JECNominal,  p_HadZH_SIG_ghza1prime2_1E4_JHUGen_JECNominal,  p_HadWH_mavjj_JECNominal,  p_HadWH_mavjj_true_JECNominal,  p_HadZH_mavjj_JECNominal,  p_HadZH_mavjj_true_JECNominal,  jetPhi,  ZZMass,  ZZPt,  PFMET, useVHMETTagged,  useQGTagging , cConstant_list)
  
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

def Tag_Untagged_and_gammaH(PhotonPt,PhotonIsCutBasedLooseID):

  ## This is the scheme used for the HIG-19-009 analysis scheme 2 but with a gammaH category on top ##

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

  Photon_Pt_Cut=400

  if(len(PhotonIsCutBasedLooseID)!=0 and PhotonPt[0]>Photon_Pt_Cut):
    return gammaHTagged
  else:
    return Untagged



