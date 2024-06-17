
'''
python3 RRtemplates_ggH.py <year> <state> <component> <tag>

<year> = [2016, 2017, 2018] 
<state> = [2e2mu, 2e2tau, 2mu2tau, 4e, 4mu, 4tau]
<component> = [SIG, BSI, BKG]
<tag> = [0, 1, 2]
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
import uproot as up
import pandas as pd
import awkward as ak
import vector as vec
from scipy import stats
from itertools import chain
import pyarrow.parquet as pq
from collections import Counter
from tqdm import trange, tqdm

#import mplhep as hep
#import seaborn as sns
#import matplotlib as mpl
#import matplotlib.pyplot as plt
#import plotly.express as px
#import plotly.graph_objs as go
#from plotly.offline import iplot as plot

#################### USER SETTINGS ####################

pd.set_option('display.min_rows', pd.options.display.max_rows)

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

#################### FIND SAMPLES FOR EACH STATE ####################

tagpath = {'0':'untagged', '1':'vbftagged', '2':'vhtagged'}
lumilst = {'MC_2016_CorrectBTag':35.9, 'MC_2017':41.5, 'MC_2018':59.7}
yearpth = {'2016':'MC_2016_CorrectBTag', '2017':'MC_2017', '2018':'MC_2018'}

if sys.argv[1] not in yearpth.keys(): print("ERROR: unsure which year to use")
lumi = lumilst[yearpth[sys.argv[1]]]

treelist4e = glob.glob('/eos/user/g/gritsan/Write/TaggedTrees/OffshellTemplateTrees20220923/nominal/cjlst/RunIILegacy/200205_CutBased/{}/OffshellAC/gg/ggTo4e*/ZZ4lAnalysis.root'.format(yearpth[sys.argv[1]]))
treelist4mu = glob.glob('/eos/user/g/gritsan/Write/TaggedTrees/OffshellTemplateTrees20220923/nominal/cjlst/RunIILegacy/200205_CutBased/{}/OffshellAC/gg/ggTo4mu*/ZZ4lAnalysis.root'.format(yearpth[sys.argv[1]]))
treelist4tau = glob.glob('/eos/user/g/gritsan/Write/TaggedTrees/OffshellTemplateTrees20220923/nominal/cjlst/RunIILegacy/200205_CutBased/{}/OffshellAC/gg/ggTo4tau*/ZZ4lAnalysis.root'.format(yearpth[sys.argv[1]]))
treelist2e2mu = glob.glob('/eos/user/g/gritsan/Write/TaggedTrees/OffshellTemplateTrees20220923/nominal/cjlst/RunIILegacy/200205_CutBased/{}/OffshellAC/gg/ggTo2e2mu*/ZZ4lAnalysis.root'.format(yearpth[sys.argv[1]]))
treelist2e2tau = glob.glob('/eos/user/g/gritsan/Write/TaggedTrees/OffshellTemplateTrees20220923/nominal/cjlst/RunIILegacy/200205_CutBased/{}/OffshellAC/gg/ggTo2e2tau*/ZZ4lAnalysis.root'.format(yearpth[sys.argv[1]]))
treelist2mu2tau = glob.glob('/eos/user/g/gritsan/Write/TaggedTrees/OffshellTemplateTrees20220923/nominal/cjlst/RunIILegacy/200205_CutBased/{}/OffshellAC/gg/ggTo2mu2tau*/ZZ4lAnalysis.root'.format(yearpth[sys.argv[1]]))

#################### CHOOSE YEAR AND TARGET HYPO ####################

if sys.argv[2] == '4e': 
    treelist = treelist4e
elif sys.argv[2] == '4mu': 
    treelist = treelist4mu
elif sys.argv[2] == '4tau': 
    treelist = treelist4tau
elif sys.argv[2] == '2e2mu':
    treelist = treelist2e2mu
elif sys.argv[2] == '2e2tau':
    treelist = treelist2e2tau
elif sys.argv[2] == '2mu2tau':
    treelist = treelist2mu2tau
else: print("ERROR: unsure which state to use")

print(treelist)

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
   
    if sys.argv[3] == 'SIG':
        print('Reweighting to SIG as target hypothesis')
        for iev,event in tqdm(enumerate(t)):
            if iev==0: weight_nom = lumi * 1000 * event.xsec / event.Bin40
            if not (event.ZZMass >= 220): continue
            if event.EventTag!=int(sys.argv[4]): continue
            ZZFlav = event.Z1Flav*event.Z2Flav
            if not ( (ZZFlav)==(121*121) or (ZZFlav)==(169*169) or (ZZFlav)==(121*169) ): continue
            hist.Fill(event.ZZMass, event.Dbkg, event.Dbsi, event.p_Gen_GG_SIG_kappaTopBot_1_ghz1_1_MCFM * event.KFactor_QCD_ggZZ_Nominal * event.overallEventWeight * event.L1prefiringWeight * weight_nom)
            histref.Fill(event.ZZMass, event.Dbkg, event.Dbsi, 1)

    elif sys.argv[3] == 'BSI':
        print('Reweighting to BSI as target hypothesis')
        for iev,event in tqdm(enumerate(t)):
            if iev==0: weight_nom = lumi * 1000 * event.xsec / event.Bin40
            if not (event.ZZMass >= 220): continue
            if event.EventTag!=int(sys.argv[4]): continue
            ZZFlav = event.Z1Flav*event.Z2Flav
            if not ( (ZZFlav)==(121*121) or (ZZFlav)==(169*169) or (ZZFlav)==(121*169) ): continue
            hist.Fill(event.ZZMass, event.Dbkg, event.Dbsi, event.p_Gen_GG_BSI_kappaTopBot_1_ghz1_1_MCFM * event.KFactor_QCD_ggZZ_Nominal * event.overallEventWeight * event.L1prefiringWeight * weight_nom)
            histref.Fill(event.ZZMass, event.Dbkg, event.Dbsi, 1)

    elif sys.argv[3] == 'BKG':
        print('Reweighting to BKG as target hypothesis')
        for iev,event in tqdm(enumerate(t)):
            if iev==0: weight_nom = lumi * 1000 * event.xsec / event.Bin40
            if not (event.ZZMass >= 220): continue
            if event.EventTag!=int(sys.argv[4]): continue
            ZZFlav = event.Z1Flav*event.Z2Flav
            if not ( (ZZFlav)==(121*121) or (ZZFlav)==(169*169) or (ZZFlav)==(121*169) ): continue
            hist.Fill(event.ZZMass, event.Dbkg, event.Dbsi, event.p_Gen_GG_BKG_MCFM * event.KFactor_QCD_ggZZ_Nominal *  event.overallEventWeight * event.L1prefiringWeight * weight_nom)
            histref.Fill(event.ZZMass, event.Dbkg, event.Dbsi, 1)

    else: 
        print('ERROR: unsure which target to reweight to')
    
    hlist.append(hist)
    hist.SetDirectory(0)
    
    hreflist.append(histref)
    histref.SetDirectory(0)
    
    f.Close()

#################### SAVE TEMPLATES TO FILE ####################

foutname = "/eos/user/l/lkang/www/research/Sandbox/RRtemplates/ggH/{}/{}/templateOutput_{}_{}_parts.root".format(tagpath[sys.argv[4]], sys.argv[1], sys.argv[2], sys.argv[3])
fout = ROOT.TFile(foutname,"RECREATE")
fout.cd()

for ihist in hlist: 
    print ("writing :", ihist.GetName(), ihist.Integral())
    ihist.Write()
    
for ihist in hreflist: 
    print ("writing :", ihist.GetName(), ihist.Integral())
    ihist.Write()

fout.Close()

#################### COMBINE TEMPLATES BY STATS ####################

histout = ROOT.TH3F('hist_{}'.format(sys.argv[3]), 'ReRECO ggH {} {} {}'.format(sys.argv[1], sys.argv[2], sys.argv[3]), len(medges)-1, medges, len(d1edges)-1, d1edges, len(d2edges)-1, d2edges)
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

foutname = "/eos/user/l/lkang/www/research/Sandbox/RRtemplates/ggH/{}/{}/templateOutput_{}_{}_final.root".format(tagpath[sys.argv[4]], sys.argv[1], sys.argv[2], sys.argv[3])
fout = ROOT.TFile(foutname, "UPDATE")
fout.cd()

print ("FINALLY writing :", histout.GetName(), histout.Integral())
histout.Write()

fout.Close()

