#!/usr/bin/env python

import os
import glob
import ROOT as ROOT
import ROOT 
from math import sqrt
import time

#from pathlib import Path
import re
#from tqdm import trange, tqdm
import numpy as np
import copy
from array import *
from GetSyst import getsyst

import sys

production = sys.argv[1]
category   = sys.argv[2]
iffile     = sys.argv[3]
targetyear = sys.argv[4]
procsystfile = ""
if len(sys.argv) > 5  : 
    procsystfile = sys.argv[5]

print (production, category)

lumi = {'MC_2016_CorrectBTag':35.9, 'MC_2017':41.5, 'MC_2018':59.7}
medges = np.array([220, 230, 240, 250, 260, 280, 310, 340, 370, 400, 475, 550, 625, 700, 800, 900, 1000, 1200, 1600, 2000, 3000, 13000], dtype='float64')

d1edges = np.arange(21, dtype='float64') / 20
d2edges = np.arange(21, dtype='float64') / 10 - 1



#input
#treelistpath = "/eos/user/l/lkang/Active_Research/Discriminants/alltaggedtrees.txt"
#treelistpath = "/eos/user/s/skyriaco/SWAN_projects/Offshel_tempmaker/outputtree_list.txt"
#treelistpath = "/eos/user/s/skyriaco/SWAN_projects/Offshel_tempmaker/output_highmass1618.txt"
#treelistpath = "ggall.txt"
#treelistpath = "./LucasTrees_gg.txt" #/eos/user/s/skyriaco/SWAN_projects/Offshel_tempmaker/
#treelistpath = "singleinput.txt"
#treelistpath = "./Trees_VBF.txt"


#treelistpath = "./background_updatedcat.txt"
treelistpath = "./gg_updatedcat.txt"

if not  procsystfile == "": 
    treelistpath = "./syst_"+procsystfile+".txt"
    

treelist = []

with open(treelistpath) as f:
    llist = [line.rstrip() for line in f]
        
for line in llist:
    if os.path.exists(line): 
        treelist.append(line)



yeardict = {}

for numfile in range(0,len(treelist)):
    filename = treelist[numfile]
    print (filename)
    ind = filename.split("/").index("200205_CutBased")
    year = filename.split("/")[ind:][1]

    if year not in yeardict.keys():
        yeardict[year] = {}
    if year in yeardict.keys():   
        if "ZZTo4l" in filename.split("/")[ind:][2]: prod = "ZZTo4l"
        else: prod = filename.split("/")[ind:][3]
        print (prod)    
        if prod not in yeardict[year]:
            if 'gg' in prod:
                yeardict[year][prod] = [[]]   #, [], []]
            else:
                yeardict[year][prod] = [[]]
        if prod == 'gg':
            yeardict[year][prod][0].append(filename)
            
            #if 'ggTo2e2mu' in filename:
            #elif 'ggTo4e' in filename:
            #    yeardict[year][prod][1].append(filename)
            #elif 'ggTo4mu' in filename:
            #    yeardict[year][prod][2].append(filename)
        elif prod == "VBF":
            yeardict[year][prod][0].append(filename)
        elif prod == "ZZTo4l":
            print ("appended", filename)
            yeardict[year][prod][0].append(filename)
        else:
            print("ERROR: Cannot recognize production mode of " + filename + "! Tree not sorted!")


# ### Check organized trees
print("=======================================================")
print (yeardict)
print("=======================================================")

refsam4l = ["VBFToContinToZZTo4l", "VBFToHiggs0L1ContinToZZTo4l", "VBFToHiggs0L1f025ph0ToZZTo4l", "VBFToHiggs0L1f05ph0ContinToZZTo4l", "VBFToHiggs0L1f05ph0ToZZTo4l", "VBFToHiggs0L1f075ph0ToZZTo4l", "VBFToHiggs0L1ToZZTo4l", "VBFToHiggs0MContinToZZTo4l", "VBFToHiggs0Mf025ph0ToZZTo4l", "VBFToHiggs0Mf05ph0ContinToZZTo4l", "VBFToHiggs0Mf05ph0ToZZTo4l", "VBFToHiggs0Mf075ph0ToZZTo4l", "VBFToHiggs0MToZZTo4l", "VBFToHiggs0PHContinToZZTo4l", "VBFToHiggs0PHf025ph0ToZZTo4l", "VBFToHiggs0PHf05ph0ContinToZZTo4l", "VBFToHiggs0PHf05ph0ToZZTo4l", "VBFToHiggs0PHf075ph0ToZZTo4l", "VBFToHiggs0PHToZZTo4l", "VBFToHiggs0PMContinToZZTo4l", "VBFToHiggs0PMToZZTo4l"]
refmel = ["p_Gen_JJEW_BKG_MCFM", "p_Gen_JJEW_BSI_ghv1_0_ghv1prime2_m1549p165_MCFM", "p_Gen_JJEW_SIG_ghv1_1_ghv1prime2_m1177p11_MCFM", "p_Gen_JJEW_BSI_ghv1_1_ghv1prime2_m1549p165_MCFM", "p_Gen_JJEW_SIG_ghv1_1_ghv1prime2_m1549p165_MCFM", "p_Gen_JJEW_SIG_ghv1_1_ghv1prime2_m2038p82_MCFM", "p_Gen_JJEW_SIG_ghv1_0_ghv1prime2_m1549p165_MCFM", "p_Gen_JJEW_BSI_ghv1_0_ghv4_0p216499_MCFM", "p_Gen_JJEW_SIG_ghv1_1_ghv4_0p164504_MCFM", "p_Gen_JJEW_BSI_ghv1_1_ghv4_0p216499_MCFM", "p_Gen_JJEW_SIG_ghv1_1_ghv4_0p216499_MCFM", "p_Gen_JJEW_SIG_ghv1_1_ghv4_0p284929_MCFM", "p_Gen_JJEW_SIG_ghv1_0_ghv4_0p216499_MCFM", "p_Gen_JJEW_BSI_ghv1_0_ghv2_0p207049_MCFM", "p_Gen_JJEW_SIG_ghv1_1_ghv2_0p157323_MCFM", "p_Gen_JJEW_BSI_ghv1_1_ghv2_0p207049_MCFM", "p_Gen_JJEW_SIG_ghv1_1_ghv2_0p207049_MCFM", "p_Gen_JJEW_SIG_ghv1_1_ghv2_0p272492_MCFM", "p_Gen_JJEW_SIG_ghv1_0_ghv2_0p207049_MCFM", "p_Gen_JJEW_BSI_ghv1_1_MCFM", "p_Gen_JJEW_SIG_ghv1_1_MCFM"]

refden = dict(zip(refsam4l, refmel))




hlist = ['ggH SIG', 'ggH BSI', 'ggH BKG', 'qqbar BKG']

#targetreweight = {"gg": ["p_Gen_GG_SIG_kappaTopBot_1_ghz1_1_MCFM*KFactor_QCD_ggZZ_Nominal", "p_Gen_GG_BSI_kappaTopBot_1_ghz1_1_MCFM*KFactor_QCD_ggZZ_Nominal", "p_Gen_GG_BKG_MCFM*KFactor_QCD_ggZZ_Nominal"],
#                 "VBF": ["p_Gen_JJEW_SIG_ghv1_1_MCFM*0.5", "p_Gen_JJEW_BSI_ghv1_1_MCFM*0.5", "p_Gen_JJEW_BKG_MCFM*0.5"],
#                 "ZZTo4l": ["1"]}
finalstate = {"4e": "121*121", "4mu": "169*169", "2e2mu": "121*169"}
proc = ["ggH_0PM", "ggH_g11g21_negative", "ggH_g11g21_positive", "back_ggZZ", "back_qqZZ", "data_obs"]




#configure what you would like to run

ltargetyear = ["MC_2017","MC_2016_CorrectBTag","MC_2018"]
ltargetprod = ["gg","VBF","ZZTo4l"]
ltargetstate = ["4mu","4e","2e2mu"]
ltargetcomp = [0,1,2]    # SIG=0 BSI=1 BKG=2    (for the qqbar bkg events in 'ZZTo4l' this choice does not matter as you can see above)
if production == "ZZTo4l" : 
    ltargetcomp = [0]
ltargetcateg = [0,1,2]  # Untag=0 VBF=1 VH=2

print ("target comp list: ", ltargetcomp)


# ### Fill histogram
def FillHist(targetprod,targetcomp,targetcateg,h_list,shape_syst_list,iffile,targetyear,correctionsOn) :


    #initialize some functions
    from CrossFeed import IsCrossFeed    
    from EWcor import EWcor
    
    #setup EW cat corrections
    ew_fparams  = []
    if ( targetprod == "VBF" ) : 
        #read textfile for EW cor parameters
        ffun_par = open("./AnalysisTools/offshellcatcorr/data/f"+targetyear[-2]+targetyear[-1]+".txt",'r')
        ffun_parlines = ffun_par.readlines() 
        ew_fparmsvh  = []
        ew_fparmsvbf  = []
        ew_fparmsevh  = []
        ew_fparmsevbf  = []

        splittedffunparlines = [ill.split() for ill in ffun_parlines ]
        for iline,line in enumerate(ffun_parlines): 
            lwords = line.split()
            print (lwords)
            if (len(lwords) > 1 ): 
                if lwords[1] == "vbftagged" :
                    for iadd in range(5,10): 
                        ew_fparmsvbf.append(float(splittedffunparlines[iline+iadd][2]))                
                if lwords[1] == "vhtagged" : 
                    for iadd in range(5,10): 
                        ew_fparmsvh.append(float(splittedffunparlines[iline+iadd][2])) 
                if lwords[1] == "evbftagged" : 
                    for iadd in range(5,10): 
                        ew_fparmsevbf.append(float(splittedffunparlines[iline+iadd][2]))
                if lwords[1] == "evhtagged" : 
                    for iadd in range(5,10): 
                        ew_fparmsevh.append(float(splittedffunparlines[iline+iadd][2]))  
        ew_fparams.append(ew_fparmsvh)
        ew_fparams.append(ew_fparmsvbf)
        ew_fparams.append(ew_fparmsevh)
        ew_fparams.append(ew_fparmsevbf)

    #setup ggF cat corrections
    if production == "gg" :
        #study in /afs/cern.ch/work/s/skyriaco/Offshell_trees/TreeEditor/testCat/cat_jul20/corr_altbin
        if targetcateg == 0 : hcor_name = "hmzzUN"    
        if targetcateg == 1 : hcor_name = "hmzzVBF"    
        if targetcateg == 2 : hcor_name = "hmzzVH"    
        fcor = ROOT.TFile("./AnalysisTools/data/offshellcatcorr/ggF_cat_corrections_"+targetyear[-2]+targetyear[-1]+".root")
        hcor = fcor.Get(hcor_name)


    
    
    hf = ROOT.TH3F("hf","", len(medges)-1, medges, len(d1edges)-1, d1edges, len(d2edges)-1, d2edges)
    hf_systdn = ROOT.TH1F("hf_kew_systdn","",100,0,2000)
    hf_systup = ROOT.TH1F("hf_kew_systup","",100,0,2000)
    hf_nom    = ROOT.TH1F("hf_nom","",100,0,2000)
    
    hf_syst = []                        
    for i,systname  in enumerate (shape_syst_list): 
        hf_syst_up = ROOT.TH3F("hf_syst_up","", len(medges)-1, medges, len(d1edges)-1, d1edges, len(d2edges)-1, d2edges)
        hf_syst_dn = ROOT.TH3F("hf_syst_dn","", len(medges)-1, medges, len(d1edges)-1, d1edges, len(d2edges)-1, d2edges)
        hf_syst_up.SetDirectory(0)
        hf_syst_dn.SetDirectory(0)
        hf_systp = (hf_syst_up,hf_syst_dn)
        hf_syst.append(hf_systp)
        
        
    
    hf.SetDirectory(0)
    hf_systdn.SetDirectory(0)
    hf_systup.SetDirectory(0)
    hf_nom.SetDirectory(0)
    
    for keynum in range(0,len(yeardict.keys())):
        year = list(yeardict.keys())[keynum]
        print (list(yeardict.keys())[keynum])
        if targetyear not in year: continue
        lumi_year = lumi[year]

        hs = ROOT.TH3F("hs","", len(medges)-1, medges, len(d1edges)-1, d1edges, len(d2edges)-1, d2edges)
        hs_systdn = ROOT.TH1F("hs_kew_systdn","",100,0,2000)
        hs_systup = ROOT.TH1F("hs_kew_systup","",100,0,2000)
        hs_nom    = ROOT.TH1F("hs_nom","",100,0,2000)
        
        hs_syst = []                        
        for i,systname  in enumerate (shape_syst_list): 
            hs_syst_up = ROOT.TH3F("hs_syst_up","", len(medges)-1, medges, len(d1edges)-1, d1edges, len(d2edges)-1, d2edges)
            hs_syst_dn = ROOT.TH3F("hs_syst_dn","", len(medges)-1, medges, len(d1edges)-1, d1edges, len(d2edges)-1, d2edges)
            hs_syst_up.SetDirectory(0)
            hs_syst_dn.SetDirectory(0)
            hs_systp = (hs_syst_up,hs_syst_dn)
            hs_syst.append(hs_systp)
            
            
        hs.SetDirectory(0)
        hs_systdn.SetDirectory(0)
        hs_systup.SetDirectory(0)
        hs_nom.SetDirectory(0)

        for idecay,decay in enumerate(yeardict[year][targetprod]):
            #print ("here:",decay)
            
            ht = ROOT.TH3F("ht","", len(medges)-1, medges, len(d1edges)-1, d1edges, len(d2edges)-1, d2edges)
            ht_systdn = ROOT.TH1F("ht_kew_systdn","",100,0,2000)
            ht_systup = ROOT.TH1F("ht_kew_systup","",100,0,2000)
            ht_nom    = ROOT.TH1F("ht_nom","",100,0,2000)
          
            ht_syst = []                        
            for i,systname  in enumerate (shape_syst_list): 
                ht_syst_up = ROOT.TH3F("ht_syst_up","", len(medges)-1, medges, len(d1edges)-1, d1edges, len(d2edges)-1, d2edges)
                ht_syst_dn = ROOT.TH3F("ht_syst_dn","", len(medges)-1, medges, len(d1edges)-1, d1edges, len(d2edges)-1, d2edges)
                ht_syst_up.SetDirectory(0)
                ht_syst_dn.SetDirectory(0)
                ht_systp = (ht_syst_up,ht_syst_dn)
                ht_syst.append(ht_systp)
                
             

            ht.SetDirectory(0)
            ht_systdn.SetDirectory(0)
            ht_systup.SetDirectory(0)
            ht_nom.SetDirectory(0)
            count = 1
            
            print ("about to fill")
            for itfile,tfile in enumerate(range(len(decay))):
                print ("thiss", (itfile, iffile,len(decay)))
                if not( itfile == int(iffile) ) :
                    continue
                print (iffile,"here")    
                print("file : ",decay[tfile])
                
                global flav
                if "2e2mu" in decay[tfile] : 
                    flav = "2e2mu"
                if "4e" in decay[tfile] : 
                    flav = "4e"
                if "4mu" in decay[tfile] : 
                    flav = "4mu"
                
                #print (flav)

                if "VBF" in decay[tfile]:
                    if  "0L1" in decay[tfile] : continue
                    #print (decay[tfile])
                    skey = decay[tfile].split("/")[-2].replace('_M125_GaSM', '')
                    sampleweight = refden[skey]
                    
                if ( os.stat(decay[tfile]).st_size > 100 ):  
                        print ("passfilesize")
                        f = ROOT.TFile(decay[tfile])
                        t = f.Get("eventTree")
                        htt = ROOT.TH3F("htt","", len(medges)-1, medges, len(d1edges)-1, d1edges, len(d2edges)-1, d2edges)
                        htt_ew_systdn = ROOT.TH1F("htt_ew_systdn","",100,0,2000)
                        htt_ew_systup = ROOT.TH1F("htt_ew_systup","",100,0,2000)
                        htt_nom    = ROOT.TH1F("htt_nom","",100,0,2000)
                        htt_syst = []
                        for i,systname  in enumerate (shape_syst_list): 
                            htt_syst_up = ROOT.TH3F("htt_syst_up","", len(medges)-1, medges, len(d1edges)-1, d1edges, len(d2edges)-1, d2edges)
                            htt_syst_dn = ROOT.TH3F("htt_syst_dn","", len(medges)-1, medges, len(d1edges)-1, d1edges, len(d2edges)-1, d2edges)
                            htt_syst_up.SetDirectory(0)
                            htt_syst_dn.SetDirectory(0)
                            htt_systp = (htt_syst_up,htt_syst_dn)
                            htt_syst.append(htt_systp)
                            

                        print ("Nevents: ",t.GetEntries())    
                        for iev,event in enumerate(t):
                            #if iev > 1 : continue
                            
                            #remove crossfeed from JHUGen EW samples

                            #event cuts

                            if not ( (event.Z1Flav*event.Z2Flav)==(121*121) or (event.Z1Flav*event.Z2Flav)==(169*169) or (event.Z1Flav*event.Z2Flav)==(121*169) ) : continue
                            if not (event.ZZMass >= 220) : continue

                            
                            if (event.EventTag == targetcateg) : 
                                
                                if production == "VBF" :
                                    #print ("here")
                                    if  IsCrossFeed(event) : continue
                                    

                                
                                wght = 1
                                #targetreweight = {"gg": ["p_Gen_GG_SIG_kappaTopBot_1_ghz1_1_MCFM*KFactor_QCD_ggZZ_Nominal", "p_Gen_GG_BSI_kappaTopBot_1_ghz1_1_MCFM*KFactor_QCD_ggZZ_Nominal", "p_Gen_GG_BKG_MCFM*KFactor_QCD_ggZZ_Nominal"],
                 #"VBF": ["p_Gen_JJEW_SIG_ghv1_1_MCFM*0.5", "p_Gen_JJEW_BSI_ghv1_1_MCFM*0.5", "p_Gen_JJEW_BKG_MCFM*0.5"],
                  #                                "ZZTo4l": ["1"]}
                  
                  
                  
                                k3nlo = 1.147
              
                
                                if production == "gg" : 
                                    
                                    if targetcomp == 0 : wght = k3nlo*event.p_Gen_GG_SIG_kappaTopBot_1_ghz1_1_MCFM*event.KFactor_QCD_ggZZ_Nominal
                                    if targetcomp == 1 : wght = k3nlo*(event.p_Gen_GG_BSI_kappaTopBot_1_ghz1_1_MCFM -event.p_Gen_GG_SIG_kappaTopBot_1_ghz1_1_MCFM - event.p_Gen_GG_BKG_MCFM)*event.KFactor_QCD_ggZZ_Nominal
                                    if targetcomp == 2 : wght = k3nlo*event.p_Gen_GG_BKG_MCFM*event.KFactor_QCD_ggZZ_Nominal

                                    #categorization corrections
                                    wcatcor = 1
                                    if correctionsOn : 
                                        corb = hcor.FindBin(event.ZZMass)
                                        wcatcor = hcor.GetBinContent(corb)
                                    wght = wght*wcatcor
                                   
                                if production == "ZZTo4l" :
                                    wght = event.KFactor_EW_qqZZ 
                                    
                                if production == "VBF" :  
                                    if targetcomp == 0 : wght = event.p_Gen_JJEW_SIG_ghv1_1_MCFM*0.5
                                    if targetcomp == 1 : wght = (event.p_Gen_JJEW_BSI_ghv1_1_MCFM - event.p_Gen_JJEW_SIG_ghv1_1_MCFM - event.p_Gen_JJEW_BKG_MCFM )*0.5
                                    if targetcomp == 2 : wght = event.p_Gen_JJEW_BKG_MCFM*0.5
                                    samplew = -1.
                                    samplew = eval( "event."+sampleweight ) 
                                    wght = wght/samplew 
                                    

                                    #categorization corrections only for pure signal
                                    wewcatcor = 1
                                    if (event.ZZMass < 600)  and int(targetcomp) == 0 and correctionsOn : 
                                        wewcatcor = EWcor(targetcateg,event.ZZMass,ew_fparams[0],ew_fparams[1],ew_fparams[2],ew_fparams[3])                                        
                                    wght = wght*wewcatcor
                                   


                                weight_nom = wght*lumi_year*1000*event.xsec*event.overallEventWeight*event.L1prefiringWeight/event.Bin40   
                                #print (weight_nom,wght,event.p_Gen_GG_SIG_kappaTopBot_1_ghz1_1_MCFM)
                                htt.Fill(event.ZZMass,event.Dbkg,event.Dbsi,weight_nom)
                                #print (event.ZZMass,"Dbsi" , event.Dbsi,"Dbkg",event.Dbkg)
                                htt_nom.Fill(event.ZZMass,weight_nom)
                                
                                #print ("for background ",weight_nom,htt.Integral())

                                


                                for isyst,systt in enumerate(htt_syst) : 
                                    syst_nm = shape_syst_list[isyst]
                                    
                                    
                                    wsystu = 1.0
                                    wsystdn = 1.0
                                    
                                    if "kf" in syst_nm :
                                        
                                        if"pdf" in syst_nm : 
                                            wsystu = event.KFactor_QCD_ggZZ_PDFScaleUp
                                            wsystdn = event.KFactor_QCD_ggZZ_PDFScaleDn
                                        if "as" in syst_nm : 
                                            wsystu = event.KFactor_QCD_ggZZ_AsUp
                                            wsystdn = event.KFactor_QCD_ggZZ_AsDn
                                        if "qcd" in syst_nm : 
                                            wsystu = event.KFactor_QCD_ggZZ_QCDScaleUp
                                            wsystdn = event.KFactor_QCD_ggZZ_QCDScaleDn
                                        wsystu = wsystu/event.KFactor_QCD_ggZZ_Nominal
                                        wsystdn = wsystdn/event.KFactor_QCD_ggZZ_Nominal   
                                        
                                    elif "pythiascale" in syst_nm :
                                        
                                        wpfu = event.PythiaWeight_fsr_muR4/event.PythiaWeight_isr_muRoneoversqrt2
                                        wpiu = event.PythiaWeight_isr_muR4/event.PythiaWeight_isr_muRoneoversqrt2
                                        wpfd = event.PythiaWeight_fsr_muR0p25/event.PythiaWeight_isr_muRoneoversqrt2
                                        wpid = event.PythiaWeight_isr_muR0p25/event.PythiaWeight_isr_muRoneoversqrt2
                                        
                                        wsystu   =wpfu*wpiu # + wpiu*wpiu )
                                        wsystdn  =wpfd*wpid #  + wpid*wpid ) 
                                        #print (wsystu,wsystdn)
                                        
                                    else :
                                        
                                        if "EWqqZZ" in syst_nm: 
                                            wsystu   = 1.0 + event.KFactor_EW_qqZZ_unc
                                            wsystdn  = 1.0 - event.KFactor_EW_qqZZ_unc
                                        
                                    #check direction of uncertainties
                                    if not (1 - wsystdn)*(1 - wsystu) < 0 : 
                                        
                                       wmax =  max( abs(1- wsystdn),abs(1 - wsystu))
                                       wsystdn = 1 - wmax
                                       wsystu  = 1 + wmax
                                    htt_syst[isyst][0].Fill(event.ZZMass,event.Dbkg,event.Dbsi,wsystu*weight_nom)                 
                                    htt_syst[isyst][1].Fill(event.ZZMass,event.Dbkg,event.Dbsi,wsystdn*weight_nom)

                        if count == 0:
                            ht.Add(htt)
                            ht_nom.Add(htt_nom)
                            ht_systdn.Add(htt_ew_systdn)
                            ht_systup.Add(htt_ew_systup)
                            
                            for isyst in range(0,len(ht_syst)) : 
                                ht_syst[isyst][0].Add(htt_syst[isyst][0])
                                ht_syst[isyst][1].Add(htt_syst[isyst][1])
                                
                        else:
                            ht.Add(htt)
                            ht_nom.Add(htt_nom)
                            ht_systdn.Add(htt_ew_systdn)
                            ht_systup.Add(htt_ew_systup)
                            
                            for isyst in range(0,len(ht_syst)) : 
                                ht_syst[isyst][0].Add(htt_syst[isyst][0])
                                ht_syst[isyst][1].Add(htt_syst[isyst][1])
            
            ht.Scale(1./count)
            ht_nom.Scale(1./count)
            ht_systdn.Scale(1./count)
            ht_systup.Scale(1./count)
            for isyst in range(0,len(ht_syst)) : 
                ht_syst[isyst][0].Scale(1./count)
                ht_syst[isyst][1].Scale(1./count)
                            
            #print ("ht = ",ht.Integral(),"count :",count)        
            #print("ht = ", ht.Integral())
            hs.Add(ht)
            #print ("hs =", hs.Integral())
            for isyst in range(0,len(hs_syst)) : 
                hs_syst[isyst][0].Add(ht_syst[isyst][0])
                hs_syst[isyst][1].Add(ht_syst[isyst][1])
                            
            hs_systdn.Add(ht_systdn)
            hs_systup.Add(ht_systup)
            hs_nom.Add(ht_nom)
            #hs_qr_up.Add(ht_qr_up)
            #hs_qr_dn.Add(ht_qr_dn) 
            #print("hs = ", hs.GetEntries())

        #print ("hf  before addition:",hf.GetEntries())    
        hf.Add(hs)
        #print  ("hf = ", hf.GetEntries())
        for isyst in range(0,len(hf_syst)) : 
            hf_syst[isyst][0].Add(hs_syst[isyst][0])
            hf_syst[isyst][1].Add(hs_syst[isyst][1])
            #hf_syst[isyst][0].Scale(1./len(yeardict.keys()))
            #hf_syst[isyst][1].Scale(1./len(yeardict.keys()))
            hf_syst[isyst][0].SetName(production+"_"+str(targetcomp)+"_"+shape_syst_list[isyst]+"_up")
            hf_syst[isyst][1].SetName(production+"_"+str(targetcomp)+"_"+shape_syst_list[isyst]+"_dn")

        hf_systdn.Add(hs_systdn)
        hf_systup.Add(hs_systup)
        hf_nom.Add(hs_nom)


        #print("hf = ", hf_nom.Integral())
        #hf.Scale(1./len(yeardict.keys()))
        #print (1./len(yeardict.keys()))
        #hf_systdn.Scale(1./len(yeardict.keys()))
        #hf_systup.Scale(1./len(yeardict.keys()))
        #hf_nom.Scale(1./len(yeardict.keys()))
        hf.SetName(production+"_"+str(targetcomp))
        #print("hf@listapp  = ", hf_nom.Integral())
        h_list.append(hf)
        
        for isyst in range(0,len(hf_syst)) :
            
            h_list.append(hf_syst[isyst][0])
            h_list.append(hf_syst[isyst][1])
            #print (" >> :",hf_syst[isyst][0].Integral(),hf_syst[isyst][1].Integral())
        #for ih in h_list : 
        #    print ("this:",ih.GetName(),ih.Integral())

syst_list = []


#
if procsystfile == "" :  
    if production == "gg" : 
        syst_list = ["kfqcd","kfpdf","kfas","pythiascale"]
    if production == "ZZTo4l" : 
        syst_list = ["EWqqZZ"]

h_list_withsyst =[]
catt = -1
if category == "Untagged" : catt = 0 
if category == "VBFtagged" : catt = 1 
if category == "VHtagged" : catt = 2

assert not (catt == -1), "Invalid Category" 


flav = ""
for tcomp in ltargetcomp: 
       print ("Running ",production," ",catt,"  comp:",tcomp)    #FillHist(production,tcomp,catt,h_list_withsyst,syst_list_ggh)
       FillHist(production,tcomp,catt,h_list_withsyst,syst_list,iffile,targetyear,1)


       
foutname = "./Output/output_"+production+"_"+category+"_"+str(iffile)+"_"+str(targetyear)+"_"+flav+"_withsyst.root"
if not  procsystfile == "" :   
    foutname = "./Output/output_"+production+"_"+category+"_"+str(iffile)+"_"+str(targetyear)+"_"+flav+"_"+procsystfile+".root"
   
print (foutname,flav)
fout = ROOT.TFile(foutname,"recreate")
fout.cd()



#=================== writting output ===============================================================================================

print  ("here")
for ihist in h_list_withsyst: 
    print ("writting :",ihist.GetName(),ihist.Integral(),targetyear)
    ihist.Write()

fout.Close()



