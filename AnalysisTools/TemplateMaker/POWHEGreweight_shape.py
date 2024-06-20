
'''
python3 POWHEGreweight_shape.py <year> <component> <tag> <syst>

<year> = [2016, 2017, 2018]
<component> = [SIG, BSI, BKG]
<tag> = [0, 1, 2]
<syst> = [nom, kfqcd_up, kfqcd_dn, kfpdf_up, kfpdf_dn, kfas_up, kfas_dn, pdfV_up, pdfV_dn, AsMZV_up, AsMZV_dn, QCDmuRV_up, QCDmuRV_dn, QCDmuFV_up, QCDmuFV_dn]
'''


#################### IMPORT STATEMENTS ####################

import re
import time
import glob
import os, sys
import subprocess
from pathlib import Path

import ROOT
import random
import numpy as np
#import uproot as up
#import pandas as pd
#import awkward as ak
#import vector as vec
#from scipy import stats
#from itertools import chain
#import pyarrow.parquet as pq
#from collections import Counter
from tqdm import trange, tqdm

#import mplhep as hep
#import seaborn as sns
#import matplotlib as mpl
#import matplotlib.pyplot as plt
#import plotly.express as px
#import plotly.graph_objs as go
#from plotly.offline import iplot as plot

#################### USER SETTINGS ####################

#pd.set_option('display.min_rows', pd.options.display.max_rows)

#sns.set(rc={"figure.figsize": (24, 15)})
#sns.set_context("poster")
#sns.set_style("whitegrid")
#sns.reset_orig()

#hep.style.use("CMS")
#plt.style.use(hep.style.CMS)
#hep.style.use("CMSTex")
#plt.style.use(hep.style.CMSTex)

ROOT.gInterpreter.Declare('''
ROOT::RDF::RNode AddArray(ROOT::RDF::RNode df, ROOT::RVec<double> &v, const std::string &name) {
    return df.Define(name, [&](ULong64_t e) { return v[e]; }, {"rdfentry_"});
}

template<typename T>
ROOT::RDF::RNode FixRVec(ROOT::RDF::RNode df, const std::string &name) {
    return df.Redefine(name, [](const ROOT::VecOps::RVec<T> &v) { return std::vector<T>(v.begin(), v.end()); }, {name});
}
''')

#################### CHOOSE YEAR AND SYST FOR TREELIST ####################

tagpath = {'0':'untagged', '1':'vbftagged', '2':'vhtagged'}
lumilst = {'MC_2016_CorrectBTag':35.9, 'MC_2017':41.5, 'MC_2018':59.7}
yearpth = {'2016':'MC_2016_CorrectBTag', '2017':'MC_2017', '2018':'MC_2018'}

if sys.argv[1] not in yearpth.keys(): print("ERROR: unsure which year to use")
#lumi = lumilst[yearpth[sys.argv[1]]]
lumi = 1

#treelist = glob.glob('/eos/user/g/gritsan/Write/TaggedTrees/OffshellTemplateTrees20220923/nominal/cjlst/RunIILegacy/200205_CutBased/{}/HighMass/ggH*/ZZ4lAnalysis.root'.format(yearpth[sys.argv[1]])) + glob.glob('/eos/user/g/gritsan/Write/TaggedTrees/OffshellTemplateTrees20220923/nominal/cjlst/RunIILegacy/200205_CutBased/{}/ggH*/ZZ4lAnalysis.root'.format(yearpth[sys.argv[1]]))

treelist = glob.glob('/eos/home-m/msrivast/CMSSW_12_2_0_/src/2023_offshellKappa/input_data/kappa_Q/final_trees_2fac_fixed/{}/HighMass/ggH*/ZZ4lAnalysis.root'.format(yearpth[sys.argv[1]])) + glob.glob('/eos/home-m/msrivast/CMSSW_12_2_0_/src/2023_offshellKappa/input_data/kappa_Q/final_trees_2fac_fixed/{}/ggH*/ZZ4lAnalysis.root'.format(yearpth[sys.argv[1]]))

print(treelist)

#################### CHECK OUTPUT EXISTENCE ####################

if os.path.isfile("/eos/user/l/lkang/www/research/Sandbox/POWHEGtemplates/nominal_w_syst_kappaQ/{}/{}/templateOutput_{}_{}_final.root".format(tagpath[sys.argv[3]], sys.argv[1], sys.argv[2], sys.argv[4])): sys.exit()

#################### DEFINE BINS FOR TEMPLATES ####################

medges = np.array([220, 230, 240, 250, 260, 280, 310, 340, 370, 400, 475, 550, 625, 700, 800, 900, 1000, 1200, 1600, 2000, 3000, 13000], dtype='float64')
d1edges = np.arange(21, dtype='float64') / 20
d2edges = np.arange(21, dtype='float64') / 10 - 1

#################### FILL TEMPLATES FOR ALL POLE MASSES ####################

hreflist = []
hlist = []

for i, fname in enumerate(tqdm(treelist)):

    sname = fname.split('/')[-2]

    if 'tune' in sname: continue
    if 'scale' in sname: continue
    if 'minlo' in sname: continue
    if 'NNLOPS' in sname: continue

    print(sname)
       
    f = ROOT.TFile.Open(fname ,"READ")
    t = f.Get("eventTree")
    n = t.GetEntries()

    hist = ROOT.TH3F("hist_"+sname, sname, len(medges)-1, medges, len(d1edges)-1, d1edges, len(d2edges)-1, d2edges)
    hist.Sumw2()
    hist.SetLineColor(i+1)
    
    histref = ROOT.TH3F("histref_"+sname, sname, len(medges)-1, medges, len(d1edges)-1, d1edges, len(d2edges)-1, d2edges)
    histref.Sumw2()
    histref.SetLineColor(i+1)
   
    for iev,event in tqdm(enumerate(t)):
        if iev==0: weight_nom = lumi * 1000 * event.genxsec * event.genBR / event.Bin40
        if event.EventTag!=int(sys.argv[3]): continue

        #========================================================================================

        syst_nm = sys.argv[4]
        wsystup = 1.0
        wsystdn = 1.0

        if "kf" in syst_nm :
            if"pdf" in syst_nm :
                wsystup = event.KFactor_QCD_ggZZ_PDFScaleUp
                wsystdn = event.KFactor_QCD_ggZZ_PDFScaleDn
            if "as" in syst_nm :
                wsystup = event.KFactor_QCD_ggZZ_AsUp
                wsystdn = event.KFactor_QCD_ggZZ_AsDn
            if "qcd" in syst_nm :
                wsystup = event.KFactor_QCD_ggZZ_QCDScaleUp
                wsystdn = event.KFactor_QCD_ggZZ_QCDScaleDn
            wsystup = wsystup/event.KFactor_QCD_ggZZ_Nominal
            wsystdn = wsystdn/event.KFactor_QCD_ggZZ_Nominal

        elif "pythiascale" in syst_nm :
            wpfu = event.PythiaWeight_fsr_muR4/event.PythiaWeight_isr_muRoneoversqrt2
            wpiu = event.PythiaWeight_isr_muR4/event.PythiaWeight_isr_muRoneoversqrt2
            wpfd = event.PythiaWeight_fsr_muR0p25/event.PythiaWeight_isr_muRoneoversqrt2
            wpid = event.PythiaWeight_isr_muR0p25/event.PythiaWeight_isr_muRoneoversqrt2
            wsystup  =wpfu*wpiu # + wpiu*wpiu )
            wsystdn  =wpfd*wpid #  + wpid*wpid )
            #print (wsystup,wsystdn)

        elif "pdfV" in syst_nm:
            wsystup = event.LHEweight_PDFVariation_Up
            wsystdn = event.LHEweight_PDFVariation_Dn

        elif "AsMZV" in syst_nm:
            wsystup = event.LHEweight_AsMZ_Up
            wsystdn = event.LHEweight_AsMZ_Dn
        elif "QCDmuRV" in syst_nm:
            # wsystup = event.LHEweight_QCDscale_muR2_muF1
            # wsystdn = event.LHEweight_QCDscale_muR0p5_muF1
            wsystup = max(event.LHEweight_QCDscale_muR2_muF1,event.LHEweight_QCDscale_muR0p5_muF1,event.LHEweight_QCDscale_muR1_muF2,event.LHEweight_QCDscale_muR1_muF0p5,event.LHEweight_QCDscale_muR0p5_muF0p5,event.LHEweight_QCDscale_muR0p5_muF2,event.LHEweight_QCDscale_muR2_muF0p5,event.LHEweight_QCDscale_muR2_muF2)
            wsystdn = min(event.LHEweight_QCDscale_muR2_muF1,event.LHEweight_QCDscale_muR0p5_muF1,event.LHEweight_QCDscale_muR1_muF2,event.LHEweight_QCDscale_muR1_muF0p5,event.LHEweight_QCDscale_muR0p5_muF0p5,event.LHEweight_QCDscale_muR0p5_muF2,event.LHEweight_QCDscale_muR2_muF0p5,event.LHEweight_QCDscale_muR2_muF2)
        elif "QCDmuFV" in syst_nm:
            wsystup = event.LHEweight_QCDscale_muR1_muF2
            wsystdn = event.LHEweight_QCDscale_muR1_muF0p5

        else :
            if "EWqqZZ" in syst_nm:
                wsystup   = 1.0 + event.KFactor_EW_qqZZ_unc
                wsystdn  = 1.0 - event.KFactor_EW_qqZZ_unc

        #check direction of uncertainties
        if not (1 - wsystdn)*(1 - wsystup) < 0 :
           wmax =  max( abs(1- wsystdn),abs(1 - wsystup))
           wsystdn = 1 - wmax
           wsystup = 1 + wmax

        if "_up" in syst_nm: wsyst = wsystup
        elif "_dn" in syst_nm: wsyst = wsystdn
        else: wsyst = 1.0

        #========================================================================================

        if sys.argv[2] == 'SIG':
            if event.Native==0: continue
            hist.Fill(event.ZZMass, event.Dbkg, event.Dbsi, wsyst * (event.p_Gen_GG_SIG_kappa4genTop_1_ghz1_1_MCFM/event.Native) * event.p_Gen_GG_SIG_kappaTopBot_1_ghz1_1_MCFM * event.KFactor_QCD_ggZZ_Nominal * event.p_Gen_CPStoBWPropRewgt * event.overallEventWeight * event.L1prefiringWeight * weight_nom)
            histref.Fill(event.ZZMass, event.Dbkg, event.Dbsi, 1)
        elif sys.argv[2] == 'BSI':
            if event.Native==0: continue
            hist.Fill(event.ZZMass, event.Dbkg, event.Dbsi, wsyst * (event.p_Gen_GG_BSI_kappa4genTop_1_ghz1_1_MCFM/event.Native) * event.p_Gen_GG_BSI_kappaTopBot_1_ghz1_1_MCFM * event.KFactor_QCD_ggZZ_Nominal * event.p_Gen_CPStoBWPropRewgt * event.overallEventWeight * event.L1prefiringWeight * weight_nom)
            histref.Fill(event.ZZMass, event.Dbkg, event.Dbsi, 1)
        elif sys.argv[2] == 'BKG':
            hist.Fill(event.ZZMass, event.Dbkg, event.Dbsi, wsyst * event.p_Gen_GG_BKG_MCFM * event.KFactor_QCD_ggZZ_Nominal * event.p_Gen_CPStoBWPropRewgt * event.overallEventWeight * event.L1prefiringWeight * weight_nom)
            histref.Fill(event.ZZMass, event.Dbkg, event.Dbsi, 1)
        else:
            print('ERROR: unsure which target to reweight to')

    """
    if sys.argv[2] == 'SIG':
        print('Reweighting to SIG as target hypothesis')
        for iev,event in tqdm(enumerate(t)):
            if iev==0: weight_nom = lumi * 1000 * event.genxsec * event.genBR / event.Bin40
            if event.EventTag!=int(sys.argv[4]): continue
            hist.Fill(event.ZZMass, event.Dbkg, event.Dbsi, event.p_Gen_GG_SIG_kappaTopBot_1_ghz1_1_MCFM * event.KFactor_QCD_ggZZ_Nominal * event.p_Gen_CPStoBWPropRewgt * event.overallEventWeight * event.L1prefiringWeight * weight_nom)
            histref.Fill(event.ZZMass, event.Dbkg, event.Dbsi, 1)

    elif sys.argv[2] == 'BSI':
        print('Reweighting to BSI as target hypothesis')
        for iev,event in tqdm(enumerate(t)):
            if iev==0: weight_nom = lumi * 1000 * event.genxsec * event.genBR / event.Bin40
            if event.EventTag!=int(sys.argv[4]): continue
            hist.Fill(event.ZZMass, event.Dbkg, event.Dbsi, event.p_Gen_GG_BSI_kappaTopBot_1_ghz1_1_MCFM * event.KFactor_QCD_ggZZ_Nominal * event.p_Gen_CPStoBWPropRewgt * event.overallEventWeight * event.L1prefiringWeight * weight_nom)
            histref.Fill(event.ZZMass, event.Dbkg, event.Dbsi, 1)

    elif sys.argv[2] == 'BKG':
        print('Reweighting to BKG as target hypothesis')
        for iev,event in tqdm(enumerate(t)):
            if iev==0: weight_nom = lumi * 1000 * event.genxsec * event.genBR / event.Bin40
            if event.EventTag!=int(sys.argv[4]): continue
            hist.Fill(event.ZZMass, event.Dbkg, event.Dbsi, event.p_Gen_GG_BKG_MCFM * event.KFactor_QCD_ggZZ_Nominal * event.p_Gen_CPStoBWPropRewgt * event.overallEventWeight * event.L1prefiringWeight * weight_nom)
            histref.Fill(event.ZZMass, event.Dbkg, event.Dbsi, 1)
    
    else: 
        print('ERROR: unsure which target to reweight to')
    """

    hlist.append(hist)
    hist.SetDirectory(0)
    
    hreflist.append(histref)
    histref.SetDirectory(0)
    
    f.Close()

#################### SAVE TEMPLATES TO FILE ####################

foutname = "/eos/user/l/lkang/www/research/Sandbox/POWHEGtemplates/nominal_w_syst_kappaQ/{}/{}/templateOutput_{}_{}_parts.root".format(tagpath[sys.argv[3]], sys.argv[1], sys.argv[2], sys.argv[4])
fout = ROOT.TFile(foutname,"RECREATE")
fout.cd()

for ihist in hlist: 
    print ("writing :", ihist.GetName(), ihist.Integral())
    ihist.Write()
    
for ihist in hreflist: 
    print ("writing :", ihist.GetName(), ihist.Integral())
    ihist.Write()

fout.Close()
"""
#################### READ STATS AND EVENTS FROM 'parts' FILE ####################

finname = "/eos/user/l/lkang/www/research/Sandbox/POWHEGtemplates/untagged/{}/templateOutput_{}_{}_parts.root".format(sys.argv[1], sys.argv[1], sys.argv[2])
fin = ROOT.TFile(finname,"READ")
hreadlist = [ fin.Get(k.GetName()) for k in fin.GetListOfKeys() if "ggH1500" not in k.GetName() ]
hlist = hreadlist[:len(hreadlist)//2]
hreflist = hreadlist[len(hreadlist)//2:]

for h in hlist:
    h.SetDirectory(0)
    print(h)
    print(h.Integral())
for h in hreflist: 
    h.SetDirectory(0)
    print(h)
    print(h.Integral())

fin.Close()
"""
#################### COMBINE TEMPLATES BY STATS ####################

histout = ROOT.TH3F('hist_{}_{}'.format(sys.argv[2], sys.argv[4]), 'POWHEG reweighted {} {}'.format(sys.argv[1], sys.argv[2]), len(medges)-1, medges, len(d1edges)-1, d1edges, len(d2edges)-1, d2edges)
histout.SetDirectory(0)

for binx in range(histout.GetNbinsX()):
    for biny in range(histout.GetNbinsY()):
        for binz in range(histout.GetNbinsZ()):
            nbin = histout.GetBin(binx+1,biny+1,binz+1)

            totstat = 0
            wgtdavg = 0

            for hnum in range(len(hreflist)):
                totstat += (hreflist[hnum].GetBinContent(nbin))
                wgtdavg += (hlist[hnum].GetBinContent(nbin)) * (hreflist[hnum].GetBinContent(nbin))

            if wgtdavg == 0: histout.SetBinContent(nbin, 0)
            else: histout.SetBinContent(nbin, wgtdavg/totstat)

print(histout.Integral())


#################### SAVE FINAL TEMPLATE TO FILE ####################

foutname = "/eos/user/l/lkang/www/research/Sandbox/POWHEGtemplates/nominal_w_syst_kappaQ/{}/{}/templateOutput_{}_{}_final.root".format(tagpath[sys.argv[3]], sys.argv[1], sys.argv[2], sys.argv[4])
fout = ROOT.TFile(foutname, "UPDATE")
fout.cd()

print ("FINALLY writing :", histout.GetName(), histout.Integral())
histout.Write()

fout.Close()

