from __future__ import print_function
from ..JHUGenMELA.MELA.python.mela import Mela, TVar, SimpleParticle_t, SimpleParticleCollection_t
import ROOT, os, re, numpy as np

def tlv(pt, eta, phi, m):
  result = ROOT.TLorentzVector()
  result.SetPtEtaPhiM(pt, eta, phi, m)
  return result

def parse_prob(probability):
  ## Functionality only tested for ggH mode ##
  parsed_dict={"Process":None,"ProdMode":None,"MatrixElement":None,"coupl_dict":{},"isReco":None,"Prod":None,"Dec":None,"JES":None,"JEC":None,"JER":None}
  # Sort whether to use Jet systematics #
  if "JES" in probability: 
    if "Up" in probability:
      parsed_dict["JES"] = "Up"
    elif "Down" in probability:
      parsed_dict["JES"] = "Down"
    else:
      raise ValueError("Invalid JES option")
  if "JEC" in probability:
    if "Nominal" in probability: 
      parsed_dict["JEC"] = "Nominal"
    else:
      raise ValueError("Invalid JEC option")
  if "JER" in probability:
    if "Up" in probability:
      parsed_dict["JER"] = "Up"
    elif "Down" in probability:
      parsed_dict["JER"] = "Down"
    else:
      raise ValueError("Invalid JER option")
  if [parsed_dict["JES"], parsed_dict["JEC"], parsed_dict["JER"]].count(None) < 2:
    raise ValueError("Invalid combination of JES,JEC,JER!")
  # Sort Process over #
  if "SIG" in probability:
    parsed_dict["Process"] = "SIG"
  elif "BKG" in probability:
    parsed_dict["Process"] = "BKG"
  elif "BSI" in probability:
    parsed_dict["Process"] = "BSI"
  #Sort Reco Or Not#
  if "GEN" in probability:
    parsed_dict["isReco"] = False
  else:
    parsed_dict["isReco"] = True
  # Sort Production Mode #
  if "GG" in probability:
    parsed_dict["ProdMode"] = "GG"
    parsed_dict["Prod"] = False
    parsed_dict["Dec"] = True
  elif "LepZH" in probability:
    parsed_dict["ProdMode"] = "LepZH"
    parsed_dict["Prod"] = True
    parsed_dict["Dec"] = False
  elif "HadZH" in probability:
    parsed_dict["ProdMode"] = "HadZH"
    if "JHUGen" in probability:
      parsed_dict["Prod"] = True
      parsed_dict["Dec"] = False
    elif "MCFM" in probability:
      parsed_dict["Prod"] = True
      parsed_dict["Dec"] = True
    else:
      raise ValueError("Choose correct Matrix element for HadZH")
  elif "LepWH" in probability:
    parsed_dict["ProdMode"] = "LepWH"
    parsed_dict["Prod"] = True
    parsed_dict["Dec"] = False
  elif "HadWH" in probability:
    parsed_dict["ProdMode"] = "HadWH"
    if "JHUGen" in probability:
      parsed_dict["Prod"] = True
      parsed_dict["Dec"] = False
    elif "MCFM" in probability:
      parsed_dict["Prod"] = True
      parsed_dict["Dec"] = True
    else:
      raise ValueError("Choose correct Matrix element for HadWH")
  elif "JJEW" in probability:
    parsed_dict["ProdMode"] = "JJEW"
    parsed_dict["Prod"] = True
    parsed_dict["Dec"] = False
  elif "JJVBF" in probability:
    parsed_dict["ProdMode"] = "JJVBF"
    if "JHUGen" in probability:
      parsed_dict["Prod"] = True
      parsed_dict["Dec"] = False
    elif "MCFM" in probability:
      parsed_dict["Prod"] = True
      parsed_dict["Dec"] = True
    else:
      raise ValueError("Choose correct Matrix element for JJVBF")
  elif "JVBF" in probability:
    parsed_dict["ProdMode"] = "JVBF"
    parsed_dict["Prod"] = True
    parsed_dict["Dec"] = False
  elif "JJQCD" in probability:
    parsed_dict["ProdMode"] = "JJQCD"
    if "JHUGen" in probability:
      parsed_dict["Prod"] = True
      parsed_dict["Dec"] = False
    elif "MCFM" in probability:
      parsed_dict["Prod"] = True
      parsed_dict["Dec"] = True
    else:
      raise ValueError("Choose correct Matrix element for JJQCD")
  elif "JQCD" in probability:
    parsed_dict["ProdMode"] = "JQCD"
    parsed_dict["Prod"] = True
    parsed_dict["Dec"] = False
  elif "ttH" in probability:
    parsed_dict["ProdMode"] = "ttH"
    parsed_dict["Prod"] = True
    parsed_dict["Dec"] = False
  elif "bbH" in probability:
    parsed_dict["ProdMode"] = "bbH"
    parsed_dict["Prod"] = True
    parsed_dict["Dec"] = False
  # Sort MatrixElement #
  if "JHUGen" in probability:
    parsed_dict["MatrixElement"] = "JHUGen"
  elif "MCFM" in probability:
    parsed_dict["MatrixElement"] = "MCFM"
  # Sort Couplings #
  coupling_names = re.findall(r"[a-zA-Z0-9]+_[0-9]", probability)
  coupling_value_tuples = re.findall("[a-zA-Z0-9]+_([+-]?(?=\.\d|\d)(?:\d+)?(?:\.?\d*))(?:[eE]([+-]?\d+))?",probability)
  for i in range(len(coupling_names)):
    coupling = coupling_names[i].split("_")[0]
    if coupling_value_tuples[i][1] == '':
      value = float(coupling_value_tuples[i][0]) 
    else:
      value = float(coupling_value_tuples[i][0]) * 10 ** float(coupling_value_tuples[i][1])
    parsed_dict["coupl_dict"][coupling] = value
  
  if parsed_dict["ProdMode"] == None:
    raise ValueError("Coupling does not have a valid Production Mode")
  if parsed_dict["MatrixElement"] == None:
    raise ValueError("Coupling does not have a valid MatrixElement")
  if parsed_dict["Process"] == None:
    raise ValueError("Coupling does not have a valid Process")
  return parsed_dict

def exportPath():
  os.system("export LD_LIBRARY_PATH=AnalysisTools/JHUGenMELA/MELA/data/$SCRAM_ARCH/:${LD_LIBRARY_PATH}")

def addprobabilities(infile,outfile,probabilities,TreePath):
  assert os.path.exists(infile)
  assert not os.path.exists(outfile)
  exportPath()
  m = Mela(13, 125)
  f = ROOT.TFile(infile)
  t = f.Get(TreePath)
  try:
    newf = ROOT.TFile(outfile, "RECREATE")
    newt = t.CloneTree(0)
    probdict = {}
    for prob in probabilities:
      probdict[prob]=np.array([0],dtype=np.float)
      newt.Branch(prob,probdict[prob],prob+"/D")
    for i, entry in enumerate(t, start=1):
      #####################################################
      # RECO probabilities, for reweighting Discriminants #
      #####################################################
      #once per event
      for prob in probdict:
        # Parse Relevant Information from Coupling String #
        parsed_prob_dict = parse_prob(prob)
        Process = None
        JetPt = None
        MatrixElement = None
        Production = None
        ns = {'t':entry,'JetPt':JetPt,'Process':Process,'MatrixElement':MatrixElement,'Production':Production,'TVar':TVar}
        # Setup the correct Jet Scales etc #
        JetPtExec='JetPt=t.'
        if parsed_prob_dict["JES"] == "Up":
          JetPtExec+='JetPt_JESUp'
        elif parsed_prob_dict["JES"] == "Down":
          JetPtExec+='JetPt_JESDown'
        elif parsed_prob_dict["JER"] == "Up":
          JetPtExec+='JetPt_JERUp'
        elif parsed_prob_dict["JER"] == "Down":
          JetPtExec+='JetPt_JESDown'
        else:
          JetPtExec+="JetPt"
        try:
          exec(JetPtExec,ns)
        except:
          print("Error in choosing JetPt Uncertainty")
        # Setup event information depending on RECO or LHE level #
        if parsed_prob_dict["isReco"]:
          leptons = SimpleParticleCollection_t(SimpleParticle_t(id, tlv(pt, eta, phi, 0)) for id, pt, eta, phi in zip(t.LepLepId, t.LepPt, t.LepEta, t.LepPhi))
          jets = SimpleParticleCollection_t(SimpleParticle_t(0, tlv(pt, eta, phi, m)) for pt, eta, phi, m in zip(t.JetPt, t.JetEta, t.JetPhi, t.JetMass))
          mothers = 0
          m.setInputEvent(leptons, jets, mothers, 0)
        else:
          leptons = SimpleParticleCollection_t(SimpleParticle_t(id, tlv(pt, eta, phi, m)) for id, pt, eta, phi, m in zip(t.LHEDaughterId, t.LHEDaughterPt, t.LHEDaughterEta, t.LHEDaughterPhi, t.LHEDaughterMass))
          jets = SimpleParticleCollection_t(SimpleParticle_t(id, tlv(pt, eta, phi, m)) for id, pt, eta, phi, m in zip(t.LHEAssociatedParticleId, t.LHEAssociatedParticlePt, t.LHEAssociatedParticleEta, t.LHEAssociatedParticlePhi, t.LHEAssociatedParticleMass))
          mothers = SimpleParticleCollection_t(SimpleParticle_t(id, ROOT.TLorentzVector(0, 0, pz, e)) for id, pz, e in zip(t.LHEMotherId, t.LHEMotherPz, t.LHEMotherE))
          m.setInputEvent(leptons, jets, mothers, 1)        
        # Sort the MatrixElement #
        MatrixExec = "MatrixElement = TVar."+parsed_prob_dict["MatrixElement"]
        exec(MatrixExec,ns)
        try:
          exec(MatrixExec,ns)
        except:
          print("Choose Valid Matrix Element")
        # Sort the production Mode and Generator #
        ProdExec = "Production = TVar."
        if parsed_prob_dict["ProdMode"] == "GG":
          ProdExec+="ZZGG"
        else:
          ProdExec+=parsed_prob_dict["ProdMode"]
        try:
          exec(ProdExec,ns)
        except:
          print("Choose Valid Production Mode")
        #Sort out the process
        ProcExec = "Process = TVar."
        if parsed_prob_dict["MatrixElement"] == "MCFM":
          if parsed_prob_dict["ProdMode"] == "BKG" or parsed_prob_dict["ProdMode"] == "BSI" and len(parsed_prob_dict["coupl_dict"]) != 0:
            ProcExec += "bkgZZ_SMHiggs"
            #May need to be fixed#
          elif parsed_prob_dict["ProdMode"] == "BKG" or parsed_prob_dict["ProdMode"] == "BSI" and len(parsed_prob_dict["coupl_dict"]) == 0:
            ProcExec += "bkgZZ_SMHiggs"
          else:
            ProcExec += "SelfDefine_spin0"
        elif parsed_prob_dict["MatrixElement"] == "JHUGen":
          ProcExec += "SelfDefine_spin0"
        try:
          exec(ProcExec,ns)
        except:
          print("Current Process Not Supported")
        m.setProcess(ns['Process'],ns['MatrixElement'],ns['Production'])
        # Sort Couplings 
        for key in parsed_prob_dict['coupl_dict']:
          if key == "ghg2":
            m.ghg2 = parsed_prob_dict['coupl_dict'][key]
          elif key == "ghg4":
            m.ghg4 = parsed_prob_dict['coupl_dict'][key]
          elif key == "ghz1":
            m.ghz1 = parsed_prob_dict['coupl_dict'][key]
          elif key == "ghz2":
            m.ghz2 = parsed_prob_dict['coupl_dict'][key]
          elif key == "ghz4":
            m.ghz4 = parsed_prob_dict['coupl_dict'][key]
          elif key == "gha2":
            m.ghgsgs2 = parsed_prob_dict['coupl_dict'][key]
          elif key == "gha4":
            m.ghgsgs4 = parsed_prob_dict['coupl_dict'][key]
          elif key == "ghza2":
            m.ghzgs2 = parsed_prob_dict['coupl_dict'][key]
          elif key == "ghza4":
            m.ghzgs4 = parsed_prob_dict['coupl_dict'][key]
          elif key == "kappaTopBot":
            m.kappa = parsed_prob_dict['coupl_dict'][key]
          elif key == "kappa":
            m.kappa = parsed_prob_dict['coupl_dict'][key]
          elif key == "kappatilde":
            m.kappa_tilde = parsed_prob_dict['coupl_dict'][key]
          elif key == "ghza1prime2":
            m.ghzgs1_prime2 = parsed_prob_dict['coupl_dict'][key]
          elif key == "ghz1prime2":
            m.ghz1_prime2 = parsed_prob_dict['coupl_dict'][key]
          elif key == "ghv1":
            m.ghz1 = parsed_prob_dict['coupl_dict'][key]
            m.ghw1 = parsed_prob_dict['coupl_dict'][key]
          elif key == "ghv2":
            m.ghz2 = parsed_prob_dict['coupl_dict'][key]
            m.ghw2 = parsed_prob_dict['coupl_dict'][key]
          elif key == "ghv4":
            m.ghz4 = parsed_prob_dict['coupl_dict'][key]
            m.ghw4 = parsed_prob_dict['coupl_dict'][key]
          elif key == "ghv1prime2":
            m.ghz1_prime2 = parsed_prob_dict['coupl_dict'][key]
            m.ghw1_prime2 = parsed_prob_dict['coupl_dict'][key]
          else:
            raise ValueError("{} is not a supported coupling!".format(key))
        if parsed_prob_dict["Prod"] == True and parsed_prob_dict["Dec"] == False:
          probdict[prob][0] = m.computeProdP()
        elif parsed_prob_dict["Prod"] == False and parsed_prob_dict["Dec"] == True:
          probdict[prob][0] = m.computeP()
        elif parsed_prob_dict["Prod"] == False and parsed_prob_dict["Dec"] == True:
          probdict[prob][0] = m.computeProdDecP()
        else:
          raise ValueError("Failed to process the probability passed here")

      #once at the end of the event
      m.resetInputEvent()

      newt.Fill()

      if i % 1000 == 0 or i == t.GetEntries():
        print(i, "/", t.GetEntries())
        
    newf.Write()
  except:
    os.remove(outfile)
    raise
