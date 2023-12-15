#!/cvmfs/cms.cern.ch/slc7_amd64_gcc900/cms/cmssw/CMSSW_12_2_0/external/slc7_amd64_gcc900/bin/python3

import os
from pathlib import Path
import argparse
import warnings
import sys, re, json
import MELAweights_v2 as MW

sys.path.append('../')
import generic_helpers as help


def parse_prob(probability):
    ## Functionality only tested for ggH mode ##
    parsed_dict = {
        "process":None,
        "production":None,
        "matrixelement":None,
        "prod":None,
        "dec":None,
        "options":{
            "jes":None, 
            "jec":None, 
            "jer":None, 
            "bsm":None, 
            "dividep":None
            },
        "couplings":{}
        }
    # Sort whether to use Jet systematics #
    if "JES" in probability: 
        if "Up" in probability:
            parsed_dict['options']["jes"] = "JetPt_JESUp"
        elif "Down" in probability:
            parsed_dict['options']["jes"] = "JetPt_JESDown"
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
    if "_Gen" in probability:
        parsed_dict["isReco"] = False
    else:
        parsed_dict["isReco"] = True
    # Sort Production Mode #
    if "GG" in probability:
        parsed_dict["ProdMode"] = "GG"
        parsed_dict["Prod"] = False
        parsed_dict["Dec"] = True
    elif "QQ" in probability:
        parsed_dict["ProdMode"] = "QQ"
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
        parsed_dict["Dec"] = True
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
        parsed_dict["ProdMode"] = "JJEWQCD"
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
    elif "IND" in probability:
        parsed_dict["ProdMode"] = "IND"
        parsed_dict["Prod"] = False
        parsed_dict["Dec"] = True
    # Sort MatrixElement #
    if "JHUGen" in probability:
        parsed_dict["MatrixElement"] = "JHUGen"
    elif "MCFM" in probability:
        parsed_dict["MatrixElement"] = "MCFM"
    # Raise Anomalous Coupling Flag #
    if "AC" in probability:
        parsed_dict["BSM"] = "AC"
    # Sort Couplings #
    coupling_names = re.findall(r"[a-zA-Z0-9]+_(?:m)*[0-9]?(?:p)*?[0-9]", probability)
    coupling_value_tuples = re.findall("[a-zA-Z0-9]+_((?:m)*[0-9]?(?:p)*?[0-9]+)(?:[eE]([+-]?\d+))?",probability)
    for i in range(len(coupling_names)):
        coupling = coupling_names[i].split("_")[0]
        if coupling_value_tuples[i][1] == '':
            if "p" in coupling_value_tuples[i][0]:
                if "m" in coupling_value_tuples[i][0]:
                    value = -float(coupling_value_tuples[i][0].split("m")[1].split("p")[0] + "." + coupling_value_tuples[i][0].split("m")[1].split("p")[1])
                else:
                    value = float(coupling_value_tuples[i][0].split("p")[0] + "." + coupling_value_tuples[i][0].split("p")[1])
            else:
                if "m" in coupling_value_tuples[i][0]:
                    value = -float(coupling_value_tuples[i][0].split("m")[1])
                else:
                    value = float(coupling_value_tuples[i][0])
        else:
            if "p" in coupling_value_tuples[i][0]:
                if "m" in coupling_value_tuples[i][0]:
                    value = -float(coupling_value_tuples[i][0].split("m")[1].split("p")[0] + "." + coupling_value_tuples[i][0].split("m")[1].split("p")[1])* 10 ** float(coupling_value_tuples[i][1])
                else:
                    value = float(coupling_value_tuples[i][0].split("p")[0] + "." + coupling_value_tuples[i][0].split("p")[1]) * 10 ** float(coupling_value_tuples[i][1])
            else:
                if "m" in coupling_value_tuples[i][0]:
                    value = -float(coupling_value_tuples[i][0]).split("m")[1] * 10 ** float(coupling_value_tuples[i][1])
                else:
                    value = float(coupling_value_tuples[i][0]) * 10 ** float(coupling_value_tuples[i][1])
        parsed_dict["coupl_dict"][coupling] = value

    if "spin1" in probability:
        parsed_dict['SPIN'] = 1
    elif "spin2" in probability:
        parsed_dict['SPIN'] = 2

    if parsed_dict["ProdMode"] == None:
        raise ValueError("Coupling does not have a valid Production Mode")
    if parsed_dict["MatrixElement"] == None:
        raise ValueError("Coupling does not have a valid MatrixElement")
    if parsed_dict["Process"] == None:
        print('\n',parsed_dict,'\n')
        raise ValueError("Coupling does not have a valid Process")
    
    return parsed_dict


def fragment_to_dict(input_line):
    input_line = input_line.strip()
    if len(input_line) == 0:
        return
    if input_line[0] == '#':
        return
    output = {}
    input_params = input_line.split()
    for param in input_params:
        param_name_loc = param.find(':')
        param_name = param[:param_name_loc].lower()
        param_values = param[param_name_loc + 1:]
        param_values = param_values.strip().split(';')
        
        if param_name == "options" or param_name == 'couplings':
            options_dict = {}
            for i in param_values:
                if i == '':
                    continue
                i = i.strip().split('=')
                if param_name == "couplings":
                    coupling_val = map(float, i[1].split(','))
                    options_dict[i[0]] = complex(*coupling_val)
                else:
                    options_dict[i[0].lower()] = i[1]
            param_values = options_dict
        
        elif param_name in ["prod", "dec"]:
            param_values = bool(int(param_values[0]))
        else:
            param_values = param_values[0]
        
        output[param_name] = param_values
    print(output)
    return output


def json_to_dict(json_file):
    with open(json_file) as json_data:
        data = json.load(json_data)

        returnable_list_of_probs = [{} for _ in range(len(data))]
        
        for n, prob_name in enumerate(data.keys()):
            returnable_list_of_probs[n]["name"] = prob_name
            
            for input_val in data[prob_name]:
                new_input_val = input_val.lower()
                if new_input_val == 'couplings':
                    returnable_list_of_probs[n][new_input_val] = {}
                    for coupling in data[prob_name][input_val]:
                        if len(data[prob_name][input_val][coupling]) != 2:
                            errortext = "Length of input for " + coupling + f" is {len(data[prob_name][input_val][coupling])}!"
                            errortext += "\nInput for couplings should be <name>:[<real>, <imaginary>]"
                            errortext = help.print_msg_box(errortext, title="ERROR")
                            raise ValueError("\n" + errortext)
                        
                        returnable_list_of_probs[n][new_input_val][coupling] = complex(*data[prob_name][input_val][coupling])
                        
                elif new_input_val == 'options':
                    returnable_list_of_probs[n][new_input_val] = {}
                    for option in data[prob_name][input_val]:
                        returnable_list_of_probs[n][new_input_val][option.lower()] = data[prob_name][input_val][option]
                        
                elif new_input_val == "particles":
                    returnable_list_of_probs[n][new_input_val] = {}
                    for particle in data[prob_name][input_val]:
                        p_id, p_mass, p_width = particle
                        returnable_list_of_probs[n][new_input_val][p_id] = (p_mass, p_width)
                else:
                    returnable_list_of_probs[n][new_input_val] = data[prob_name][input_val]
        return returnable_list_of_probs



def main(raw_args=None):
    parser = argparse.ArgumentParser()
    input_possibilities = parser.add_mutually_exclusive_group(required=True)
    input_possibilities.add_argument('-i', '--ifile', type=str, nargs='+', help="individual files you want weights applied to")
    input_possibilities.add_argument('-id', '--idirectory', type=str, help="An entire folder you want weights applied to")
    
    parser.add_argument('-o', '--outdr', type=str, required=True, help="The output folder")
    parser.add_argument('-t', '--tBranch', type=str, default="eventTree", help="The name of the TBranch you are using")
    parser.add_argument('-s', '--subdr', nargs=1, type=str, default="", help="Optional subdirectory, otherwise will default to the input files")
    
    config_possibilities = parser.add_mutually_exclusive_group(required=True)
    config_possibilities.add_argument('-p', '--pyfragment', type=str, help="The pyfragment containing your branch names")
    config_possibilities.add_argument('-b', '--bfile', type=str, help="The file containing your branch names")
    config_possibilities.add_argument('-j', '--jsonFile', type=str, help="The JSON file containing your branch names")
    
    parser.add_argument('-l', '--lhe2root', action="store_true", help="Enable this if you want to use lhe2root/GEN level naming from LHE2ROOT")
    parser.add_argument('-ow', '--overwrite', action="store_true", help="Enable if you want to overwrite files in the output folder")
    parser.add_argument('-v', '--verbose', choices=[0,1,2,3,4,5], type=int, default=0)
    parser.add_argument('-vl', '--verbose_local', choices=[0,1,2], type=int, default=0)
    parser.add_argument('-n', '--number', type=int, default=-1)
    args = parser.parse_args(raw_args)
    
    template_input = parser.format_help()
    
    inputfiles = args.ifile
    input_directory = args.idirectory
    
    if input_directory: #if you put in a directory instead of a set of files - this will recurse over that evertything in that file
        # looking for ROOT files
        inputfiles = help.recurse_through_folder(input_directory, ".root")
    
    pthsubdirs = args.subdr if args.subdr else inputfiles
    outputdir = args.outdr
    
    branchfile = args.bfile
    pyfragment = args.pyfragment
    json = args.jsonFile
    
    inputFile = None
    if branchfile:
        inputFile = branchfile
    elif pyfragment:
        inputFile = pyfragment
    elif json:
        inputFile = json
    
    tbranch = args.tBranch.strip() #nasty extra spaces make us sad!
    lhe2root = args.lhe2root
    overwrite = args.overwrite
    verbosity = args.verbose
    local_verbosity = args.verbose_local
    n_events = args.number
    
    if not os.environ.get("LD_LIBRARY_PATH"):
        errortext = "\nPlease setup MELA first using the following command:"
        errortext += "\neval $(./setup.sh env)\n"
        errortext = help.print_msg_box(errortext, title="ERROR")
        raise os.error("\n"+errortext)

    if not outputdir.endswith("/"):
        outputdir = outputdir+"/"
    
    if not os.path.exists(inputFile):
        errortext = "File '" + branchfile + "' cannot be located. Please try again with valid input.\n"
        errortext = help.print_msg_box(errortext, title="ERROR")
        print(template_input)
        raise FileNotFoundError("\n" + errortext)
    
    
    if pyfragment:
        branchlist = []
        with open(pyfragment) as f:
            branchlist = [line.strip() for line in f]
            branchlist = [fragment_to_dict(branch) for branch in branchlist]
            branchlist = [x for x in branchlist if x != None]
    elif json:
        branchlist = json_to_dict(json)
    elif branchfile:
        print("WIP")
        exit()
        
    
    
    
    for inputfile, pthsubdir in zip(inputfiles, pthsubdirs):
        if not pthsubdir.endswith("/"):
            pthsubdir = pthsubdir+"/"

        pthsubdir = pthsubdir.split("/")[-2]
        
        if not os.path.exists(inputfile):
            errortext = "ROOT file '" + inputfile + "' cannot be located. Please try again with valid input.\n"
            errortext = help.print_msg_box(errortext, title="ERROR")
            print(template_input)
            raise FileExistsError("\n" + errortext)

        if pthsubdir not in inputfile:
            errortext = "tSubdirectory '" + pthsubdir + "' cannot be located. Please try again with valid input.\n"
            errortext = help.print_msg_box(errortext, title="ERROR")
            print(template_input)
            raise FileExistsError("\n" + errortext)
                    

        # print("\n================ Reading user input ================\n")

        User_text = "Input PTree is '{}'".format(inputfile)
        User_text += "\nInput branch is '{}'".format(tbranch)
        User_text += "\nPath subdirectory is '{}'".format(pthsubdir)
        User_text += "\nOutput directory is '{}'".format(outputdir[:-1])
        
        if lhe2root: User_text += "\nMELA parser expecting lhe2root branch names"
        else: User_text += "\nMELA parser expecting CJLST branch names"
        
        User_text += "\n\nThe following probabilities will be calculated:\n\n"
        User_text += "\n".join(branch['name'] for branch in branchlist)

        print(help.print_msg_box(User_text, title="Reading user input"))
        #================ Set input file path and output file path ================
        
        ind = inputfile.split("/").index(pthsubdir)

        tagtreefile = "/".join(inputfile.split("/")[ind:])
        outtreefilename = outputdir+tagtreefile

        print("\n================ Processing user input ================\n")

        if os.path.exists(outtreefilename):
            if overwrite:
                warningtext =  "Overwriting "+outtreefilename+"\n"
                warnings.warn("\n" + help.print_msg_box(warningtext, title="WARNING"))
                os.remove(outtreefilename)
            else:
                errortext = outtreefilename + "' or parts of it already exist!\n"
                errortext = help.print_msg_box(errortext, title="ERROR")
                raise FileExistsError("\n" + errortext)

        else:
            print("Pre-existing output PTree not found --- safe to proceed")
            if not os.path.exists("/".join(outtreefilename.split("/")[:-1])):
                Path("/".join(outtreefilename.split("/")[:-1])).mkdir(True, True)

        print("Read '"+inputfile+"'\n")
        print("Write '"+outtreefilename+"'\n")
        
        calculated_probabilities = MW.addprobabilities(branchlist, inputfile, tbranch, verbosity, lhe2root, local_verbosity, n_events)
        MW.dump(inputfile, tbranch, outtreefilename, calculated_probabilities)
        
if __name__ == "__main__":
    
    VALID_MATRIXELEMENT = {
        "MCFM",
        "JHUGen",
        "ANALYTICAL"
    }
    
    VALID_PRODUCTION = {
        "ZZGG",
        "ZZQQB",
        "ZZQQB_STU", #// Should be the same as ZZQQB, just for crosscheck
        "ZZINDEPENDENT",

        "ttH", #// ttH
        "bbH", #// bbH

        "JQCD", #// ? + 1 jet

        "JJQCD",# // SBF
        "JJVBF",# // VBF
        "JJEW",# // VBF+VH (had.)
        "JJEWQCD",# // VBF+VH+QCD, all hadronic
        "Had_ZH",# // ZH, Z->uu/dd
        "Had_WH",# // W(+/-)H, W->ud
        "Lep_ZH",# // ZH, Z->ll/nunu
        "Lep_WH",# // W(+/-)H, W->lnu

        # // s-channel contributions
        "ZZQQB_S",
        "JJQCD_S",
        "JJVBF_S",
        "JJEW_S",
        "JJEWQCD_S",
        "Had_ZH_S",
        "Had_WH_S",
        "Lep_ZH_S",
        "Lep_WH_S",

        # // t+u-channel contributions
        "ZZQQB_TU",
        "JJQCD_TU",
        "JJVBF_TU",
        "JJEW_TU",
        "JJEWQCD_TU",
        "Had_ZH_TU",
        "Had_WH_TU",
        "Lep_ZH_TU",
        "Lep_WH_TU",

        "GammaH", #// gammaH, stable A (could implement S and TU in the future
    }
    
    VALID_PROCESS = {
        "HSMHiggs", #// Call this for any MCFM |H|**2-only ME.
        "H0_g1prime2",
        "H0hplus",
        "H0minus",
        "H0_Zgsg1prime2",
        "H0_Zgs",
        "H0_Zgs_PS",
        "H0_gsgs",
        "H0_gsgs_PS",

        "D_g1g1prime2",
        "D_g1g2",
        "D_g1g2_pi_2",
        "D_g1g4",
        "D_g1g4_pi_2",
        "D_zzzg",
        "D_zzgg",
        "D_zzzg_PS",
        "D_zzgg_PS",
        "D_zzzg_g1prime2",
        "D_zzzg_g1prime2_pi_2",

        "H1minus", #// 1-
        "H1plus", #// 1+

        "H2_g1", #// 2m+, Zg, gg
        "H2_g2", #// 2h2+
        "H2_g3", #// 2h3+
        "H2_g4", #// 2h+
        "H2_g5", #// 2b+
        "H2_g1g5", #// 2m+
        "H2_g6", #// 2h6+
        "H2_g7", #// 2h7+
        "H2_g8", #// 2h-
        "H2_g9", #// 2h9-
        "H2_g10", #// 2h10-

        "bkgGammaGamma", #// gamma+gamma cont.
        "bkgZGamma", #// Z+gamma cont.
        "bkgZJets", #// Z + 0/1/2 jets (ZZGG, JQCD, JJQCD)
        "bkgZZ", #// qq/gg->ZZ cont.
        "bkgWW", #// qq/gg->WW cont.
        "bkgWWZZ", #// gg->ZZ+WW cont.

        "bkgZZ_SMHiggs", #// ggZZ cont. + SMHigg
        "bkgWW_SMHiggs", #// ggWW cont. + SMHiggs
        "bkgWWZZ_SMHiggs", #// ggZZ+WW cont. + SMHiggs

        "HSMHiggs_WWZZ", #// MCFM |H|**2 ZZ+WW with ZZ-WW interference

        # /**** For width ***/
        "D_gg10",

        # /***** Self Defined******/
        "SelfDefine_spin0",
        "SelfDefine_spin1",
        "SelfDefine_spin2",
    }
    
    VALID_OPTION = {
        "dividep",
        "matchmh",
        "jetpt"
    }
    
    main()
    
