# from ..JHUGenMELA.MELA.python.mela import Mela, TVar, SimpleParticle_t, SimpleParticleCollection_t
import ROOT, os, sys, numpy as np, uproot, shutil
sys.path.append('../JHUGenMELA/MELA/python/')
sys.path.append('../')

from mela import Mela, TVar, SimpleParticle_t, SimpleParticleCollection_t, TUtil
from tqdm import tqdm
from generic_helpers import print_msg_box

def tlv(pt, eta, phi, m):
    result = ROOT.TLorentzVector()
    result.SetPtEtaPhiM(pt, eta, phi, m)
    return result

def exportPath():
    os.system("export LD_LIBRARY_PATH=../JHUGenMELA/MELA/data/$SCRAM_ARCH/:${LD_LIBRARY_PATH}")

def addprobabilities(list_of_prob_dicts, infile, tTree, outfile, verbosity, 
                    is_gen=False, local_verbose=False, N_events=-1):
    
    
    assert os.path.exists(infile)
    #assert not os.path.exists(outfile)
    
    # if os.path.exists(outfile):
    #   for i in range(1000):
    #     if not os.path.exists(outfile.replace(".root", "_{}.root".format(i))): 
    #       outfile = outfile.replace(".root", "_{}.root".format(i))
    #       break
    
    #print(outfile)
    
    exportPath()
    m = Mela(13, 125, verbosity)#TVar.DEBUG_MECHECK) #<- this is the debugger!
    #Use it as another argument if you'd like to debug code
    #Always initialize MELA at m=125 GeV
    
    shutil.copy2(infile, outfile)
    
    f = uproot.open(infile)
    t = f[tTree]
    
    if N_events < 0:
        N_events = t.num_entries
    
    if is_gen:
        relevant_branches = [
            "LHEDaughterId", 
            "LHEDaughterPt", 
            "LHEDaughterEta", 
            "LHEDaughterPhi", 
            "LHEDaughterMass",
            "LHEAssociatedParticleId", 
            "LHEAssociatedParticlePt",
            "LHEAssociatedParticleEta",
            "LHEAssociatedParticlePhi", 
            "LHEAssociatedParticleMass",
            "LHEMotherId",
            "LHEMotherPz",
            "LHEMotherE"
        ]
    else:
        relevant_branches = [
            "LepLepId", 
            "LepPt", 
            "LepEta", 
            "LepPhi",
            "JetPt", 
            "JetEta",
            "JetPhi",
            "JetMass"
        ]
    if np.any([x not in t.keys() for x in relevant_branches]):
        try:
            os.remove(outfile)
        except:
            pass
        finally:
            raise KeyError("Invalid keys for MELAcalc!")

    t_data = t.arrays(relevant_branches, library='np')
    if local_verbose:
        print("The branches being used are:")
        print(*relevant_branches, sep='\n')
        print()
    
    probabilities = {}
    
    for prob_dict in list_of_prob_dicts:
        probabilities[prob_dict['name']] = np.full(t.num_entries, -1, dtype=np.float64)
        
        prob_name      = prob_dict['name']
        process        = prob_dict['process']
        production     = prob_dict['production']
        matrix_element = prob_dict['matrixelement']


        if 'particles' in prob_dict.keys():
            particles = prob_dict['particles']
        else:
            particles = dict()
        
        if 25 in particles.keys(): #sets the higgs mass and width
            hmass, hwidth  = particles[25]
            del particles[25] #higgs is a special case!
        else:
            hmass  = 125
            hwidth = 0.004
        
        calc_production = prob_dict['prod']
        calc_decay = prob_dict['dec']
        
        #The following quantities can be multi valued (i.e. you can have multiple couplings)
        couplings = prob_dict['couplings']
        
        
        if 'options' in prob_dict.keys():
            options = prob_dict['options']
        else:
            options = {'dummy':'you stupid'}
        
        
        if local_verbose: #This is the verbose printout area
            gigabox = []
            
            titular = "PROBABILITY BRANCH"
            infotext = "NAME = " + prob_name
            
            
            if 'hmass' in prob_dict.keys() and 'hwidth' in prob_dict.keys():
                infotext += f"\nM_H={hmass}, Ga_H={hwidth}"
            else:
                infotext += f"\nM_H=125, Ga_H=DEFAULT"
            
            for particle in particles.keys():
                infotext += f"\nM and Ga of {particle} = {particles[particle][0]}, {particles[particle][1]}"
            
            infotext = print_msg_box(infotext, title=titular)
            
            gigabox.append(infotext)
            
            infotext = print_msg_box(process + ", " + matrix_element + ", " + production, title="Process, Matrix Element, Production")
            gigabox.append(infotext)
            
            infotext = []
            for coupl in couplings:
                infotext.append(coupl + f" = {couplings[coupl]}")
            infotext = "\n".join(infotext)
            infotext = print_msg_box(infotext, title="Couplings")
            gigabox.append(infotext)
            
            infotext = "prod = " + str(calc_production) + "\nDec = " + str(calc_decay)
            infotext += "\nRunning "
            if calc_production and calc_decay:
                infotext += "ComputeProdDecP()"
            elif calc_production:
                infotext += "ComputeProdP()"
            elif calc_decay:
                infotext += "ComputeP()"
            else:
                raise ValueError("Need to select a probability calculation!")
            
            infotext = print_msg_box(infotext, title="Calculation Function")
            gigabox.append(infotext)
            
            infotext = []
            for option in options.keys():
                infotext += [f"{option} = {options[option]}"]
                # infotext += "\n"+option + "=" + options[option]
            infotext = print_msg_box("\n".join(infotext), title="Options set")
            gigabox.append(infotext)
            
            infotext = []
            for coupl in couplings.keys():
                infotext += [f"{coupl} = {couplings[coupl]}"]
            infotext = print_msg_box("\n".join(infotext), title="Couplings")
            gigabox.append(infotext)
            
            gigabox = print_msg_box("\n".join(gigabox), title=prob_name)
            print(gigabox)
            
            print('\n\n')
    
        try:
            MELA_process = eval("TVar." + process)
        except:
            errortext = process + " is not a valid TVar!"
            raise KeyError("\n" + print_msg_box(errortext, title="ERROR"))
        
        try: 
            MELA_matrix_element = eval("TVar." + matrix_element)
        except:
            errortext = matrix_element + " is not a valid TVar!"
            raise KeyError("\n" + print_msg_box(errortext, title="ERROR"))
        
        try:
            MELA_production = eval("TVar." + production)
        except:
            errortext = production + " is not a valid TVar!"
            raise KeyError("\n" + print_msg_box(errortext, title="ERROR"))
        
        if 'jetpt' in options.keys(): #JetPt_{JES,JER}_{Up,Down}
            JetPt = t[options['jetpt']].array(library='np')
        elif is_gen:
            JetPt = t_data['LHEAssociatedParticlePt']
        else:
            JetPt = t_data["JetPt"]
        
        match_hmass_exactly = False
        if "matchmh" in options.keys():
            match_hmass_exactly = t[options['matchmh']].array(library='np')
        
        for i in tqdm(range(N_events), position=0, leave=True, desc=prob_name):
            if is_gen:
                inputEventNum = 1
                
                leptons = [
                    SimpleParticle_t(
                        pid,
                        tlv(
                            pt,
                            eta,
                            phi,
                            m
                            )
                        ) for pid, pt, eta, phi, m in zip(
                            t_data["LHEDaughterId"][i],
                            t_data["LHEDaughterPt"][i], 
                            t_data["LHEDaughterEta"][i], 
                            t_data["LHEDaughterPhi"][i], 
                            t_data["LHEDaughterMass"][i]
                            )
                        ]
                leptons = SimpleParticleCollection_t(leptons)
                
                jets = [
                    SimpleParticle_t(
                        pid, 
                        tlv(
                            pt,
                            eta,
                            phi,
                            m
                            )
                        ) for pid, pt, eta, phi, m in zip(
                            t_data["LHEAssociatedParticleId"][i],
                            JetPt[i], 
                            t_data["LHEAssociatedParticleEta"][i], 
                            t_data["LHEAssociatedParticlePhi"][i], 
                            t_data["LHEAssociatedParticleMass"][i]
                        )
                    ]
                jets = SimpleParticleCollection_t(jets)
        
                mothers = [
                    SimpleParticle_t(
                        pid,
                        ROOT.TLorentzVector(
                            0, 
                            0, 
                            pz,
                            e
                            )
                        ) for pid, pz, e in zip(
                            t_data["LHEMotherId"][i], 
                            t_data["LHEMotherPz"][i], 
                            t_data["LHEMotherE"][i]
                        )
                    ]
                mothers = SimpleParticleCollection_t(mothers)
            else:
                inputEventNum = 0
                
                leptons = [
                    SimpleParticle_t(
                        pid,
                        tlv(
                            pt,
                            eta, 
                            phi,
                            0
                            )
                        ) for pid, pt, eta, phi in zip(
                            t_data["LepLepId"][i], 
                            t_data["LepPt"][i], 
                            t_data["LepEta"][i], 
                            t_data["LepPhi"][i], 
                        )
                ]
                leptons = SimpleParticleCollection_t(leptons)
                
                jets = [
                    SimpleParticle_t(
                        0, 
                        tlv(
                            pt,
                            eta,
                            phi,
                            m
                            )
                        ) for pt, eta, phi, m in zip(
                            JetPt[i], 
                            t_data["JetEta"][i], 
                            t_data["JetPhi"][i], 
                            t_data["JetMass"][i]
                        )
                    ]
                jets = SimpleParticleCollection_t(jets)
                
                mothers = 0
            
            if np.any(match_hmass_exactly):
                m.setMelaHiggsMassWidth(match_hmass_exactly[i], hwidth, 0) #Use the tree specified in matchmh to match the mass
            else:
                m.setMelaHiggsMassWidth(hmass,hwidth,0)
            
            # if z_changed:
            for particle in particles: #particle sets the ID
                TUtil.SetMass(particles[particle][0], particle)
                TUtil.SetDecayWidth(particles[particle][1], particle)
            
            # Setup event information depending on RECO or LHE level #
            m.setInputEvent(leptons, jets, mothers, inputEventNum)
            
            m.setProcess(MELA_process, MELA_matrix_element, MELA_production)
            
            # set_couplings_list = []
            special_cases = {"ghv1", "ghv2", "ghv4"}
            for coupl in couplings:
                if i == 0 and coupl not in dir(m) and coupl not in special_cases:
                    errortext = "Attribute " + coupl + " does not exist!"
                    raise ModuleNotFoundError("\n" + print_msg_box(errortext, title="ERROR"))
                    
                if 'ghz' or 'ghw' in coupl:
                    # set_couplings_list.append("m.differentiate_HWW_HZZ = True")
                    m.differentiate_HWW_HZZ = True
                
                if coupl not in special_cases:
                    # set_couplings_list.append("m." + coupl + " = couplings[coupl]")
                    setattr(m, coupl, couplings[coupl])
                ###### NOW BEGINS THE SPECIAL CASES ######
                elif 'ghv1' in coupl:
                    # set_couplings_list.append("m.ghz1 = couplings[coupl]")
                    # set_couplings_list.append("m.ghw1 = couplings[coupl]")
                    setattr(m, 'ghz1', couplings[coupl])
                    setattr(m, 'ghw1', couplings[coupl])
                elif 'ghv2' in coupl:
                    # set_couplings_list.append("m.ghz2 = couplings[coupl]")
                    # set_couplings_list.append("m.ghw2 = couplings[coupl]")
                    setattr(m, 'ghz2', couplings[coupl])
                    setattr(m, 'ghw2', couplings[coupl])
                elif 'ghv4' in coupl:
                    # set_couplings_list.append("m.ghz4 = couplings[coupl]")
                    # set_couplings_list.append("m.ghw4 = couplings[coupl]")
                    setattr(m, 'ghz4', couplings[coupl])
                    setattr(m, 'ghw4', couplings[coupl])
                else:
                    errortext = coupl + " Is an unhandled special case!"
                    raise ValueError("\n" + print_msg_box(errortext, title="ERROR")) #handles the "special cases"
        
            # set_couplings_str = "\n".join(set_couplings_list)
            # compiled_couplings = compile(set_couplings_str, "<string>", "exec")

            
            if 'BSM' in options.keys() and options['BSM'] == "AC": #jerry-rigged BSM calculation
                gha2_cpl       = couplings["gha2"]
                ghz2_cpl       = couplings["ghz2"]
                ghza2_cpl      = couplings["ghza2"]
                ghz1prime2_cpl = couplings["ghz1prime2"]
                gha4_cpl       = couplings["gha4"]
                ghz4_cpl       = couplings["ghz4"]
                ghza4_cpl      = couplings["ghza4"]
                
                sin2thetaW = 0.23119
                mZ = 91.1876 # [GeV]
                lambda_Z1 = 10*1000 # [TeV] -> [GeV]
            
                m.dV_A = 1 + (gha2_cpl - ghz2_cpl)*(1-sin2thetaW) + ghza2_cpl*(np.sqrt((1-sin2thetaW)/sin2thetaW) - 2*np.sqrt(sin2thetaW*(1-sin2thetaW)))
                m.dP_A = 1
                m.dM_A = 1
                m.dFour_A = (gha4_cpl - ghz4_cpl)*(1-sin2thetaW) + ghza4_cpl*(np.sqrt((1-sin2thetaW)/sin2thetaW) - 2*np.sqrt(sin2thetaW*(1-sin2thetaW)))

                m.dV_Z = 1 - 2*((sin2thetaW*(1-sin2thetaW))/(1-sin2thetaW-sin2thetaW))*(gha2_cpl-ghz2_cpl) - 2*np.sqrt(sin2thetaW*(1-sin2thetaW))*ghza2_cpl - (mZ**2)/(2*(1-sin2thetaW-sin2thetaW))*(ghz1prime2_cpl/lambda_Z1**2)
                m.dP_Z = 1 - sin2thetaW/(1-sin2thetaW-sin2thetaW)*(gha2_cpl-ghz2_cpl) - np.sqrt(sin2thetaW/(1-sin2thetaW))*ghza2_cpl - (mZ**2)/(2*(1-sin2thetaW-sin2thetaW))*(ghz1prime2_cpl/lambda_Z1**2)
                m.dM_Z = m.dP_Z
                m.dFour_Z = -np.sqrt(sin2thetaW/(1-sin2thetaW))*m.dFour_A

                m.dAAWpWm = 1
                m.dZAWpWm = m.dP_Z
                m.dZZWpWm = 2*m.dP_Z - 1
            
            if calc_decay and calc_production:
                probabilities[prob_name][i] = np.float64(m.computeProdDecP())
            elif calc_decay:
                probabilities[prob_name][i] = np.float64(m.computeP())
            elif calc_production:
                probabilities[prob_name][i] = np.float64(m.computeProdP())
            else:
                raise KeyError("Need to specify either production or decay!")
        
            m.resetInputEvent()
    
        if 'dividep' in options.keys():
            if local_verbose > 1:
                print("Dividing probability", prob_name, "by", options['dividep'])
                old = probabilities[prob_name]
            
            divisor_name = options['dividep']
            
            if divisor_name == prob_name:
                probabilities[prob_name + "_scaled"] = np.ones(probabilities[prob_name].shape, dtype=np.float64)
            else:
                probabilities[prob_name] /= probabilities[divisor_name]
            
            if local_verbose > 1:
                new = probabilities[prob_name]
                print(f"{'old':^9} {'new':^9}")
                print(*[(i,j) for i,j in zip(old, new)], sep='\n')
    
    
    newf = uproot.update(outfile)
    newf[tTree + "_MELAcalc"] = probabilities