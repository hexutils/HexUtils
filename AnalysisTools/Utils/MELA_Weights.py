from ..JHUGenMELA.MELA.python.mela import Mela, TVar, SimpleParticle_t, SimpleParticleCollection_t
import ROOT, os, re, numpy as np
import tqdm

def tlv(pt, eta, phi, m):
  result = ROOT.TLorentzVector()
  result.SetPtEtaPhiM(pt, eta, phi, m)
  return result

def parse_prob(probability):
  ## Functionality only tested for ggH mode ##
  parsed_dict={"Process":None,"ProdMode":None,"MatrixElement":None,"coupl_dict":{},"isReco":None,"Prod":None,"Dec":None,"JES":None,"JEC":None,"JER":None}
  # Sort whether to use Jet systematics #
  probability = probability.lower()
  if "jes" in probability: 
    if "up" in probability:
      parsed_dict["JES"] = "Up"
    elif "down" in probability:
      parsed_dict["JES"] = "Down"
    else:
      raise ValueError("Invalid JES option")
  if "jec" in probability:
    if "nominal" in probability: 
      parsed_dict["JEC"] = "Nominal"
    else:
      raise ValueError("Invalid JEC option")
  if "jer" in probability:
    if "up" in probability:
      parsed_dict["JER"] = "Up"
    elif "down" in probability:
      parsed_dict["JER"] = "Down"
    else:
      raise ValueError("Invalid JER option")
  if [parsed_dict["JES"], parsed_dict["JEC"], parsed_dict["JER"]].count(None) < 2:
    raise ValueError("Invalid combination of JES,JEC,JER!")
  # Sort Process over #
  if "sig" in probability:
    parsed_dict["Process"] = "SIG"
  elif "bkg" in probability:
    parsed_dict["Process"] = "BKG"
  elif "bsi" in probability:
    parsed_dict["Process"] = "BSI"
  #Sort Reco Or Not#
  if "_gen" in probability:
    parsed_dict["isReco"] = False
  else:
    parsed_dict["isReco"] = True
  # Sort Production Mode #
  if "gg" in probability:
    parsed_dict["ProdMode"] = "GG"
    parsed_dict["Prod"] = False
    parsed_dict["Dec"] = True
  elif "lepzh" in probability:
    parsed_dict["ProdMode"] = "LepZH"
    parsed_dict["Prod"] = True
    parsed_dict["Dec"] = False
  elif "hadzh" in probability:
    parsed_dict["ProdMode"] = "HadZH"
    if "jhugen" in probability:
      parsed_dict["Prod"] = True
      parsed_dict["Dec"] = False
    elif "mcfm" in probability:
      parsed_dict["Prod"] = True
      parsed_dict["Dec"] = True
    else:
      raise ValueError("Choose correct Matrix element for HadZH")
  elif "lepwh" in probability:
    parsed_dict["ProdMode"] = "LepWH"
    parsed_dict["Prod"] = True
    parsed_dict["Dec"] = False
  elif "hadwh" in probability:
    parsed_dict["ProdMode"] = "HadWH"
    if "jhugen" in probability:
      parsed_dict["Prod"] = True
      parsed_dict["Dec"] = False
    elif "mcfm" in probability:
      parsed_dict["Prod"] = True
      parsed_dict["Dec"] = True
    else:
      raise ValueError("Choose correct Matrix element for HadWH")
  elif "jjew" in probability:
    parsed_dict["ProdMode"] = "JJEW"
    parsed_dict["Prod"] = True
    parsed_dict["Dec"] = True
  elif "jjvbf" in probability:
    parsed_dict["ProdMode"] = "JJVBF"
    if "jhugen" in probability:
      parsed_dict["Prod"] = True
      parsed_dict["Dec"] = False
    elif "mcfm" in probability:
      parsed_dict["Prod"] = True
      parsed_dict["Dec"] = True
    else:
      raise ValueError("Choose correct Matrix element for JJVBF")
  elif "jvbf" in probability:
    parsed_dict["ProdMode"] = "JJEWQCD"
    parsed_dict["Prod"] = True
    parsed_dict["Dec"] = False
  elif "jjqcd" in probability:
    parsed_dict["ProdMode"] = "JJQCD"
    if "jhugen" in probability:
      parsed_dict["Prod"] = True
      parsed_dict["Dec"] = False
    elif "mcfm" in probability:
      parsed_dict["Prod"] = True
      parsed_dict["Dec"] = True
    else:
      raise ValueError("Choose correct Matrix element for JJQCD")
  elif "jqcd" in probability:
    parsed_dict["ProdMode"] = "JQCD"
    parsed_dict["Prod"] = True
    parsed_dict["Dec"] = False
  elif "tth" in probability:
    parsed_dict["ProdMode"] = "ttH"
    parsed_dict["Prod"] = True
    parsed_dict["Dec"] = False
  elif "bbh" in probability:
    parsed_dict["ProdMode"] = "bbH"
    parsed_dict["Prod"] = True
    parsed_dict["Dec"] = False
  # Sort MatrixElement #
  if "jhugen" in probability:
    parsed_dict["MatrixElement"] = "JHUGen"
  elif "mcfm" in probability:
    parsed_dict["MatrixElement"] = "MCFM"
  # Sort Couplings #
  coupling_names = re.findall(r"[a-zA-Z0-9]+_[0-9]", probability)
  
  # print('\nThe coupling names are as follows:\n', coupling_names)
  
  coupling_value_tuples = re.findall("[a-zA-Z0-9]+_([0-9]?(?:p)*?[0-9]+)(?:[eE]([+-]?\d+))?",probability)
  for i in range(len(coupling_names)):
    coupling = coupling_names[i].split("_")[0]
    if coupling_value_tuples[i][1] == '':
      if "p" in coupling_value_tuples[i][0]:
        value = float(coupling_value_tuples[i][0].split("p")[0] + "." + coupling_value_tuples[i][0].split("p")[1])
      else:
        value = float(coupling_value_tuples[i][0]) 
    else:
      if "p" in coupling_value_tuples[i][0]:
        value = float(coupling_value_tuples[i][0].split("p")[0] + "." + coupling_value_tuples[i][0].split("p")[1]) * 10 ** float(coupling_value_tuples[i][1])
      else:
        value = float(coupling_value_tuples[i][0]) * 10 ** float(coupling_value_tuples[i][1])
    
    # print("The value passed to the dictionary is: ", value, "with coupling key", coupling)
    parsed_dict["coupl_dict"][coupling] = value
    
  if parsed_dict["ProdMode"] == None:
    raise ValueError("Coupling does not have a valid Production Mode")
  if parsed_dict["MatrixElement"] == None:
    raise ValueError("Coupling does not have a valid MatrixElement")
  if parsed_dict["Process"] == None:
    print('\n',parsed_dict,'\n')
    raise ValueError("Coupling does not have a valid Process")
  # print (parsed_dict)
  return parsed_dict

def exportPath():
  os.system("export LD_LIBRARY_PATH=AnalysisTools/JHUGenMELA/MELA/data/$SCRAM_ARCH/:${LD_LIBRARY_PATH}")

def addprobabilities(infile,outfile,probabilities,TreePath, 
                    hasJets=False, 
                    SampleHypothesisMCFM=None, SampleHypothesisJHUGen=None,
                    ZPrime=None, higgsMass=125, couplings=[None], verbosity=0, 
                    **kwargs):
  
  HasMCFMSampleHypothesis = False
  HasJHUGenSampleHypothesis = False
  
  zPrimeMass = None
  zPrimeWidth = None
  
  if ZPrime != None:
    #input should be of form ZPrime-(Mass)-(Width)_Higgs-(Mass)
    
    zPrimeMass, zPrimeWidth = ZPrime
    
    zPrimeMass = float(zPrimeMass)
    zPrimeWidth = float(zPrimeWidth)    
  
  if SampleHypothesisMCFM != None:
    HasMCFMSampleHypothesis = True
  if SampleHypothesisJHUGen != None:
    HasJHUGenSampleHypothesis = True
  assert os.path.exists(infile)
  #assert not os.path.exists(outfile)

  if os.path.exists(outfile):
    for i in range(1000):
      if not os.path.exists(outfile.replace(".root", "_{}.root".format(i))): 
        outfile = outfile.replace(".root", "_{}.root".format(i))
        break

  #print(outfile)

  exportPath()
  
  if verbosity == 0:
    verbosity = TVar.SILENT
  elif verbosity == 1:
    verbosity = TVar.ERROR
  elif verbosity == 2:
    verbosity = TVar.INFO
  elif verbosity == 3:
    verbosity = TVar.DEBUG
  elif verbosity == 4:
    verbosity = TVar.DEBUG_VERBOSE
  elif verbosity == 5:
    verbosity = TVar.DEBUG_MECHECK
  
  m = Mela(13, 125, verbosity)# <- this is the debugger! 
  #Use it as another argument if you'd like to debug code
  #Always initialize MELA at m=125 GeV
  # print('\nThis is the mass of the "Higgs":', higgsMass)
  if ZPrime != None:
    m.Ga_Zprime = zPrimeWidth
    m.M_Zprime = zPrimeMass
  
  f = ROOT.TFile(infile)
  t = f.Get(TreePath)
  # print(infile, TreePath, t)
  try:
    newf = ROOT.TFile(outfile, "RECREATE")
    newt = t.CloneTree(0)
    # print(newt)
    newtbranches = newt.GetListOfBranches()
    probdict = {}

  
    for prob in probabilities: 
      probname = prob
      #print(probname)
      if probname in newtbranches:
        for i in range(1000):
            probname = prob+"_{}".format(i)
            #print(probname)
            if not probname in newtbranches: break
      #print(probname, prob)
      probdict[prob]=np.array([0],dtype=np.float32)
      newt.Branch(probname,probdict[prob],probname+"/F")
      #print(probdict)
    if HasMCFMSampleHypothesis:
      probdict[SampleHypothesisMCFM]=np.array([0],dtype=np.float32)
    if HasJHUGenSampleHypothesis:
      probdict[SampleHypothesisJHUGen]=np.array([0],dtype=np.float32)
    #print(probdict)

    #print(parse_prob(prob))
    
    #sys.exit()

    for i, entry in enumerate(tqdm.tqdm(t, desc="Events Processed for " + infile, total=t.GetEntries()), start=1):
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
        if hasJets:
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
          leptons = SimpleParticleCollection_t(SimpleParticle_t(pid, tlv(pt, eta, phi, 0)) for pid, pt, eta, phi in zip(t.LepLepId, t.LepPt, t.LepEta, t.LepPhi))
          jets = SimpleParticleCollection_t(SimpleParticle_t(0, tlv(pt, eta, phi, m)) for pt, eta, phi, m in zip(t.JetPt, t.JetEta, t.JetPhi, t.JetMass))
          mothers = 0
          m.setInputEvent(leptons, jets, mothers, 0)
        else:
          leptons = SimpleParticleCollection_t(SimpleParticle_t(pid, tlv(pt, eta, phi, m)) for pid, pt, eta, phi, m in zip(t.LHEDaughterId, t.LHEDaughterPt, t.LHEDaughterEta, t.LHEDaughterPhi, t.LHEDaughterMass))
          jets = SimpleParticleCollection_t(SimpleParticle_t(pid, tlv(pt, eta, phi, m)) for pid, pt, eta, phi, m in zip(t.LHEAssociatedParticleId, t.LHEAssociatedParticlePt, t.LHEAssociatedParticleEta, t.LHEAssociatedParticlePhi, t.LHEAssociatedParticleMass))
          mothers = SimpleParticleCollection_t(SimpleParticle_t(pid, ROOT.TLorentzVector(0, 0, pz, e)) for pid, pz, e in zip(t.LHEMotherId, t.LHEMotherPz, t.LHEMotherE))
          m.setInputEvent(leptons, jets, mothers, 1)
          # print(leptons)
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
        #print("\n\n", ProdExec, "\n\n")
        try:
          #print("\n\n", ProdExec, "\n\n")
          exec(ProdExec,ns)
        except:
          print("Choose Valid Production Mode")
        #Sort out the process
        ProcExec = "Process = TVar."

        if parsed_prob_dict["MatrixElement"] == "MCFM":
            '''
            ProcExec += "bkgZZ_SMHiggs"
            '''
            if parsed_prob_dict["ProdMode"] == "GG":
                if parsed_prob_dict["Process"] == "BKG":
                    if len(parsed_prob_dict["coupl_dict"]) == 0:
                        ProcExec += "bkgZZ"
                    else:
                        ProcExec += "bkgZZ"
                elif parsed_prob_dict["Process"] == "BSI":
                    if len(parsed_prob_dict["coupl_dict"]) == 0:
                        ProcExec += "bkgZZ_SMHiggs"
                    else:
                        ProcExec += "bkgZZ_SMHiggs"
                elif parsed_prob_dict["Process"] == "SIG":
                    if len(parsed_prob_dict["coupl_dict"]) == 0:
                        ProcExec += "HSMHiggs"
                    else:
                        ProcExec += "HSMHiggs"
                else:
                    ProcExec += "SelfDefine_spin0"
            elif parsed_prob_dict["ProdMode"] == "JVBF":
                if parsed_prob_dict["Process"] == "BKG":
                    if len(parsed_prob_dict["coupl_dict"]) == 0:
                        ProcExec += "bkgZZ"
                    else:
                        ProcExec += "bkgZZ"
                elif parsed_prob_dict["Process"] == "BSI":
                    if len(parsed_prob_dict["coupl_dict"]) == 0:
                        ProcExec += "bkgZZ_SMHiggs"
                    else:
                        ProcExec += "bkgZZ_SMHiggs"
                elif parsed_prob_dict["Process"] == "SIG":
                    if len(parsed_prob_dict["coupl_dict"]) == 0:
                        ProcExec += "HSMHiggs"
                    else:
                        ProcExec += "HSMHiggs"
                else:
                    ProcExec += "SelfDefine_spin0"
            elif parsed_prob_dict["ProdMode"] == "JJEW":
                if parsed_prob_dict["Process"] == "BKG":
                    if len(parsed_prob_dict["coupl_dict"]) == 0:
                        ProcExec += "bkgZZ"
                    else:
                        ProcExec += "bkgZZ"
                elif parsed_prob_dict["Process"] == "BSI":
                    if len(parsed_prob_dict["coupl_dict"]) == 0:
                        ProcExec += "bkgZZ_SMHiggs"
                    else:
                        ProcExec += "bkgZZ_SMHiggs"
                elif parsed_prob_dict["Process"] == "SIG":
                    if len(parsed_prob_dict["coupl_dict"]) == 0:
                        ProcExec += "HSMHiggs"
                    else:
                        ProcExec += "HSMHiggs"
                else:
                    ProcExec += "SelfDefine_spin0"
            DivideP = True 
            
        elif parsed_prob_dict["MatrixElement"] == "JHUGen":
            ProcExec += "SelfDefine_spin0"
        
        try:
            exec(ProcExec,ns)
        except:
            print("Current Process Not Supported")
        
        #print("\n\n", parsed_prob_dict, "\n\n")

        # print("\n\n", parsed_prob_dict, "\n\n")

        #print("\n\n", ns, "\n\n")

        #print("\n\n", ns['Process'],ns['MatrixElement'],ns['Production'], "\n\n")

        #print("\n\n", ns, "\n\n")

        #print("\n\n===========================================================================================================================================================\n\n")


        #print(parsed_prob_dict['coupl_dict'])
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
            m.kappa_top = parsed_prob_dict['coupl_dict'][key]
            m.kappa_top_tilde = 0 
            m.kappa_bot = parsed_prob_dict['coupl_dict'][key]
            m.kappa_bot_tilde = 0
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
            
          elif key == "ghzpzp1":
            m.ghzpzp1 = parsed_prob_dict['coupl_dict'][key]
          elif key == "ghzpzp4":
            m.ghzpzp4 = parsed_prob_dict['coupl_dict'][key]
          elif key == "ghzpzp2":
            m.ghzpzp2 = parsed_prob_dict['coupl_dict'][key]
          else:
            raise ValueError(str(key) + " is not a supported coupling!")
        
        if ZPrime != None:
          m.Ga_Zprime = zPrimeWidth
          m.M_Zprime = zPrimeMass
          m.setMelaHiggsMassWidth(higgsMass, 0.001, 0)
          # m.setMelaHiggsWidth(0.001,0)
          # print("\nzPrime set to width and mass of", m.Ga_Zprime, "&", m.M_Zprime, '\n')
          
        if couplings != [None]:
          # print('couplings!', couplings)
          for coupling_duo in couplings: #sets all the couplings set earlier
            setattr(m, coupling_duo[0], coupling_duo[1])
            # print(coupling_duo[0], "set to", getattr(m, coupling_duo[0]))
          
        if parsed_prob_dict["Prod"] == True and parsed_prob_dict["Dec"] == False:
          probdict[prob][0] = m.computeProdP()
        elif parsed_prob_dict["Prod"] == False and parsed_prob_dict["Dec"] == True:
          probdict[prob][0] = m.computeP()
        elif parsed_prob_dict["Prod"] == True and parsed_prob_dict["Dec"] == True:
          probdict[prob][0] = m.computeProdDecP()
        else:
          raise ValueError("Failed to process the probability passed here")
      if HasMCFMSampleHypothesis:
        for prob in probdict:
          if (prob != SampleHypothesisMCFM) and ("MCFM" in prob):
            probdict[prob][0] /= probdict[SampleHypothesisMCFM][0]
        # Now divide the Sample Hypothesis by itself to make the probability = 1
        probdict[SampleHypothesisMCFM][0] /= probdict[SampleHypothesisMCFM][0]
      if HasJHUGenSampleHypothesis:
        for prob in probdict:
          if (prob != SampleHypothesisJHUGen) and ("JHUGen" in prob):
            
            if probdict[prob][0] == 0 or probdict[SampleHypothesisJHUGen][0] == 0:
              print('\ndivision with a zero!',probdict[prob][0],probdict[SampleHypothesisJHUGen][0])
              
            # probdict[prob][0] /= probdict[SampleHypothesisJHUGen][0]
            #print(probdict[prob][0])
        # Now divide the Sample Hypothesis by itself to make the probability = 1
        # probdict[SampleHypothesisJHUGen][0] /= probdict[SampleHypothesisJHUGen][0]
      #once at the end of the event
      m.resetInputEvent()
      newt.Fill()

      # if i % 1000 == 0 or i == t.GetEntries():
        # print(i, "/", t.GetEntries())
        
    newf.Write()
  except:
    os.remove(outfile)
    raise