import os
import ROOT

# This initializes discriminat splines for categorizations #
def getDVBF2jetsConstant(DVBF2jetsSpline,ZZMass):
  return DVBF2jetsSpline.Eval(ZZMass)
def getDVBF1jetConstant(DVBF1jetSpline,ZZMass):
  return DVBF1jetSpline.Eval(ZZMass)
def getDWHhConstant(DWHhSpline, ZZMass):
  return DWHhSpline.Eval(ZZMass)
def getDZHhConstant(DZHhSpline,ZZMass):
  return DZHhSpline.Eval(ZZMass)
def getDVBF2jetsWP( ZZMass,  useQGTagging):
  if (useQGTagging):
    assert 0
    return 0.363
  else:
    return 0.46386

def getDVBF1jetWP( ZZMass,  useQGTagging):
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

def getDVBF2jetsConstant_shiftWP(DVBF2jetsSpline, ZZMass,  useQGTagging,  newWP) :
  oldc = getDVBF2jetsConstant(DVBF2jetsSpline,ZZMass)
  oldWP = getDVBF2jetsWP(ZZMass, useQGTagging)
  return oldc * (oldWP/newWP) * ((1-newWP)/(1-oldWP))

def getDVBF1jetConstant_shiftWP(DVBF1jetSpline, ZZMass,  useQGTagging,  newWP) :
  oldc = getDVBF1jetConstant(DVBF1jetSpline,ZZMass)
  oldWP = getDVBF1jetWP(ZZMass, useQGTagging)
  return oldc * (oldWP/newWP) * ((1-newWP)/(1-oldWP))

def getDWHhConstant_shiftWP(DWHhSpline, ZZMass,  useQGTagging,  newWP):
  oldc = getDWHhConstant(DWHhSpline,ZZMass)
  oldWP = getDWHhWP(ZZMass, useQGTagging)
  return oldc * (oldWP/newWP) * ((1-newWP)/(1-oldWP))

def getDZHhConstant_shiftWP( ZZMass,  useQGTagging,  newWP):
  oldc = getDZHhConstant(ZZMass)
  oldWP = getDZHhWP(ZZMass, useQGTagging)
  return oldc * (oldWP/newWP) * ((1-newWP)/(1-oldWP))

def getDbkgVBFdecConstant( ZZflav,  ZZMass): # ZZflav==id1*id2*id3*id4
  if (abs(ZZflav)==11*11*11*11 or abs(ZZflav)==2*11*11*11*11 or abs(ZZflav)==2*11*11*2*11*11): 
    return DbkgVBFdecSpline4l.Eval(ZZMass)  
  if (abs(ZZflav)==11*11*13*13 or abs(ZZflav)==2*11*11*13*13 or abs(ZZflav)==2*11*11*2*13*13): 
    return DbkgVBFdecSpline2l2l.Eval(ZZMass)
  if (abs(ZZflav)==13*13*13*13 or abs(ZZflav)==2*13*13*13*13 or abs(ZZflav)==2*13*13*2*13*13): 
    return DbkgVBFdecSpline4l.Eval(ZZMass)
  print "Invalid ZZflav " + str(ZZflav)
  assert 0
  return 0

def getDbkgVHdecConstant( ZZflav,  ZZMass): # ZZflav==id1*id2*id3*id4
  if (abs(ZZflav)==11*11*11*11 or abs(ZZflav)==2*11*11*11*11 or abs(ZZflav)==2*11*11*2*11*11): 
    return DbkgVHdecSpline4l.Eval(ZZMass);
  if (abs(ZZflav)==11*11*13*13 or abs(ZZflav)==2*11*11*13*13 or abs(ZZflav)==2*11*11*2*13*13): 
    return DbkgVHdecSpline2l2l.Eval(ZZMass)
  if (abs(ZZflav)==13*13*13*13 or abs(ZZflav)==2*13*13*13*13 or abs(ZZflav)==2*13*13*2*13*13): 
    return DbkgVHdecSpline4l.Eval(ZZMass)
  print "Invalid ZZflav " + str(ZZflav)
  assert 0
  return 0

def getDbkgkinConstant( ZZflav,  ZZMass): # ZZflav==id1*id2*id3*id4
  if (abs(ZZflav)==11*11*11*11 or abs(ZZflav)==2*11*11*11*11 or abs(ZZflav)==2*11*11*2*11*11):
     return DbkgkinSpline4e.Eval(ZZMass)
  if (abs(ZZflav)==11*11*13*13 or abs(ZZflav)==2*11*11*13*13 or abs(ZZflav)==2*11*11*2*13*13):
     return DbkgkinSpline2e2mu.Eval(ZZMass)
  if (abs(ZZflav)==13*13*13*13 or abs(ZZflav)==2*13*13*13*13 or abs(ZZflav)==2*13*13*2*13*13):
     return DbkgkinSpline4mu.Eval(ZZMass)
  print "Invalid ZZflav " + str(ZZflav) 
  assert 0
  return 0

def getDbkgConstant( ZZflav,  ZZMass):
  return getDbkgkinConstant(ZZflav, ZZMass)

