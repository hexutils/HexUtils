#!/usr/bin/env python
# convert jupyter to python get_ipython().system('jupyter nbconvert --to script CategorizedTemplateMake-Parts.ipynb')

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
#get_ipython().run_line_magic('jsroot', 'on')

import sys

production = sys.argv[1]
category   = sys.argv[2]

print (production, category)

lumi = {'MC_2016_CorrectBTag':35.9, 'MC_2017':41.5, 'MC_2018':59.7}




medges = np.array([220, 230, 240, 250, 260, 280, 310, 340, 370, 400, 475, 550, 625, 700, 800, 900, 1000, 1200, 1600, 2000, 3000, 13000], dtype='float64')
# medges = np.array([220, 230, 240, 250, 260, 280, 310, 340, 370, 400, 475, 550, 625, 700, 800, 900, 1000, 1200, 1600, 2000, 13000], dtype='float64')
## medges = np.array([220, 260, 370, 625, 1000, 13000], dtype='float64')
## medges = np.array([220, 400, 3000, 13000], dtype='float64')
# medges = 5*np.arange(401, dtype='float64')
#d1edges = np.arange(21, dtype='float64') / 20 * 12780 + 220
##d1edges = np.array([ 220.,  316.,  412.,  508.,  604.,  700.,  796.,  892.,  988., 1084., 1180., 1276., 1372., 1468., 1564., 1660., 1756., 1852., 1948., 2044., 13000])
##d1edges = np.array([ 220.,  828., 1436., 2044.])
#d1edges = np.array([220, 4480, 8740, 13000], dtype='float64')
#d1edges = np.array([220, 13000], dtype='float64')
d1edges = np.arange(21, dtype='float64') / 20
#d1edges = np.arange(6, dtype='float64') / 5
# d1edges = np.arange(4, dtype='float64') / 3
# d1edges = np.arange(3, dtype='float64') / 2
d2edges = np.arange(21, dtype='float64') / 10 - 1
#d2edges = np.arange(6, dtype='float64') / 2.5 - 1
# d2edges = np.arange(4, dtype='float64') / 1.5 - 1
# d2edges = np.arange(3, dtype='float64') / 1 - 1


print("medges", len(medges))
print("medges", (medges))
print("d1edges", len(d1edges))
print("d1edges", (d1edges))
print("d2edges", len(d2edges))
print("d2edges", (d2edges))


#input
#treelistpath = "/eos/user/l/lkang/Active_Research/Discriminants/alltaggedtrees.txt"
#treelistpath = "/eos/user/s/skyriaco/SWAN_projects/Offshel_tempmaker/outputtree_list.txt"
#treelistpath = "/eos/user/s/skyriaco/SWAN_projects/Offshel_tempmaker/output_highmass1618.txt"
treelistpath = "/eos/user/s/skyriaco/SWAN_projects/Offshel_tempmaker/alloutput.txt"
#treelistpath = "singleinput.txt"

treelist = []

with open(treelistpath) as f:
    llist = [line.rstrip() for line in f]
        
for line in llist:
    if os.path.exists(line): 
        treelist.append(line)



yeardict = {}

for numfile in range(0,len(treelist)):
    filename = treelist[numfile]
    ind = filename.split("/").index("200205_CutBased")

    year = filename.split("/")[ind:][1]

    if year not in yeardict.keys():
        yeardict[year] = {}
    else:
        if "ZZTo4l" in filename.split("/")[ind:][2]: prod = "ZZTo4l"
        else: prod = filename.split("/")[ind:][3]
            
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
#print (yeardict)

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



# ### Fill histogram
def FillHist(targetprod,targetcomp,targetcateg,h_list,shape_syst_list) :

#    print (targetreweight[targetprod][targetcomp])
#    print (targetprod,targetcomp,targetcateg)
#    weight = "{}*((Z1Flav*Z2Flav)==(121*121) ||(Z1Flav*Z2Flav)==(169*169) ||(Z1Flav*Z2Flav)==(121*169)  )*137.1*(ZZMass>=220)*(EventTag=={})*1000*xsec*overallEventWeight*L1prefiringWeight/Bin40".format(targetreweight[targetprod][targetcomp], targetcateg)
#    weightewzzup = "{}*(1.0 + KFactor_EW_qqZZ_unc)*((Z1Flav*Z2Flav)==(121*121) ||(Z1Flav*Z2Flav)==(169*169) ||(Z1Flav*Z2Flav)==(121*169)  )*137.1*(ZZMass>=220)*(EventTag=={})*1000*xsec*overallEventWeight*L1prefiringWeight/Bin40".format(targetreweight[targetprod][targetcomp], targetcateg)
#    weightewzzdn = "{}*(1.0 - KFactor_EW_qqZZ_unc)*((Z1Flav*Z2Flav)==(121*121) ||(Z1Flav*Z2Flav)==(169*169) ||(Z1Flav*Z2Flav)==(121*169)  )*137.1*(ZZMass>=220)*(EventTag=={})*1000*xsec*overallEventWeight*L1prefiringWeight/Bin40".format(targetreweight[targetprod][targetcomp], targetcateg)
    
#    weightqrup = "{}*((Z1Flav*Z2Flav)==(121*121) ||(Z1Flav*Z2Flav)==(169*169) ||(Z1Flav*Z2Flav)==(121*169)  )*137.1*(ZZMass>=220)*(EventTag=={})*1000*xsec*overallEventWeight*L1prefiringWeight/Bin40".format(targetreweight[targetprod][targetcomp], targetcateg)
#    weightqrdn = "{}*((Z1Flav*Z2Flav)==(121*121) ||(Z1Flav*Z2Flav)==(169*169) ||(Z1Flav*Z2Flav)==(121*169)  )*137.1*(ZZMass>=220)*(EventTag=={})*1000*xsec*overallEventWeight*L1prefiringWeight/Bin40".format(targetreweight[targetprod][targetcomp], targetcateg)

    
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
        
    
    #hf_qr_up  = ROOT.TH1F("hf_qr_up","",100,0,2000)
    #hf_qr_dn  = ROOT.TH1F("hf_qr_dn","",100,0,2000)

    
    
    
    hf.SetDirectory(0)
    hf_systdn.SetDirectory(0)
    hf_systup.SetDirectory(0)
    hf_nom.SetDirectory(0)
    
    for keynum in range(0,len(yeardict.keys())):
        year = list(yeardict.keys())[keynum]
        print (list(yeardict.keys())[keynum])
        #if year != targetyear: continue
        #print("\n", year, lumi[year])

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
            
        
        #hs_qr_up  = ROOT.TH1F("hs_qr_up","",100,0,2000)
        #hs_qr_dn  = ROOT.TH1F("hs_qr_dn","",100,0,2000)
        
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
                
                


        
            #ht_qr_up  = ROOT.TH1F("ht_qr_up","",100,0,2000)
            #ht_qr_dn  = ROOT.TH1F("ht_qr_dn","",100,0,2000)
            
            #ht_qr_up.SetDirectory(0)
            #ht_qr_dn.SetDirectory(0)

            ht.SetDirectory(0)
            ht_systdn.SetDirectory(0)
            ht_systup.SetDirectory(0)
            ht_nom.SetDirectory(0)
            count = 0
            
            print ("about to fill")
            for itfile,tfile in enumerate(range(len(decay))):
                
                #print(decay[tfile])
                if "VBF" in decay[tfile]:
                    skey = decay[tfile].split("/")[-2].replace('_M125_GaSM', '')
                    sampleweight = refden[skey]

                if ( os.stat(decay[tfile]).st_size > 100 ):  
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


                        
                        #htt_qr_up  = ROOT.TH1F("hs_qr_up","",100,0,2000)
                        #htt_qr_dn  = ROOT.TH1F("hs_qr_dn","",100,0,2000)
            
                        #Load branches


                        for iev,event in enumerate(t):
                            #if iev > 1000 : continue
                            if not ( (event.Z1Flav*event.Z2Flav)==(121*121) or (event.Z1Flav*event.Z2Flav)==(169*169) or (event.Z1Flav*event.Z2Flav)==(121*169) ) : continue
                            if not (event.ZZMass >= 220) : continue
                            
                            if (event.EventTag == targetcateg) : 

                                
                                wght = 0
                                #targetreweight = {"gg": ["p_Gen_GG_SIG_kappaTopBot_1_ghz1_1_MCFM*KFactor_QCD_ggZZ_Nominal", "p_Gen_GG_BSI_kappaTopBot_1_ghz1_1_MCFM*KFactor_QCD_ggZZ_Nominal", "p_Gen_GG_BKG_MCFM*KFactor_QCD_ggZZ_Nominal"],
                 #"VBF": ["p_Gen_JJEW_SIG_ghv1_1_MCFM*0.5", "p_Gen_JJEW_BSI_ghv1_1_MCFM*0.5", "p_Gen_JJEW_BKG_MCFM*0.5"],
                  #                                "ZZTo4l": ["1"]}

                                

                                if production == "gg" : 
                                    if targetcomp == 0 : wght = event.p_Gen_GG_SIG_kappaTopBot_1_ghz1_1_MCFM*event.KFactor_QCD_ggZZ_Nominal
                                    if targetcomp == 1 : wght = event.p_Gen_GG_BSI_kappaTopBot_1_ghz1_1_MCFM*event.KFactor_QCD_ggZZ_Nominal
                                    if targetcomp == 2 : wght = event.p_Gen_GG_BKG_MCFM*event.KFactor_QCD_ggZZ_Nominal
                                    
                                if production == "ZZTo4l" :
                                    wght =1
                                if production == "VBF" : 
                                    if targetcomp == 0 : wght = event.p_Gen_JJEW_SIG_ghv1_1_MCFM*0.5
                                    if targetcomp == 1 : wght = event.p_Gen_JJEW_BSI_ghv1_1_MCFM*0.5
                                    if targetcomp == 2 : wght = event.p_Gen_JJEW_BKG_MCFM*0.5
                                    

                                weight_nom = wght*137.1*1000*event.xsec*event.overallEventWeight*event.L1prefiringWeight/event.Bin40   
                                
                                htt.Fill(event.ZZMass,event.Dbsi,event.Dbkg,weight_nom)
                                htt_nom.Fill(event.ZZMass,weight_nom)
                                
                                for isyst,systt in enumerate(htt_syst) : 
                                    #need to change here the up and down systematics
                                    wsystu,wsystdn  = getsyst("pdf",0,2018,event.ZZMass)
                                    #print (wsystu,wsystdn)
                                    #print (htt_syst[isyst])
                                    htt_syst[isyst][0].Fill(event.ZZMass,event.Dbsi,event.Dbkg,wsystu*weight_nom)                     
                                    htt_syst[isyst][1].Fill(event.ZZMass,event.Dbsi,event.Dbkg,wsystdn*weight_nom)
                                    #print (weight_nom,wsystu,wsystdn)

                                    

                        #t.Draw("Dbsi:Dbkg:ZZMass>>htt",weight,"")                        
                        #t.Draw("ZZMass>>htt_nom",weight,"")
                        #t.Draw("ZZMass>>htt_ew_systup",weightewzzup,"")
                        #t.Draw("ZZMass>>htt_ew_systdn",weightewzzdn,"")
                        #t.Draw("ZZMass>>htt_qr_up",weightqrup,"")    
                        #t.Draw("ZZMass>>htt_qr_dn",weightqrdn,"")    
                        #print ("htt_up:", htt_ew_systup.Integral())
                        #print ("htt_dn:", htt_ew_systdn.Integral())
                        #print("doneevents",htt.Integral())
                        if count == 0:
                            #print("ADDED --- htt = ", htt.Integral())
                            ht.Add(htt)
                            ht_nom.Add(htt_nom)
                            ht_systdn.Add(htt_ew_systdn)
                            ht_systup.Add(htt_ew_systup)
                            
                            for isyst in range(0,len(ht_syst)) : 
                                ht_syst[isyst][0].Add(htt_syst[isyst][0])
                                ht_syst[isyst][1].Add(htt_syst[isyst][1])
                                

                            #ht_qr_up.Add(htt_qr_up)
                            #ht_qr_dn.Add(htt_qr_dn)
                            
                            
                            count+=1
                        elif htt.Integral() > ((ht.Integral()/count) + 2*sqrt((ht.Integral()/count))): 
                            print("SKIPPED --- htt = ", htt.Integral())
                        elif htt.Integral() < ((ht.Integral()/count) - 2*sqrt((ht.Integral()/count))): 
                            print("SKIPPED --- htt = ", htt.Integral())
                        else:
                            #print("ADDED --- htt = ", htt.Integral())
                            ht.Add(htt)
                            ht_nom.Add(htt_nom)
                            ht_systdn.Add(htt_ew_systdn)
                            ht_systup.Add(htt_ew_systup)
                            
                            for isyst in range(0,len(ht_syst)) : 
                                ht_syst[isyst][0].Add(htt_syst[isyst][0])
                                ht_syst[isyst][1].Add(htt_syst[isyst][1])
                                
                                            
                            #ht_qr_up.Add(htt_qr_up)
                            #ht_qr_dn.Add(htt_qr_dn)    
                            
                            count+=1
            #print ("ht = ", ht.Integral())
            #print ("count :",count)
            ht.Scale(1./count)
            ht_nom.Scale(1./count)
            ht_systdn.Scale(1./count)
            ht_systup.Scale(1./count)
            for isyst in range(0,len(ht_syst)) : 
                ht_syst[isyst][0].Scale(1./count)
                ht_syst[isyst][1].Scale(1./count)
                            
                    
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
            #print("hs = ", hs.Integral())

        hf.Add(hs)
        #print  ("hf = ", hf.Integral())
        for isyst in range(0,len(hf_syst)) : 
            hf_syst[isyst][0].Add(hs_syst[isyst][0])
            hf_syst[isyst][1].Add(hs_syst[isyst][1])
            hf_syst[isyst][0].Scale(1./len(yeardict.keys()))
            hf_syst[isyst][1].Scale(1./len(yeardict.keys()))
            hf_syst[isyst][0].SetName(production+"_"+str(targetcomp)+"_"+shape_syst_list[isyst]+"_up")
            hf_syst[isyst][1].SetName(production+"_"+str(targetcomp)+"_"+shape_syst_list[isyst]+"_dn")

        hf_systdn.Add(hs_systdn)
        hf_systup.Add(hs_systup)
        hf_nom.Add(hs_nom)


        #print("hf = ", hf_nom.Integral())
        hf.Scale(1./len(yeardict.keys()))
        hf_systdn.Scale(1./len(yeardict.keys()))
        hf_systup.Scale(1./len(yeardict.keys()))
        hf_nom.Scale(1./len(yeardict.keys()))
        hf.SetName(production+"_"+str(targetcomp))
        h_list.append(hf)

        for isyst in range(0,len(hf_syst)) :
            
            h_list.append(hf_syst[isyst][0])
            h_list.append(hf_syst[isyst][1])
            #print (" >> :",hf_syst[isyst][0].Integral(),hf_syst[isyst][1].Integral())
        #for ih in h_list : 
        #    print ("this:",ih.GetName(),ih.Integral())

syst_list = []
if production == "gg" : 
    syst_list = ["qcd_ren","qcd_fact","pdf","a_strong"]
h_list_withsyst =[]
catt = -1
if category == "Untagged" : catt = 0 
if category == "VBFtagged" : catt = 1 
if category == "VHtagged" : catt = 2

assert not (catt == -1), "Invalid Category" 


for tcomp in ltargetcomp: 
       print ("Running ",production," ",catt,"  comp:",tcomp)    #FillHist(production,tcomp,catt,h_list_withsyst,syst_list_ggh)
       FillHist(production,tcomp,catt,h_list_withsyst,syst_list)

       

'''
        
#=========================================  

syst_list_vbf = []

h_ew_unt =[]
for tcomp in ltargetcomp: 
       FillHist("VBF",tcomp,0,h_ew_unt,syst_list_vbf)

h_ew_vbf =[]
for tcomp in ltargetcomp: 
       FillHist("VBF",tcomp,1,h_ew_vbf,syst_list_vbf)

h_ew_vh =[]
for tcomp in ltargetcomp: 
       FillHist("VBF",tcomp,2,h_ew_vh,syst_list_vbf)      
              
#=========================================  

'''


foutname = "output_"+production+"_"+category+"_withsyst.root"
fout = ROOT.TFile(foutname,"recreate")
fout.cd()

print  ("here")
for ihist in h_list_withsyst: 
    print ("writting :",ihist.GetName(),ihist.Integral())
    ihist.Write()

fout.Close()


#check that syst are not overwritten 



'''
h_bkg_unt =[]
FillHist("ZZTo4l",0,0,h_bkg_unt)
h_bkg_vbf =[]
FillHist("ZZTo4l",0,1,h_bkg_vbf)
h_bkg_vh =[]
FillHist("ZZTo4l",0,2,h_bkg_vh)      
'''       


# ### Add to 'hlist' if the output looks reasonable above

'''

c1 = ROOT.TCanvas("c1","c1",1800,600)
c1.Divide(3,1)
h_bkg_unt[3].SetLineColor(2)
h_bkg_vh[3].SetLineColor(2)
h_bkg_vbf[3].SetLineColor(2)

h_bkg_unt[1].SetLineStyle(2)
h_bkg_vh[1].SetLineStyle(2)
h_bkg_vbf[1].SetLineStyle(2)


h_bkg_unt[2].SetLineStyle(2)
h_bkg_vh[2].SetLineStyle(2)
h_bkg_vbf[2].SetLineStyle(2)


c1.cd(1).SetLogy()
#c1.cd(1)

print (h_bkg_unt[1].Integral())
h_bkg_unt[3].Draw("hist")
h_bkg_unt[3].GetXaxis().SetTitle("qqZZ Untagged background m4l [GeV]")
h_bkg_unt[1].Draw("hist,same")
h_bkg_unt[2].Draw("hist,same")
c1.cd(2).SetLogy()
#c1.cd(2)
h_bkg_vh[3].Draw("hist")
h_bkg_vh[3].GetXaxis().SetTitle("qqZZ VHtagged background m4l [GeV]")
h_bkg_vh[1].Draw("hist,same")
h_bkg_vh[2].Draw("hist,same")



c1.cd(3).SetLogy()
#c1.cd(3)
h_bkg_vbf[3].Draw("hist")
h_bkg_vbf[3].GetXaxis().SetTitle("qqZZ VBFtagged background m4l [GeV]")
h_bkg_vbf[1].Draw("hist,same")
h_bkg_vbf[2].Draw("hist,same")


ROOT.gStyle.SetOptStat(1)
c1.Draw()
ROOT.gStyle.SetOptStat(1)
c1.Update()

c1.SaveAs("back_ew_qqzz.png")
c1.SaveAs("back_ew_qqzz.pdf")





'''






'''
print  (h_gg_unt)


# In[ ]:


print (h_list)


# In[ ]:


hlist


# In[ ]:


for h in h_list:
    print (h)
    print(h.Integral())


# # Unroll and Visualize all histograms in 'hlist'

# ##### Do not proceed if your 'hlist' is not filled. Recall it expects 7 histograms ordered like: ['ggH SIG', 'ggH BSI', 'ggH BKG', 'EW SIG', 'EW BSI', 'EW BKG', 'qqbar BKG']
# ##### If you simply want to test the unrolling section, just fill the list with 7 copies of the same TH3F histogram

# ### Unroll all 7 histograms

# In[ ]:


hlist1d = []
hlisttemp = h_list
for hf in hlisttemp:
    totgbins = hf.GetNbinsX() * hf.GetNbinsY() * hf.GetNbinsZ()
    totgedges = np.arange(totgbins+1, dtype='float64')

    #hf1d = ROOT.TH1F("hf1d","",len(totgedges)-1, totgedges)
    hf1d = ROOT.TH1F("hf1d","",totgbins, 0, totgbins)
    hf1d.SetDirectory(0)

    bincount = 1

    for xbin in trange(hf.GetNbinsX()):
        for ybin in range(hf.GetNbinsY()):
            for zbin in range(hf.GetNbinsZ()):
                gbin = hf.GetBin(xbin+1, ybin+1, zbin+1)

                #if gbin<400: print(xbin, ybin, zbin)
                #print(gbin)
                #print(bincount)
                if bincount>totgbins: 
                    print("WHAT")
                    break
                    
                #if hf.GetBinContent(gbin) != 0: print(hf.GetBinContent(gbin))
                #print(hf.GetBinContent(gbin))
                
                hf1d.SetBinContent(bincount, hf.GetBinContent(gbin))
                bincount += 1
                #if hf.GetBinContent(gbin) != 0: print("YAY")
    
    hlist1d.append(hf1d)


# In[ ]:


c1 = ROOT.TCanvas("c1","c1",4480,600)
c1.Divide(len(hlist1d),1)
for i in range(len(hlist1d)):
    c1.cd(i+1)
    print(hlist1d[i].Integral())
    hlist1d[i].Draw("hist")

ROOT.gStyle.SetOptStat(1)
c1.Draw()


# ### Isolate INT from the BSI histograms and also add the total combination of statistics as a new histogram at the end

# In[ ]:


hlist1d[1].Add(hlist1d[0], -1)
hlist1d[1].Add(hlist1d[2], -1)

hlist1d[4].Add(hlist1d[3], -1)
hlist1d[4].Add(hlist1d[5], -1)


# In[ ]:


c1 = ROOT.TCanvas("c1","c1",4480,600)
c1.Divide(len(hlist1d),1)
for i in range(len(hlist1d)):
    c1.cd(i+1)
    print(hlist1d[i].Integral())
    hlist1d[i].Draw("hist")

ROOT.gStyle.SetOptStat(1)
c1.Draw()


# In[ ]:


hf1d = ROOT.TH1F("hf1d","",totgbins, 0, totgbins)
hf1d.SetDirectory(0)
hf1d.Add(hlist1d[1])
hlist1d.insert(1, hf1d)


# In[ ]:


c1 = ROOT.TCanvas("c1","c1",4480,600)
c1.Divide(len(hlist1d),1)
for i in range(len(hlist1d)):
    c1.cd(i+1)
    print(hlist1d[i].Integral())
    hlist1d[i].Draw("hist")

ROOT.gStyle.SetOptStat(1)
c1.Draw()


# In[ ]:


hf1d = ROOT.TH1F("hf1d","",totgbins, 0, totgbins)
hf1d.SetDirectory(0)
hf1d.Add(hlist1d[5])
hlist1d.insert(5, hf1d)


# In[ ]:


c1 = ROOT.TCanvas("c1","c1",4480,600)
c1.Divide(len(hlist1d),1)
for i in range(len(hlist1d)):
    c1.cd(i+1)
    print(hlist1d[i].Integral())
    hlist1d[i].Draw("hist")

ROOT.gStyle.SetOptStat(1)
c1.Draw()


# In[ ]:


for i in range(hlist1d[1].GetXaxis().GetNbins()):
    b = i+1
    if hlist1d[1].GetBinContent(b) >= 0:
        hlist1d[1].SetBinContent(b, 0)

for i in range(hlist1d[2].GetXaxis().GetNbins()):
    b = i+1
    if hlist1d[2].GetBinContent(b) <= 0:
        hlist1d[2].SetBinContent(b, 0)


# In[ ]:


c1 = ROOT.TCanvas("c1","c1",4480,600)
c1.Divide(len(hlist1d),1)
for i in range(len(hlist1d)):
    c1.cd(i+1)
    print(hlist1d[i].Integral())
    hlist1d[i].Draw("hist")

ROOT.gStyle.SetOptStat(1)
c1.Draw()


# In[ ]:


for i in range(hlist1d[5].GetXaxis().GetNbins()):
    b = i+1
    if hlist1d[5].GetBinContent(b) >= 0:
        hlist1d[5].SetBinContent(b, 0)

for i in range(hlist1d[6].GetXaxis().GetNbins()):
    b = i+1
    if hlist1d[6].GetBinContent(b) <= 0:
        hlist1d[6].SetBinContent(b, 0)


# In[ ]:


c1 = ROOT.TCanvas("c1","c1",4480,600)
c1.Divide(len(hlist1d),1)
for i in range(len(hlist1d)):
    c1.cd(i+1)
    print(hlist1d[i].Integral())
    hlist1d[i].Draw("hist")

ROOT.gStyle.SetOptStat(1)
c1.Draw()


# In[ ]:


hf1d = ROOT.TH1F("hf1d","",totgbins, 0, totgbins)
for i in range(len(hlist1d)):
    hf1d.Add(hlist1d[i])
hlist1d.append(hf1d)
print(hf1d.Integral())


# In[ ]:


c1 = ROOT.TCanvas("c1","c1",4480,600)
c1.Divide(len(hlist1d),1)
for i in range(len(hlist1d)):
    c1.cd(i+1)
    print(hlist1d[i].Integral())
    hlist1d[i].Draw("hist")

ROOT.gStyle.SetOptStat(1)
c1.Draw()


# In[ ]:


hlist1d[1].Scale(-1)
hlist1d[5].Scale(-1)


# In[ ]:


c1 = ROOT.TCanvas("c1","c1",4480,600)
c1.Divide(len(hlist1d),1)
for i in range(len(hlist1d)):
    c1.cd(i+1)
    print(hlist1d[i].Integral())
    hlist1d[i].Draw("hist")

ROOT.gStyle.SetOptStat(1)
c1.Draw()


# In[ ]:


hf1d = ROOT.TH1F("hf1d","",totgbins, 0, totgbins)
hf1d.Add(hlist1d[-1])


# In[ ]:


hlist1d.append(hf1d)


# In[ ]:


c1 = ROOT.TCanvas("c1","c1",4480,600)
c1.Divide(len(hlist1d),1)
for i in range(len(hlist1d)):
    c1.cd(i+1)
    print(hlist1d[i].Integral())
    hlist1d[i].Draw("hist")

ROOT.gStyle.SetOptStat(1)
c1.Draw()


# In[ ]:


hf1dt = hlist1d.pop(-1)


# In[ ]:


for i in range(hlist1d[-1].GetXaxis().GetNbins()):
    b = i+1
    if hlist1d[-1].GetBinContent(b) <= 0:
        hlist1d[-1].SetBinContent(b, 0)


# ### Check the final template collection and yields for the datacard

# In[ ]:


c1 = ROOT.TCanvas("c1","c1",4480,600)
c1.Divide(len(hlist1d),1)
for i in range(len(hlist1d)):
    c1.cd(i+1)
    print(hlist1d[i].Integral())
    hlist1d[i].Draw("hist")

ROOT.gStyle.SetOptStat(1)
c1.Draw()


# In[ ]:





# # Saving the whole thing to a .root file for use with a corresponding datacard

# ### Checking the names used to save the histograms

# In[ ]:


for i in proc:
    print(i)


# ### Set directory and output file names

# In[ ]:


diname = "/eos/user/s/skyriaco/SWAN_projects/Offshel_tempmaker/Output/"
foname = "Cat_4mu_137p1invfb_ggH4landVBF4landqqbar_mostEW_RECOpassedevents_mvar21d1reg20d2reg20.input.root"


# In[ ]:


print(diname+foname)


# ### Write to a .root file

# In[ ]:


fo = ROOT.TFile(diname+foname,"CREATE")

for i in range(len(proc)):
    hlist1d[i].Write(proc[i], ROOT.TFile.kSingleKey)

fo.Close()


# ### Check the saved file

# In[ ]:


fo = ROOT.TFile(diname+foname)
# fo = ROOT.TFile("/eos/user/l/lkang/Active_Research/Templates/SManalysis_split/2017/Untag/4mu/Untag_4mu_137p1invfb_ggH4landVBF4landqqbar_mostEW_RECOpassedevents_mvar21d1reg20d2reg20.input.root")

fo.ls()

c1 = ROOT.TCanvas("c1","c1",4480,600)
c1.Divide(len(proc),1)
for i in range(len(proc)):
    c1.cd(i+1)
    eval("print(proc[i], '\t\t=', fo."+proc[i]+".Integral())")
#     eval("print(fo."+proc[i]+".Integral())")
    eval("fo."+proc[i]+".Draw('hist')")
print()    

c1.Draw()
fo.Close()


#
#



# In[ ]:

'''


