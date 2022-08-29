import ROOT
import os
import sys
import copy
ROOT.gROOT.SetBatch(True)


procsyst = ""
if len(sys.argv) > 1 : 
    procsyst = sys.argv[1]

treelistpath = "./back_output_temps.txt"

if not  procsyst == "" : 
    os.system('find Output_'+procsyst+' -name "*.root" > syst_temp_'+procsyst+'.txt')
    treelistpath = './syst_temp_'+procsyst+'.txt'


category = ["Untagged","VBFtagged","VHtagged"]
year16 = ["2016","2016","2016"]
year17 = ["2017","2017","2017"]
year18 = ["2018","2018","2018"]

finpaths = list(zip(category,year16)) +list(zip(category,year17)) + list(zip(category,year18))

paths = []
for el in finpaths :
    ell = list(el)
    paths.append(ell)
print paths

#finpaths[0].append("this")




with open(treelistpath) as f:
    llist = [line.rstrip() for line in f]
    for line in llist:
        if os.path.exists(line):
            for el in paths :
                if el[0] in line  and el[1] in line : 
                    el.append(line)
                else:     
                    continue
print (paths)

for el in paths: 
    print "---------------------------------------------"
    print el[0],el[1]
    hnevs = []
    hists = []
    for ifile in range(2,len(el)) : 
        finn = ROOT.TFile(el[ifile])
        finn.cd()
        for ihist,key in enumerate(finn.GetListOfKeys()): 
            if "TH3F" in key.GetClassName(): 
                h_name  = key.GetName()
                h_temp  = finn.Get(h_name)
                h_new = copy.deepcopy(h_temp)
                
                if ifile == 2 : 
                    hnevs.append(h_new.GetEntries())
                    print h_name,h_new.Integral()
                    h_new.Scale(h_new.GetEntries())
                    hists.append(h_new)

                else: 
                    print h_name,h_new.Integral()
                    h_new.Scale(h_new.GetEntries())
                    hists[ihist].Add(h_new)
                    hnevs[ihist] = hnevs[ihist] + h_new.GetEntries()  

    if procsyst == "" : 
        fout = ROOT.TFile("./Templates/background_"+el[0]+"_"+el[1]+".root","recreate")
    else : 
        fout = ROOT.TFile("./Templates_syst/background_"+el[0]+"_"+el[1]+"_"+procsyst+"_temporary.root","recreate")

    fout.cd()
    
    for ihist,hist in enumerate(hists) : 
        count = hnevs[ihist]
        hist.Scale(1./count)
        if not procsyst == "" : 
            hnew = hist.GetName()
            hnew = hnew+"_"+procsyst
            hnew = hnew.replace("U","_up")
            hnew = hnew.replace("D","_dn")
            hist.SetName(hnew)
        print "Writting:",hist.GetName(),hist.Integral()    
        hist.Write()
            
            
    fout.Close()
    print "---------------------------------------------"





if procsyst == "": 
    os.system("hadd -f -k  background_Untagged.root  ./Templates/*Untagged*.root")
    os.system("hadd -f -k background_VHtagged.root  ./Templates/*VHtagged*.root")
    os.system("hadd -f -k background_VBFtagged.root  ./Templates/*VBFtagged*.root")
else : 
    os.system("hadd -f -k background_Untagged_"+procsyst+".root  ./Templates_syst/*Untagged*"+procsyst+"_temporary.root")
    os.system("hadd -f -k background_VHtagged_"+procsyst+".root  ./Templates_syst/*VHtagged*"+procsyst+"_temporary.root")
    os.system("hadd -f -k background_VBFtagged_"+procsyst+".root  ./Templates_syst/*VBFtagged*"+procsyst+"_temporary.root")

 
print ("Checking correcting total yields for jet uncertainty")
#need to make sure the total yield for each sys matches the nominal yield
#jet syst should only affect the percategory yield + shapes



if not procsyst == "" : 
    totyield_nominal =[0,0,0]
    totyield_syst = [0,0,0]
    proc = "ZZTo4l"

    for cat in category: 
        fnom = ROOT.TFile("background_"+cat+".root")
        fsyst = ROOT.TFile("background_"+cat+"_"+procsyst+".root")
    
        for ipros in range(0,2): 
            for key in fnom.GetListOfKeys(): 
                if proc+"_"+str(ipros) == key.GetName():
                    ht = fnom.Get(key.GetName())
                    totyield_nominal[ipros] += ht.Integral()
            for key in fsyst.GetListOfKeys():
                systname = procsyst.replace("U","_up")
                systname = systname.replace("D","_dn")
                if proc+"_"+str(ipros)+"_"+systname == key.GetName():
                    ht = fsyst.Get(key.GetName())
                    totyield_syst[ipros] += ht.Integral()

    print (totyield_syst, totyield_nominal)

for ipros in range(0,2):
    
    if abs (totyield_syst[ipros] - totyield_nominal[ipros] ) > 0.1 : 
        print "WARNING SYST HAS DIF Total YIELD "




   




'''
def plot(year,category) : 

    treelistpath = "./output_temps.txt"

    finpaths = []

    with open(treelistpath) as f:
        llist = [line.rstrip() for line in f]
        
    for line in llist:
        print line
        if os.path.exists(line): 
        
            if category in line and str(year) in line : 
                finpaths.append(line)
            


    h_0 =  ROOT.TH1F("h_0","",100,0,1)

    if category == "VHtagged" : 
        h_0 =  ROOT.TH1F("h_0","",1000,0,1)

    if category == "VBFtagged" : 
        h_0 =  ROOT.TH1F("h_0","",1000,0,1)



    for ifile,f in enumerate(finpaths): 

        finn = ROOT.TFile(f)
        finn.cd(); 
        htemp = finn.Get("VBF_0")
        print ifile,f,htemp.Integral(),htemp.GetEntries()
        h_0.Fill(htemp.Integral())
    
    c1 = ROOT.TCanvas("c1","",800,600)
    c1.cd()


    h_0.Draw()
    c1.SaveAs("hist_VBF_"+str(year)+"_"+str(category)+".png")


'''


#plot(2018,"Untagged")
#plot(2017,"Untagged")
#plot(2016,"Untagged")

#plot(2018,"VHtagged")
#plot(2017,"VHtagged")
#plot(2016,"VHtagged")

#plot(2018,"VBFtagged")
#plot(2017,"VBFtagged")
#plot(2016,"VBFtagged")
