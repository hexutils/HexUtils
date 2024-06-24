
########## IMPORTS ##########

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

import mplhep as hep
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objs as go
from plotly.offline import iplot as plot

pd.set_option('display.min_rows', pd.options.display.max_rows)

sns.set(rc={"figure.figsize": (24, 15)})
sns.set_context("poster")
sns.set_style("whitegrid")
sns.reset_orig()

hep.style.use("CMS")
plt.style.use(hep.style.CMS)
# hep.style.use("CMSTex")
# plt.style.use(hep.style.CMSTex)

ROOT.gInterpreter.Declare('''
ROOT::RDF::RNode AddArray(ROOT::RDF::RNode df, ROOT::RVec<double> &v, const std::string &name) {
    return df.Define(name, [&](ULong64_t e) { return v[e]; }, {"rdfentry_"});
}

template<typename T>
ROOT::RDF::RNode FixRVec(ROOT::RDF::RNode df, const std::string &name) {
    return df.Redefine(name, [](const ROOT::VecOps::RVec<T> &v) { return std::vector<T>(v.begin(), v.end()); }, {name});
}
''')

"""
%jsroot on

%%capture
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=np.VisibleDeprecationWarning)
np.seterr(invalid='ignore')
np.seterr(divide = 'ignore')
pd.set_option('mode.chained_assignment', None)

from IPython.display import Audio
wave = np.sin(2*np.pi*400*np.arange(10000*2)/10000)
chime = Audio('https://freesound.org/data/previews/335/335908_5865517-lq.mp3', rate=10000, autoplay=True)
"""

########## DEFINITIONS ##########

lumi = {'2016':35.9, '2017':41.5, '2018':59.7}
medges = np.array([220, 230, 240, 250, 260, 280, 310, 340, 370, 400, 475, 550, 625, 700, 800, 900, 1000, 1200, 1600, 2000, 3000, 13000], dtype='float64')
d1edges = np.arange(21, dtype='float64') / 20
d2edges = np.arange(21, dtype='float64') / 10 - 1


