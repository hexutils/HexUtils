#!/cvmfs/cms.cern.ch/slc7_amd64_gcc900/cms/cmssw/CMSSW_12_2_0/external/slc7_amd64_gcc900/bin/python3

import os
from pathlib import Path
import argparse
import warnings
import sys
# import MELAweights as MW

sys.path.append('../')
import generic_helpers as help


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
        param_values = param[param_name_loc + 1:].lower()
        param_values = param_values.split(';')
        if param_name == "options" or param_name == 'couplings':
            options_dict = {}
            for i in param_values:
                i = i.strip().split('=')
                if param_name == "couplings":
                    options_dict[i[0]] = tuple( map(float, i[1].split(',')) )
                else:
                    options_dict[i[0]] = i[1]
            param_values = options_dict
        else:
            param_values = param_values[0]
        output[param_name] = param_values
    
    return output
    

def main(raw_args=None):
    parser = argparse.ArgumentParser()
    input_possibilities = parser.add_mutually_exclusive_group(required=True)
    input_possibilities.add_argument('-i', '--ifile', type=str, nargs='+', help="individual files you want weights applied to")
    input_possibilities.add_argument('-id', '--idirectory', type=str, help="An entire folder you want weights applied to")
    
    parser.add_argument('-o', '--outdr', type=str, required=True, help="The output folder")
    parser.add_argument('-t', '--tBranch', type=str, default="eventTree", help="The name of the TBranch you are using")
    parser.add_argument('-s', '--subdr', nargs=1, type=str, default="", help="Optional subdirectory, otherwise will default to the input files")
    parser.add_argument('-b', '--bfile', type=str, required=True, help="The file containing your branch names")
    parser.add_argument('-l', '--lhe2root', action="store_true", help="Enable this if you want to use lhe2root naming")
    parser.add_argument('-ow', '--overwrite', action="store_true", help="Enable if you want to overwrite files in the output folder")
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
    tbranch = args.tBranch.strip() #nasty extra spaces make us sad!
    lhe2root = args.lhe2root
    overwrite = args.overwrite
    
    if not os.environ.get("LD_LIBRARY_PATH"):
        errortext = "\nPlease setup MELA first using the following command:"
        errortext += "\neval $(./setup.sh env)\n"
        errortext = help.print_msg_box(errortext, title="ERROR")
        raise os.error("\n"+errortext)

    if not outputdir.endswith("/"):
        outputdir = outputdir+"/"
    
    if not os.path.exists(branchfile):
        errortext = "Branches file '" + branchfile + "' cannot be located. Please try again with valid input.\n"
        errortext = help.print_msg_box(errortext, title="ERROR")
        print(template_input)
        raise FileNotFoundError("\n" + errortext)
    
    branchlist = []
    with open(branchfile) as f:
        branchlist = [line.strip() for line in f]
        branchlist = [fragment_to_dict(branch) for branch in branchlist]
        branchlist = [x for x in branchlist if x != None]
        # print(*branchlist, sep='\n')
    
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
        
        User_text += "\n\nThe following probabilities will be calculated:\n"
        User_text += "\n".join(branch['name'] for branch in branchlist)

        print(help.print_msg_box(User_text, title="Reading user input"))
        #================ Set input file path and output file path ================
        
        ind = inputfile.split("/").index(pthsubdir)

        tagtreefile = "/".join(inputfile.split("/")[ind:])
        outtreefilename = outputdir+tagtreefile

        print("\n================ Processing user input ================\n")

        if os.path.exists(outtreefilename):
            if overwrite:
                warningtext =  "Overwriting"+outtreefilename+"\n"
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
        
if __name__ == "__main__":
    main()
    
