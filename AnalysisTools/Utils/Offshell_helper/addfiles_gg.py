import ROOT
import os
import sys
import copy
ROOT.gROOT.SetBatch(True)

flav = sys.argv[1]

print flav

category = ["Untagged","VBFtagged","VHtagged"]
year16 = ["2016","2016","2016"]
year17 = ["2017","2017","2017"]
year18 = ["2018","2018","2018"]


treelistpath = "./output_gg.txt"

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
                if el[0] in line  and el[1] in line  and str(flav) in line: 
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
        print ">>",el[ifile]
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

    fout = ROOT.TFile("./Templates/gg_"+el[0]+"_"+el[1]+"_"+flav+".root","recreate")
    fout.cd()
    
    for ihist,hist in enumerate(hists) : 
        count = hnevs[ihist]
        hist.Scale(1./count)
        print "Writting:",hist.GetName(),hist.Integral()
        hist.Write()
            
            
    fout.Close()
    print "---------------------------------------------"






os.system("hadd gg_Untagged_"+str(flav)+".root  ./Templates/*Untagged*"+str(flav)+".root")
os.system("hadd gg_VHtagged_"+str(flav)+".root  ./Templates/*VHtagged*"+str(flav)+".root")
os.system("hadd gg_VBFtagged_"+str(flav)+".root  ./Templates/*VBFtagged*"+str(flav)+".root")





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
