#!/usr/bin/env python
import abc
import re
import argparse, os
import numpy as np
import tqdm

import lhe_reader
import uproot
import vector

import Mela

def LHE_line_to_simpleParticle_t(lhe_line):
    line_list = lhe_line.strip().split()
    id = int(line_list[0])
    vec = [float(i) for i in line_list[6:10]] #px, py, pz, e
    return Mela.SimpleParticle_t(id, *vec, False)

def MELA_simpleParticle_toVector(simpleParticle):
    id = simpleParticle.id
    vec = simpleParticle.PxPyPzE_vector
    return id, vector.obj(px=vec[0], py=vec[1], pz=vec[2], E=vec[3])

class LHEEvent(object, metaclass=abc.ABCMeta):
    def __init__(self, event, isgen):
        """A class for a single LHE event in a file

        Parameters
        ----------
        event : str
            The string consisting of a single event between <event> and </event>
        isgen : bool
            Whether it was a generation quantity

        Raises
        ------
        ValueError
            Raises when the number of particles is wrong in the event
        """
        lines = event.split("\n")
        self.lines = lines[1:-1]
        self.isgen = isgen

        self.weights = {}
        for line in lines:
            if "<wgt" not in line: continue
            match = re.match("<wgt id='(.*)'>\s+([+\-\d.e]+)\s+<\/wgt>", line)
            if match: self.weights[match.group(1)] = float(match.group(2))

        lines = [line for line in lines if not ("<" in line or ">" in line or not line.split("#")[0].strip())]
        nparticles, _, weight, _, _, _ = lines[0].split()

        nparticles = int(nparticles)
        self.weight = float(weight)
        if nparticles != len(lines)-1:
            raise ValueError(f"Wrong number of particles! Should be {nparticles}, have {len(lines)-1}")

        daughters_lhe, associated_lhe, mothers_lhe = self.extracteventparticles()

        self.daughters =  Mela.SimpleParticleCollection_t([LHE_line_to_simpleParticle_t(line) for line in daughters_lhe])
        self.associated = Mela.SimpleParticleCollection_t([LHE_line_to_simpleParticle_t(line) for line in associated_lhe])
        self.mothers =    Mela.SimpleParticleCollection_t([LHE_line_to_simpleParticle_t(line) for line in mothers_lhe])

    @abc.abstractmethod
    def extracteventparticles(self, lines, isgen): "has to be a classmethod that returns daughters, associated, mothers"

class LHEEvent_Hwithdecay(LHEEvent):
    def __init__(self, event, isgen):
        super().__init__(event, isgen)

    def extracteventparticles(self):
        daughters, mothers, associated = [], [], []
        ids = [None]
        mother1s = [None]
        mother2s = [None]
        for line in self.lines:
            id, status, mother1, mother2 = (int(_) for _ in line.split()[0:4])
            ids.append(id)
            if (1 <= abs(id) <= 6 or abs(id) == 21) and not self.isgen:
                line = line.replace(str(id), "0", 1)  #replace the first instance of the jet id with 0, which means unknown jet
            mother1s.append(mother1)
            mother2s.append(mother2)
            if status == -1:
                mothers.append(line)
            elif status == 1 and (1 <= abs(id) <= 6 or 11 <= abs(id) <= 16 or abs(id) in (21, 22)):
                while True:
                    if mother1 != mother2 or mother1 is None:
                        associated.append(line)
                        break
                    if ids[mother1] in (25, 39):
                        daughters.append(line)
                        break
                    mother2 = mother2s[mother1]
                    mother1 = mother1s[mother1]

        if not self.isgen: mothers = None
        return daughters, associated, mothers

class LHEEvent_HwithdecayOnly(LHEEvent):
    def __init__(self, event, isgen):
        super().__init__(event, isgen)

    def extracteventparticles(self):
        daughters, mothers, associated = [], [], []
        ids = [None]
        mother1s = [None]
        mother2s = [None]
        for line in self.lines:
            try:
                id, status, mother1, mother2 = (int(_) for _ in line.split()[0:4])
            except:
                continue

            ids.append(id)
            if (1 <= abs(id) <= 6 or abs(id) == 21) and not self.isgen:
                line = line.replace(str(id), "0", 1)  #replace the first instance of the jet id with 0, which means unknown jet
            mother1s.append(mother1)
            mother2s.append(mother2)
            if status == -1:
                mothers.append(line)
            if(abs(id) == 22 ):
                associated.append(line)
            if ( 11 <= abs(id) <= 16 ):
                daughters.append(line)

        if not self.isgen: mothers = []
        return daughters, associated, mothers

class LHEEvent_StableHiggs(LHEEvent):
    def __init__(self, event, isgen):
        super().__init__(event, isgen)
    
    def extracteventparticles(self):
        daughters, mothers, associated = [], [], []
        for line in self.lines:
            id, status, mother1, mother2 = (int(_) for _ in line.split()[0:4])
            if (1 <= abs(id) <= 6 or abs(id) == 21) and not self.isgen:
                line = line.replace(str(id), "0", 1)  #replace the first instance of the jet id with 0, which means unknown jet
            if status == -1:
                mothers.append(line)
            if id == 25:
                if status != 1:
                    raise ValueError("Higgs has status {}, expected it to be 1\n\n".format(status) + "\n".join(self.lines))
                daughters.append(line)

            if abs(id) in (0, 1, 2, 3, 4, 5, 11, 12, 13, 14, 15, 16, 21) and status == 1:
                associated.append(line)

        if len(daughters) != 1:
            raise ValueError("More than one H in the event??\n\n"+"\n".join(self.lines))
        if self.nassociatedparticles is not None and len(associated) != self.nassociatedparticles:
            raise ValueError("Wrong number of associated particles (expected {}, found {})\n\n".format(self.nassociatedparticles, len(associated))+"\n".join(self.lines))
        if len(mothers) != 2:
            raise ValueError("{} mothers in the event??\n\n".format(len(mothers))+"\n".join(self.lines))

        if not self.isgen: mothers = []
        return daughters, associated, mothers

    nassociatedparticles = None


class LHEEvent_StableHiggsVH(LHEEvent):
    def __init__(self, event, isgen):
        super().__init__(event, isgen)

    def extracteventparticles(self):
        daughters, mothers, associated = [], [], []
        ids = [None]
        mother1s = [None]
        mother2s = [None]
        for line in self.lines:
            id, status, mother1, mother2 = (int(_) for _ in line.split()[0:4])
            ids.append(id)

            mother1s.append(mother1)
            mother2s.append(mother2)
            if status == -1:
                mothers.append(line)
            elif id == 25:
                daughters.append(line)
            elif status == 1 and (1 <= abs(id) <= 6 or 11 <= abs(id) <= 16 or abs(id) in (21, 22)):

                if mother1 is None or ids is None or mother1s[mother1] is None :
                    continue

                if mother1 == mother2 and abs(ids[mother1]) in (23,24) and not ids[mother1s[mother1]] == 25 :
                    associated.append(line)

        if not self.isgen: mothers = []
        return daughters, associated, mothers


class LHEEvent_VHHiggsdecay(LHEEvent):
    def __init__(self, event, isgen):
        super().__init__(event, isgen)

    def extracteventparticles(self):
        daughters, mothers, associated = [], [], []
        ids = [None]
        mother1s = [None]
        mother2s = [None]
        for line in self.lines:
            id, status, mother1, mother2 = (int(_) for _ in line.split()[0:4])
            ids.append(id)

            mother1s.append(mother1)
            mother2s.append(mother2)
            if status == -1:
                mothers.append(line)
            elif status == 1 and (1 <= abs(id) <= 6 or 11 <= abs(id) <= 16 or abs(id) in (21, 22)):
        
                if mother1 is None or ids is None or mother1s[mother1] is None :
                    continue
          
                if mother1 == mother2 and abs(ids[mother1]) in (23,24) and  not ids[mother1s[mother1]] == 25 :
                    associated.append(line)
            
                if mother1 == mother2 and abs(ids[mother1]) == 23 and  ids[mother1s[mother1]] == 25:
                    daughters.append(line)
            
        if not self.isgen: mothers = []
        return daughters, associated, mothers


class LHEEvent_StableHiggsZHHAWK(LHEEvent):
    def __init__(self, event, isgen):
        super().__init__(event, isgen)

    def extracteventparticles(self):
        daughters, mothers, associated = [], [], []
        for line in self.lines:
            id, status, mother1, mother2 = (int(_) for _ in line.split()[0:4])
            if (1 <= abs(id) <= 6 or abs(id) == 21) and not self.isgen:
                line = line.replace(str(id), "0", 1)  #replace the first instance of the jet id with 0, which means unknown jet
            if status == -1:
                mothers.append(line)
            if id == 25:
                if status != 1:
                    raise ValueError("Higgs has status {}, expected it to be 1\n\n".format(status) + "\n".join(lines))
                daughters.append(line)
            
            if abs(id) in (0, 1, 2, 3, 4, 5, 11, 12, 13, 14, 15, 16, 21,22) and status == 1:
                associated.append(line)

        if len(daughters) != 1:
            raise ValueError("More than one H in the event??\n\n"+"\n".join(self.lines))
        if self.nassociatedparticles is not None and len(associated) != self.nassociatedparticles:
            raise ValueError("Wrong number of associated particles (expected {}, found {})\n\n".format(self.nassociatedparticles, len(associated))+"\n".join(lines))
        if len(mothers) != 2:
            raise ValueError("{} mothers in the event??\n\n".format(len(mothers))+"\n".join(self.lines))

        if not self.isgen: mothers = []
        return daughters, associated, mothers

    nassociatedparticles = None

def main(raw_args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("outputfile")
    parser.add_argument("inputfile", nargs="+")
    g = parser.add_mutually_exclusive_group(required=True)
    g.add_argument("--vbf", action="store_true")
    g.add_argument("--vbf_withdecay", action="store_true")
    g.add_argument("--zh", action="store_true")
    g.add_argument("--zh_withdecay", action="store_true")
    g.add_argument("--zh_lep", action="store_true")
    g.add_argument("--zh_lep_hawk", action="store_true")
    g.add_argument("--wh_withdecay", action="store_true")
    g.add_argument("--wh_lep", action="store_true")
    g.add_argument("--wh", action="store_true")
    g.add_argument("--ggH4l", action="store_true") # for ggH 4l JHUGen and prophecy  
    g.add_argument("--ggH4lMG", action="store_true") # for ggH4l Madgraph with weights
    parser.add_argument("--use_flavor", action="store_true")
    parser.add_argument("--merge_photon", action="store_true") # for ggH 4l JHUGen and prophecy
    parser.add_argument("--calc_prodprob", action="store_true")
    parser.add_argument("--calc_decayprob", action="store_true")
    parser.add_argument("--CJLST", action="store_true")
    parser.add_argument("--MELAcalc", action="store_true")
    parser.add_argument('-v', '--verbose', action="store_true") #if enabled it will be verbose
    parser.add_argument('-n', '--n_events', type=int, default=-1)
    parser.add_argument("-t", "--tree_name", type=str, default="tree")
    args = parser.parse_args(raw_args) #This allows the parser to take in command line arguments if raw_args=None

    if os.path.exists(args.outputfile): 
        raise IOError(args.outputfile+" already exists")
    
    for i in args.inputfile:
        if not os.path.exists(i) and not args.CJLST:
            raise IOError(i+" doesn't exist")
    
    t = {}
    c = {}

    branchnames_scalar = ("costheta1", "costheta2", "Phi1", "costhetastar", "Phi", "HJJpz","M4L","MZ1","MZ2","costheta1d","costheta2d","Phid","costhetastard","Phi1d")
    if args.zh or args.wh or args.zh_withdecay or args.wh_withdecay or args.zh_lep or args.wh_lep or args.zh_lep_hawk:
        branchnames_scalar += ("mV", "mVstar", "pxj1", "pyj1", "pzj1", "Ej1", "pxj2", "pyj2", "pzj2", "Ej2", "ptV")
    elif args.vbf or args.vbf_withdecay:
        branchnames_scalar += ("q2V1", "q2V2","Dphijj")
    
    branchnames_scalar += (
        "ptdau1","pxdau1","pydau1","pzdau1","Edau1","flavdau1", 
        "ptdau2","pxdau2","pydau2","pzdau2","Edau2","flavdau2",
        "ptdau3","pxdau3","pydau3","pzdau3","Edau3","flavdau3",
        "ptdau4","pxdau4","pydau4","pzdau4","Edau4","flavdau4",
        
        "ptH", "pxH",  "pyH",  "pzH",  "EH","rapH","rapHJJ","decayMode","qfl1","qfl2","qfl1mom","qfl2mom",
        "pxj1", "pyj1", "pzj1", "Ej1",
        "pxj2", "pyj2", "pzj2", "Ej2",
        "pxph1","pyph1","pzph1","Eph1",
        "weight",
    )
    
    branchnames_vector = tuple()
    if args.MELAcalc:
        branchnames_vector += ("LHEDaughterId","LHEDaughterPt","LHEDaughterEta","LHEDaughterPhi","LHEDaughterMass")
        branchnames_vector += ("LHEAssociatedParticleId","LHEAssociatedParticlePt","LHEAssociatedParticleEta","LHEAssociatedParticlePhi","LHEAssociatedParticleMass")
        branchnames_vector += ("LHEMotherId","LHEMotherPx","LHEMotherPy", "LHEMotherPz", "LHEMotherE")

    all_events = []
    for inputfile in args.inputfile:
        reader = lhe_reader.lhe_reader(inputfile)
        all_events += reader.all_events
        c[inputfile] = reader.cross_section
        del reader, inputfile

    for branch in branchnames_scalar:
        t[branch] = np.zeros(len(all_events), dtype=np.single)
    for branch in branchnames_vector:
        t[branch] = np.zeros( (len(all_events), 4), dtype=np.single )

    if args.ggH4l:
        inputfclass = LHEEvent_HwithdecayOnly
    elif args.vbf or args.zh_lep or args.wh_lep:
        inputfclass = LHEEvent_StableHiggs
    elif args.zh or args.wh:
        inputfclass = LHEEvent_StableHiggsVH
    elif args.zh_withdecay or args.wh_withdecay:
        inputfclass = LHEEvent_VHHiggsdecay
    elif args.zh_lep_hawk:
        inputfclass = LHEEvent_StableHiggsZHHAWK
    else:
        inputfclass = LHEEvent_Hwithdecay

    if args.n_events > 0:
        all_events = all_events[:min(len(all_events), args.n_events)]
    
    m = Mela.Mela()
    if args.zh or args.zh_withdecay:
        production = Mela.Production.Had_ZH
    elif args.wh or args.wh_withdecay:
        production = Mela.Production.Had_WH
    elif args.vbf or args.vbf_withdecay:
        production = Mela.Production.JJVBF
    elif args.zh_lep or args.zh_lep_hawk:
        production = Mela.Production.Lep_ZH
    elif args.wh_lep:
        production = Mela.Production.Lep_WH
    elif args.ggH4l or args.ggH4l_MG:
        production = Mela.Production.ZZGG
    
    
    for i, event in tqdm.tqdm(enumerate(all_events), total=len(all_events)):
        
        
        m.setProcess(Mela.Process.SelfDefine_spin0, Mela.MatrixElement.JHUGen, production)
        the_event = inputfclass(event, True)
        m.setInputEvent(the_event.daughters, the_event.associated, the_event.mothers, True, False)

        if args.ggH4l or args.ggH4lMG:
            t['M4L'][i], t['MZ2'][i], t['MZ1'][i], t['costheta1d'][i], t['costheta2d'][i], t['Phid'][i], t['costhetastard'][i], t['Phi1d'][i] = m.computeDecayAngles()
        
        associated_list = [MELA_simpleParticle_toVector(particle) for particle in the_event.associated.toList()]
        daughter_list = [MELA_simpleParticle_toVector(particle) for particle in the_event.daughters.toList()]
        mothers_list = [MELA_simpleParticle_toVector(particle) for particle in the_event.mothers.toList()] if args.use_flavor else []
        
        t["weight"][i] = the_event.weight
        for rwgt_id in the_event.weights.keys():
            if i == 0:
                t[f"weight_{rwgt_id}"] = np.zeros( (len(all_events)), dtype=np.single )

            t[f"weight_{rwgt_id}"][i] = the_event.weights[rwgt_id]
                
        
        higgs = vector.obj(px=0, py=0, pz=0, E=0)
        for p, id_and_vec in enumerate(daughter_list):
            id, vec = id_and_vec
            higgs += vec
            t[f"flavdau{p+1}"][i] = id
            t[f"ptdau{p+1}"][i] =   vec.pt
            t[f"pxdau{p+1}"][i] =   vec.px
            t[f"pydau{p+1}"][i] =  vec.py
            t[f"pzdau{p+1}"][i] =  vec.pz
            t[f"Edau{p+1}"][i] = vec.E
        
        t["ptH"][i] = higgs.pt
        t["pxH"][i] = higgs.px
        t["pyH"][i] = higgs.py
        t["pzH"][i] = higgs.pz
        t["EH"][i] = higgs.E
        t["rapH"][i] = higgs.rapidity
            
        if args.vbf or args.zh or args.wh  or args.zh_lep_hawk:
            for p, id_and_vec in enumerate(associated_list):
                id, vec = id_and_vec
                t[f"pxj{p+1}"][i] =   vec.px
                t[f"pyj{p+1}"][i] =  vec.py
                t[f"pzj{p+1}"][i] =  vec.pz
                t[f"Ej{p+1}"][i] = vec.E
        
        if args.MELAcalc:
            for p, id_and_vec in enumerate(associated_list):
                id, vec = id_and_vec
                t["LHEAssociatedParticleId"][i][p] =   id
                t["LHEAssociatedParticlePt"][i][p] =   vec.pt
                t["LHEAssociatedParticleEta"][i][p] =  vec.eta
                t["LHEAssociatedParticlePhi"][i][p] =  vec.phi
                t["LHEAssociatedParticleMass"][i][p] = vec.M
            
            
            for p, id_and_vec in enumerate(daughter_list):
                id, vec = id_and_vec
                t["LHEDaughterId"][i][p] = id
                t["LHEDaughterPt"][i][p] =   vec.pt
                t["LHEDaughterEta"][i][p] =  vec.eta
                t["LHEDaughterPhi"][i][p] =  vec.phi
                t["LHEDaughterMass"][i][p] = vec.M
            
            for p, id_and_vec in enumerate(mothers_list):
                id, vec = id_and_vec
                t["LHEMotherId"][i][p] = id
                t["LHEMotherPx"][i][p] = vec.px
                t["LHEMotherPy"][i][p] = vec.py
                t["LHEMotherPz"][i][p] = vec.pz
                t["LHEMotherE"][i][p] =  vec.E
            
    
    with uproot.recreate(args.outputfile) as newf:
        newf[args.tree_name] = t
        newf["CrossSection"] = c

if __name__ == "__main__":
    errorfile = open("error.txt", 'w+')
    main()
