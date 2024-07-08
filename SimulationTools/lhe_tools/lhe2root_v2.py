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

def check_enum(entry):
    found = False
    i = 0
    possible_value = tuple(Mela.Production.__dict__['__entries'].keys())
    while (not found) and (i < len(possible_value)):
        if entry.lower() == possible_value[i].lower():
            found = True
            entry = possible_value[i]
        i += 1
    if not found:
        possible_value = tuple(map(str.lower, possible_value))
        errortext = "Unknown Production Mode given!"
        errortext += "\nThe following are valid Production modes"
        errortext += "\n" + "\n".join(possible_value)
        raise ValueError("\n" + errortext)
    return entry

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

class LHEEvent_DecayOnly(LHEEvent):
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
            elif (11 <= abs(id) <= 16) and status == 1:
                daughters.append(line)
            elif status == 1:
                associated.append(line)

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
                    raise ValueError("Higgs has status {}, expected it to be 1\n\n".format(status) + "\n".join(self.lines))
                daughters.append(line)
            
            if abs(id) in (0, 1, 2, 3, 4, 5, 11, 12, 13, 14, 15, 16, 21,22) and status == 1:
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

def main(raw_args=None):
    LHE2ROOT_OPTIONS = [
        "vbf", "vbf_withdecay", 
        "zh", "zh_withdecay", "zh_lep", "zh_lep_hawk",
        "wh_withdecay", "wh_lep", "wh",
        "ggh4l", "ggh4lmg",
        "decayonly_default"
        ]
    PRODUCTION_OPTIONS = [
        "JJVBF", "ZZGG",
        "Had_ZH", "Lep_ZH",
        "Had_WH", "Lep_WH"
    ]
    parser = argparse.ArgumentParser()
    parser.add_argument("outputfile")
    parser.add_argument("inputfile", nargs="+")
    parser.add_argument("-m", "--mode", default="decayonly_default", type=str, choices=LHE2ROOT_OPTIONS)
    parser.add_argument("-p", "--production", type=check_enum, required=True, choices=PRODUCTION_OPTIONS)
    parser.add_argument("--remove_flavor", action="store_true")
    parser.add_argument("--merge_photon", action="store_true") # for ggH 4l JHUGen and prophecy
    parser.add_argument("--CJLST", action="store_true")
    parser.add_argument("--no_mothers", action="store_true")
    parser.add_argument('-n', '--n_events', type=int, default=-1)
    parser.add_argument("-t", "--tree_name", type=str, default="tree")
    parser.add_argument("-ow", "--overwrite", action="store_true")
    args = parser.parse_args(raw_args) #This allows the parser to take in command line arguments if raw_args=None

    mode = args.mode
    production = eval(f"Mela.Production.{args.production}")

    if os.path.exists(args.outputfile) and not args.overwrite:
        raise IOError(args.outputfile+" already exists")
    
    for i in args.inputfile:
        if not os.path.exists(i) and not args.CJLST:
            raise IOError(i+" doesn't exist")
    
    t = {}
    c = {}

    branchnames_scalar = ("costheta1", "costheta2", "Phi1", "costhetastar", "Phi", "M4L","MZ1","MZ2","costheta1d","costheta2d","Phid","costhetastard","Phi1d")

    if production in (Mela.Production.Had_ZH, Mela.Production.Lep_ZH, Mela.Production.Had_WH, Mela.Production.Lep_WH):
        branchnames_scalar += ("mV", "mVstar", "pxj1", "pyj1", "pzj1", "Ej1", "pxj2", "pyj2", "pzj2", "Ej2", "ptV", "rapHJJ")
    elif production in (Mela.Production.JJVBF, ):
        branchnames_scalar += ("q2V1", "q2V2","Dphijj", "rapHJJ", "HJJpz", "mJJ")
    
    branchnames_scalar += (
        "ptdau1","pxdau1","pydau1","pzdau1","Edau1","flavdau1", 
        "ptdau2","pxdau2","pydau2","pzdau2","Edau2","flavdau2",
        "ptdau3","pxdau3","pydau3","pzdau3","Edau3","flavdau3",
        "ptdau4","pxdau4","pydau4","pzdau4","Edau4","flavdau4",
        
        "ptH", "pxH",  "pyH",  "pzH",  "EH", "rapH",
        "pxj1", "pyj1", "pzj1", "Ej1",
        "pxj2", "pyj2", "pzj2", "Ej2",
        "weight",
    )
    
    branchnames_vector = tuple()
    if not args.no_mothers:
        branchnames_vector += ("LHEDaughterId","LHEDaughterPt","LHEDaughterEta","LHEDaughterPhi","LHEDaughterMass")
        branchnames_vector += ("LHEAssociatedParticleId","LHEAssociatedParticlePt","LHEAssociatedParticleEta","LHEAssociatedParticlePhi","LHEAssociatedParticleMass")
        branchnames_vector += ("LHEMotherId","LHEMotherPx","LHEMotherPy", "LHEMotherPz", "LHEMotherE")

    all_events = []
    for inputfile in args.inputfile:
        reader = lhe_reader.lhe_reader(inputfile)
        try:
            c[inputfile] = reader.cross_section
        except:
            print(inputfile, " has a corrupted header and xsec cannot be read!")
            del reader, inputfile
            continue
        all_events += reader.all_events
        del reader, inputfile

    xsecs, sigmas = zip(*tuple(c.values()))
    xsecs = np.array(xsecs)
    sigmas = np.array(sigmas)
    weights = (1/sigmas)**2
    weighted_xsec = (xsecs*weights).sum()/weights.sum()
    c["xsec"] = (weighted_xsec, 1/(np.sqrt(weights).sum()))

    for branch in branchnames_scalar:
        t[branch] = np.zeros(len(all_events), dtype=np.single)
    for branch in branchnames_vector:
        t[branch] = np.zeros( (len(all_events), 4), dtype=np.single )

    if mode in ("ggh4l", "vbf_withdecay"):
        inputfclass = LHEEvent_Hwithdecay
    elif mode in ("vbf", "zh_lep", "wh_lep"):
        inputfclass = LHEEvent_StableHiggs
    elif mode in ("zh", "wh"):
        inputfclass = LHEEvent_StableHiggsVH
    elif mode in ("zh_withdecay", "wh_withdecay"):
        inputfclass = LHEEvent_VHHiggsdecay
    elif mode in ("zh_lep_hawk", ):
        inputfclass = LHEEvent_StableHiggsZHHAWK
    else:
        inputfclass = LHEEvent_DecayOnly

    if args.n_events > 0:
        all_events = all_events[:min(len(all_events), args.n_events)]
    all_events = tuple(all_events)
    m = Mela.Mela()

    # if mode in ("zh", "zh_withdecay"):
    #     production = Mela.Production.Had_ZH
    # elif mode in ("wh", "wh_withdecay"):
    #     production = Mela.Production.Had_WH
    # elif mode in ("vbf", "vbf_withdecay"):
    #     production = Mela.Production.JJVBF
    # elif mode in ("zh_lep", "zh_lep_hawk"):
    #     production = Mela.Production.Lep_ZH
    # elif mode in ("wh_lep", ):
    #     production = Mela.Production.Lep_WH
    # elif mode in ggH4l or args.ggH4l_MG:
    #     production = Mela.Production.ZZGG
    
    
    for i, event in tqdm.tqdm(enumerate(all_events), total=len(all_events), desc="Converting..."):
        
        
        m.setProcess(Mela.Process.SelfDefine_spin0, Mela.MatrixElement.JHUGen, production)
        the_event = inputfclass(event, True)
        m.setInputEvent(the_event.daughters, the_event.associated, the_event.mothers, True)
        
        associated_list = tuple([MELA_simpleParticle_toVector(particle) for particle in the_event.associated.toList()])
        daughter_list   = tuple([MELA_simpleParticle_toVector(particle) for particle in the_event.daughters.toList()])
        mothers_list    = tuple([MELA_simpleParticle_toVector(particle) for particle in the_event.mothers.toList()] if not args.remove_flavor else [])
        
        
        if production == Mela.Production.ZZGG:
            t['M4L'][i], t['MZ2'][i], t['MZ1'][i], t['costheta1d'][i], t['costheta2d'][i], t['Phid'][i], t['costhetastard'][i], t['Phi1d'][i] = m.computeDecayAngles()
            
        elif production in (Mela.Production.Had_ZH, Mela.Production.Lep_ZH, Mela.Production.Had_WH, Mela.Production.Lep_WH):
            t["mV"][i], t["mVstar"][i], t["costheta1"][i], t["costheta2"][i], t["Phi"][i], t["costhetastar"][i], t["Phi1"][i]= m.computeVHAngles(production)
            t['M4L'][i], t['MZ2'][i], t['MZ1'][i], t['costheta1d'][i], t['costheta2d'][i], t['Phid'][i], t['costhetastard'][i], t['Phi1d'][i] = m.computeDecayAngles()

        elif production == Mela.Production.JJVBF:
            t["HJJpz"][i] = sum( [p[1] for p in daughter_list] + [p[1] for p in associated_list], vector.obj(px=0, py=0, pz=0, E=0)).pz
            t["q2V1"][i], t["q2V2"][i], t["costheta1"][i], t["costheta2"][i], t["Phi"][i], t["costhetastar"][i], t["Phi1"][i]= m.computeVBFAngles()
            t["mJJ"][i] = (associated_list[0][1] + associated_list[1][1]).M

            if associated_list[0][1].pt > associated_list[1][1].pt:
                t["Dphijj"][i] = associated_list[0][1].deltaphi(associated_list[1][1])
            else:
                t["Dphijj"][i] = associated_list[1][1].deltaphi(associated_list[0][1])
            
            if mode in ("vbf_withdecay", "decayonly_default"):
                t['M4L'][i], t['MZ2'][i], t['MZ1'][i], t['costheta1d'][i], t['costheta2d'][i], t['Phid'][i], t['costhetastard'][i], t['Phi1d'][i] = m.computeDecayAngles()    
        
        t["weight"][i] = the_event.weight #This is the event weight
        for rwgt_id in the_event.weights.keys(): #This is the madgraph weight
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
            t[f"pydau{p+1}"][i] =   vec.py
            t[f"pzdau{p+1}"][i] =   vec.pz
            t[f"Edau{p+1}"][i] =    vec.E
        
        t["ptH"][i] =  higgs.pt
        t["pxH"][i] =  higgs.px
        t["pyH"][i] =  higgs.py
        t["pzH"][i] =  higgs.pz
        t["EH"][i] =   higgs.E
        t["rapH"][i] = higgs.rapidity
        
        if production in (Mela.Production.JJVBF, Mela.Production.Lep_ZH, Mela.Production.Had_ZH, Mela.Production.Had_WH, Mela.Production.Lep_WH):
            t["rapHJJ"][i] = sum( [p[1] for p in daughter_list] + [p[1] for p in associated_list], vector.obj(px=0, py=0, pz=0, E=0)).rapidity
            
        for p, id_and_vec in enumerate(associated_list):
            id, vec = id_and_vec
            t[f"pxj{p+1}"][i] =   vec.px
            t[f"pyj{p+1}"][i] =   vec.py
            t[f"pzj{p+1}"][i] =   vec.pz
            t[f"Ej{p+1}"][i] =    vec.E
        
        if not args.no_mothers:
            for p, id_and_vec in enumerate(associated_list):
                id, vec = id_and_vec
                t["LHEAssociatedParticleId"][i][p] =   id
                t["LHEAssociatedParticlePt"][i][p] =   vec.pt
                t["LHEAssociatedParticleEta"][i][p] =  vec.eta
                t["LHEAssociatedParticlePhi"][i][p] =  vec.phi
                t["LHEAssociatedParticleMass"][i][p] = vec.M
            
            
            for p, id_and_vec in enumerate(daughter_list):
                id, vec = id_and_vec
                t["LHEDaughterId"][i][p] =   id
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
        for filename, (cross_section, err) in c.items():
            f_dumped = filename.split("/")[-1]
            newf[f"CrossSection/{f_dumped}"] = {"Value":[cross_section], "Uncertainty":[err]}

if __name__ == "__main__":
    errorfile = open("error.txt", 'w+')
    main()
