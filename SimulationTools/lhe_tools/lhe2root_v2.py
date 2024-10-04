#!/usr/bin/env python
import abc
import re
import argparse, os
import warnings
import numpy as np
import tqdm

import lhe_reader
import uproot
import vector

import Mela
import multiprocessing

def check_enum(entry):
    if entry.lower() == "noprod":
        return entry
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
        if not isgen:
            self.mothers = None
        else:
            self.mothers =    Mela.SimpleParticleCollection_t([LHE_line_to_simpleParticle_t(line) for line in mothers_lhe])

    @abc.abstractmethod
    def extracteventparticles(self): "has to be a classmethod that returns daughters, associated, mothers"

class LHEEvent_Hwithdecay(LHEEvent):
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

class NLO_qqH_DecayOnly(LHEEvent):
    def __init__(self, event, isgen, ignore_quark_gluon_events=False):
        self.ignore_quark_gluon_events = ignore_quark_gluon_events
        super().__init__(event, isgen)
        if not self.ignore_quark_gluon_events:
            for n, mother_particle in enumerate(self.mothers): #reset the id value
                if mother_particle.id == 21:
                    if n == 0:
                        replace = 1
                    else:
                        replace = 0
                    mother_particle.id = -self.mothers.toList()[replace].id

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
                if self.ignore_quark_gluon_events and id == 21:
                    return [], [], []
                mothers.append(line)
            elif (11 <= abs(id) <= 16) and status == 1:
                daughters.append(line)
            elif status == 1:
                associated.append(line)

        if not self.isgen: mothers = []
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
            try: 
                id, status, mother1, mother2 = (int(_) for _ in line.split()[0:4])
                ids.append(id)
            except:
                continue

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
        # print(associated)
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
        "qqH_ignore", "qqH",
        "decayonly_default"
        ]
    PRODUCTION_OPTIONS = [
        "JJVBF", "ZZGG",
        "Had_ZH", "Lep_ZH",
        "Had_WH", "Lep_WH",
        "ZZQQB",
        "noprod", 
        "VH"
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
    parser.add_argument("-d", "--drop_nonzero", action="store_true")
    parser.add_argument("-nAssoc", "--numAssociated", type=int, default=2, help="Allocates N associated particles. Default is 2.")
    parser.add_argument("-nDaughters", "--numDaughters", type=int, default=4, help="Allocates N final-state leptons. Default is 4.")
    parser.add_argument("-nMothers", "--numMothers", type=int, default=2, help="Allocates N mother particles. Default is 2.")
    args = parser.parse_args(raw_args) #This allows the parser to take in command line arguments if raw_args=None

    drop_nonzero = args.drop_nonzero
    mode = args.mode


    if args.production not in ["noprod", "VH"]:
        production = eval(f"Mela.Production.{args.production}")
    elif args.production == "VH":
        production = "VH"
    else:
        production = None #Just as a placeholder

    if os.path.exists(args.outputfile) and not args.overwrite:
        raise IOError(args.outputfile+" already exists")
    
    for i in args.inputfile:
        if not os.path.exists(i) and not args.CJLST:
            raise IOError(i+" doesn't exist")
    
    t = {}
    c = {}

    branchnames_scalar = ("M4L","MTotal")
    if production is not None:
        branchnames_scalar += (
            "MZ1","MZ2","costheta1d","costheta2d","Phid","costhetastard","Phi1d"
        )
        if production == Mela.Production.JJVBF:
            branchnames_scalar += (
                "costheta1", "costheta2", "Phi1", "costhetastar", "Phi"
            )
    else:
        branchnames_scalar += (
            "MZ1","MZ2"
        )

    if production in (Mela.Production.Had_ZH, Mela.Production.Lep_ZH, Mela.Production.Had_WH, Mela.Production.Lep_WH, "VH"):
        branchnames_scalar += ("mV", "mVstar", "pxj1", "pyj1", "pzj1", "Ej1", "pxj2", "pyj2", "pzj2", "Ej2", "ptV", "rapHJJ", "costheta1", "costheta2", "Phi", "costhetastar", "Phi1")
    elif production in (Mela.Production.JJVBF, ):
        branchnames_scalar += ("q2V1", "q2V2","Dphijj", "rapHJJ", "HJJpz", "mJJ", "DRjj", "ptj1", "ptj2")
    
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
    
    branchnames_vector = dict()
    if not args.no_mothers:
        branchnames_vector.update({
            "LHEDaughterId" : args.numDaughters,
            "LHEDaughterPt" : args.numDaughters,
            "LHEDaughterEta" : args.numDaughters,
            "LHEDaughterPhi" : args.numDaughters,
            "LHEDaughterMass" : args.numDaughters
        })
        branchnames_vector.update({
            "LHEAssociatedParticleId" : args.numAssociated,
            "LHEAssociatedParticlePt" : args.numAssociated,
            "LHEAssociatedParticleEta" : args.numAssociated,
            "LHEAssociatedParticlePhi" : args.numAssociated,
            "LHEAssociatedParticleMass" : args.numAssociated
        })
        branchnames_vector.update({
            "LHEMotherId" : args.numMothers,
            "LHEMotherPx" : args.numMothers,
            "LHEMotherPy" : args.numMothers,
            "LHEMotherPz" : args.numMothers,
            "LHEMotherE" : args.numMothers
        })

    all_events = []
    for inputfile in args.inputfile:
        reader = lhe_reader.lhe_reader(inputfile)
        try:
            c[inputfile] = reader.cross_section
        except:
            warnings.warn(inputfile, " has a corrupted header and xsec cannot be read!")
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
    for branch, vector_length in branchnames_vector.items():
        t[branch] = np.zeros( (len(all_events), vector_length), dtype=np.single )
    del branch

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
    elif mode in ("qqH_ignore", "qqH"):
        inputfclass = NLO_qqH_DecayOnly
    else:
        inputfclass = LHEEvent_DecayOnly

    if args.n_events > 0:
        all_events = all_events[:min(len(all_events), args.n_events)]
    all_events = tuple(all_events)
    if production is not None:
        # m = Mela.Mela(13, 125, Mela.VerbosityLevel.DEBUG_MECHECK)
        m = Mela.Mela()
    else:
        m = None

    # events = [inputfclass(event, True) for event in all_events]
    # associated_particles = [tuple(map(MELA_simpleParticle_toVector, i.associated.toList())) for i in events]
    # daughter_particles = [tuple(map(MELA_simpleParticle_toVector, i.daughters.toList())) for i in events]
    # mother_particles = [tuple(map(MELA_simpleParticle_toVector, i.mothers.toList())) for i in events]


    zero_events = []
    for i, event in tqdm.tqdm(enumerate(all_events), total=len(all_events), desc="Converting..."):
        if mode == "qqH_ignore":
            the_event = inputfclass(event, not args.no_mothers, True)
        else:
            the_event = inputfclass(event, not args.no_mothers)

        associated_list = tuple([MELA_simpleParticle_toVector(particle) for particle in the_event.associated.toList()])
       # print("this is assoclist: ", associated_list)
        daughter_list   = tuple([MELA_simpleParticle_toVector(particle) for particle in the_event.daughters.toList()])
       # print("this is daughters' list: ", daughter_list)
        if not args.no_mothers:
            mothers_list    = tuple([MELA_simpleParticle_toVector(particle) for particle in the_event.mothers.toList()]) if not args.remove_flavor else []
        #    print("this is mothers list: ", mothers_list)
        else:
            mothers_list = None
        #    print("No mothers")

        if len(daughter_list) == 0:
            zero_events.append(i)
            continue

        if m is not None and production != "VH":
            m.setProcess(Mela.Process.SelfDefine_spin0, Mela.MatrixElement.JHUGen, production)
            m.setInputEvent(the_event.daughters, the_event.associated, the_event.mothers, True)

        t['MTotal'][i] = sum( [p[1] for p in daughter_list] + [p[1] for p in associated_list], vector.obj(px=0, py=0, pz=0, E=0)).M

        if production is None:
            t['M4L'][i] = sum( [p[1] for p in daughter_list], vector.obj(px=0, py=0, pz=0, E=0)).M
            
            highest_pair = (None, None, 0) #the higher Z Mass is MZ1
            for n, p in enumerate(daughter_list):
                for nn, pp in enumerate(daughter_list[n+1:]):
                    if p[0]*pp[0] > 0:
                        continue
                    mass = (p[1] + pp[1]).M
                    if mass > highest_pair[2]:
                        highest_pair = (n, nn+n+1, mass)
            del n, p, nn, pp, mass

            highest_pair = np.array(highest_pair[:2]) #remove the mass part
            t['MZ1'][i] = sum([p[1] for n, p in enumerate(daughter_list) if n in highest_pair], vector.obj(px=0, py=0, pz=0, E=0)).M
            t['MZ2'][i] = sum([p[1] for n, p in enumerate(daughter_list) if n not in highest_pair], vector.obj(px=0, py=0, pz=0, E=0)).M
            del highest_pair

        elif production in (Mela.Production.ZZGG, Mela.Production.ZZQQB):
            t['M4L'][i], t['MZ2'][i], t['MZ1'][i], t['costheta1d'][i], t['costheta2d'][i], t['Phid'][i], t['costhetastard'][i], t['Phi1d'][i] = m.computeDecayAngles()
            
        elif production in (Mela.Production.Had_ZH, Mela.Production.Lep_ZH, Mela.Production.Had_WH, Mela.Production.Lep_WH):
            t["mV"][i], t["mVstar"][i], t["costheta1"][i], t["costheta2"][i], t["Phi"][i], t["costhetastar"][i], t["Phi1"][i]= m.computeVHAngles(production)
            t['M4L'][i], t['MZ2'][i], t['MZ1'][i], t['costheta1d'][i], t['costheta2d'][i], t['Phid'][i], t['costhetastard'][i], t['Phi1d'][i] = m.computeDecayAngles()
        
        elif production == "VH":
            if associated_list[0][0] in  [11, -11, 12, -12, 13, -13, 14, -14, 15, -15, 16, -16] and (associated_list[0][0] + associated_list[1][0]) == 0:
                m.setProcess(Mela.Process.SelfDefine_spin0, Mela.MatrixElement.JHUGen, Mela.Production.Lep_ZH)
                m.setInputEvent(the_event.daughters, the_event.associated, the_event.mothers, True)
                t["mV"][i], t["mVstar"][i], t["costheta1"][i], t["costheta2"][i], t["Phi"][i], t["costhetastar"][i], t["Phi1"][i]= m.computeVHAngles(Mela.Production.Lep_ZH)
                t['M4L'][i], t['MZ2'][i], t['MZ1'][i], t['costheta1d'][i], t['costheta2d'][i], t['Phid'][i], t['costhetastard'][i], t['Phi1d'][i] = m.computeDecayAngles()

            elif associated_list[0][0] in  [11, -11, 12, -12, 13, -13, 14, -14, 15, -15, 16, -16] and (associated_list[0][0] + associated_list[1][0]) != 0:
                m.setProcess(Mela.Process.SelfDefine_spin0, Mela.MatrixElement.JHUGen, Mela.Production.Lep_WH)
                m.setInputEvent(the_event.daughters, the_event.associated, the_event.mothers, True)
                t["mV"][i], t["mVstar"][i], t["costheta1"][i], t["costheta2"][i], t["Phi"][i], t["costhetastar"][i], t["Phi1"][i]= m.computeVHAngles(Mela.Production.Lep_WH)
                t['M4L'][i], t['MZ2'][i], t['MZ1'][i], t['costheta1d'][i], t['costheta2d'][i], t['Phid'][i], t['costhetastard'][i], t['Phi1d'][i] = m.computeDecayAngles()
        
            elif associated_list[0][0] in [1, -1, 2, -2, 3, -3, 4, -4, 5, -5, 6, -6] and  (associated_list[0][0] + associated_list[1][0]) == 0 :
                m.setProcess(Mela.Process.SelfDefine_spin0, Mela.MatrixElement.JHUGen, Mela.Production.Had_ZH)
                m.setInputEvent(the_event.daughters, the_event.associated, the_event.mothers, True)
                t["mV"][i], t["mVstar"][i], t["costheta1"][i], t["costheta2"][i], t["Phi"][i], t["costhetastar"][i], t["Phi1"][i]= m.computeVHAngles(Mela.Production.Had_ZH)
                t['M4L'][i], t['MZ2'][i], t['MZ1'][i], t['costheta1d'][i], t['costheta2d'][i], t['Phid'][i], t['costhetastard'][i], t['Phi1d'][i] = m.computeDecayAngles()

            elif associated_list[0][0] in [1, -1, 2, -2, 3, -3, 4, -4, 5, -5, 6, -6] and  (associated_list[0][0] + associated_list[1][0]) != 0 :
                m.setProcess(Mela.Process.SelfDefine_spin0, Mela.MatrixElement.JHUGen, Mela.Production.Had_WH)
                m.setInputEvent(the_event.daughters, the_event.associated, the_event.mothers, True)
                t["mV"][i], t["mVstar"][i], t["costheta1"][i], t["costheta2"][i], t["Phi"][i], t["costhetastar"][i], t["Phi1"][i]= m.computeVHAngles(Mela.Production.Had_WH)
                t['M4L'][i], t['MZ2'][i], t['MZ1'][i], t['costheta1d'][i], t['costheta2d'][i], t['Phid'][i], t['costhetastard'][i], t['Phi1d'][i] = m.computeDecayAngles()

        elif production == Mela.Production.JJVBF:
            t["HJJpz"][i] = sum( [p[1] for p in daughter_list] + [p[1] for p in associated_list], vector.obj(px=0, py=0, pz=0, E=0)).pz
            t["q2V1"][i], t["q2V2"][i], t["costheta1"][i], t["costheta2"][i], t["Phi"][i], t["costhetastar"][i], t["Phi1"][i]= m.computeVBFAngles()
            t["mJJ"][i] = (associated_list[0][1] + associated_list[1][1]).M

            if associated_list[0][1].pt > associated_list[1][1].pt:
                t["Dphijj"][i] = associated_list[0][1].deltaphi(associated_list[1][1])
                t["DRjj"][i] = associated_list[0][1].deltaR(associated_list[1][1])
            else:
                t["Dphijj"][i] = associated_list[1][1].deltaphi(associated_list[0][1])
                t["DRjj"][i] = associated_list[1][1].deltaR(associated_list[0][1])

            t["ptj1"][i] = associated_list[0][1].pt
            t["ptj2"][i] = associated_list[1][1].pt 

            
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
        
        if production in (Mela.Production.JJVBF, Mela.Production.Lep_ZH, Mela.Production.Had_ZH, Mela.Production.Had_WH, Mela.Production.Lep_WH, "VH"):
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
            
    zero_events = np.array(zero_events, dtype=int)
    if drop_nonzero:
        for branch, item in t.items():
            t[branch] = np.delete(item, zero_events, axis=0)
    with uproot.recreate(args.outputfile) as newf:
        newf[args.tree_name] = t
        for filename, (cross_section, err) in c.items():
            f_dumped = filename.split("/")[-1]
            newf[f"CrossSection/{f_dumped}"] = {"Value":[cross_section], "Uncertainty":[err]}

if __name__ == "__main__":
    errorfile = open("error.txt", 'w+')
    main()
