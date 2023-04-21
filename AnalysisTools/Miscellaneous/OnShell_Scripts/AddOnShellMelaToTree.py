import os
import sys
from AnalysisTools.Utils import Config as Config

# Arguments should be a path to the directory with all templates #

outputdir = sys.argv[1]
# Input is the txt files that list the path to the processed trees #
Input_Trees = sys.argv[2]
MELA_Probabilities = sys.argv[3] 

# Load up the analysis configuration #

Analysis_Config = Config.Analysis_Config("gammaH_Photons_Decay_Only_Optimal_Binning")
#Analysis_Config = Config.Analysis_Config("gammaH_Photons_Decay_Only")
# For condor submission setup a few directories etc #
CMSSW_PATH = Analysis_Config.CMSSW_PATH
Work_Dir = Analysis_Config.Work_Dir
if not outputdir.endswith("/"):
  outputdir = outputdir+"/"

if not os.path.exists(outputdir):
  os.mkdir(outputdir)

condor_dir = outputdir+"condor/"
if not os.path.exists(outputdir+"condor"):
  os.mkdir(outputdir+"condor")

# Open the list of input Trees #
with open(Input_Trees,'r') as tree_list: 
  # Format should include the native probabilities separated by a space at the end of the file name in the input 
  job_num = 0
  for line in tree_list:
    fin = line.split()[0]
    jhuprob = line.split()[1]
    input_string = ''
    ### For Condor submission ###
    Path_To_Condor_Template = "OnShell_Scripts/OnShell_MELA_Probs/condor_template.sub"
    Path_To_Bash_Template = "OnShell_Scripts/OnShell_MELA_Probs/MELA_submission_template.sh"
    #############################
    cmd = "python3 MELAcalc.py"
    input_string += " -i " + fin.strip('\n')
    #### Parse the subdirectory path ###
    path = fin
    head_tail = os.path.split(path)
    parsed_subdir = head_tail[0].split("/")
    parsed_subdir = parsed_subdir[1:]
    sub = ""
    for i in parsed_subdir[::-1][:4]:
      sub = "/"+ i + sub
    input_string += " -s " + sub
    # ========Output Directory======#
    sub_out_parsed = sub.split("/")
    sub_out = ''
    for i in sub_out_parsed[1:-1]:
      sub_out += "/" + i  
    input_string += " -o " + outputdir+sub_out
    # ====== branchfile ===========#
    input_string += " -b " + MELA_Probabilities
    # ====== Misc Setting for OnShell ==== #
    input_string += " -l False "
    # ====== Add the JHUGen Probability from the input ====== #
    input_string += " -j " + jhuprob
    # ====== Setup Condor Submission ===== #
    condor_submission_string = "condor_submit"
    copy_bash_string = "cp "+Path_To_Bash_Template +" "+condor_dir+"submit_"+str(job_num)+".sh"
    copy_condor_string= "cp "+Path_To_Condor_Template +" "+condor_dir+"condor_"+str(job_num)+".sub"
    path_to_bash=condor_dir+"submit_"+str(job_num)+".sh"
    path_to_condor=condor_dir+"condor_"+str(job_num)+".sub"
    os.system(copy_bash_string)
    os.system(copy_condor_string)
    template_cmd = cmd + input_string 
    print(template_cmd)
    # Now we fill the template correctly #
    os.system("sed -i \"s+CMSSW+cd "+CMSSW_PATH+"+g\" "+path_to_bash)
    os.system("sed -i \"s+UTILS+cd "+Work_Dir+"+g\" "+path_to_bash)
    os.system("sed -i \"s+COMMAND+"+template_cmd+"+g\" "+path_to_bash)
    # Now we fill the condor script corretly #
    os.system("sed -i \"s+NAME+executable              = "+path_to_bash+"+g\" "+path_to_condor)
    os.system("sed -i \"s+OUTOUT+"+condor_dir+"Out"+str(job_num)+".out+g\" "+path_to_condor)
    os.system("sed -i \"s+OUTERR+"+condor_dir+"Out"+str(job_num)+".err+g\" "+path_to_condor)
    os.system("sed -i \"s+OUTLOG+"+condor_dir+"Out"+str(job_num)+".log+g\" "+path_to_condor)
    os.system("condor_submit "+path_to_condor)
    print("condor_submit "+path_to_condor)
    job_num = job_num + 1
    

#MELAcalc.py -i <inputfile> -s <subdirectory> -o <outputdir> -b <branchfile> (-l <lhe2root>) (-m <mcfmprob>)
