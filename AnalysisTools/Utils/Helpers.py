import math

def checkNegative(var):
    return any( val<0 for val in var )

def checkZero(var):
    return any( val==0 for val in var )

def checkNanInf(var):
    return any( ( math.isnan(val) or math.isinf(val) ) for val in var )

def HadWH_Scale_Nominal(p_HadWH_mavjj_JECNominal,p_HadWH_mavjj_true_JECNominal,pConst_HadWH_SIG_ghw1_1_JHUGen_JECNominal):
  return p_HadWH_mavjj_JECNominal / p_HadWH_mavjj_true_JECNominal / pConst_HadWH_SIG_ghw1_1_JHUGen_JECNominal

def HadZH_Scale_Nominal(p_HadZH_mavjj_JECNominal,p_HadZH_mavjj_true_JECNominal,pConst_HadZH_SIG_ghz1_1_JHUGen_JECNominal):
  return p_HadZH_mavjj_JECNominal / p_HadZH_mavjj_true_JECNominal / pConst_HadZH_SIG_ghz1_1_JHUGen_JECNominal
