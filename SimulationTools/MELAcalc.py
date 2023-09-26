#!/cvmfs/cms.cern.ch/slc7_amd64_gcc900/cms/cmssw/CMSSW_12_2_0/external/slc7_amd64_gcc900/bin/python3

import os
from pathlib import Path
import argparse
import warnings
import sys
import MELAweights as MW

sys.path.append('../')
import generic_helpers as help

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
    parser.add_argument('-m', '--mcfmprob', type=str, default='', help="mcfm probabilities")
    parser.add_argument('-j', '--jhuprob', type=str, default='', help="JHUGen probabilities")
    parser.add_argument('-jt', '--jets', action="store_true", help="Enable if you have jets")
    parser.add_argument('-hm', '--hmass', type=float, default=125, help="The mass of the Higgs")
    parser.add_argument('-z', '--zprime', type=float, nargs=2, default=0, help="The mass and width of a Z Prime as 2 arguments")
    parser.add_argument('-c', '--couplings', type=str, default='', help="A file containing the Zff couplings you are using")
    parser.add_argument('-v', '--verbose', type=int, default=-1, choices=[-1,0,1,2,3,4,5], help="The verbosity level of MELA")
    parser.add_argument('-ow', '--overwrite', action="store_true", help="Enable if you want to overwrite files in the output folder")
    args = parser.parse_args(raw_args)
    
    # template_input = '\nMELAcalc.py -i <inputfile> -o <outputdir> -b <branchfile> \n(-s <subdr>) (-l <lhe2root>) (-m <mcfmprob>) (-j <jhuprob>) (-z <mass> <width>) (-h <mass>)(-c <couplings file>)\n'
    template_input = parser.format_help()
    
    inputfiles = args.ifile
    input_directory = args.idirectory
    
    if input_directory: #if you put in a directory instead of a set of files - this will recurse over that evertything in that file
        # looking for ROOT files
        inputfiles = help.recurse_through_folder(input_directory, ".root")
    
    pthsubdirs = args.subdr if args.subdr else inputfiles
    outputdir = args.outdr
    branchfile = args.bfile
    tbranch = args.tBranch
    lhe2root = args.lhe2root
    mcfmprob = args.mcfmprob
    jhuprob = args.jhuprob
    zp = args.zprime
    higgs_mass = args.hmass
    couplings = args.couplings
    overwrite = args.overwrite
    has_jets = args.jets
    
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
    
    lst_of_couplings = []
    if couplings:
        if not os.path.exists(couplings):
            errortext = "Couplings file " + couplings +" Cannot be located. Please try again with valid input.\n"
            errortext = help.print_msg_box(errortext, title="ERROR")
            print(template_input)
            raise FileNotFoundError("\n" + errortext)
        with open(couplings) as f:
            couplings_temp = f.readlines()
            coupling_template = "couplings must be of form <coupling name>-<value> for each line\n"
            for coupling_duo in couplings_temp:
                coupling_duo = coupling_duo.strip().split('-')
                coupling_duo[1] = float(coupling_duo[1])
                
                if coupling_duo == '':
                    continue
                
                elif len(coupling_duo) != 2:
                    errortext = coupling_template
                    errortext = help.print_msg_box(errortext, title="ERROR")
                    print(template_input)
                    raise ValueError("\n" + errortext)
                
                lst_of_couplings.append(coupling_duo)
    
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
        User_text += "\nPath subdirectory is '{}'".format(pthsubdir)
        User_text += "\nOutput directory is '{}'".format(outputdir[:-1])
        
        if jhuprob: User_text += "\nJHUGen Prob is '{}'".format(jhuprob)
        if zp: User_text += "\n\nZPrime mass/width = {:.2f}/{:.5f} with 'Higgs' mass of {:.2f} GeV".format(*zp, higgs_mass)
        if couplings:
            User_text += "\n\nThe following Zff couplings are explicily used:\n"
            User_text += "\n".join([i[0] + ' = ' + str(i[1]).strip() for i in lst_of_couplings]) + "\n"
            
        if lhe2root: User_text += "\nMELA parser expecting lhe2root branch names"
        else: User_text += "\nMELA parser expecting CJLST branch names"
        
        User_text += "\n\nThe following probabilities will be calculated:\n"
        User_text += "\n".join(branchlist)

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
        
        if zp: #bool('') = False, bool('any string') =  True  
            if jhuprob and mcfmprob:
                MW.addprobabilities(inputfile, outtreefilename, branchlist, tbranch, 
                                SampleHypothesisMCFM = mcfmprob, SampleHypothesisJHUGen = jhuprob, ZPrime=zp, 
                                couplings=lst_of_couplings, verbosity=args.verbose, higgsMass=higgs_mass,
                                hasJets=has_jets)
            elif mcfmprob:
                #MW.addprobabilities(inputfile, outtreefilename, branchlist, "ZZTree/candTree", SampleHypothesisMCFM = mcfmprob)
                MW.addprobabilities(inputfile, outtreefilename, branchlist, tbranch ,
                                SampleHypothesisMCFM = mcfmprob, ZPrime=zp, couplings=lst_of_couplings,
                                verbosity=args.verbose, higgsMass=higgs_mass,
                                hasJets=has_jets)
            elif jhuprob:
                MW.addprobabilities(inputfile, outtreefilename, branchlist, tbranch, 
                                SampleHypothesisJHUGen = jhuprob, ZPrime=zp, couplings=lst_of_couplings,
                                verbosity=args.verbose, higgsMass=higgs_mass,
                                hasJets=has_jets)
                #MW.addprobabilities(inputfile, outtreefilename, branchlist, "ZZTree/candTree", SampleHypothesisJHUGen = mcfmprob)
            else:
                MW.addprobabilities(inputfile, outtreefilename, branchlist, tbranch, ZPrime=zp, couplings=lst_of_couplings,
                                verbosity=args.verbose, higgsMass=higgs_mass,
                                hasJets=has_jets)
                #MW.addprobabilities(inputfile, outtreefilename, branchlist, "ZZTree/candTree")
        else:
            if jhuprob and mcfmprob:
                MW.addprobabilities(inputfile, outtreefilename, branchlist, tbranch, 
                                SampleHypothesisMCFM = mcfmprob, SampleHypothesisJHUGen = jhuprob, couplings=lst_of_couplings,
                                verbosity=args.verbose, higgsMass=higgs_mass,
                                hasJets=has_jets)
                
            elif mcfmprob:
                #MW.addprobabilities(inputfile, outtreefilename, branchlist, "eventTree", SampleHypothesisMCFM = mcfmprob)
                MW.addprobabilities(inputfile, outtreefilename, branchlist, tbranch, 
                                SampleHypothesisMCFM = mcfmprob, couplings=lst_of_couplings, verbosity=args.verbose, higgsMass=higgs_mass,
                                hasJets=has_jets)
            elif jhuprob:
                MW.addprobabilities(inputfile, outtreefilename, branchlist, tbranch, 
                                SampleHypothesisJHUGen = jhuprob, couplings=lst_of_couplings, verbosity=args.verbose, higgsMass=higgs_mass,
                                hasJets=has_jets)
                #MW.addprobabilities(inputfile, outtreefilename, branchlist, "ZZTree/candTree", SampleHypothesisJHUGen = mcfmprob)
            else:
                MW.addprobabilities(inputfile, outtreefilename, branchlist, tbranch, couplings=lst_of_couplings, verbosity=args.verbose, higgsMass=higgs_mass,
                                hasJets=has_jets)
                #MW.addprobabilities(inputfile, outtreefilename, branchlist, "ZZTree/candTree")
            
if __name__ == "__main__":
    main()
