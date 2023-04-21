import os
import sys
import ROOT
from Unroll_gen   import Unroll 
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
        h_temp = fin.Get(h_name)
        #print h_name
        #ideally here we unroll and add index and rate
        
        thist = copy.deepcopy(h_temp)
     
        #calculate interference template
        if "_1" in h_name:
            hpurename = h_name.replace("_1","_0")
            hbackname = h_name.replace("_1","_2")

            hpure = fin.Get(hpurename)
            hback = fin.Get(hbackname)

            #print  - hpure.Integral() - hback.Integral() + thist.Integral()

            thist.Add(hpure,-1)
            thist.Add(hback,-1)
            #print thist.Integral()
            
         
        hns = h_name.replace("gg","offggH")
        hns = hns.replace("VBF","offqqH")
        hns = hns.replace("ZZTo4l_0","back_qqZZ")
        hns = hns.replace("_0","_0PM")
        if "ggH" in hns : hns = hns.replace("_1","_g11g21")
        if "qqH" in hns : hns = hns.replace("_1","_g12g22")
        
        hns = hns.replace("qcd_","qcd")        
        if "offqqH_2" in hns :
            hns = hns.replace("offqqH_2","back_VVZZ")
        if "offggH_2" in hns :
            hns = hns.replace("offggH_2","back_ggZZ")
        
        thist.SetName(hns)    
        r_ate = thist.Integral()
        tp,tn = Unroll(thist)

        if len(hists) > 0:
            if hists[len(hists)-1].GetName() == tp.GetName() or hists[len(hists)-1].GetName() == tn.GetName() : continue
        
        if tp.GetName() == tn.GetName() : 

            
            processes.append((tn.GetName(),r_ate))
            tn.SetName(tn.GetName())
            hists.append(tn)

        else :
            
            tp.SetName(tp.GetName())
            tn.SetName(tn.GetName())
            
            #for ibinn in tp.GetXaxis().GetNbins():
            #    print (tp.GetBinContent(ibinn))
            r_ate = tp.Integral()

            #print tp.GetName(),r_ate
            #processes.append((tp.GetName(),r_ate)) if abs(r_ate) > 0  else 0
            hists.append(tp) if abs(r_ate) > 0  else 0
            r_ate = tn.Integral()
            #print tn.GetName(),r_ate
            processes.append((tn.GetName(),r_ate)) if abs(r_ate) > 0 else 0
            
            hists.append(tn) if abs(r_ate) > 0  else 0
            



            
chanell = nm.replace(".root","")    
n_fout  = chanell+".input.root"
fout =  ROOT.TFile.Open(n_fout,"recreate")
fout.cd()
data_obs = copy.deepcopy(hists[0])
data_obs.SetName("data_obs")
for i,hist in enumerate(hists):
    if i > 1 : 
      data_obs.Add(hist)
for his in hists:
    
    hns = his.GetName()
    hns = hns.replace("_up","Up")    
    hns = hns.replace("_dn","Down")    
    his.SetName(hns)
    print fout.GetName(),"writing ",his.GetName()," ",his.Integral()
    his.Write()
     
data_obs.Write()

fout.Close()
totyield = data_obs.Integral()
            
            
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
