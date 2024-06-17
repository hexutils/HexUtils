
'''
python3 ScaleTemplates.py <path to .root file with histograms>

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

#################### READ STATS AND EVENTS FROM 'parts' FILE ####################

finname = sys.argv[1]
fin = ROOT.TFile(finname,"READ")
hlist = [ fin.Get(k.GetName()) for k in fin.GetListOfKeys() if "ggH1500" not in k.GetName() ]

for h in hlist:
    h.SetDirectory(0)
    print(h)
    print(h.Integral())

fin.Close()

#################### SCALE HISTOGRAMS ####################

for h in hlist:
    h.Scale(1000)

#################### SAVE FINAL TEMPLATE TO FILE ####################

foutname = sys.argv[1].replace(".root", "_scaled.root")
fout = ROOT.TFile(foutname, "UPDATE")
fout.cd()

for h in hlist:
    print ("FINALLY writing :", h.GetName(), h.Integral())
    h.Write()

fout.Close()

