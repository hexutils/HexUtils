import os
import sys
from AnalysisTools.Utils import Config as Config

# Arguments should be a path to the directory with all templates #

outputdir = sys.argv[1]
Input_Trees = sys.argv[2:]

# Load up the analysis configuration # 

Analysis_Config = Config.Analysis_Config("gammaH_Photons_Decay_Only_Optimal_Binning")
#Analysis_Config = Config.Analysis_Config("gammaH_Photons_Decay_Only")
Production_Modes = Analysis_Config.Production_Modes
Event_Categories = Analysis_Config.Event_Categories
Final_States = Analysis_Config.Final_States
Years = Analysis_Config.Years
# For condor submission setup a few directories etc #
CMSSW_PATH = Analysis_Config.CMSSW_PATH 
Work_Dir = Analysis_Config.Work_Dir
# Input is the txt files that list the path to the processed trees #

if not outputdir.endswith("/"):
  outputdir = outputdir+"/"

if not os.path.exists(outputdir):
  os.mkdir(outputdir)

condor_dir = ""
if not os.path.exists(outputdir+"condor"):
  os.mkdir(outputdir+"condor")

condor_dir = outputdir+"condor/"
def separate_by_year(Input_File):
  Files_By_Year = {"2016":[],"2017":[],"2018":[],"Run2":[]}
  with open(Input_File) as f:
    for line in f:
      if "16" in line:
        Files_By_Year["2016"].append(line)
        Files_By_Year["Run2"].append(line)
      if "17" in line:
        Files_By_Year["2017"].append(line)
        Files_By_Year["Run2"].append(line)
      if "18" in line:
        Files_By_Year["2018"].append(line)
        Files_By_Year["Run2"].append(line)
  return Files_By_Year


# Make the output directories for each input tree text file #
for fin in Input_Trees:
  ### For Condor submission ###
  job_num = 0 
  Path_To_Condor_Template = "OnShell_Scripts/OnShell_Template_CondorSubs/condor_template.sub"
  Path_To_Bash_Template = "OnShell_Scripts/OnShell_Template_Submission_Scripts/template_submission_template.sh"
  #############################
  cmd = "python3 CategorizedTemplateMaker.py"
  files_by_year = separate_by_year(fin)
  input_string = " -i " + fin
  if "SIGNAL" in fin.upper():
    SubFolder_Name = "signal_Templates/"
    for pm in Production_Modes:
      production_mode_string = " -p " + pm
      for category in Event_Categories: 
        category_string = " -c " + category
        for fs in Final_States:
          final_state_string = " -f " + fs
          for year in files_by_year.keys():
            if files_by_year[year] != [] and year in Years:
              year_string = " -y " +year
              out_string = " -o "+ outputdir+SubFolder_Name
              # Setup and submit the jobs to condor#
              condor_submission_string = "condor_submit"
              copy_bash_string = "cp "+Path_To_Bash_Template +" "+condor_dir+"submit_"+str(job_num)+".sh"
              copy_condor_string= "cp "+Path_To_Condor_Template +" "+condor_dir+"condor_"+str(job_num)+".sub"
              path_to_bash=condor_dir+"submit_"+str(job_num)+".sh"
              path_to_condor=condor_dir+"condor_"+str(job_num)+".sub"
              os.system(copy_bash_string)
              os.system(copy_condor_string)
              template_cmd = cmd + input_string + production_mode_string + category_string + final_state_string + year_string + out_string
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
              print 
              job_num = job_num + 1
            else:
              continue         
  elif "EW_BKG" in fin.upper():
    SubFolder_Name = "ew_bkg_Templates/"
    files_by_year = separate_by_year(fin)
    input_string = " -i " + fin
    production_mode_string = " -p ew_bkg "
    for category in Event_Categories:
        category_string = " -c " + category
        for fs in Final_States:
          final_state_string = " -f " + fs
          for year in files_by_year.keys():
            if files_by_year[year] != [] and year in Years:
              year_string = " -y " +year
              out_string = " -o "+ outputdir+SubFolder_Name
              # Setup and submit the jobs to condor#
              condor_submission_string = "condor_submit"
              copy_bash_string = "cp "+Path_To_Bash_Template +" "+condor_dir+"submit_"+str(job_num)+".sh"
              copy_condor_string= "cp "+Path_To_Condor_Template +" "+condor_dir+"condor_"+str(job_num)+".sub"
              path_to_bash=condor_dir+"submit_"+str(job_num)+".sh"
              path_to_condor=condor_dir+"condor_"+str(job_num)+".sub"
              os.system(copy_bash_string)
              os.system(copy_condor_string)
              template_cmd = cmd + input_string + production_mode_string + category_string + final_state_string + year_string + out_string
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
              print
              job_num = job_num + 1
            else:
              continue

  elif "GG4L_BKG" in fin.upper():
    SubFolder_Name = "gg4l_bkg_Templates/"
    files_by_year = separate_by_year(fin)
    input_string = " -i " + fin
    production_mode_string = " -p ggZZ "
    for category in Event_Categories:
        category_string = " -c " + category
        for fs in Final_States:
          final_state_string = " -f " + fs
          for year in files_by_year.keys():
            if files_by_year[year] != [] and year in Years:
              year_string = " -y " +year
              out_string = " -o "+ outputdir+SubFolder_Name
              # Setup and submit the jobs to condor#
              condor_submission_string = "condor_submit"
              copy_bash_string = "cp "+Path_To_Bash_Template +" "+condor_dir+"submit_"+str(job_num)+".sh"
              copy_condor_string= "cp "+Path_To_Condor_Template +" "+condor_dir+"condor_"+str(job_num)+".sub"
              path_to_bash=condor_dir+"submit_"+str(job_num)+".sh"
              path_to_condor=condor_dir+"condor_"+str(job_num)+".sub"
              os.system(copy_bash_string)
              os.system(copy_condor_string)
              template_cmd = cmd + input_string + production_mode_string + category_string + final_state_string + year_string + out_string
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
              print
              job_num = job_num + 1
            else:
              continue

  elif "QQ4L_BKG" in fin.upper():
    SubFolder_Name = "qq4l_bkg_Templates/"
    files_by_year = separate_by_year(fin)
    input_string = " -i " + fin
    production_mode_string = " -p qqZZ "
    for category in Event_Categories:
        category_string = " -c " + category
        for fs in Final_States:
          final_state_string = " -f " + fs
          for year in files_by_year.keys():
            if files_by_year[year] != [] and year in Years:
              year_string = " -y " +year
              out_string = " -o "+ outputdir+SubFolder_Name
              # Setup and submit the jobs to condor#
              condor_submission_string = "condor_submit"
              copy_bash_string = "cp "+Path_To_Bash_Template +" "+condor_dir+"submit_"+str(job_num)+".sh"
              copy_condor_string= "cp "+Path_To_Condor_Template +" "+condor_dir+"condor_"+str(job_num)+".sub"
              path_to_bash=condor_dir+"submit_"+str(job_num)+".sh"
              path_to_condor=condor_dir+"condor_"+str(job_num)+".sub"
              os.system(copy_bash_string)
              os.system(copy_condor_string)
              template_cmd = cmd + input_string + production_mode_string + category_string + final_state_string + year_string + out_string
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
              print
              job_num = job_num + 1
            else:
              continue

  elif "ZX" in fin.upper():
    SubFolder_Name = "ZX_Templates/"
    files_by_year = separate_by_year(fin)
    input_string = " -i " + fin
    production_mode_string = " -p ZX "
    for category in Event_Categories:
        category_string = " -c " + category
        for fs in Final_States:
          final_state_string = " -f " + fs
          for year in files_by_year.keys():
            if files_by_year[year] != [] and year in Years:
              year_string = " -y " +year
              out_string = " -o "+ outputdir+SubFolder_Name
              # Setup and submit the jobs to condor#
              condor_submission_string = "condor_submit"
              copy_bash_string = "cp "+Path_To_Bash_Template +" "+condor_dir+"submit_"+str(job_num)+".sh"
              copy_condor_string= "cp "+Path_To_Condor_Template +" "+condor_dir+"condor_"+str(job_num)+".sub"
              path_to_bash=condor_dir+"submit_"+str(job_num)+".sh"
              path_to_condor=condor_dir+"condor_"+str(job_num)+".sub"
              os.system(copy_bash_string)
              os.system(copy_condor_string)
              template_cmd = cmd + input_string + production_mode_string + category_string + final_state_string + year_string + out_string
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
              print
              job_num = job_num + 1
            else:
              continue
