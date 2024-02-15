import ROOT, os, sys, numpy as np, uproot, shutil
sys.path.append('../JHUGenMELA/MELA/python/')
sys.path.append('../')

from mela import Mela, SimpleParticle_t, SimpleParticleCollection_t
from ROOT import TVar, TUtil
from tqdm import tqdm
from generic_helpers import print_msg_box

def tlv(pt, eta, phi, m):
    result = ROOT.TLorentzVector()
    result.SetPtEtaPhiM(pt, eta, phi, m)
    return result

def exportPath():
    os.system("export LD_LIBRARY_PATH=../JHUGenMELA/MELA/data/$SCRAM_ARCH/:${LD_LIBRARY_PATH}")


class MELA_calc(object):
    def __init__(self) -> None:
        
    def make_MELA_input_lists(
        self, 
        lepton_ids, lepton_vecs, 
        jet_ids, jet_vecs,
        mother_ids, mother_vecs
        )