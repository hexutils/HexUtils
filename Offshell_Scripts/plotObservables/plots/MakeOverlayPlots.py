import os
import sys
import ROOT
import copy

from ROOT import kRed,kBlue,kBlack
ROOT.gROOT.SetBatch(True)

import tdrstyle

nm = sys.argv[1]


fUn  = ROOT.TFile.Open("../Untagged."+nm+".root")
fVBF = ROOT.TFile.Open("../VBFtagged."+nm+".root")
fVH  = ROOT.TFile.Open("../VHtagged."+nm+".root")








def plotStack(filein): 
    
    hists = []
    if "Untagged" in filein.GetName(): 
        cat = "Untagged"
    if "VBFtagged" in filein.GetName(): 
        cat = "VBFtagged"
    if "VHtagged" in filein.GetName(): 
        cat = "VHtagged"

    for key in filein.GetListOfKeys(): 
        
        if "Up" in key.GetName() or "Down" in key.GetName():  
            continue
        hist = filein.Get(key.GetName())
        hname = key.GetName()

        if "back_qqZZ" == hname : 
            hist.SetLineColor(ROOT.kBlack)
            hist.SetFillColor(ROOT.kAzure + 6)
            hists.append(hist)

        if "offggH_0PM"  ==  hname : 
            hist.SetLineColor(ROOT.kRed)
            hist.SetFillColor(ROOT.kRed)
            hist.SetFillStyle(3335)
            hists.append(hist)

        if "offqqH_0PM"  ==  hname :             
            hist.SetLineColor(ROOT.kBlue)
            hist.SetFillStyle(3144)
            hist.SetFillColor(ROOT.kBlue)
            hists.append(hist)

        if "qqH_0PM"  ==  hname :             
            hist.SetLineColor(ROOT.kGreen +3)
            hist.SetFillColor(ROOT.kGreen -1)
            hists.append(hist)
            

    
    
    for hist in hists : 
        if "back" not in hist.GetName() and not "qqH_0PM" == hist.GetName(): 
            hist.Reset()
        for key in filein.GetListOfKeys(): 
            if "Up" in key.GetName() or "Down" in key.GetName():  
                continue
            htemp = filein.Get(key.GetName())
            hname = key.GetName()    
            if hist.GetName() == "offggH_0PM" and "offggH" in hname: 
                hist.Add(htemp)
            if hist.GetName() == "offggH_0PM" and "back_ggZZ" in hname: 
                hist.Add(htemp)
            if hist.GetName() == "offqqH_0PM" and "offqqH" in hname: 
                hist.Add(htemp)
            if hist.GetName() == "offqqH_0PM" and "back_VVZZ" in hname: 
                hist.Add(htemp)

                
    hstack = ROOT.THStack("hstack","")
    leg = ROOT.TLegend(.65,.5,.85,.88)
    leg.SetBorderSize(0)
    leg.SetHeader(cat)


    hdata = ROOT.TH1F("hdata","",800,0,100)
    hdata.SetMarkerColor(ROOT.kBlack)
    hdata.SetMarkerStyle(20)
    hdata.SetLineColor(ROOT.kBlack)
    leg.AddEntry(hdata,"Observed","pl")

    leg.SetBorderSize(0)
    leg.SetFillColor(0)
    leg.SetFillStyle(0)
    leg.SetTextFont(42)
    leg.SetTextSize(0.035)




    for hist in hists : 
        if "offgg" in hist.GetName(): 
            hhname = "gg #rightarrow 4l s+b+i"
        if "offqq" in hist.GetName(): 
            hhname = "EW s+b+i"
        if "back" in hist.GetName(): 
            hhname = "q#bar{q}#rightarrow 4l bkg"
        if "qqH_0PM" in hist.GetName(): 
            hhname = "Cross-feed"
        leg.AddEntry(hist,hhname,"f")
        

    #stack order

    for hist in hists :      
       if hist.GetName() == "qqH_0PM": 
           hstack.Add(hist)
           break
    for hist in hists :      
       if hist.GetName() == "back_qqZZ": 
           hstack.Add(hist)
           break
    for hist in hists :      
       if hist.GetName() == "offggH_0PM": 
           hstack.Add(hist)
           break
    for hist in hists :      
       if hist.GetName() == "offqqH_0PM": 
           hstack.Add(hist)
           break



    c1 = ROOT.TCanvas("c1","",800,800)
    
    if "projx" == nm: 
        c1.cd().SetLogx()
    else: 
        c1.cd()
    
    c1.SetBottomMargin(0.15)
    c1.SetLeftMargin(0.15)
    #c1.SetRightMargin(0.1)
    #c1.SetTopMargin(0.1)

    hstack.Draw("hist")
    
    if "projx" == nm: 
        hstack.GetXaxis().SetTitle("m_{4l} (GeV)")

    if "projy" == nm: 
        if "Untagged" ==  cat : 
            hstack.GetXaxis().SetTitle("D^{kin}_{bkg}")
        if "VBFtagged" ==  cat : 
            hstack.GetXaxis().SetTitle("D^{VBF+dec}_{bkg}")
        if "VHtagged" ==  cat : 
            hstack.GetXaxis().SetTitle("D^{VBF+dec}_{bkg}")

    if "projz" == nm: 
        if "Untagged" ==  cat : 
            hstack.GetXaxis().SetTitle("D^{gg,dec}_{bsi}")
        if "VBFtagged" ==  cat : 
            hstack.GetXaxis().SetTitle("D^{VBF+dec}_{bsi}")
        if "VHtagged" ==  cat : 
            hstack.GetXaxis().SetTitle("D^{VBF+dec}_{bsi}")



    hstack.GetXaxis().SetTitleSize(0.06)
    hstack.GetXaxis().CenterTitle(True)
    hstack.GetYaxis().SetTitle("Events / bin")
    hstack.GetYaxis().SetTitleSize(0.06)
    hstack.GetYaxis().CenterTitle(True)

    
    hstack.SetMinimum(0)

    leg.Draw()
    ROOT.gStyle.SetOptStat(0)
    
    savename = cat
    if "projx" == nm: 
        savename = cat+"M4L"
    if "projy" == nm: 
        savename = cat+"Dbkg"
    if "projz" == nm: 
        savename = cat+"Dbsi"

    tdrstyle.cmsPrel(137100, 13., False)
    
    c1.Update()    
    c1.SaveAs(savename+".png")
    c1.SaveAs(savename+".pdf")
    c1.Close()



plotStack(fUn)
plotStack(fVBF)
plotStack(fVH)

