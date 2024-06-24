import os
import sys
import ROOT
from Unroll_flow import Unrollflow as Unrollflow
from Unroll_gen  import Unrollgen as Unrollgen
from Rebin   import Rebin 
#from Rebin_dbs2          import Rebin 
import copy
nm = sys.argv[1]

#name = name.replace("_GEN_210702","")
#backfile = nm.replace("ggh","background")
#finbck = ROOT.TFile.Open(backfile)

processes=[]
fin = ROOT.TFile.Open(nm)
hists = []
#chanell  = "hzz4l_"+name.replace("templates_ggh_PhotonCouplings_decay_","")

#lumi = 300.0
#totggH = 17.568 + 10.39 + 9.249
#totsig_18002 =  4.7 + 0.3 + 5.7 + 0.3 + 0.7 + 2.1 + 0.2 + 0.5 + 1.5 + 5.5+3.2+98.9+.2+.1+1.1+.1+.1+1.1
#factorggH = totsig_18002/77.5*lumi/totggH 

#yeilds from writeup: gg0PM, bkg_gg , bkg_qqZZ 
#yields2e2mu = [6*2000.58,3468.04*lumi/3000.,6*(13.8/(3*77.)*lumi)]
#yields4e = [6*1011.14,1634.57*lumi/3000.,6*(13.8/(3*77.)*lumi)]
#yields4mu = [6*1257.96,2387.72*lumi/3000.,6*(13.8/(3*77.)*lumi)]





#print chanell
for key in fin.GetListOfKeys():
    if "TH3F" in key.GetClassName():
        h_name = key.GetName()
        print h_name
        h_temp = fin.Get(h_name)
        #print h_name
        #ideally here we unroll and add index and rate
        #print ("here:",h_name) 

        
        if "Un" in nm : 
            category = "Un"
        if "VH" in nm : 
            category = "VH"
        if "VBF" in nm : 
            category = "VBF"


        
        if "btag" in h_name and "ZZTo4" in h_name : 
            continue
        if "jes" in h_name and "ZZTo4" in h_name and category == "Un": 
            continue
        #if "jer" in h_name and "ZZTo4" in h_name and category == "Un": 
        #    continue



        #if not ( "data" in h_name or  "DATA"in h_name ) : 
        #    #print h_name
        #    h_temp.Scale((77.8)/137.5)




        if "jes" in h_name and "ZZTo4" in h_name and category == "Un"  : 
            continue
        if "jer" in h_name and "ZZTo4" in h_name and category == "Un" : 
            continue


        if h_name.count("Up") > 1 : continue 
        if h_name.count("Down") > 1 : continue 
        if h_name.count("JES") > 1 : continue 
        if h_name.count("JER") > 1 : continue 
        if h_name.count("jer") > 1 : continue 
        if h_name.count("jes") > 1 : continue 
        if h_name.count("btag") > 1 : continue 
        #print (">",h_name)
        thist = copy.deepcopy(h_temp)
     
        #calculate interference template
        #if "_1" in h_name:
        #    hpurename = h_name.replace("_1","_0")
        #    hbackname = h_name.replace("_1","_2")

        #    hpure = fin.Get(hpurename)
        #    hback = fin.Get(hbackname)

        #print  - hpure.Integral() - hback.Integral() + thist.Integral()

        #    thist.Add(hpure,-1)
        #    thist.Add(hback,-1)
        #print thist.Integral()
            
        #if("ZZTo4l" == h_name): 
        #    print h_name
        hns = h_name.replace("gg","offggH")
        hns = hns.replace("ZH125","qqH")       
        hns = hns.replace("JES","jes")
        hns = hns.replace("ttH125","ttH")
        hns = hns.replace("JER","jer")
        hns = hns.replace("VBF","offqqH")
        hns = hns.replace("ZZTo4l_0","back_qqZZ")
        hns = hns.replace("_ZX","_zjets")
        hns = hns.replace("_0","_0PM")

        if "ggH" in hns : hns = hns.replace("_1","_g11g21")
        if "qqH" in hns : hns = hns.replace("_1","_g12g22")
        
        hns = hns.replace("qcd","qcd")        
        if "offqqH_2" in hns :
            hns = hns.replace("offqqH_2","back_VVZZ")
        if "offggH_2" in hns :
            hns = hns.replace("offggH_2","back_ggZZ")
        
        #print hns

        thist.SetName(hns)    
        r_ate = thist.Integral()

        #if hns == "back_qqZZ": 

        #if "qqZZ" in hns : 
        #    print hns,r_ate
        
        #hnew = thist.Project3D("xy")
        if category == "Un" :  
            hnew = Rebin(thist,5,6)
            tn,tp = Unrollgen(hnew) #,category)
         
        else : 
            tn,tp = Unrollflow(thist,category)
        


        #new.GetNBinsZ()
        
        

        #if "g12g22" in tp.GetName(): 
        #if "qqZZ" in hns : 
        if "data" in hns : 
            print tn.GetName(),tp.GetName(),"interference comps:",tn.Integral(),tp.Integral()

        #if hns == "back_qqZZ": 
        #    print tn.Integral(),tp.Integral()
        #if hns == "ttH_0PM": 
        #    print tn.Integral(),tp.Integral()
        #print (tn.Integral(),tp.Integral(),hns)
        #if ("0PM_negative" in tn.GetName()):
        #    continue
        if ("back" in tp.GetName() or "0PM" in tp.GetName() or "ttH" in tp.GetName() ):
            print hns
            hns = tp.GetName()
            hns = hns.replace("_positive","")
            tp.SetName(hns)

        if ("back" in tn.GetName() or "ttH" in tn.GetName() or "0PM" in tn.GetName() ):
            hns = tn.GetName()
            hns = hns.replace("_negative","")
            tn.SetName(hns)
        

        if len(hists) > 0:
            if hists[len(hists)-1].GetName() == tp.GetName() or hists[len(hists)-1].GetName() == tn.GetName() : continue

        if tp.GetName() == tn.GetName()  : 

            
            processes.append((tp.GetName(),r_ate))
            tp.SetName(tp.GetName())
            print ("appending positive  ",tp.GetName(),tp.Integral())
            hists.append(tp)

        else :
            
            #print "here :",tp.GetName(),tn.GetName()
            

            tp.SetName(tp.GetName())
            tn.SetName(tn.GetName())
            
            #for ibinn in tp.GetXaxis().GetNbins():
            #    print (tp.GetBinContent(ibinn))
            r_ate = tp.Integral()
            #print tp.GetName(),r_ate
            #processes.append((tp.GetName(),r_ate)) if abs(r_ate) > 0  else 0
            if abs(r_ate) > 0 : 
                hists.append(tp) 
                #print ("appending ",tp.GetName())


            r_ate = tn.Integral()
            #print tn.GetName(),r_ate
            if abs(r_ate) > 0 and not "0PM" in tn.GetName() :
                processes.append((tn.GetName(),r_ate))  #else 0
                hists.append(tn)
                #print ("appending ",tn.GetName())
            



            
##data_obs = copy.deepcopy(hists[0])
#data_obs.SetName("data_obs")
#data_obs.Reset()

#with open('yields.txt') as yil:
#    lines = yil.readlines()

#vbfline = []
#vbfrate = []
#untagline = []
#untagrate = []
#vhline = []
#vhrate = []

'''
for line in lines :
    #print ("heeeeere:",line)
    l_ine = line.split()
    if "VBF" in l_ine and "offggH_0PM" in l_ine :
        vbfline = l_ine
    if "VBF" in l_ine and "offggH_0PM" not in l_ine :
        vbfrate = l_ine
    if "Untag" in l_ine and "offggH_0PM" in l_ine :
        untagline = l_ine
    if "Untag" in l_ine and "offggH_0PM" not in l_ine :
        untagrate = l_ine

    if "VH" in l_ine and "offggH_0PM" in l_ine :
        vhline = l_ine
    if "VH" in l_ine and "offggH_0PM" not in l_ine :
        vhrate = l_ine
    
'''
      
chanell = nm.replace(".root","")    
n_fout  = chanell+".inp.root"
n_fout = n_fout.replace(".input/","")

#print (n_fout)
fout =  ROOT.TFile.Open(n_fout,"recreate")
fout.cd()
        
hist_pre = copy.deepcopy(hists)    
hist_prenames = list(map((lambda x: x.GetName() ),hist_pre ))



#print hists

hupdated = []

    
for his in hists:
    hns = his.GetName()
    hnss = his.GetName()



    #Symmetrize weird systematic bins:
    
    if "Up" in hns or "up" in hns : 
        nmm= hns.split("_")
        nom_nam = nmm[0]
        #print (">>>",hnss,his.Integral)
        for ifield,field in enumerate(nmm):
            if "Up" not in hns:
                if ifield < len(nmm) -2 and ifield > 0:
                    nom_nam = nom_nam+"_"+field
            else :
                if ifield < len(nmm) -1 and ifield > 0:
                    nom_nam = nom_nam+"_"+field

        if "Up" in hns : down_nam = hns.replace("Up","Down")
        if "up" in hns : down_nam = hns.replace("_up","_dn")
        #down_nam = hns.replace("up","dn")        
        #print (hns,nom_nam,down_nam)
        ihnom = -1
        ihdown = -1
        for ihh,hh in enumerate(hists):
            if hh.GetName() == nom_nam :
               ihnom = ihh
            if hh.GetName() == down_nam:
               ihdown = ihh

        
        hnom  = hists[ihnom]
        hdown = hists[ihdown]

        #fix bins
        #print (hns,hnom.GetName(),hdown.GetName(),his.Integral(),hnom.Integral(),hdown.Integral())
        c_0u = his.GetBinContent(1)
        c_0n = hnom.GetBinContent(1)
        c_0d = hdown.GetBinContent(1)
        
        '''
        for ibin in range(hnom.GetXaxis().GetNbins()+1):

            c_nom = hnom.GetBinContent(ibin)
            c_down = hdown.GetBinContent(ibin)
            c_up = his.GetBinContent(ibin)

            if c_down == 0:
                hdown.SetBinContent(ibin,c_nom)
            if c_up == 0 :
                his.SetBinContent(ibin,c_nom)
            if c_nom == 0:     
                hdown.SetBinContent(ibin,c_nom)
                his.SetBinContent(ibin,c_nom)

            if (c_nom - c_down)*(c_nom - c_up) > 0 :
	        #print ("bad:",c_up,c_nom,c_down)
		if  (c_0u - c_0n)*(c_up - c_nom) > 0:
                    delta = abs(c_up - c_nom)
                    delta = -(c_up - c_nom)/abs((c_up - c_nom))*delta

                    if c_nom +delta > 0 : 
  
                        if ((c_nom + delta )/c_nom < 1.5 and (c_nom + delta )/c_nom > 0.5) :   
                            hdown.SetBinContent(ibin,c_nom +delta)
                        else: 
                            if delta > 0 : 
                                hdown.SetBinContent(ibin,1.5*c_nom)
                            else : 
                                hdown.SetBinContent(ibin,0.5*c_nom)
                else :
	            delta = abs(c_down - c_nom)
                    delta = -(c_down - c_nom)/abs((c_down - c_nom))*delta

                    if c_nom + delta > 0  :
                          
                        if ((c_nom + delta )/c_nom < 1.5 and (c_nom + delta )/c_nom > 0.5) :   
                            his.SetBinContent(ibin,c_nom +delta)
                        else: 
                            if delta > 0 : 
                                his.SetBinContent(ibin,1.5*c_nom)
                            else : 
                                his.SetBinContent(ibin,0.5*c_nom)
  

                    #his.SetBinContent(ibin,c_nom + delta)
                    
                        
		c_nom = hnom.GetBinContent(ibin)
                c_down = hdown.GetBinContent(ibin)
                c_up = his.GetBinContent(ibin)

        


        '''     
        hupdated.append(his)
        hupdated.append(hdown)    
    
    rate = -1.
    ratesyst = his.Integral()
    rateor = 1.0
    hsysname = ""
    if "back" in hns:
        hns = hns.replace("_positive","")
    if "up" not in hns and "dn" not in hns:
        hupdated.append(his)    

for hiss  in hupdated :

    hns = hiss.GetName()
    #print hns
    hns = hns.replace("_up","Up")    
    hns = hns.replace("_dn","Down")
    hns = hns.replace("a_strong","astrong")
    hns = hns.replace("qcd_fact","qcd_fact")
    hns = hns.replace("qcd_ren","qcdren")


    #name fixes to match 19-009 cards
    hns = hns.replace ("jes","CMS_scale_j")
    hns = hns.replace ("jer","CMS_res_j")
    if (not "CMS_btag_scale" in hns): 
        hns = hns.replace ("btag","CMS_btag_scale")
    hns = hns.replace ("EWqqZZ","EWcorr_qqZZ")
    hns = hns.replace ("pythiascale","CMS_pythia_scale")
    hns = hns.replace ("CMS_btag_scale","CMS_btag_comb")

    #synch with 19-009
    if "QCD" in hns : 
        if "ggH" in hns or "back_gg" in hns : 
            prodd = "_ggH"
        if "qqH" in hns or "back_VV" in hns : 
            prodd = "_qqH" 
        if "qqZZ" in hns : 
            prodd = "_qqbar"
        hns = hns.replace ("QCDmuRV","QCDscale_muR"+prodd)
        hns = hns.replace ("QCDmuFV","QCDscale_muF"+prodd)
    if "pdfV" in hns : 
        
        if "gg" in hns or "back_gg" in hns : 
            prodd = "_Higgs_gg"
        if "qqH" in hns or "back_VV" in hns: 
            prodd = "_Higgs_qqbar"
        if "qqZZ" in hns : 
            prodd = "_qqbar"
        hns = hns.replace ("pdfV","pdf"+prodd)
    if "AsMZV" in hns : 
        if "gg" in hns or "back_gg" in hns : 
            prodd = "_Higgs_gg"
        if "qqH" in hns  or "back_VV" in hns :
            prodd = "_Higgs_qqbar"
        if "back_qqZZ" in hns : 
            prodd = "_qqbar"
        hns = hns.replace ("AsMZV","pdf_As"+prodd)



    

    #print "fin:",hns
    
    hiss.SetName(hns)
    #if hns == "offqqH_0PM":
        #hdupl = copy.deepcopy(hiss)
        #hdupl.SetName("qqH_0PM")
        #inttt = hdupl.Integral()
        #hiss.Scale((2.6 + 3.85 )/3.85)
        #hiss.Write()
    #print hiss.GetName(),hiss.Integral()
    #if "positive" in hns:
    #    print hns,hiss.Integral()
    #    continue
    if hiss.Integral() <  0 :
        print ("Negative integral !!!", hiss.GetName() )
        continue
    #if hiss.Integral() < 0.00001 :
    #    print ("tiny integral !!!", hiss.GetName() )
    #    continue
    #print "here",hns
    #if "g12g22" in hns and ( "Up" in hns or "Down" in hns ):
    #    print "Not writting ",hns
    #    continue

    #if "Untagged" in fin.GetName() or "offgg" in hns: 
    #    if "btag" in hns : 
    #        continue
    #    if "scale_j" in hns : 
    #        continue
    #    if "res_j" in hns : 
    #        continue

    namee = hns
    if ("offgg"  in namee  )  and ( "QCDscale" in namee or "pdf_" in namee) : 
           continue
    
    
    if ("offgg"  in namee  or "back_gg" in namee )  and ( "kf" in namee) : 
        #print namee

        #print "duplicating and chaning name!"
        #if "kfqcd" in hns: 
            
            #htnew = copy.deepcopy(hiss)
            


        if "kfpdf" in hns : 
            hns = hns.replace("kfpdf","pdf_Higgs_gg")
        if "kfqcd" in hns : 
            hns = hns.replace("kfqcd","QCDscale_muR_ggH")
        if "kfas" in hns : 
            hns = hns.replace("kfas","pdf_As_Higgs_gg")
        hiss.SetName(hns)
        hiss.Write()
    else : 
        print "Writting:",hiss.GetName()


        hiss.Write()

    

    #if not ( "Up" in hiss.GetName() or "Down" in hiss.GetName() ) : 
    #    print ("data adding:",hiss.GetName(),hiss.Integral())
    #    data_obs.Add(hiss)
        


#data_obs.Write()
fout.Close()
#totyield = data_obs.Integral()
            
            
'''


            
#create and append background
for key in finbck.GetListOfKeys():
    if "TH3F" in key.GetClassName():
        #print key.GetName()
        h_name = key.GetName()
        h_temp = finbck.Get(h_name)
        r_ate = h_temp.Integral()
        hns = h_name.replace("template","")
        thist = copy.deepcopy(h_temp)
        
        thist.SetName(hns)
        tp,tn = Unroll(thist)
        intt  = tn.Integral()
        tflat = copy.deepcopy(tn)
        tflat.Reset()

        r_ate = lumi*intt/5.
        tn.Scale(r_ate/intt)

        
        
        
        #fill flat bckground :             
        nbins  = tflat.GetXaxis().GetNbins()
        #tflat.SetName("bkg_ggZZ")
        #tflatintt = tflatintt/5.
        for i in range(0,nbins) :
            tflat.SetBinContent(i,1)
        #r_ate = r_ate/5.
        r_ate = r_ate + 6.
        tfintt = tflat.Integral()
        tflat.Scale(6./tfintt)
        tn.Add(tflat)
        processes.append(("bkg_qqZZ",r_ate))
        #processes.append(("bkg_ggZZ",tflatintt))
        tn.SetName("bkg_qqZZ")
        hists.append(tn)
        #hists.append(tflat)

            
#write output root file            



#Write output datacard

proc = len(processes)
f = open(chanell+".GEN.txt", "w")
f.write("imax 1\n")
f.write("jmax "+str(proc -1)+"\n")
f.write("kmax *\n")
f.write("------------\n")
f.write("shapes * * $CHANNEL.GEN.input.root $PROCESS $PROCESS_$SYSTEMATIC\n")
f.write("------------\n")
f.write("bin "+str(chanell)+"\n")
f.write("observation "+ str(totyield)+"\n")
f.write("------------\n")

line= "bin"
line_p = "process"
line_rate = "rate"
line_indx = "process"
lineQCDsyst = "QCDsyst_bkg lnN"         
ibkg = 0 
for i,procc in enumerate(processes):
    line =line +" "+chanell
    line_p = line_p + " " +procc[0]
    if "bkg_qq" in procc[0] :
        
        line_indx = line_indx +" "+str(ibkg+1)
        lineQCDsyst = lineQCDsyst + " 1.1"
        ibkg += 1
    else :
        line_indx = line_indx +" -"+ str(i+1)
        lineQCDsyst = lineQCDsyst + " -"
    #if ("0PM" in procc[0] ) :
    #print chanell,procc[0]  , procc[1] 
    #if ("bkg" in procc[0] ) :
    #  print chanell,procc[0]  , procc[1] 
    
    line_rate = line_rate+ " "+str(procc[1])
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
f.write(lineQCDsyst)

f.close()

#print "written datacard"
'''
        #'''
        #tflatintt = 0
        #if ("2e2mu" in nm ) :
        #    r_ate = yields2e2mu[1]
        #    tn.Scale(yields2e2mu[1]/intt)
        #    tflatintt = yields2e2mu[2]
	#if ("4mu" in nm ) :
        #    r_ate = yields4mu[1]
        #    tn.Scale(yields4mu[1]/intt)
        #    tflatintt = yields4mu[2]

        #if ("4e" in nm ) :
        #    r_ate = yields4e[1]
        #    tn.Scale(yields4e[1]/intt)
        #    tflatintt = yields4e[2]
        #'''

