import os,glob
import sys
import ROOT
import copy
from Addsyst_functions import *

# Expected input is a root file with the extension .input.root #
# This script will parse out the histograms in this root file 
# The output we expect is a text file for input into combine 

Input_Dir = sys.argv[1]
output_dir = sys.argv[1]

if not os.path.exists(output_dir):
  os.mkdir(output_dir)

for filename in glob.iglob(Input_Dir+'/**', recursive=True):
  if os.path.isfile(filename) and ('.root' in filename):
    nm = filename
    filename_no_path = nm
    if "/" in filename:
      filename_no_path = nm.split("/")[-1]
    # Remove the any potential filepath #
    fin = ROOT.TFile.Open(nm)
    
    # For right now we do not apply shape systematics 
    # I need to of couse fix the systematics at some point 
    
    processes      =[]
    rate           =[]
    shapesyst      =[]
    applyshapesyst =[]
    procsyst       =[]
    fin = ROOT.TFile.Open(nm)
    obs = 0
    
    for key in fin.GetListOfKeys():
        if "TH1" in key.GetClassName():
            h_name = key.GetName()
            print(h_name)
            if "Up" not in h_name and "Down" not in h_name and "data" not in h_name: #Up and Down are for tune up tune down QCD stuff
                hist = fin.Get(h_name)
                
                hrate = hist.Integral()
                processes.append(h_name)
                rate.append(hrate)
                h_temp = fin.Get(h_name)
                print ("this:",h_name , hrate)
            elif "data" not in h_name:
                hnml = h_name.split("_")
                syst_name = hnml[2]
                for iel,el  in enumerate(hnml):
                    if iel> 2: 
                        syst_name = syst_name +"_"+el 
                syst_name = syst_name.replace("Down","")        
                syst_name = syst_name.replace("Up","")        
                syst_name = syst_name.replace("positive_","")        
                syst_name = syst_name.replace("negative_","")        
                print (syst_name)
                if syst_name not in applyshapesyst : applyshapesyst.append(syst_name)
                psyst = h_name.replace("Down","")
                psyst = psyst.replace("Up","")
                if psyst not in procsyst : procsyst.append(psyst)
                #print (h_name)
            else :
                hist = fin.Get(h_name)
                hrate = hist.Integral()
                obs = hrate
                print ("data :",obs)
    
                
    '''
    
    '''
    
    #Write output datacard
    
    proc = len(processes)
    category = filename_no_path.replace("input.root","onshell.txt")
    chanel = category.replace(".onshell.txt","")
    print("here",category)
    f = open(output_dir+"/"+category, "w")
    
    f.write("imax 1\n")
    f.write("jmax "+str(proc -1)+"\n")
    f.write("kmax *\n")
    f.write("------------\n")
    f.write("shapes * * $CHANNEL.input.root $PROCESS $PROCESS_$SYSTEMATIC\n")
    f.write("------------\n")
    f.write("bin "+str(chanel)+"\n")
    f.write("observation "+ str(obs)+"\n")
    f.write("------------\n")
    
    line= "bin"
    line_p = "process"
    line_rate = "rate"
    line_indx = "process"
    
    #construct shapy syst lines
    lineSHsyst= []
    print (procsyst)
    for isyst,syst in enumerate(applyshapesyst):
        lineSHsyst.append(syst)
        print(syst)
        lineSHsyst[isyst] = lineSHsyst[isyst] + " shape1 "
        for proc in processes :
          pas = False
          for procs in procsyst :
              if syst in procs :
                  if proc+"_"+syst == procs:
                    pas = True
                    print (proc,syst,procs)
                    break
                  else:
                    pas =  False  
          if pas :
              lineSHsyst[isyst] = lineSHsyst[isyst] + " 1"
          else :     
              lineSHsyst[isyst] = lineSHsyst[isyst] + " -"
    
    scale_syst = []
    addlumi(scale_syst,processes)
    addhzzbr(scale_syst,processes)
    addCMS_EFF_e(scale_syst,processes)
    addCMS_EFF_mu(scale_syst,processes)
    #addEWcorr_qqZZ(scale_syst,processes)
    
    
              
    ibkg = 0 
    for i,procc in enumerate(processes):
        line =line +" "+chanel
        line_p = line_p + " " +procc
        if "bkg_" in procc :
            
            line_indx = line_indx +" "+str(ibkg+1)
            #lineQCDsyst = lineQCDsyst + " 1.1"
            ibkg += 1
        else :
            line_indx = line_indx +" -"+ str(i+1)
            #lineQCDsyst = lineQCDsyst + " -"
        #if ("0PM" in procc[0] ) :
        #print chanell,procc[0]  , procc[1] 
        #if ("bkg" in procc[0] ) :
        #  print chanell,procc[0]  , procc[1] 
        
        line_rate = line_rate+ " "+str(rate[i])
    line = line+"\n"
    line_p = line_p + "\n"
    line_indx = line_indx + "\n"
    line_rate = line_rate+"\n"            
    #lineQCDsyst = lineQCDsyst +"\n"        
    f.write(line)
    f.write(line_p)
    f.write(line_indx)
    f.write(line_rate)
    f.write("------------\n")
    for scalesyst in scale_syst :
        payload = scalesyst+"\n"
        f.write(payload)
    for shapsyst in lineSHsyst :
        payload = shapsyst+"\n"
        f.write(payload)
    
    
    f.close()
    print (applyshapesyst)
    #print "written datacard"
    
