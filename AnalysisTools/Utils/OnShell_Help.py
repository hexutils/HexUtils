def notdijet(p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal):
  return p_JJVBF_SIG_ghv1_1_JHUGen_JECNominal <= 0

def MassFilter(m4l):
  if 105 <= m4l <= 140:
    return False
  else:
    return True

def HadWH_Scale_Nominal(p_HadWH_mavjj_JECNominal,p_HadWH_mavjj_true_JECNominal,pConst_HadWH_SIG_ghw1_1_JHUGen_JECNominal):
  return p_HadWH_mavjj_JECNominal / p_HadWH_mavjj_true_JECNominal / pConst_HadWH_SIG_ghw1_1_JHUGen_JECNominal

def HadZH_Scale_Nominal(p_HadZH_mavjj_JECNominal,p_HadZH_mavjj_true_JECNominal,pConst_HadZH_SIG_ghz1_1_JHUGen_JECNominal):
  return p_HadZH_mavjj_JECNominal / p_HadZH_mavjj_true_JECNominal / pConst_HadZH_SIG_ghz1_1_JHUGen_JECNominal

