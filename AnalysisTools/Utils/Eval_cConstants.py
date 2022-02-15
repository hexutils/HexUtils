import ROOT

# This initializes discriminat splines for categorizations #
def getDVBF2jetsConstant(cConstants,ZZMass):
  return cConstants["D2jetVBFSpline"].Eval(ZZMass)
def getDVBF1jetConstant(cConstants,ZZMass):
  return cConstants["D1jetVBFSpline"].Eval(ZZMass)
def getDWHhConstant(cConstants,ZZMass):
  return cConstants["D2jetWHSpline"].Eval(ZZMass)
def getDZHhConstant(cConstants,ZZMass):
  return cConstants["D2jetZHSpline"].Eval(ZZMass)
def getDVBF2jetsWP( ZZMass,  useQGTagging):
  if (useQGTagging):
    assert 0
    return 0.363
  else:
    return 0.46386

def getDVBF1jetWP(ZZMass,useQGTagging):
  if (useQGTagging):
    assert 0 
    return 0.716
  else:
    #return 0.37605;
    return 0.58442
def getDWHhWP(ZZMass,useQGTagging):
  if (useQGTagging):
    assert(0)
    return 0.965
  else:
    return 0.88384

def getDZHhWP(ZZMass,useQGTagging):
  if (useQGTagging):
    assert 0
    return 0.9952
  else:
    return 0.91315

def getDVBF2jetsConstant_shiftWP(cConstants, ZZMass,  useQGTagging,  newWP) :
  oldc = getDVBF2jetsConstant(cConstants,ZZMass)
  oldWP = getDVBF2jetsWP(ZZMass, useQGTagging)
  return oldc * (oldWP/newWP) * ((1-newWP)/(1-oldWP))

def getDVBF1jetConstant_shiftWP(cConstants, ZZMass,  useQGTagging,  newWP) :
  oldc = getDVBF1jetConstant(cConstants,ZZMass)
  oldWP = getDVBF1jetWP(ZZMass, useQGTagging)
  return oldc * (oldWP/newWP) * ((1-newWP)/(1-oldWP))

def getDWHhConstant_shiftWP(cConstants, ZZMass,  useQGTagging,  newWP):
  oldc = getDWHhConstant(DWHhSpline,ZZMass)
  oldWP = getDWHhWP(ZZMass, useQGTagging)
  return oldc * (oldWP/newWP) * ((1-newWP)/(1-oldWP))

def getDZHhConstant_shiftWP(cConstants, ZZMass,  useQGTagging,  newWP):
  oldc = getDZHhConstant(cConstants,ZZMass)
  oldWP = getDZHhWP(ZZMass, useQGTagging)
  return oldc * (oldWP/newWP) * ((1-newWP)/(1-oldWP))

def getDbkgVBFdecConstant(cConstants, ZZflav, ZZMass): # ZZflav==id1*id2*id3*id4
  if (abs(ZZflav)==11*11*11*11 or abs(ZZflav)==2*11*11*11*11 or abs(ZZflav)==2*11*11*2*11*11): 
    return cConstants["DbkgjjEWQCDSpline4lJJVBF"].Eval(ZZMass)  
  if (abs(ZZflav)==11*11*13*13 or abs(ZZflav)==2*11*11*13*13 or abs(ZZflav)==2*11*11*2*13*13): 
    return cConstants["DbkgjjEWQCDSpline2l2lJJVBF"].Eval(ZZMass)
  if (abs(ZZflav)==13*13*13*13 or abs(ZZflav)==2*13*13*13*13 or abs(ZZflav)==2*13*13*2*13*13): 
    return cConstants["DbkgjjEWQCDSpline4lJJVBF"].Eval(ZZMass)
  print("Invalid ZZflav " + str(ZZflav))
  assert 0
  return 0

def getDbkgVHdecConstant(cConstants, ZZflav,  ZZMass): # ZZflav==id1*id2*id3*id4
  if (abs(ZZflav)==11*11*11*11 or abs(ZZflav)==2*11*11*11*11 or abs(ZZflav)==2*11*11*2*11*11): 
    return cConstants["DbkgjjEWQCDSpline4lHadVH"].Eval(ZZMass)
  if (abs(ZZflav)==11*11*13*13 or abs(ZZflav)==2*11*11*13*13 or abs(ZZflav)==2*11*11*2*13*13): 
    return cConstants["DbkgjjEWQCDSpline2l2lHadVH"].Eval(ZZMass)
  if (abs(ZZflav)==13*13*13*13 or abs(ZZflav)==2*13*13*13*13 or abs(ZZflav)==2*13*13*2*13*13): 
    return cConstants["DbkgjjEWQCDSpline4lHadVH"].Eval(ZZMass)
  print("Invalid ZZflav " + str(ZZflav))
  assert 0
  return 0

def getDbkgkinConstant(cConstants, ZZflav,  ZZMass): # ZZflav==id1*id2*id3*id4
  if (abs(ZZflav)==11*11*11*11 or abs(ZZflav)==2*11*11*11*11 or abs(ZZflav)==2*11*11*2*11*11):
     return cConstants["DggbkgkinSpline4e"].Eval(ZZMass)
  if (abs(ZZflav)==11*11*13*13 or abs(ZZflav)==2*11*11*13*13 or abs(ZZflav)==2*11*11*2*13*13):
     return cConstants["DggbkgkinSpline2e2mu"].Eval(ZZMass)
  if (abs(ZZflav)==13*13*13*13 or abs(ZZflav)==2*13*13*13*13 or abs(ZZflav)==2*13*13*2*13*13):
     return cConstants["DggbkgkinSpline4mu"].Eval(ZZMass)
  print("Invalid ZZflav " + str(ZZflav))
  assert 0
  return 0

def getDbkgConstant(cConstants, ZZflav,  ZZMass):
  return getDbkgkinConstant(cConstants, ZZflav, ZZMass)
