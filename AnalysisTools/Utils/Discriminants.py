import os
from .Eval_cConstants import *
from ..data import gConstants as gCon
from numpy import sqrt as sqrt
#======================================================================================================#
#========================== OnShell_Categorization and Bkg Discriminants ==============================#
#======================================================================================================#

def D_bkg_kin(p_GG_SIG_ghg2_1_ghz1_1_JHUGen,p_QQB_BKG_MCFM,cConstants,ZZFlav,ZZMass):
  return p_GG_SIG_ghg2_1_ghz1_1_JHUGen/(p_GG_SIG_ghg2_1_ghz1_1_JHUGen + p_QQB_BKG_MCFM*getDbkgkinConstant(cConstants,ZZFlav,ZZMass)) 

def D_bkg(p_GG_SIG_ghg2_1_ghz1_1_JHUGen,p_m4l_SIG,p_QQB_BKG_MCFM,p_m4l_BKG,cConstants,ZZFlav,ZZMass):
  return p_GG_SIG_ghg2_1_ghz1_1_JHUGen*p_m4l_SIG/(p_GG_SIG_ghg2_1_ghz1_1_JHUGen*p_m4l_SIG + p_QQB_BKG_MCFM*p_m4l_BKG*getDbkgConstant(cConstants,ZZFlav,ZZMass))

def D_bkg_kin_VBFdecay(p_JJVBF_S_SIG_ghv1_1_MCFM_JECNominal,p_HadZH_S_SIG_ghz1_1_MCFM_JECNominal,p_HadWH_S_SIG_ghw1_1_MCFM_JECNominal,p_JJVBF_BKG_MCFM_JECNominal,p_HadZH_BKG_MCFM_JECNominal,p_HadWH_BKG_MCFM_JECNominal,p_JJQCD_BKG_MCFM_JECNominal,p_HadZH_mavjj_JECNominal,p_HadZH_mavjj_true_JECNominal,p_HadWH_mavjj_JECNominal,p_HadWH_mavjj_true_JECNominal,pConst_JJVBF_S_SIG_ghv1_1_MCFM_JECNominal,pConst_HadZH_S_SIG_ghz1_1_MCFM_JECNominal,pConst_HadWH_S_SIG_ghw1_1_MCFM_JECNominal,pConst_JJVBF_BKG_MCFM_JECNominal,pConst_HadZH_BKG_MCFM_JECNominal,pConst_HadWH_BKG_MCFM_JECNominal,pConst_JJQCD_BKG_MCFM_JECNominal,cConstants,ZZFlav,ZZMass):

   constant = getDbkgVBFdecConstant(cConstants,ZZFlav,ZZMass)

   vbf = p_JJVBF_S_SIG_ghv1_1_MCFM_JECNominal/pConst_JJVBF_S_SIG_ghv1_1_MCFM_JECNominal
   zh = p_HadZH_S_SIG_ghz1_1_MCFM_JECNominal/pConst_HadZH_S_SIG_ghz1_1_MCFM_JECNominal
   wh = p_HadWH_S_SIG_ghw1_1_MCFM_JECNominal/pConst_HadWH_S_SIG_ghw1_1_MCFM_JECNominal
   constA = 1./(1./pConst_JJVBF_S_SIG_ghv1_1_MCFM_JECNominal+1./pConst_HadZH_S_SIG_ghz1_1_MCFM_JECNominal+1./pConst_HadWH_S_SIG_ghw1_1_MCFM_JECNominal)

   vbs = p_JJVBF_BKG_MCFM_JECNominal/pConst_JJVBF_BKG_MCFM_JECNominal
   zzz = p_HadZH_BKG_MCFM_JECNominal/pConst_HadZH_BKG_MCFM_JECNominal
   wzz = p_HadWH_BKG_MCFM_JECNominal/pConst_HadWH_BKG_MCFM_JECNominal
   qcdzz = p_JJQCD_BKG_MCFM_JECNominal/pConst_JJQCD_BKG_MCFM_JECNominal
   constB = 1./(1./pConst_JJVBF_BKG_MCFM_JECNominal+1./pConst_HadZH_BKG_MCFM_JECNominal+1./pConst_HadWH_BKG_MCFM_JECNominal+1./pConst_JJQCD_BKG_MCFM_JECNominal)

   scale_Pmjj_vb=1
   scale_Pmjj_z = p_HadZH_mavjj_JECNominal/p_HadZH_mavjj_true_JECNominal
   scale_Pmjj_w = p_HadWH_mavjj_JECNominal/p_HadWH_mavjj_true_JECNominal

   vbf *= scale_Pmjj_vb
   vbs *= scale_Pmjj_vb

   zh *= scale_Pmjj_z
   zzz *= scale_Pmjj_z

   wh *= scale_Pmjj_w
   wzz *= scale_Pmjj_w


   PA = (vbf + zh + wh)*constA
   PB = (vbs + zzz + wzz + qcdzz)*constB

   return PA/(PA+constant*PB)

def D_bkg_VBFdecay(p_JJVBF_S_SIG_ghv1_1_MCFM_JECNominal,p_HadZH_S_SIG_ghz1_1_MCFM_JECNominal,p_HadWH_S_SIG_ghw1_1_MCFM_JECNominal,p_JJVBF_BKG_MCFM_JECNominal,p_HadZH_BKG_MCFM_JECNominal,p_HadWH_BKG_MCFM_JECNominal,p_JJQCD_BKG_MCFM_JECNominal,p_HadZH_mavjj_JECNominal,p_HadZH_mavjj_true_JECNominal,p_HadWH_mavjj_JECNominal,p_HadWH_mavjj_true_JECNominal,pConst_JJVBF_S_SIG_ghv1_1_MCFM_JECNominal,pConst_HadZH_S_SIG_ghz1_1_MCFM_JECNominal,pConst_HadWH_S_SIG_ghw1_1_MCFM_JECNominal,pConst_JJVBF_BKG_MCFM_JECNominal,pConst_HadZH_BKG_MCFM_JECNominal,pConst_HadWH_BKG_MCFM_JECNominal,pConst_JJQCD_BKG_MCFM_JECNominal,cConstants,ZZFlav,ZZMass,p_m4l_BKG,p_m4l_SIG,notdijet):
        if notdijet or p_m4l_SIG <= 0: return -999

        result = D_bkg_kin_VBFdecay(p_JJVBF_S_SIG_ghv1_1_MCFM_JECNominal,p_HadZH_S_SIG_ghz1_1_MCFM_JECNominal,p_HadWH_S_SIG_ghw1_1_MCFM_JECNominal,p_JJVBF_BKG_MCFM_JECNominal,p_HadZH_BKG_MCFM_JECNominal,p_HadWH_BKG_MCFM_JECNominal,p_JJQCD_BKG_MCFM_JECNominal,p_HadZH_mavjj_JECNominal,p_HadZH_mavjj_true_JECNominal,p_HadWH_mavjj_JECNominal,p_HadWH_mavjj_true_JECNominal,pConst_JJVBF_S_SIG_ghv1_1_MCFM_JECNominal,pConst_HadZH_S_SIG_ghz1_1_MCFM_JECNominal,pConst_HadWH_S_SIG_ghw1_1_MCFM_JECNominal,pConst_JJVBF_BKG_MCFM_JECNominal,pConst_HadZH_BKG_MCFM_JECNominal,pConst_HadWH_BKG_MCFM_JECNominal,pConst_JJQCD_BKG_MCFM_JECNominal,cConstants,ZZFlav,ZZMass)

        result = 1/result - 1
        result *= p_m4l_BKG / p_m4l_SIG * getDbkgConstant(cConstants, ZZFlav,  ZZMass) / getDbkgkinConstant(cConstants, ZZFlav,ZZMass)
        result = 1/(1+result)

        return result

def D_bkg_kin_HadVHdecay(p_JJVBF_S_SIG_ghv1_1_MCFM_JECNominal,p_HadZH_S_SIG_ghz1_1_MCFM_JECNominal,p_HadWH_S_SIG_ghw1_1_MCFM_JECNominal,p_JJVBF_BKG_MCFM_JECNominal,p_HadZH_BKG_MCFM_JECNominal,p_HadWH_BKG_MCFM_JECNominal,p_JJQCD_BKG_MCFM_JECNominal,p_HadZH_mavjj_JECNominal,p_HadZH_mavjj_true_JECNominal,p_HadWH_mavjj_JECNominal,p_HadWH_mavjj_true_JECNominal,pConst_JJVBF_S_SIG_ghv1_1_MCFM_JECNominal,pConst_HadZH_S_SIG_ghz1_1_MCFM_JECNominal,pConst_HadWH_S_SIG_ghw1_1_MCFM_JECNominal,pConst_JJVBF_BKG_MCFM_JECNominal,pConst_HadZH_BKG_MCFM_JECNominal,pConst_HadWH_BKG_MCFM_JECNominal,pConst_JJQCD_BKG_MCFM_JECNominal,cConstants,ZZFlav,ZZMass):

   constant = getDbkgVHdecConstant(cConstants,ZZFlav,ZZMass)

   vbf = p_JJVBF_S_SIG_ghv1_1_MCFM_JECNominal/pConst_JJVBF_S_SIG_ghv1_1_MCFM_JECNominal
   zh = p_HadZH_S_SIG_ghz1_1_MCFM_JECNominal/pConst_HadZH_S_SIG_ghz1_1_MCFM_JECNominal
   wh = p_HadWH_S_SIG_ghw1_1_MCFM_JECNominal/pConst_HadWH_S_SIG_ghw1_1_MCFM_JECNominal
   constA = 1./(1./pConst_JJVBF_S_SIG_ghv1_1_MCFM_JECNominal+1./pConst_HadZH_S_SIG_ghz1_1_MCFM_JECNominal+1./pConst_HadWH_S_SIG_ghw1_1_MCFM_JECNominal)

   vbs = p_JJVBF_BKG_MCFM_JECNominal/pConst_JJVBF_BKG_MCFM_JECNominal
   zzz = p_HadZH_BKG_MCFM_JECNominal/pConst_HadZH_BKG_MCFM_JECNominal
   wzz = p_HadWH_BKG_MCFM_JECNominal/pConst_HadWH_BKG_MCFM_JECNominal
   qcdzz = p_JJQCD_BKG_MCFM_JECNominal/pConst_JJQCD_BKG_MCFM_JECNominal
   constB = 1./(1./pConst_JJVBF_BKG_MCFM_JECNominal+1./pConst_HadZH_BKG_MCFM_JECNominal+1./pConst_HadWH_BKG_MCFM_JECNominal+1./pConst_JJQCD_BKG_MCFM_JECNominal)

   scale_Pmjj_vb=1
   scale_Pmjj_z = p_HadZH_mavjj_JECNominal/p_HadZH_mavjj_true_JECNominal
   scale_Pmjj_w = p_HadWH_mavjj_JECNominal/p_HadWH_mavjj_true_JECNominal

   vbf *= scale_Pmjj_vb
   vbs *= scale_Pmjj_vb

   zh *= scale_Pmjj_z
   zzz *= scale_Pmjj_z

   wh *= scale_Pmjj_w
   wzz *= scale_Pmjj_w


   PA = (vbf + zh + wh)*constA
   PB = (vbs + zzz + wzz + qcdzz)*constB

   return PA/(PA+constant*PB)

def D_bkg_HadVHdecay(p_JJVBF_S_SIG_ghv1_1_MCFM_JECNominal,p_HadZH_S_SIG_ghz1_1_MCFM_JECNominal,p_HadWH_S_SIG_ghw1_1_MCFM_JECNominal,p_JJVBF_BKG_MCFM_JECNominal,p_HadZH_BKG_MCFM_JECNominal,p_HadWH_BKG_MCFM_JECNominal,p_JJQCD_BKG_MCFM_JECNominal,p_HadZH_mavjj_JECNominal,p_HadZH_mavjj_true_JECNominal,p_HadWH_mavjj_JECNominal,p_HadWH_mavjj_true_JECNominal,pConst_JJVBF_S_SIG_ghv1_1_MCFM_JECNominal,pConst_HadZH_S_SIG_ghz1_1_MCFM_JECNominal,pConst_HadWH_S_SIG_ghw1_1_MCFM_JECNominal,pConst_JJVBF_BKG_MCFM_JECNominal,pConst_HadZH_BKG_MCFM_JECNominal,pConst_HadWH_BKG_MCFM_JECNominal,pConst_JJQCD_BKG_MCFM_JECNominal,cConstants,ZZFlav,ZZMass,p_m4l_BKG,p_m4l_SIG,notdijet):
        if notdijet or p_m4l_SIG <= 0: return -999

        result = D_bkg_kin_HadVHdecay(p_JJVBF_S_SIG_ghv1_1_MCFM_JECNominal,p_HadZH_S_SIG_ghz1_1_MCFM_JECNominal,p_HadWH_S_SIG_ghw1_1_MCFM_JECNominal,p_JJVBF_BKG_MCFM_JECNominal,p_HadZH_BKG_MCFM_JECNominal,p_HadWH_BKG_MCFM_JECNominal,p_JJQCD_BKG_MCFM_JECNominal,p_HadZH_mavjj_JECNominal,p_HadZH_mavjj_true_JECNominal,p_HadWH_mavjj_JECNominal,p_HadWH_mavjj_true_JECNominal,pConst_JJVBF_S_SIG_ghv1_1_MCFM_JECNominal,pConst_HadZH_S_SIG_ghz1_1_MCFM_JECNominal,pConst_HadWH_S_SIG_ghw1_1_MCFM_JECNominal,pConst_JJVBF_BKG_MCFM_JECNominal,pConst_HadZH_BKG_MCFM_JECNominal,pConst_HadWH_BKG_MCFM_JECNominal,pConst_JJQCD_BKG_MCFM_JECNominal,cConstants,ZZFlav,ZZMass)

        result = 1/result - 1
        result *= p_m4l_BKG / p_m4l_SIG * getDbkgConstant(cConstants, ZZFlav,  ZZMass) / getDbkgkinConstant(cConstants, ZZFlav,ZZMass)
        result = 1/(1+result)

        return result


def D_g4(p_GG_SIG_ghg2_1_ghz1_1_JHUGen,p_GG_SIG_ghg2_1_ghz4_1_JHUGen):
  return p_GG_SIG_ghg2_1_ghz1_1_JHUGen/(p_GG_SIG_ghg2_1_ghz1_1_JHUGen + pow(2.521, 2)*p_GG_SIG_ghg2_1_ghz4_1_JHUGen) # Note the hardcoded c-constant!


def DVBF2j_ME(p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal,p_JJQCD_SIG_ghg2_1_JHUGen_JECNominal,ZZMass,cConstants):
  c_Mela2j = getDVBF2jetsConstant(cConstants,ZZMass)  
  return 1./(1.+ c_Mela2j*p_JJQCD_SIG_ghg2_1_JHUGen_JECNominal/p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal)


def DVBF1j_ME(p_JVBF_SIG_ghv1_1_JHUGen_JECNominal,pAux_JVBF_SIG_ghv1_1_JHUGen_JECNominal,p_JQCD_SIG_ghg2_1_JHUGen_JECNominal,ZZMass,cConstants):

  c_Mela1j = getDVBF1jetConstant(cConstants,ZZMass)
  return 1./(1.+ c_Mela1j*p_JQCD_SIG_ghg2_1_JHUGen_JECNominal/(p_JVBF_SIG_ghv1_1_JHUGen_JECNominal*pAux_JVBF_SIG_ghv1_1_JHUGen_JECNominal))


def DWHh_ME(p_HadWH_SIG_ghw1_1_JHUGen_JECNominal,p_JJQCD_SIG_ghg2_1_JHUGen_JECNominal,p_HadWH_mavjj_JECNominal,p_HadWH_mavjj_true_JECNominal,ZZMass,cConstants):

  c_MelaWH = getDWHhConstant(cConstants,ZZMass)
  # protection from dividing by 0 #
  if p_HadWH_SIG_ghw1_1_JHUGen_JECNominal == 0:
    return 0
  else:
    return 1./(1.+ c_MelaWH*(p_HadWH_mavjj_true_JECNominal*p_JJQCD_SIG_ghg2_1_JHUGen_JECNominal)/(p_HadWH_mavjj_JECNominal*p_HadWH_SIG_ghw1_1_JHUGen_JECNominal))


def DZHh_ME(p_HadZH_SIG_ghz1_1_JHUGen_JECNominal,p_JJQCD_SIG_ghg2_1_JHUGen_JECNominal,p_HadZH_mavjj_JECNominal,p_HadZH_mavjj_true_JECNominal,ZZMass,cConstants):
  c_MelaZH = getDZHhConstant(cConstants,ZZMass)
  return 1./(1.+ c_MelaZH*(p_HadZH_mavjj_true_JECNominal*p_JJQCD_SIG_ghg2_1_JHUGen_JECNominal)/(p_HadZH_mavjj_JECNominal*p_HadZH_SIG_ghz1_1_JHUGen_JECNominal))


def jetPgOverPq( jetQGLikelihood,  jetPhi):
  if(jetQGLikelihood<0.):
    rand=ROOT.TRandom3()
    rand.SetSeed(abs(int(sin(jetPhi)*100000)))
    return 1./rand.Uniform() - 1.
  else:    
    return 1./jetQGLikelihood - 1.
  

def DVBF2j_ME_QG(p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal,p_JJQCD_SIG_ghg2_1_JHUGen_JECNominal,ZZMass,jetQGLikelihood,jetPhi, cConstants):

  DVBF2jME = DVBF2j_ME(p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal, p_JJQCD_SIG_ghg2_1_JHUGen_JECNominal, ZZMass, cConstants)
  GOverQ = ROOT.TMath.Power(jetPgOverPq(jetQGLikelihood[0],jetPhi[0]) * jetPgOverPq(jetQGLikelihood[1],jetPhi[1]) , 1./3.)
  return 1./(1.+ (1./DVBF2jME - 1.) * GOverQ)


def DVBF1j_ME_QG(p_JVBF_SIG_ghv1_1_JHUGen_JECNominal,pAux_JVBF_SIG_ghv1_1_JHUGen_JECNominal,p_JQCD_SIG_ghg2_1_JHUGen_JECNominal,ZZMass,jetQGLikelihood,jetPhi,cConstants):

  DVBF1jME = DVBF1j_ME(p_JVBF_SIG_ghv1_1_JHUGen_JECNominal, pAux_JVBF_SIG_ghv1_1_JHUGen_JECNominal, p_JQCD_SIG_ghg2_1_JHUGen_JECNominal, ZZMass, cConstants)
  GOverQ = ROOT.TMath.Power( jetPgOverPq(jetQGLikelihood[0],jetPhi[0]) , 1./3. )
  return 1./(1.+ (1./DVBF1jME - 1.) * GOverQ)


def DWHh_ME_QG(p_HadWH_SIG_ghw1_1_JHUGen_JECNominal,p_JJQCD_SIG_ghg2_1_JHUGen_JECNominal,p_HadWH_mavjj_JECNominal,p_HadWH_mavjj_true_JECNominal,ZZMass,jetQGLikelihood,jetPhi, cConstants):

  DWHhME = DWHh_ME(p_HadWH_SIG_ghw1_1_JHUGen_JECNominal, p_JJQCD_SIG_ghg2_1_JHUGen_JECNominal, p_HadWH_mavjj_JECNominal, p_HadWH_mavjj_true_JECNominal, ZZMass, cConstants)
  GOverQ = ROOT.TMath.Power( jetPgOverPq(jetQGLikelihood[0],jetPhi[0]) * jetPgOverPq(jetQGLikelihood[1],jetPhi[1]) , 1./3. )
  return 1./(1.+ (1./DWHhME - 1.) * GOverQ)


def DZHh_ME_QG(p_HadZH_SIG_ghz1_1_JHUGen_JECNominal,p_JJQCD_SIG_ghg2_1_JHUGen_JECNominal,p_HadZH_mavjj_JECNominal,p_HadZH_mavjj_true_JECNominal,ZZMass,jetQGLikelihood,jetPhi, cConstants):
  DZHhME = DZHh_ME(p_HadZH_SIG_ghz1_1_JHUGen_JECNominal, p_JJQCD_SIG_ghg2_1_JHUGen_JECNominal, p_HadZH_mavjj_JECNominal, p_HadZH_mavjj_true_JECNominal, ZZMass, cConstants)
  GOverQ = ROOT.TMath.Power( jetPgOverPq(jetQGLikelihood[0],jetPhi[0]) * jetPgOverPq(jetQGLikelihood[1],jetPhi[1]) , 1./3. )
  return 1./(1.+ (1./DZHhME - 1.) * GOverQ)

#==============================================================================================================#
#================================= OnShell Anomalous Coupling Disriminants ====================================#
#==============================================================================================================#
def D_0minus_decay(p_GG_SIG_ghg2_1_ghz1_1_JHUGen, p_GG_SIG_ghg2_1_ghz4_1_JHUGen ,m4l, gConstants):
        try:
          return p_GG_SIG_ghg2_1_ghz1_1_JHUGen / (p_GG_SIG_ghg2_1_ghz1_1_JHUGen + p_GG_SIG_ghg2_1_ghz4_1_JHUGen*gCon.getvalue("g4","HZZ2e2mu",m4l,gConstants)**2)
        except ZeroDivisionError:
          return 0

def D_CP_decay(p_GG_SIG_ghg2_1_ghz1_1_ghz4_1_JHUGen,p_GG_SIG_ghg2_1_ghz1_1_JHUGen,p_GG_SIG_ghg2_1_ghz4_1_JHUGen,m4l,gConstants):
        try:
          return p_GG_SIG_ghg2_1_ghz1_1_ghz4_1_JHUGen*gCon.getvalue("g4","HZZ2e2mu",m4l,gConstants) / (2 * sqrt(p_GG_SIG_ghg2_1_ghz1_1_JHUGen * p_GG_SIG_ghg2_1_ghz4_1_JHUGen*gCon.getvalue("g4","HZZ2e2mu",m4l,gConstants)**2))
        except ZeroDivisionError:
          return 0

def D_0hplus_decay(p_GG_SIG_ghg2_1_ghz1_1_JHUGen,p_GG_SIG_ghg2_1_ghz1_1_ghz2_1_JHUGen,m4l,gConstants):
        try:
          return p_GG_SIG_ghg2_1_ghz1_1_JHUGen / (p_GG_SIG_ghg2_1_ghz1_1_JHUGen + p_GG_SIG_ghg2_1_ghz1_1_ghz2_1_JHUGen*gCon.getvalue("g2","HZZ2e2mu",m4l,gConstants)**2)
        except ZeroDivisionError:
          return 0

def D_int_decay(p_GG_SIG_ghg2_1_ghz1_1_ghz2_1_JHUGen,p_GG_SIG_ghg2_1_ghz1_1_JHUGen,p_GG_SIG_ghg2_1_ghz2_1_JHUGen,m4l,gConstants):
        try:
          return p_GG_SIG_ghg2_1_ghz1_1_ghz2_1_JHUGen*gCon.getvalue("g2","HZZ2e2mu",m4l,gConstants) / (2 * sqrt(p_GG_SIG_ghg2_1_ghz1_1_JHUGen * p_GG_SIG_ghg2_1_ghz2_1_JHUGen*gCon.getvalue("g2","HZZ2e2mu",m4l,gConstants)**2))
        except ZeroDivisionError:
          return 0

def D_L1_decay(p_GG_SIG_ghg2_1_ghz1_1_JHUGen,p_GG_SIG_ghg2_1_ghz1prime2_1E4_JHUGen,m4l,gConstants):
        try:
          return p_GG_SIG_ghg2_1_ghz1_1_JHUGen / (p_GG_SIG_ghg2_1_ghz1_1_JHUGen + p_GG_SIG_ghg2_1_ghz1prime2_1E4_JHUGen / 1e4**2*gCon.getvalue("L1","HZZ2e2mu",m4l,gConstants)**2)
        except ZeroDivisionError:
          return 0

def D_L1int_decay(p_GG_SIG_ghg2_1_ghz1_1_ghz1prime2_1E4_JHUGen,p_GG_SIG_ghg2_1_ghz1_1_JHUGen,p_GG_SIG_ghg2_1_ghz1prime2_1E4_JHUGen,m4l,gConstants):
        try:
          return p_GG_SIG_ghg2_1_ghz1_1_ghz1prime2_1E4_JHUGen /1e4*gCon.getvalue("L1","HZZ2e2mu",m4l,gConstants) / (2 * sqrt(p_GG_SIG_ghg2_1_ghz1_1_JHUGen * p_GG_SIG_ghg2_1_ghz1prime2_1E4_JHUGen / 1e4**2*gCon.getvalue("L1","HZZ2e2mu",m4l,gConstants)**2))
        except ZeroDivisionError:
          return 0

def D_L1Zg_decay(p_GG_SIG_ghg2_1_ghz1_1_JHUGen,p_GG_SIG_ghg2_1_ghza1prime2_1E4_JHUGen,m4l,gConstants):
        try:
          return p_GG_SIG_ghg2_1_ghz1_1_JHUGen / (p_GG_SIG_ghg2_1_ghz1_1_JHUGen + p_GG_SIG_ghg2_1_ghza1prime2_1E4_JHUGen / 1e4**2*gCon.getvalue("L1Zgs","HZZ2e2mu",m4l,gConstants)**2)
        except ZeroDivisionError:
          return 0

def D_L1Zgint_decay(p_GG_SIG_ghg2_1_ghz1_1_ghza1prime2_1E4_JHUGen,p_GG_SIG_ghg2_1_ghz1_1_JHUGen,p_GG_SIG_ghg2_1_ghza1prime2_1E4_JHUGen,m4l,gConstants):
        try:
          return p_GG_SIG_ghg2_1_ghz1_1_ghza1prime2_1E4_JHUGen / 1e4*gCon.getvalue("L1Zgs","HZZ2e2mu",m4l,gConstants) / (2 * sqrt(p_GG_SIG_ghg2_1_ghz1_1_JHUGen * p_GG_SIG_ghg2_1_ghza1prime2_1E4_JHUGen / 1e4**2*gCon.getvalue("L1Zgs","HZZ2e2mu",m4l,gConstants)**2))
        except ZeroDivisionError:
          return 0

def D_L1L1Zg_decay(p_GG_SIG_ghg2_1_ghz1prime2_1E4_JHUGen, p_GG_SIG_ghg2_1_ghza1prime2_1E4_JHUGen,m4l,gConstants):
        try:
          return p_GG_SIG_ghg2_1_ghz1prime2_1E4_JHUGen / 1e4**2*gCon.getvalue("L1","HZZ2e2mu",m4l,gConstants)**2 / (p_GG_SIG_ghg2_1_ghz1prime2_1E4_JHUGen / 1e4**2*gCon.getvalue("L1","HZZ2e2mu",m4l,gConstants)**2 + p_GG_SIG_ghg2_1_ghza1prime2_1E4_JHUGen / 1e4**2*gCon.getvalue("L1Zgs","HZZ2e2mu",m4l,gConstants)**2)
        except ZeroDivisionError:
          return 0

def D_L1L1Zgint_decay(p_GG_SIG_ghg2_1_ghz1prime2_1E4_ghza1prime2_1E4_JHUGen,p_GG_SIG_ghg2_1_ghz1prime2_1E4_JHUGen,p_GG_SIG_ghg2_1_ghza1prime2_1E4_JHUGen,m4l,gConstants):
        try:
          return p_GG_SIG_ghg2_1_ghz1prime2_1E4_ghza1prime2_1E4_JHUGen / 1e4**2*gCon.getvalue("L1","HZZ2e2mu",m4l,gConstants)*gCon.getvalue("L1Zgs","HZZ2e2mu",m4l,gConstants) / (2 * sqrt(p_GG_SIG_ghg2_1_ghz1prime2_1E4_JHUGen / 1e4**2*gCon.getvalue("L1","HZZ2e2mu",m4l,gConstants)**2 * p_GG_SIG_ghg2_1_ghza1prime2_1E4_JHUGen / 1e4**2*gCon.getvalue("L1Zgs","HZZ2e2mu",m4l,gConstants)**2))
        except ZeroDivisionError:
          return 0

def D_0minus_Zg_decay(p_GG_SIG_ghg2_1_ghz1_1_JHUGen,p_GG_SIG_ghg2_1_ghza4_1_JHUGen,m4l,gConstants):
        try:
          return p_GG_SIG_ghg2_1_ghz1_1_JHUGen / (p_GG_SIG_ghg2_1_ghz1_1_JHUGen + p_GG_SIG_ghg2_1_ghza4_1_JHUGen*gCon.getvalue("g4Zg","HZZ2e2mu",m4l,gConstants)**2)
        except ZeroDivisionError:
          return 0

def D_CP_Zg_decay(p_GG_SIG_ghg2_1_ghz1_1_ghza4_1_JHUGen,p_GG_SIG_ghg2_1_ghz1_1_JHUGen,p_GG_SIG_ghg2_1_ghza4_1_JHUGen,m4l,gConstants):
        try:
          return p_GG_SIG_ghg2_1_ghz1_1_ghza4_1_JHUGen*gCon.getvalue("g4Zg","HZZ2e2mu",m4l,gConstants) / (2 * sqrt(p_GG_SIG_ghg2_1_ghz1_1_JHUGen * p_GG_SIG_ghg2_1_ghza4_1_JHUGen*gCon.getvalue("g4Zg","HZZ2e2mu",m4l,gConstants)**2))
        except ZeroDivisionError:
          return 0

def D_0hplus_Zg_decay(p_GG_SIG_ghg2_1_ghz1_1_JHUGen,p_GG_SIG_ghg2_1_ghza2_1_JHUGen,m4l,gConstants):
        try:
          return p_GG_SIG_ghg2_1_ghz1_1_JHUGen / (p_GG_SIG_ghg2_1_ghz1_1_JHUGen + p_GG_SIG_ghg2_1_ghza2_1_JHUGen*gCon.getvalue("g2Zg","HZZ2e2mu",m4l,gConstants)**2)
        except ZeroDivisionError:
          return 0

def D_int_Zg_decay(p_GG_SIG_ghg2_1_ghz1_1_ghza2_1_JHUGen,p_GG_SIG_ghg2_1_ghz1_1_JHUGen,p_GG_SIG_ghg2_1_ghza2_1_JHUGen,m4l,gConstants):
        try:
          return p_GG_SIG_ghg2_1_ghz1_1_ghza2_1_JHUGen*gCon.getvalue("g2Zg","HZZ2e2mu",m4l,gConstants) / (2 * sqrt(p_GG_SIG_ghg2_1_ghz1_1_JHUGen * p_GG_SIG_ghg2_1_ghza2_1_JHUGen*gCon.getvalue("g2Zg","HZZ2e2mu",m4l,gConstants)**2))
        except ZeroDivisionError:
          return 0

def D_0minus_gg_decay(p_GG_SIG_ghg2_1_ghz1_1_JHUGen,p_GG_SIG_ghg2_1_gha4_1_JHUGen,m4l,gConstants):
        try:
          return p_GG_SIG_ghg2_1_ghz1_1_JHUGen / (p_GG_SIG_ghg2_1_ghz1_1_JHUGen + p_GG_SIG_ghg2_1_gha4_1_JHUGen*gCon.getvalue("g4gg","HZZ2e2mu",m4l,gConstants)**2)
        except ZeroDivisionError:
          return 0

def D_CP_gg_decay(p_GG_SIG_ghg2_1_ghz1_1_gha4_1_JHUGen,p_GG_SIG_ghg2_1_ghz1_1_JHUGen,p_GG_SIG_ghg2_1_gha4_1_JHUGen,m4l,gConstants):
        try:
          return p_GG_SIG_ghg2_1_ghz1_1_gha4_1_JHUGen*gCon.getvalue("g4gg","HZZ2e2mu",m4l,gConstants) / (2 * sqrt(p_GG_SIG_ghg2_1_ghz1_1_JHUGen * p_GG_SIG_ghg2_1_gha4_1_JHUGen*gCon.getvalue("g4gg","HZZ2e2mu",m4l,gConstants)**2))
        except ZeroDivisionError:
          return 0

def D_0hplus_gg_decay(p_GG_SIG_ghg2_1_ghz1_1_JHUGen,p_GG_SIG_ghg2_1_gha2_1_JHUGen,m4l,gConstants):
        try:
          return p_GG_SIG_ghg2_1_ghz1_1_JHUGen / (p_GG_SIG_ghg2_1_ghz1_1_JHUGen + p_GG_SIG_ghg2_1_gha2_1_JHUGen*gCon.getvalue("g2gg","HZZ2e2mu",m4l,gConstants)**2)
        except ZeroDivisionError:
          return 0

def D_int_gg_decay(p_GG_SIG_ghg2_1_ghz1_1_gha2_1_JHUGen,p_GG_SIG_ghg2_1_ghz1_1_JHUGen,m4l,gConstants):
        try:
          return p_GG_SIG_ghg2_1_ghz1_1_gha2_1_JHUGen*gCon.getvalue("g2gg","HZZ2e2mu",m4l,gConstants) / (2 * sqrt(p_GG_SIG_ghg2_1_ghz1_1_JHUGen * p_GG_SIG_ghg2_1_gha2_1_JHUGen*gCon.getvalue("g2gg","HZZ2e2mu",m4l,gConstants)**2))
        except ZeroDivisionError:
          return 0
#=============================================================================================================#
#================================== VBF Anomalous Coupling Disriminants ======================================#
#=============================================================================================================#
def D_0minus_VBF(p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal,p_JJVBF_SIG_ghv4_1_JHUGen_JECNominal,notdijet,m4l,gConstants):
        if notdijet: return -999
        try:
          return p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal / (p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal + p_JJVBF_SIG_ghv4_1_JHUGen_JECNominal*gCon.getvalue("g4","VBF",m4l,gConstants)**2)
        except ZeroDivisionError:
          return 0
def D_CP_VBF(p_JJVBF_SIG_ghv1_1_ghv4_1_JHUGen_JECNominal,p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal,p_JJVBF_SIG_ghv4_1_JHUGen_JECNominal,notdijet,m4l,gConstants):
        if notdijet: return -999
        try:
          return p_JJVBF_SIG_ghv1_1_ghv4_1_JHUGen_JECNominal*gCon.getvalue("g4","VBF",m4l,gConstants) / (2 * sqrt(p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal * p_JJVBF_SIG_ghv4_1_JHUGen_JECNominal*gCon.getvalue("g4","VBF",m4l,gConstants)**2))
        except ZeroDivisionError:
          return 0
def D_0hplus_VBF(p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal,p_JJVBF_SIG_ghv2_1_JHUGen_JECNominal,notdijet,m4l,gConstants):
        if notdijet: return -999
        try:
          return p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal / (p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal + p_JJVBF_SIG_ghv2_1_JHUGen_JECNominal*gCon.getvalue("g2","VBF",m4l,gConstants)**2)
        except ZeroDivisionError:
          return 0 
def D_int_VBF(p_JJVBF_SIG_ghv1_1_ghv2_1_JHUGen_JECNominal,p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal,p_JJVBF_SIG_ghv2_1_JHUGen_JECNominal,notdijet,m4l,gConstants):
        if notdijet: return -999
        try:
          return p_JJVBF_SIG_ghv1_1_ghv2_1_JHUGen_JECNominal*gCon.getvalue("g2","VBF",m4l,gConstants) / (2 * sqrt(p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal * p_JJVBF_SIG_ghv2_1_JHUGen_JECNominal*gCon.getvalue("g2","VBF",m4l,gConstants)**2))
        except ZeroDivisionError:
          return 0
def D_L1_VBF(p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal,p_JJVBF_SIG_ghv1prime2_1E4_JHUGen_JECNominal,notdijet,m4l,gConstants):
        if notdijet: return -999
        try:
          return p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal / (p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal + p_JJVBF_SIG_ghv1prime2_1E4_JHUGen_JECNominal / 1e4**2*gCon.getvalue("L1","VBF",m4l,gConstants)**2)
        except ZeroDivisionError:
          return 0
def D_L1int_VBF(p_JJVBF_SIG_ghv1_1_ghv1prime2_1E4_JHUGen_JECNominal,p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal,p_JJVBF_SIG_ghv1prime2_1E4_JHUGen_JECNominal,notdijet,m4l,gConstants):
        if notdijet: return -999
        try:
          return p_JJVBF_SIG_ghv1_1_ghv1prime2_1E4_JHUGen_JECNominal / 1e4*gCon.getvalue("L1","VBF",m4l,gConstants) / (2 * sqrt(p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal * p_JJVBF_SIG_ghv1prime2_1E4_JHUGen_JECNominal / 1e4**2*gCon.getvalue("L1","VBF",m4l,gConstants)**2))
        except ZeroDivisionError:
          return 0
def D_L1Zg_VBF(p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal,p_JJVBF_SIG_ghza1prime2_1E4_JHUGen_JECNominal,notdijet,m4l,gConstants):
        if notdijet: return -999
        try:
          return p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal / (p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal + p_JJVBF_SIG_ghza1prime2_1E4_JHUGen_JECNominal / 1e4**2*gCon.getvalue("L1Zgs","VBF",m4l,gConstants)**2)
        except ZeroDivisionError:
          return 0
def D_L1Zgint_VBF(p_JJVBF_SIG_ghv1_1_ghza1prime2_1E4_JHUGen_JECNominal,p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal,p_JJVBF_SIG_ghza1prime2_1E4_JHUGen_JECNominal,notdijet,m4l,gConstants):
        if notdijet: return -999
        try:
          return p_JJVBF_SIG_ghv1_1_ghza1prime2_1E4_JHUGen_JECNominal / 1e4*gCon.getvalue("L1Zgs","VBF",m4l,gConstants) / (2 * sqrt(p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal * p_JJVBF_SIG_ghza1prime2_1E4_JHUGen_JECNominal / 1e4**2*gCon.getvalue("L1Zgs","VBF",m4l,gConstants)**2))
        except ZeroDivisionError:
          return 0
def D_0minus_Zg_VBF(p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal,p_JJVBF_SIG_ghza4_1_JHUGen_JECNominal,notdijet,m4l,gConstants):
        if notdijet: return -999
        try:
          return p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal / (p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal + p_JJVBF_SIG_ghza4_1_JHUGen_JECNominal*gCon.getvalue("g4Zg","VBF",m4l,gConstants)**2)
        except ZeroDivisionError:
          return 0
def D_CP_Zg_VBF(p_JJVBF_SIG_ghv1_1_ghza4_1_JHUGen_JECNominal,p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal,p_JJVBF_SIG_ghza4_1_JHUGen_JECNominal,notdijet,m4l,gConstants):
        if notdijet: return -999
        try:
          return p_JJVBF_SIG_ghv1_1_ghza4_1_JHUGen_JECNominal*gCon.getvalue("g4Zg","VBF",m4l,gConstants) / (2 * sqrt(p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal * p_JJVBF_SIG_ghza4_1_JHUGen_JECNominal*gCon.getvalue("g4Zg","VBF",m4l,gConstants)**2))
        except ZeroDivisionError:
          return 0
def D_0hplus_Zg_VBF(p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal,p_JJVBF_SIG_ghza2_1_JHUGen_JECNominal,notdijet,m4l,gConstants):
        if notdijet: return -999
        try:
          return p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal / (p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal + p_JJVBF_SIG_ghza2_1_JHUGen_JECNominal*gCon.getvalue("g2Zg","VBF",m4l,gConstants)**2)
        except ZeroDivisionError:
          return 0
def D_int_Zg_VBF(p_JJVBF_SIG_ghv1_1_ghza2_1_JHUGen_JECNominal,p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal,p_JJVBF_SIG_ghza2_1_JHUGen_JECNominal,notdijet,m4l,gConstants):
        if notdijet: return -999
        try:
          return p_JJVBF_SIG_ghv1_1_ghza2_1_JHUGen_JECNominal*gCon.getvalue("g2Zg","VBF",m4l,gConstants) / (2 * sqrt(p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal * p_JJVBF_SIG_ghza2_1_JHUGen_JECNominal*gCon.getvalue("g2Zg","VBF",m4l,gConstants)**2))
        except ZeroDivisionError:
          return 0
def D_0minus_gg_VBF(p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal,p_JJVBF_SIG_gha4_1_JHUGen_JECNominal,notdijet,m4l,gConstants):
        if notdijet: return -999
        try:
          return p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal / (p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal + p_JJVBF_SIG_gha4_1_JHUGen_JECNominal*gCon.getvalue("g4gg","VBF",m4l,gConstants)**2)
        except ZeroDivisionError:
          return 0
def D_CP_gg_VBF(p_JJVBF_SIG_ghv1_1_gha4_1_JHUGen_JECNominal,p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal,p_JJVBF_SIG_gha4_1_JHUGen_JECNominal,notdijet,m4l,gConstants):
        if notdijet: return -999
        try:
          return p_JJVBF_SIG_ghv1_1_gha4_1_JHUGen_JECNominal*gCon.getvalue("g4gg","VBF",m4l,gConstants) / (2 * sqrt(p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal * p_JJVBF_SIG_gha4_1_JHUGen_JECNominal*gCon.getvalue("g4gg","VBF",m4l,gConstants)**2))
        except ZeroDivisionError:
          return 0
def D_0hplus_gg_VBF(p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal,p_JJVBF_SIG_gha2_1_JHUGen_JECNominal,notdijet,m4l,gConstants):
        if notdijet: return -999
        try:
          return p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal / (p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal + p_JJVBF_SIG_gha2_1_JHUGen_JECNominal*gCon.getvalue("g2gg","VBF",m4l,gConstants)**2)
        except ZeroDivisionError:
          return 0
def D_int_gg_VBF(p_JJVBF_SIG_ghv1_1_gha2_1_JHUGen_JECNominal,p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal,p_JJVBF_SIG_gha2_1_JHUGen_JECNominal,notdijet,m4l,gConstants):
        if notdijet: return -999
        try:
          return p_JJVBF_SIG_ghv1_1_gha2_1_JHUGen_JECNominal*gCon.getvalue("g2gg","VBF",m4l,gConstants) / (2 * sqrt(p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal * p_JJVBF_SIG_gha2_1_JHUGen_JECNominal*gCon.getvalue("g2gg","VBF",m4l,gConstants)**2))
        except ZeroDivisionError:
          return 0

#==============================================================================================================#
#============================= VBF with Decay Anomalous Coupling Disriminants =================================#
#==============================================================================================================#

def D_0minus_VBFdecay(p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal,p_GG_SIG_ghg2_1_ghz1_1_JHUGen,p_JJVBF_SIG_ghv4_1_JHUGen_JECNominal,p_GG_SIG_ghg2_1_ghz4_1_JHUGen,notdijet,m4l,gConstants):
        if notdijet: return -999
        try:
          return p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal*p_GG_SIG_ghg2_1_ghz1_1_JHUGen / (p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal*p_GG_SIG_ghg2_1_ghz1_1_JHUGen + p_JJVBF_SIG_ghv4_1_JHUGen_JECNominal*p_GG_SIG_ghg2_1_ghz4_1_JHUGen*(gCon.getvalue("g4","VBF",m4l,gConstants)*gCon.getvalue("g4","HZZ2e2mu",m4l,gConstants))**2)
        except ZeroDivisionError:
          return 0
def D_0hplus_VBFdecay(p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal,p_GG_SIG_ghg2_1_ghz1_1_JHUGen,p_JJVBF_SIG_ghv2_1_JHUGen_JECNominal,p_GG_SIG_ghg2_1_ghz2_1_JHUGen,notdijet,m4l,gConstants):
        if notdijet: return -999
        try:
          return p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal*p_GG_SIG_ghg2_1_ghz1_1_JHUGen / (p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal*p_GG_SIG_ghg2_1_ghz1_1_JHUGen + p_JJVBF_SIG_ghv2_1_JHUGen_JECNominal*p_GG_SIG_ghg2_1_ghz2_1_JHUGen * (gCon.getvalue("g2","VBF",m4l,gConstants)*gCon.getvalue("g2","HZZ2e2mu",m4l,gConstants))**2)
        except ZeroDivisionError:
          return 0
def D_L1_VBFdecay(p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal,p_GG_SIG_ghg2_1_ghz1_1_JHUGen,p_JJVBF_SIG_ghv1prime2_1E4_JHUGen_JECNominal,p_GG_SIG_ghg2_1_ghz1prime2_1E4_JHUGen,notdijet,m4l,gConstants):
        if notdijet: return -999
        try:
          return p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal*p_GG_SIG_ghg2_1_ghz1_1_JHUGen / (p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal*p_GG_SIG_ghg2_1_ghz1_1_JHUGen + p_JJVBF_SIG_ghv1prime2_1E4_JHUGen_JECNominal / 1e4**2 * p_GG_SIG_ghg2_1_ghz1prime2_1E4_JHUGen/1e4**2 * (gCon.getvalue("L1","VBF",m4l,gConstants)*gCon.getvalue("L1","HZZ2e2mu",m4l,gConstants))**2)
        except ZeroDivisionError:
          return 0
def D_L1Zg_VBFdecay(p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal,p_GG_SIG_ghg2_1_ghz1_1_JHUGen,p_JJVBF_SIG_ghza1prime2_1E4_JHUGen_JECNominal,p_GG_SIG_ghg2_1_ghza1prime2_1E4_JHUGen,notdijet,m4l,gConstants):
        if notdijet: return -999
        try:
          return p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal*p_GG_SIG_ghg2_1_ghz1_1_JHUGen / (p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal*p_GG_SIG_ghg2_1_ghz1_1_JHUGen + p_JJVBF_SIG_ghza1prime2_1E4_JHUGen_JECNominal / 1e4**2 * p_GG_SIG_ghg2_1_ghza1prime2_1E4_JHUGen/1e4**2 * (gCon.getvalue("L1Zg","VBF",m4l,gConstants)*gCon.getvalue("L1Zg","HZZ2e2mu",m4l,gConstants))**2)
        except ZeroDivisionError:
          return 0
def D_0minus_Zg_VBFdecay(p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal,p_GG_SIG_ghg2_1_ghz1_1_JHUGen,p_JJVBF_SIG_ghza4_1_JHUGen_JECNominal,p_GG_SIG_ghg2_1_ghza4_1_JHUGen,notdijet,m4l,gConstants):
        if notdijet: return -999
        try:
          return p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal*p_GG_SIG_ghg2_1_ghz1_1_JHUGen / (p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal*p_GG_SIG_ghg2_1_ghz1_1_JHUGen + p_JJVBF_SIG_ghza4_1_JHUGen_JECNominal*p_GG_SIG_ghg2_1_ghza4_1_JHUGen * (gCon.getvalue("g4Zg","VBF",m4l,gConstants)*gCon.getvalue("g4Zg","HZZ2e2mu",m4l,gConstants))**2)
        except ZeroDivisionError:
          return 0
def D_0hplus_Zg_VBFdecay(p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal,p_GG_SIG_ghg2_1_ghz1_1_JHUGen,p_JJVBF_SIG_ghza2_1_JHUGen_JECNominal,p_GG_SIG_ghg2_1_ghza2_1_JHUGen,notdijet,m4l,gConstants):
        if notdijet: return -999
        try:
          return p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal*p_GG_SIG_ghg2_1_ghz1_1_JHUGen / (p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal*p_GG_SIG_ghg2_1_ghz1_1_JHUGen + p_JJVBF_SIG_ghza2_1_JHUGen_JECNominal*p_GG_SIG_ghg2_1_ghza2_1_JHUGen * (gCon.getvalue("g2Zg","VBF",m4l,gConstants)*gCon.getvalue("g2Zg","HZZ2e2mu",m4l,gConstants))**2)
        except ZeroDivisionError:
          return 0
def D_0minus_gg_VBFdecay(p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal,p_GG_SIG_ghg2_1_ghz1_1_JHUGen,p_JJVBF_SIG_gha4_1_JHUGen_JECNominal,p_GG_SIG_ghg2_1_gha4_1_JHUGen,notdijet,m4l,gConstants):
        if notdijet: return -999
        try:
          return p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal*p_GG_SIG_ghg2_1_ghz1_1_JHUGen / (p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal*p_GG_SIG_ghg2_1_ghz1_1_JHUGen + p_JJVBF_SIG_gha4_1_JHUGen_JECNominal*p_GG_SIG_ghg2_1_gha4_1_JHUGen * (gCon.getvalue("g4gg","VBF",m4l,gConstants)*gCon.getvalue("g4gg","HZZ2e2mu",m4l,gConstants))**2)
        except ZeroDivisionError:
          return 0
def D_0hplus_gg_VBFdecay(p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal,p_GG_SIG_ghg2_1_ghz1_1_JHUGen,p_JJVBF_SIG_gha2_1_JHUGen_JECNominal,p_GG_SIG_ghg2_1_gha2_1_JHUGen,notdijet,m4l,gConstants):
        if notdijet: return -999
        try:
          return p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal*p_GG_SIG_ghg2_1_ghz1_1_JHUGen / (p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal*p_GG_SIG_ghg2_1_ghz1_1_JHUGen + p_JJVBF_SIG_gha2_1_JHUGen_JECNominal*p_GG_SIG_ghg2_1_gha2_1_JHUGen * (gCon.getvalue("g2gg","VBF",m4l,gConstants)*gCon.getvalue("g2gg","HZZ2e2mu",m4l,gConstants))**2)
        except ZeroDivisionError:
          return 0

#==============================================================================================================#
#=============================== VH Hadronic Anomalous Coupling Disriminants ==================================#
#==============================================================================================================#

def D_0minus_HadVH(p_HadWH_SIG_ghw1_1_JHUGen_JECNominal,p_HadZH_SIG_ghz1_1_JHUGen_JECNominal,p_HadWH_SIG_ghw4_1_JHUGen_JECNominal,p_HadZH_SIG_ghz4_1_JHUGen_JECNominal,WH_scale,ZH_scale,notdijet,m4l,gConstants):
        if notdijet: return -999
        try:
          return (
                 (p_HadWH_SIG_ghw1_1_JHUGen_JECNominal * WH_scale + p_HadZH_SIG_ghz1_1_JHUGen_JECNominal * ZH_scale)
               /
                 (
                   (p_HadWH_SIG_ghw1_1_JHUGen_JECNominal * WH_scale + p_HadZH_SIG_ghz1_1_JHUGen_JECNominal * ZH_scale)
                 +
                   (p_HadWH_SIG_ghw4_1_JHUGen_JECNominal * WH_scale + p_HadZH_SIG_ghz4_1_JHUGen_JECNominal * ZH_scale)*gCon.getvalue("g4","VH",m4l,gConstants)**2
                 )
               )
        except ZeroDivisionError:
          return 0
def D_CP_HadVH(p_HadZH_SIG_ghz1_1_ghz4_1_JHUGen_JECNominal,p_HadWH_SIG_ghw1_1_JHUGen_JECNominal,p_HadWH_SIG_ghw4_1_JHUGen_JECNominal,p_HadZH_SIG_ghz1_1_JHUGen_JECNominal,p_HadZH_SIG_ghz4_1_JHUGen_JECNominal,WH_scale,ZH_scale,notdijet):
        if notdijet: return -999
        try:
          return .5 * (
                     p_HadZH_SIG_ghz1_1_ghz4_1_JHUGen_JECNominal * WH_scale / (2 * sqrt(p_HadWH_SIG_ghw1_1_JHUGen_JECNominal * WH_scale * p_HadWH_SIG_ghw4_1_JHUGen_JECNominal * WH_scale))
                    +
                     p_HadZH_SIG_ghz1_1_ghz4_1_JHUGen_JECNominal * ZH_scale / (2 * sqrt(p_HadZH_SIG_ghz1_1_JHUGen_JECNominal * ZH_scale * p_HadZH_SIG_ghz4_1_JHUGen_JECNominal * ZH_scale))
                    )
        except ZeroDivisionError:
          return 0
def D_0hplus_HadVH(p_HadWH_SIG_ghw1_1_JHUGen_JECNominal,p_HadZH_SIG_ghz1_1_JHUGen_JECNominal,p_HadWH_SIG_ghw2_1_JHUGen_JECNominal,p_HadZH_SIG_ghz2_1_JHUGen_JECNominal,WH_scale,ZH_scale,notdijet,m4l,gConstants):
        if notdijet: return -999
        try:
          return (
                 (p_HadWH_SIG_ghw1_1_JHUGen_JECNominal * WH_scale + p_HadZH_SIG_ghz1_1_JHUGen_JECNominal * ZH_scale)
               /
                 (
                   (p_HadWH_SIG_ghw1_1_JHUGen_JECNominal * WH_scale + p_HadZH_SIG_ghz1_1_JHUGen_JECNominal * ZH_scale)
                 +
                   (p_HadWH_SIG_ghw2_1_JHUGen_JECNominal * WH_scale + p_HadZH_SIG_ghz2_1_JHUGen_JECNominal * ZH_scale)*gCon.getvalue("g2","VH",m4l,gConstants)**2
                 )
               )
        except ZeroDivisionError:
          return 0
def D_int_HadVH(p_HadZH_SIG_ghz1_1_ghz2_1_JHUGen_JECNominal,p_HadWH_SIG_ghw1_1_JHUGen_JECNominal,p_HadWH_SIG_ghw2_1_JHUGen_JECNominal,p_HadZH_SIG_ghz1_1_JHUGen_JECNominal,p_HadZH_SIG_ghz2_1_JHUGen_JECNominal,WH_scale,ZH_scale,notdijet):
        if notdijet: return -999
        try:
          return .5 * (
                     p_HadZH_SIG_ghz1_1_ghz2_1_JHUGen_JECNominal * WH_scale / (2 * sqrt(p_HadWH_SIG_ghw1_1_JHUGen_JECNominal * WH_scale * p_HadWH_SIG_ghw2_1_JHUGen_JECNominal * WH_scale))
                    +
                     p_HadZH_SIG_ghz1_1_ghz2_1_JHUGen_JECNominal * ZH_scale / (2 * sqrt(p_HadZH_SIG_ghz1_1_JHUGen_JECNominal * ZH_scale * p_HadZH_SIG_ghz2_1_JHUGen_JECNominal * ZH_scale))
                    )
        except ZeroDivisionError:
          return 0
def D_L1_HadVH(p_HadWH_SIG_ghw1_1_JHUGen_JECNominal,p_HadZH_SIG_ghz1_1_JHUGen_JECNominal,p_HadWH_SIG_ghw1prime2_1E4_JHUGen_JECNominal,p_HadZH_SIG_ghz1prime2_1E4_JHUGen_JECNominal,WH_scale,ZH_scale,notdijet,m4l,gConstants):
        if notdijet: return -999
        try:
          return (
                 (p_HadWH_SIG_ghw1_1_JHUGen_JECNominal * WH_scale + p_HadZH_SIG_ghz1_1_JHUGen_JECNominal * ZH_scale)
               /
                 (
                   (p_HadWH_SIG_ghw1_1_JHUGen_JECNominal * WH_scale + p_HadZH_SIG_ghz1_1_JHUGen_JECNominal * ZH_scale)
                 +
                   (p_HadWH_SIG_ghw1prime2_1E4_JHUGen_JECNominal / 1e4**2 * WH_scale + p_HadZH_SIG_ghz1prime2_1E4_JHUGen_JECNominal / 1e4**2 * ZH_scale)*gCon.getvalue("L1","VH",m4l,gConstants)**2
                 )
               )
        except ZeroDivisionError:
          return 0
def D_L1int_HadVH(p_HadWH_SIG_ghw1_1_ghw1prime2_1E4_JHUGen_JECNominal,p_HadWH_SIG_ghw1_1_JHUGen_JECNominal,p_HadWH_SIG_ghw1prime2_1E4_JHUGen_JECNominal,p_HadZH_SIG_ghz1_1_ghz1prime2_1E4_JHUGen_JECNominal,p_HadZH_SIG_ghz1_1_JHUGen_JECNominal,p_HadZH_SIG_ghz1prime2_1E4_JHUGen_JECNominal,WH_scale,ZH_scale,notdijet,m4l,gConstants):
        if notdijet: return -999
        try:
          return .5 * (
                     p_HadWH_SIG_ghw1_1_ghw1prime2_1E4_JHUGen_JECNominal / 1e4 * WH_scale / (2 * sqrt(p_HadWH_SIG_ghw1_1_JHUGen_JECNominal * WH_scale * p_HadWH_SIG_ghw1prime2_1E4_JHUGen_JECNominal / 1e4**2 * WH_scale))
                    +
                     p_HadZH_SIG_ghz1_1_ghz1prime2_1E4_JHUGen_JECNominal / 1e4 * ZH_scale / (2 * sqrt(p_HadZH_SIG_ghz1_1_JHUGen_JECNominal * ZH_scale * p_HadZH_SIG_ghz1prime2_1E4_JHUGen_JECNominal / 1e4**2 * ZH_scale))
                    )
        except ZeroDivisionError:
          return 0
def D_L1Zg_HadVH(p_HadWH_SIG_ghw1_1_JHUGen_JECNominal,p_HadZH_SIG_ghz1_1_JHUGen_JECNominal,p_HadWH_SIG_ghzgs1prime2_1E4_JHUGen_JECNominal,p_HadZH_SIG_ghza1prime2_1E4_JHUGen_JECNominal,WH_scale,ZH_scale,notdijet,m4l,gConstants):
        if notdijet: return -999
        try:
          return (
                 (p_HadWH_SIG_ghw1_1_JHUGen_JECNominal * WH_scale + p_HadZH_SIG_ghz1_1_JHUGen_JECNominal * ZH_scale)
               /
                 (
                   (p_HadWH_SIG_ghw1_1_JHUGen_JECNominal * WH_scale + p_HadZH_SIG_ghz1_1_JHUGen_JECNominal * ZH_scale)
                 +
                   (p_HadWH_SIG_ghzgs1prime2_1E4_JHUGen_JECNominal / 1e4**2 * WH_scale + p_HadZH_SIG_ghza1prime2_1E4_JHUGen_JECNominal / 1e4**2 * ZH_scale)
                          * gCon.getvalue("L1Zgs","VH",m4l,gConstants)**2
                 )
               )
        except ZeroDivisionError:
          return 0
def D_L1Zgint_HadVH(p_HadZH_SIG_ghz1_1_ghz1prime2_1E4_JHUGen_JECNominal,p_HadZH_SIG_ghz1_1_JHUGen_JECNominal,p_HadZH_SIG_ghza1prime2_1E4_JHUGen_JECNominal,WH_scale,ZH_scale,notdijet,m4l,gConstants):
        if notdijet: return -999
        try:
          return p_HadZH_SIG_ghz1_1_ghz1prime2_1E4_JHUGen_JECNominal / 1e4 * ZH_scale / (2 * sqrt(p_HadZH_SIG_ghz1_1_JHUGen_JECNominal * ZH_scale * p_HadZH_SIG_ghza1prime2_1E4_JHUGen_JECNominal / 1e4**2 * ZH_scale))
          """
          return .5 * (
                     self.M2g1ghzgs1prime2_HadWH / (2 * sqrt(p_HadWH_SIG_ghw1_1_JHUGen_JECNominal * WH_scale * p_HadWH_SIG_ghzgs1prime2_1E4_JHUGen_JECNominal / 1e4**2 * WH_scale))
                    +
                     t.p_HadZH_SIG_ghz1_1_ghz1prime2_1E4_JHUGen_JECNominal / 1e4 * ZH_scale / (2 * sqrt(p_HadZH_SIG_ghz1_1_JHUGen_JECNominal * ZH_scale * p_HadZH_SIG_ghza1prime2_1E4_JHUGen_JECNominal / 1e4**2 * ZH_scale))
                    )
          """
        except ZeroDivisionError:
          return 0
def D_0minus_Zg_HadVH(p_HadWH_SIG_ghw1_1_JHUGen_JECNominal,p_HadZH_SIG_ghz1_1_JHUGen_JECNominal,p_HadWH_SIG_ghza4_1_JHUGen_JECNominal,p_HadZH_SIG_ghza4_1_JHUGen_JECNominal,WH_scale,ZH_scale,notdijet,m4l,gConstants):
        if notdijet: return -999
        try:
          return (
                 (p_HadWH_SIG_ghw1_1_JHUGen_JECNominal * WH_scale + p_HadZH_SIG_ghz1_1_JHUGen_JECNominal * ZH_scale)
               /
                 (
                   (p_HadWH_SIG_ghw1_1_JHUGen_JECNominal * WH_scale + p_HadZH_SIG_ghz1_1_JHUGen_JECNominal * ZH_scale)
                 +
                   (p_HadWH_SIG_ghza4_1_JHUGen_JECNominal * WH_scale + p_HadZH_SIG_ghza4_1_JHUGen_JECNominal * ZH_scale)
                          * gCon.getvalue("g4Zg","VH",m4l,gConstants)**2
                 )
               )
        except ZeroDivisionError:
          return 0
def D_CP_Zg_HadVH(p_HadZH_SIG_ghz1_1_ghza4_1_JHUGen_JECNominal,p_HadZH_SIG_ghz1_1_JHUGen_JECNominal,p_HadZH_SIG_ghza4_1_JHUGen_JECNominal,WH_scale,ZH_scale,notdijet):
        if notdijet: return -999
        try:
          return p_HadZH_SIG_ghz1_1_ghza4_1_JHUGen_JECNominal * ZH_scale / (2 * sqrt(p_HadZH_SIG_ghz1_1_JHUGen_JECNominal * ZH_scale * p_HadZH_SIG_ghza4_1_JHUGen_JECNominal * ZH_scale))
        except ZeroDivisionError:
          return 0
def D_0hplus_Zg_HadVH(p_HadWH_SIG_ghw1_1_JHUGen_JECNominal,p_HadZH_SIG_ghz1_1_JHUGen_JECNominal,p_HadWH_SIG_ghza2_1_JHUGen_JECNominal,p_HadZH_SIG_ghza2_1_JHUGen_JECNominal,WH_scale,ZH_scale,notdijet,m4l,gConstants):
        if notdijet: return -999
        try:
          return (
                 (p_HadWH_SIG_ghw1_1_JHUGen_JECNominal * WH_scale + p_HadZH_SIG_ghz1_1_JHUGen_JECNominal * ZH_scale)
               /
                 (
                   (p_HadWH_SIG_ghw1_1_JHUGen_JECNominal * WH_scale + p_HadZH_SIG_ghz1_1_JHUGen_JECNominal * ZH_scale)
                 +
                   (p_HadWH_SIG_ghza2_1_JHUGen_JECNominal * WH_scale + p_HadZH_SIG_ghza2_1_JHUGen_JECNominal * ZH_scale)
                          * gCon.getvalue("g2Zg","VH",m4l,gConstants)**2
                 )
               )
        except ZeroDivisionError:
          return 0
def D_int_Zg_HadVH(p_HadZH_SIG_ghz1_1_ghza2_1_JHUGen_JECNominal,p_HadZH_SIG_ghz1_1_JHUGen_JECNominal,p_HadZH_SIG_ghza2_1_JHUGen_JECNominal,WH_scale,ZH_scale,notdijet,m4l,gConstants):
        if notdijet: return -999
        try:
          return p_HadZH_SIG_ghz1_1_ghza2_1_JHUGen_JECNominal * ZH_scale / (2 * sqrt(p_HadZH_SIG_ghz1_1_JHUGen_JECNominal * ZH_scale * p_HadZH_SIG_ghza2_1_JHUGen_JECNominal * ZH_scale))
        except ZeroDivisionError:
          return 0
def D_0minus_gg_HadVH(p_HadWH_SIG_ghw1_1_JHUGen_JECNominal,p_HadZH_SIG_ghz1_1_JHUGen_JECNominal,p_HadWH_SIG_gha4_1_JHUGen_JECNominal,p_HadZH_SIG_gha4_1_JHUGen_JECNominal,WH_scale,ZH_scale,notdijet,m4l,gConstants):
        if notdijet: return -999
        try:
          return (
                 (p_HadWH_SIG_ghw1_1_JHUGen_JECNominal * WH_scale + p_HadZH_SIG_ghz1_1_JHUGen_JECNominal * ZH_scale)
               /
                 (
                   (p_HadWH_SIG_ghw1_1_JHUGen_JECNominal * WH_scale + p_HadZH_SIG_ghz1_1_JHUGen_JECNominal * ZH_scale)
                 +
                   (p_HadWH_SIG_gha4_1_JHUGen_JECNominal * WH_scale + p_HadZH_SIG_gha4_1_JHUGen_JECNominal * ZH_scale)
                          * gCon.getvalue("g4gg","VH",m4l,gConstants)**2
                 )
               )
        except ZeroDivisionError:
          return 0
def D_CP_gg_HadVH(p_HadZH_SIG_ghz1_1_gha4_1_JHUGen_JECNominal,p_HadZH_SIG_ghz1_1_JHUGen_JECNominal,p_HadZH_SIG_gha4_1_JHUGen_JECNominal,WH_scale,ZH_scale,notdijet):
        if notdijet: return -999
        try:
          return p_HadZH_SIG_ghz1_1_gha4_1_JHUGen_JECNominal * ZH_scale / (2 * sqrt(p_HadZH_SIG_ghz1_1_JHUGen_JECNominal * ZH_scale * p_HadZH_SIG_gha4_1_JHUGen_JECNominal * ZH_scale))
        except ZeroDivisionError:
          return 0
def D_0hplus_gg_HadVH(p_HadWH_SIG_ghw1_1_JHUGen_JECNominal,p_HadZH_SIG_ghz1_1_JHUGen_JECNominal,p_HadWH_SIG_gha2_1_JHUGen_JECNominal,p_HadZH_SIG_gha2_1_JHUGen_JECNominal,WH_scale,ZH_scale,notdijet,m4l,gConstants):
        if notdijet: return -999
        try:
          return (
                 (p_HadWH_SIG_ghw1_1_JHUGen_JECNominal * WH_scale + p_HadZH_SIG_ghz1_1_JHUGen_JECNominal * ZH_scale)
               /
                 (
                   (p_HadWH_SIG_ghw1_1_JHUGen_JECNominal * WH_scale + p_HadZH_SIG_ghz1_1_JHUGen_JECNominal * ZH_scale)
                 +
                   (p_HadWH_SIG_gha2_1_JHUGen_JECNominal * WH_scale + p_HadZH_SIG_gha2_1_JHUGen_JECNominal * ZH_scale)
                          * gCon.getvalue("g2gg","VH",m4l,gConstants)**2
                 )
               )
        except ZeroDivisionError:
          return 0
def D_int_gg_HadVH(p_HadZH_SIG_ghz1_1_gha2_1_JHUGen_JECNominal,p_HadZH_SIG_ghz1_1_JHUGen_JECNominal,p_HadZH_SIG_gha2_1_JHUGen_JECNominal,WH_scale,ZH_scale,notdijet,m4l,gConstants):
        if notdijet: return -999
        try:
          return p_HadZH_SIG_ghz1_1_gha2_1_JHUGen_JECNominal * ZH_scale / (2 * sqrt(p_HadZH_SIG_ghz1_1_JHUGen_JECNominal * ZH_scale * p_HadZH_SIG_gha2_1_JHUGen_JECNominal * ZH_scale))
        except ZeroDivisionError:
          return 0

## VH Discriminants with Decay information ## 

####################################################
#VHdecay hadronic anomalous couplings discriminants#
####################################################

def D_0minus_HadVHdecay(p_HadWH_SIG_ghw1_1_JHUGen_JECNominal,p_HadZH_SIG_ghz1_1_JHUGen_JECNominal,p_GG_SIG_ghg2_1_ghz1_1_JHUGen,p_HadWH_SIG_ghw4_1_JHUGen_JECNominal,p_HadZH_SIG_ghz4_1_JHUGen_JECNominal,p_GG_SIG_ghg2_1_ghz4_1_JHUGen,WH_scale,ZH_scale,notdijet,m4l,gConstants):
        if notdijet: return -999
        try:
          return (
                 (p_HadWH_SIG_ghw1_1_JHUGen_JECNominal * WH_scale + p_HadZH_SIG_ghz1_1_JHUGen_JECNominal * ZH_scale)*p_GG_SIG_ghg2_1_ghz1_1_JHUGen
               /
                 (
                   (p_HadWH_SIG_ghw1_1_JHUGen_JECNominal * WH_scale + p_HadZH_SIG_ghz1_1_JHUGen_JECNominal * ZH_scale)
                        *p_GG_SIG_ghg2_1_ghz1_1_JHUGen
                 + (p_HadWH_SIG_ghw4_1_JHUGen_JECNominal * WH_scale + p_HadZH_SIG_ghz4_1_JHUGen_JECNominal * ZH_scale)*gCon.getvalue("g4","VH",m4l,gConstants)**2
                        *p_GG_SIG_ghg2_1_ghz4_1_JHUGen*gCon.getvalue("g4","HZZ2e2mu",m4l,gConstants)**2
                 )
               )
        except ZeroDivisionError:
          return 0
def D_0hplus_HadVHdecay(p_HadWH_SIG_ghw1_1_JHUGen_JECNominal,p_HadZH_SIG_ghz1_1_JHUGen_JECNominal,p_GG_SIG_ghg2_1_ghz1_1_JHUGen,p_HadWH_SIG_ghw2_1_JHUGen_JECNominal,p_HadZH_SIG_ghz2_1_JHUGen_JECNominal,p_GG_SIG_ghg2_1_ghz2_1_JHUGen,WH_scale,ZH_scale,notdijet,m4l,gConstants):
        if notdijet: return -999
        try:
          return (
                 (p_HadWH_SIG_ghw1_1_JHUGen_JECNominal * WH_scale + p_HadZH_SIG_ghz1_1_JHUGen_JECNominal * ZH_scale)*p_GG_SIG_ghg2_1_ghz1_1_JHUGen
               /
                 (
                   (p_HadWH_SIG_ghw1_1_JHUGen_JECNominal * WH_scale + p_HadZH_SIG_ghz1_1_JHUGen_JECNominal * ZH_scale)
                        *p_GG_SIG_ghg2_1_ghz1_1_JHUGen
                 + (p_HadWH_SIG_ghw2_1_JHUGen_JECNominal * WH_scale + p_HadZH_SIG_ghz2_1_JHUGen_JECNominal * ZH_scale)*gCon.getvalue("g2","VH",m4l,gConstants)**2
                        *p_GG_SIG_ghg2_1_ghz2_1_JHUGen*gCon.getvalue("g2","HZZ2e2mu",m4l,gConstants)**2
                 )
               )
        except ZeroDivisionError:
          return 0
def D_L1_HadVHdecay(p_HadWH_SIG_ghw1_1_JHUGen_JECNominal,p_HadZH_SIG_ghz1_1_JHUGen_JECNominal,p_GG_SIG_ghg2_1_ghz1_1_JHUGen,p_HadWH_SIG_ghw1prime2_1E4_JHUGen_JECNominal,p_HadZH_SIG_ghz1prime2_1E4_JHUGen_JECNominal,p_GG_SIG_ghg2_1_ghz1prime2_1E4_JHUGen,WH_scale,ZH_scale,notdijet,m4l,gConstants):
        if notdijet: return -999
        try:
          return (
                 (p_HadWH_SIG_ghw1_1_JHUGen_JECNominal * WH_scale + p_HadZH_SIG_ghz1_1_JHUGen_JECNominal * ZH_scale)*p_GG_SIG_ghg2_1_ghz1_1_JHUGen
               /
                 (
                   (p_HadWH_SIG_ghw1_1_JHUGen_JECNominal * WH_scale + p_HadZH_SIG_ghz1_1_JHUGen_JECNominal * ZH_scale)
                        *p_GG_SIG_ghg2_1_ghz1_1_JHUGen
                 + (p_HadWH_SIG_ghw1prime2_1E4_JHUGen_JECNominal / 1e4**2 * WH_scale + p_HadZH_SIG_ghz1prime2_1E4_JHUGen_JECNominal / 1e4**2 * ZH_scale)*gCon.getvalue("L1","VH",m4l,gConstants)**2
                        *p_GG_SIG_ghg2_1_ghz1prime2_1E4_JHUGen / 1e4**2*gCon.getvalue("L1","HZZ2e2mu",m4l,gConstants)**2
                 )
               )
        except ZeroDivisionError:
          return 0
def D_L1Zg_HadVHdecay(p_HadWH_SIG_ghw1_1_JHUGen_JECNominal,p_HadZH_SIG_ghz1_1_JHUGen_JECNominal,p_GG_SIG_ghg2_1_ghz1_1_JHUGen,p_HadZH_SIG_ghza1prime2_1E4_JHUGen_JECNominal,p_GG_SIG_ghg2_1_ghza1prime2_1E4_JHUGen,WH_scale,ZH_scale,notdijet,m4l,gConstants):
        if notdijet: return -999
        try:
          return (
                 ((p_HadWH_SIG_ghw1_1_JHUGen_JECNominal * WH_scale + p_HadZH_SIG_ghz1_1_JHUGen_JECNominal * ZH_scale)
                    *p_GG_SIG_ghg2_1_ghz1_1_JHUGen)
               /
                 (
                   (p_HadWH_SIG_ghw1_1_JHUGen_JECNominal * WH_scale + p_HadZH_SIG_ghz1_1_JHUGen_JECNominal * ZH_scale)
                        *p_GG_SIG_ghg2_1_ghz1_1_JHUGen
                 + ( 0  + p_HadZH_SIG_ghza1prime2_1E4_JHUGen_JECNominal / 1e4**2 * ZH_scale)*gCon.getvalue("L1Zg","VH",m4l,gConstants)**2
                        *p_GG_SIG_ghg2_1_ghza1prime2_1E4_JHUGen / 1e4**2*gCon.getvalue("L1Zg","HZZ2e2mu",m4l,gConstants)**2
                 )
               )
        except ZeroDivisionError:
          return 0
def D_0minus_Zg_HadVHdecay(p_HadWH_SIG_ghw1_1_JHUGen_JECNominal,p_HadZH_SIG_ghz1_1_JHUGen_JECNominal,p_GG_SIG_ghg2_1_ghz1_1_JHUGen,p_HadZH_SIG_ghza4_1_JHUGen_JECNominal,p_GG_SIG_ghg2_1_ghza4_1_JHUGen,WH_scale,ZH_scale,notdijet,m4l,gConstants):
        if notdijet: return -999
        try:
          return (
                 ((p_HadWH_SIG_ghw1_1_JHUGen_JECNominal * WH_scale + p_HadZH_SIG_ghz1_1_JHUGen_JECNominal * ZH_scale)
                    *p_GG_SIG_ghg2_1_ghz1_1_JHUGen)
               /
                 (
                   (p_HadWH_SIG_ghw1_1_JHUGen_JECNominal * WH_scale + p_HadZH_SIG_ghz1_1_JHUGen_JECNominal * ZH_scale)
                        *p_GG_SIG_ghg2_1_ghz1_1_JHUGen
                 + ( 0  +  p_HadZH_SIG_ghza4_1_JHUGen_JECNominal * ZH_scale )*gCon.getvalue("g4Zg","VH",m4l,gConstants)**2
                        *p_GG_SIG_ghg2_1_ghza4_1_JHUGen*gCon.getvalue("g4HZg","HZZ2e2mu",m4l,gConstants)**2
                 )
               )
        except ZeroDivisionError:
          return 0
def D_0hplus_Zg_HadVHdecay(p_HadWH_SIG_ghw1_1_JHUGen_JECNominal,p_HadZH_SIG_ghz1_1_JHUGen_JECNominal,p_GG_SIG_ghg2_1_ghz1_1_JHUGen,p_HadZH_SIG_ghza2_1_JHUGen_JECNominal,p_GG_SIG_ghg2_1_ghza2_1_JHUGen,WH_scale,ZH_scale,notdijet,m4l,gConstants):
        if notdijet: return -999
        try:
          return (
                 ((p_HadWH_SIG_ghw1_1_JHUGen_JECNominal * WH_scale + p_HadZH_SIG_ghz1_1_JHUGen_JECNominal * ZH_scale)
                    *p_GG_SIG_ghg2_1_ghz1_1_JHUGen)
               /
                 (
                   (p_HadWH_SIG_ghw1_1_JHUGen_JECNominal * WH_scale + p_HadZH_SIG_ghz1_1_JHUGen_JECNominal * ZH_scale)
                        *p_GG_SIG_ghg2_1_ghz1_1_JHUGen
                 + ( 0  + p_HadZH_SIG_ghza2_1_JHUGen_JECNominal * ZH_scale)*gCon.getvalue("g2Zg","VH",m4l,gConstants)**2
                        *p_GG_SIG_ghg2_1_ghza2_1_JHUGen*gCon.getvalue("g2Zg","HZZ2e2mu",m4l,gConstants)**2
                 )
               )
        except ZeroDivisionError:
          return 0
def D_0minus_gg_HadVHdecay(p_HadWH_SIG_ghw1_1_JHUGen_JECNominal,p_HadZH_SIG_ghz1_1_JHUGen_JECNominal,p_GG_SIG_ghg2_1_ghz1_1_JHUGen,p_HadZH_SIG_gha4_1_JHUGen_JECNominal,p_GG_SIG_ghg2_1_gha4_1_JHUGen,WH_scale,ZH_scale,notdijet,m4l,gConstants):
        if notdijet: return -999
        try:
          return (
                 ((p_HadWH_SIG_ghw1_1_JHUGen_JECNominal * WH_scale + p_HadZH_SIG_ghz1_1_JHUGen_JECNominal * ZH_scale)
                    *p_GG_SIG_ghg2_1_ghz1_1_JHUGen)
               /
                 (
                   (p_HadWH_SIG_ghw1_1_JHUGen_JECNominal * WH_scale + p_HadZH_SIG_ghz1_1_JHUGen_JECNominal * ZH_scale)
                        *p_GG_SIG_ghg2_1_ghz1_1_JHUGen
                 + ( 0  + p_HadZH_SIG_gha4_1_JHUGen_JECNominal * ZH_scale)*gCon.getvalue("g4gg","VH",m4l,gConstants)**2
                        *p_GG_SIG_ghg2_1_gha4_1_JHUGen*gCon.getvalue("g4gg","HZZ2e2mu",m4l,gConstants)**2
                 )
               )
        except ZeroDivisionError:
          return 0
def D_0hplus_gg_HadVHdecay(p_HadWH_SIG_ghw1_1_JHUGen_JECNominal,p_HadZH_SIG_ghz1_1_JHUGen_JECNominal,p_GG_SIG_ghg2_1_ghz1_1_JHUGen,p_HadZH_SIG_gha2_1_JHUGen_JECNominal,p_GG_SIG_ghg2_1_gha2_1_JHUGen,WH_scale,ZH_scale,notdijet,m4l,gConstants):
        if notdijet: return -999
        try:
          return (
                 ((p_HadWH_SIG_ghw1_1_JHUGen_JECNominal * WH_scale + p_HadZH_SIG_ghz1_1_JHUGen_JECNominal * ZH_scale)
                    *p_GG_SIG_ghg2_1_ghz1_1_JHUGen)
               /
                 (
                   (p_HadWH_SIG_ghw1_1_JHUGen_JECNominal * WH_scale + p_HadZH_SIG_ghz1_1_JHUGen_JECNominal * ZH_scale)
                        *p_GG_SIG_ghg2_1_ghz1_1_JHUGen
                 + ( 0  + p_HadZH_SIG_gha2_1_JHUGen_JECNominal * ZH_scale)*gCon.getvalue("g2gg","VH",m4l,gConstants)**2
                        *p_GG_SIG_ghg2_1_gha2_1_JHUGen*gCon.getvalue("g2gg","HZZ2e2mu",m4l,gConstants)**2
                 )
               )
        except ZeroDivisionError:
          return 0
