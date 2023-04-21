from __future__ import print_function
from AnalysisTools.JHUGenMELA.MELA.python.mela import Mela, TVar, SimpleParticle_t, SimpleParticleCollection_t
if __name__ == "__main__":
  m = Mela(13, 125)
import ROOT, os, numpy as np

def tlv(pt, eta, phi, m):
  result = ROOT.TLorentzVector()
  result.SetPtEtaPhiM(pt, eta, phi, m)
  return result

def addprobabilities(infile, outfile):
  assert os.path.exists(infile)
  assert not os.path.exists(outfile)
  f = ROOT.TFile(infile)
  t = f.Get("ZZTree/candTree")
  try:
    newf = ROOT.TFile(outfile, "RECREATE")
    newt = t.CloneTree(0)
    p_GG_SIG_ghg2_1_ghz1_1_JHUGen = np.array([0], dtype=np.float)
    p_GG_SIG_ghg2_1_gha2_1_JHUGen = np.array([0], dtype=np.float)
    nbadSM = nbadg2gg = 0
    p_Gen_GG_SIG_ghg2_1_ghz1_1_JHUGen = np.array([0], dtype=np.float)
    p_Gen_GG_SIG_ghg2_1_gha2_1_JHUGen = np.array([0], dtype=np.float)
    newt.Branch("p_Gen_GG_SIG_ghg2_1_ghz1_1_JHUGen", p_Gen_GG_SIG_ghg2_1_ghz1_1_JHUGen, "p_Gen_GG_SIG_ghg2_1_ghz1_1_JHUGen/D")
    newt.Branch("p_Gen_GG_SIG_ghg2_1_gha2_1_JHUGen", p_Gen_GG_SIG_ghg2_1_gha2_1_JHUGen, "p_Gen_GG_SIG_ghg2_1_ghz1_1_JHUGen/D")

    for i, entry in enumerate(t, start=1):
      #########################################
      # Reco probabilities, for discriminants #
      #########################################

      #once per event
      leptons = SimpleParticleCollection_t(SimpleParticle_t(id, tlv(pt, eta, phi, 0)) for id, pt, eta, phi in zip(t.LepLepId, t.LepPt, t.LepEta, t.LepPhi))
      jets = SimpleParticleCollection_t(SimpleParticle_t(0, tlv(pt, eta, phi, m)) for pt, eta, phi, m in zip(t.JetPt, t.JetEta, t.JetPhi, t.JetMass))
      mothers = 0
      m.setInputEvent(leptons, jets, mothers, 0)

      #for every ME you want to calculate
      m.setProcess(TVar.SelfDefine_spin0, TVar.JHUGen, TVar.ZZGG) #can get examples of this from Ulascan's pyFragments
      m.ghg2 = 1
      m.ghz1 = 1
      p_GG_SIG_ghg2_1_ghz1_1_JHUGen[0] = m.computeP() #for VBF or VH etc. probabilities this is computeProdP()

      if not np.isclose(p_GG_SIG_ghg2_1_ghz1_1_JHUGen[0], t.p_GG_SIG_ghg2_1_ghz1_1_JHUGen, rtol=1e-2, atol=1e-15): nbadSM += 1
      m.setProcess(TVar.SelfDefine_spin0, TVar.JHUGen, TVar.ZZGG) #can get examples of this from Ulascan's pyFragments
      m.ghg2 = 1
      m.ghgsgs2 = 1
      p_GG_SIG_ghg2_1_gha2_1_JHUGen[0] = m.computeP() #for VBF or VH etc. probabilities this is computeProdP()

      if not np.isclose(p_GG_SIG_ghg2_1_gha2_1_JHUGen[0], t.p_GG_SIG_ghg2_1_gha2_1_JHUGen, rtol=1e-2, atol=1e-15): nbadg2gg += 1

      #once at the end of the event
      m.resetInputEvent()

      ######################################
      # LHE probabilities, for reweighting #
      ######################################

      #once per event
      leptons = SimpleParticleCollection_t(SimpleParticle_t(id, tlv(pt, eta, phi, m)) for id, pt, eta, phi, m in zip(t.LHEDaughterId, t.LHEDaughterPt, t.LHEDaughterEta, t.LHEDaughterPhi, t.LHEDaughterMass))
      jets = SimpleParticleCollection_t(SimpleParticle_t(id, tlv(pt, eta, phi, m)) for id, pt, eta, phi, m in zip(t.LHEAssociatedParticleId, t.LHEAssociatedParticlePt, t.LHEAssociatedParticleEta, t.LHEAssociatedParticlePhi, t.LHEAssociatedParticleMass))
      mothers = SimpleParticleCollection_t(SimpleParticle_t(id, ROOT.TLorentzVector(0, 0, pz, e)) for id, pz, e in zip(t.LHEMotherId, t.LHEMotherPz, t.LHEMotherE))
      m.setInputEvent(leptons, jets, mothers, 1)

      #for every ME you want to calculate
      m.setProcess(TVar.SelfDefine_spin0, TVar.JHUGen, TVar.ZZGG) #can get examples of this from Ulascan's pyFragments
      m.ghg2 = 1
      m.ghz1 = 1
      p_Gen_GG_SIG_ghg2_1_ghz1_1_JHUGen[0] = m.computeP() #for VBF or VH etc. probabilities this is computeProdP()

      m.setProcess(TVar.SelfDefine_spin0, TVar.JHUGen, TVar.ZZGG) #can get examples of this from Ulascan's pyFragments
      m.ghg2 = 1
      m.ghgsgs2 = 1
      p_Gen_GG_SIG_ghg2_1_gha2_1_JHUGen[0] = m.computeP() #for VBF or VH etc. probabilities this is computeProdP()

      #once at the end of the event
      m.resetInputEvent()

      newt.Fill()

      if i % 1000 == 0 or i == t.GetEntries():
        print(i, "/", t.GetEntries())
        break

      if i % 1000 == 0 or i == t.GetEntries():
        print(i, "/", t.GetEntries())
        break

    newf.Write()
  except:
    os.remove(outfile)
    raise

  print(nbadSM, "/", t.GetEntries(), "mismatched SM probabilities")
  print(nbadg2gg, "/", t.GetEntries(), "mismatched g2gg probabilities")

if __name__ == "__main__":
  addprobabilities("/eos/cms/store/group/phys_higgs/cmshzz4l/cjlst/RunIILegacy/200205_CutBased/MC_2016/ggH125/ZZ4lAnalysis.root", "test.root")

