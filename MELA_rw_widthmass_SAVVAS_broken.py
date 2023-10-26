from __future__ import print_function
from array import array
from AnalysisTools.JHUGenMELA.MELA.python.mela import Mela, TVar, SimpleParticle_t, SimpleParticleCollection_t
import ROOT, os, sys, numpy as np


fin = sys.argv[1]




def tlv(pt, eta, phi, m):
  result = ROOT.TLorentzVector()
  result.SetPtEtaPhiM(pt, eta, phi, m)
  return result

def addprobabilities(infile, outfile):
  assert os.path.exists(infile)
  #assert not os.path.exists(outfile)
  f = ROOT.TFile(infile)
  t = f.Get("ZZTree/candTree")
  try:
    newf = ROOT.TFile(outfile, "RECREATE")
    newt = t.CloneTree(0)

    widthRW =  np.array([0], dtype=np.float64)
    massRW_SIG     =  np.array([0], dtype=np.float64)
    massRW_Interf  =  np.array([0], dtype=np.float64)
    

    newt.Branch("widthRW",widthRW,"widthRW")
    newt.Branch("massRW_SIG",massRW_SIG,"massRW_SIG")
    newt.Branch("massRW_Interf",massRW_Interf,"massRW_Interf")



    m = Mela(13,125) #,TVar.DEBUG)
    #m.setMelaHiggsMassWidth(10000,0.004,0)
    #mY = Mela(13,500)
    for i, entry in enumerate(t, start=1):
      #########################################
      # Reco probabilities, for discriminants #
      #########################################

      #once per event
      leptons = SimpleParticleCollection_t(SimpleParticle_t(id, tlv(pt, eta, phi, 0)) for id, pt, eta, phi in zip(t.LepLepId, t.LepPt, t.LepEta, t.LepPhi))
      jets = SimpleParticleCollection_t(SimpleParticle_t(0, tlv(pt, eta, phi, mass)) for pt, eta, phi, mass in zip(t.JetPt, t.JetEta, t.JetPhi, t.JetMass))
      mothers = 0

      #m.setInputEvent(leptons, jets, mothers, 0)
      #probs
      #MCFM 004029 

      #for every ME you want to calculate
      #m.setMelaHiggsMass(125,0)
      #m.setMelaHiggsWidth(0.004029,0)

      

      #m.setProcess(TVar.SelfDefine_spin0, TVar.JHUGen, TVar.ZZGG) #can get examples of this from Ulascan's pyFragments
      #m.ghg2 = 1
      #m.ghz1 = 1
      #p_GG_SIG_ghg2_1_ghz1_1_JHUGen[0] = m.computeP() #for VBF or VH etc. probabilities this is computeProdP()

      
      #for every ME you want to calculate
      #m.setProcess(TVar.SelfDefine_spin0, TVar.JHUGen, TVar.ZZGG) #can get examples of this from Ulascan's pyFragments
      #m.ghg2 = 1
      #m.ghz1 = 1
      #p_GG_SIG_ghg2_1_ghz1_1_JHUGen[0] = m.computeP() #for VBF or VH etc. probabilities this is computeProdP()



      #if not np.isclose(p_GG_SIG_ghg2_1_ghz1_1_JHUGen[0], t.p_GG_SIG_ghg2_1_ghz1_1_JHUGen, rtol=1e-2, atol=1e-15): nbadSM += 1
      #m.setProcess(TVar.SelfDefine_spin0, TVar.JHUGen, TVar.ZZGG) #can get examples of this from Ulascan's pyFragments
      #m.ghg2 = 1
      #m.ghgsgs2 = 1
      #p_GG_SIG_ghg2_1_gha2_1_JHUGen[0] = m.computeP() #for VBF or VH etc. probabilities this is computeProdP()

      #if not np.isclose(p_GG_SIG_ghg2_1_gha2_1_JHUGen[0], t.p_GG_SIG_ghg2_1_gha2_1_JHUGen, rtol=1e-2, atol=1e-15): nbadg2gg += 1

      #once at the end of the event
      #m.resetInputEvent()

      ######################################
      # LHE probabilities, for reweighting #
      ######################################

      #once per event
      leptons = SimpleParticleCollection_t(SimpleParticle_t(id, tlv(pt, eta, phi, ma)) for id, pt, eta, phi, ma in zip(t.LHEDaughterId, t.LHEDaughterPt, t.LHEDaughterEta, t.LHEDaughterPhi, t.LHEDaughterMass))
      jets = SimpleParticleCollection_t(SimpleParticle_t(id, tlv(pt, eta, phi, ma)) for id, pt, eta, phi, ma in zip(t.LHEAssociatedParticleId, t.LHEAssociatedParticlePt, t.LHEAssociatedParticleEta, t.LHEAssociatedParticlePhi, t.LHEAssociatedParticleMass))
      mothers = SimpleParticleCollection_t(SimpleParticle_t(id, ROOT.TLorentzVector(0, 0, pz, e)) for id, pz, e in zip(t.LHEMotherId, t.LHEMotherPz, t.LHEMotherE))



      #m.setInputEvent(leptons, jets, mothers, 1)
      #m.setMelaHiggsMassWidth(125,0.004,0)

      #m.setProcess(TVar.SelfDefine_spin0, TVar.JHUGen, TVar.ZZGG) #can get examples of this from Ulascan's pyFragments
      #m.ghg2 = 1
      #m.ghz1 = 1
      #p_Gen_GG_SIG_ghg2_1_ghz1_1_JHUGen[0] = m.computeP() #for VBF or VH etc. probabilities this is computeProdP()
      #print ("125:",p_Gen_GG_SIG_ghg2_1_ghz1_1_JHUGen[0],t.GenHMass)

      #for tt in range(0,6): 
      #  print ("\n")
      #m.setMelaHiggsMass(500.,0)


      #-----------------------------------------------------------

      #MASS + WIDTH      values   : 

      #EW samples  width  : 0.004029 GeV
      #ggf samples width  : 0.00407  GeV
      

      # Values from https://twiki.cern.ch/twiki/bin/view/LHCPhysics/CERNYellowReportPageBR#TotalWidthAnchor 
      #width @125.00      : 0.004088 GeV
      #width @125.38      : 0.004140 GeV


      # look at pyfragments for specifics 

      #-----------------------------------------------------------



      #find input coupling values 






      genHmass[0] = t.GenHMass

      m.setMelaHiggsMassWidth(125,0.004029,0)
      m.setInputEvent(leptons, jets, mothers, 1)
      m.ghg2 = 1
      m.ghz1 = 1
      prop_125_29[0] = m.getXPropagator(TVar.FixedWidth)

      
      m.setMelaHiggsMassWidth(125.38,0.004029,0)
      m.setInputEvent(leptons, jets, mothers, 1)
      m.ghg2 = 1
      m.ghz1 = 1
      prop_125p38_29[0] = m.getXPropagator(TVar.FixedWidth)

      m.setMelaHiggsMassWidth(125,0.00407,0)
      m.setInputEvent(leptons, jets, mothers, 1)
      m.ghg2 = 1
      m.ghz1 = 1
      prop_125_7[0] = m.getXPropagator(TVar.FixedWidth)



      m.setMelaHiggsMassWidth(125.38,0.00407,0)
      m.setInputEvent(leptons, jets, mothers, 1)
      m.ghg2 = 1
      m.ghz1 = 1
      prop_125p38_7[0] = m.getXPropagator(TVar.FixedWidth)




      #m.setProcess(TVar.SelfDefine_spin0, TVar.JHUGen, TVar.ZZGG) #can get examples of this from Ul
      #val1  = m.computeP() #for VBF or VH etc. probabilities this is computePro
      #p_Gen_GG_SIG_ghg2_1_ghz1_1_JHUGen[0] =val1 
      


      #print (t.GenHMass)

      #m.resetInputEvent()
      #m.setMelaHiggsMassWidth(500,-1,0)
      #m.ghg2 = 1
      #m.ghz1 = 1
      #m.setInputEvent(leptons, jets, mothers, 1)
      #m.setProcess(TVar.SelfDefine_spin0, TVar.JHUGen, TVar.ZZGG)
      #val2 = m.computeP()
      

      #print (val1,val2,)

      #m.ghg2 = 1
      #m.ghz1 = 1
      #m.setMelaHiggsMass(5000,0)
      #p_Gen_GG_SIG_ghg2_1_ghz1_1_JHUGen_m38[0] = m.computeP() #for VBF or VH etc. probabilities this is computeProdP()
      #print ("500:",p_Gen_GG_SIG_ghg2_1_ghz1_1_JHUGen_m38[0],t.GenHMass)
      #m.resetInputEvent()


      

      #mp38.setInputEvent(leptons, jets, mothers, 1)
    
      #mp38.setProcess(TVar.SelfDefine_spin0, TVar.JHUGen, TVar.ZZGG) #can get examples of this from Ulascan's pyFragments
      #mp38.ghg2 = 1
      #mp38.ghz1 = 1
      #print ("z1:",mp38.ghz1)
      #mp38v = mp38.computeP() #for VBF or VH etc. probabilities this is computeProdP()
      #print ("p38 :",mp38v)
      #mp38.resetInputEvent()



      #m500.setInputEvent(leptons, jets, mothers, 1)
      #m500.resetMass(500,0)
      #m500.setProcess(TVar.SelfDefine_spin0, TVar.JHUGen, TVar.ZZGG) #can get examples of this from Ulascan's pyFragments
      #m500.ghg2 = 1
      #m500.ghz1 = 1
      #m500v = m500.computeP() 
      #print ("m500 :",m500v)
      #print (m500.getMelaHiggsMass())
      #m500.resetInputEvent()




      #once at the end of the event
      m.resetInputEvent()
      #mp38.resetInputEvent()
      

      newt.Fill()

      #if i % 1000 == 0 or i == t.GetEntries():
      #  print(i, "/", t.GetEntries())
      #  break

      #if i % 1000 == 0 or i == t.GetEntries():
      #  print(i, "/", t.GetEntries())
      #  break

    newf.Write()
  except:
    os.remove(outfile)
    raise

  print(nbadSM, "/", t.GetEntries(), "mismatched SM probabilities")
  print(nbadg2gg, "/", t.GetEntries(), "mismatched g2gg probabilities")

#if __name__ == "__main__":
# addprobabilities("/eos/cms/store/group/phys_higgs/cmshzz4l/cjlst/RunIILegacy/200205_CutBased/MC_2016/ggH125/ZZ4lAnalysis.root", "test.root")
#addprobabilities("/eos/cms/store/group/phys_higgs/cmshzz4l/cjlst/RunIILegacy/200205_CutBased/MC_2017/OffshellAC/gg/ggTo2e2mu_0PMH125_MCFM701/ZZ4lAnalysis.root","test.root")
if __name__ == "__main__":
  #m500 = Mela(13, 500)
  #mp38 = Mela(13, 125.38)

  fout = "testRW_SAVVAS.root"
  
  addprobabilities(fin,fout) 
  #"/eos/cms/store/group/phys_higgs/cmshzz4l/cjlst/RunIILegacy/200205_CutBased/MC_2017/OffshellAC/gg/ggTo4mu_0PMH125_MCFM701/ZZ4lAnalysis.root","test_off_500.root")
