
import time
import glob
import os, sys
from pathlib import Path
from datetime import timedelta
import numpy as np
import uproot as up
import pandas as pd
import awkward as ak
import vector as vec
from scipy import stats
from itertools import chain
from collections import Counter
from tqdm import trange, tqdm



"""
treelist16 = [
    '/eos/user/l/lkang/Active_Research/TaggedTrees/MC_validation_WPsel_non2junderflow_fix/cjlst/RunIILegacy/200205_CutBased/MC_2016_CorrectBTag/OffshellAC/VBF/VBFToHiggs0MToZZTo4l_M125_GaSM/ZZ4lAnalysis.root',
    '/eos/user/l/lkang/Active_Research/TaggedTrees/MC_validation_WPsel_non2junderflow_fix/cjlst/RunIILegacy/200205_CutBased/MC_2016_CorrectBTag/OffshellAC/VBF/VBFToContinToZZTo4l/ZZ4lAnalysis.root',
    '/eos/user/l/lkang/Active_Research/TaggedTrees/MC_validation_WPsel_non2junderflow_fix/cjlst/RunIILegacy/200205_CutBased/MC_2016_CorrectBTag/OffshellAC/VBF/VBFToHiggs0L1ContinToZZTo4l_M125_GaSM/ZZ4lAnalysis.root',
    '/eos/user/l/lkang/Active_Research/TaggedTrees/MC_validation_WPsel_non2junderflow_fix/cjlst/RunIILegacy/200205_CutBased/MC_2016_CorrectBTag/OffshellAC/VBF/VBFToHiggs0L1f05ph0ContinToZZTo4l_M125_GaSM/ZZ4lAnalysis.root',
    '/eos/user/l/lkang/Active_Research/TaggedTrees/MC_validation_WPsel_non2junderflow_fix/cjlst/RunIILegacy/200205_CutBased/MC_2016_CorrectBTag/OffshellAC/VBF/VBFToHiggs0MContinToZZTo4l_M125_GaSM/ZZ4lAnalysis.root',
    '/eos/user/l/lkang/Active_Research/TaggedTrees/MC_validation_WPsel_non2junderflow_fix/cjlst/RunIILegacy/200205_CutBased/MC_2016_CorrectBTag/OffshellAC/VBF/VBFToHiggs0Mf025ph0ToZZTo4l_M125_GaSM/ZZ4lAnalysis.root',
    '/eos/user/l/lkang/Active_Research/TaggedTrees/MC_validation_WPsel_non2junderflow_fix/cjlst/RunIILegacy/200205_CutBased/MC_2016_CorrectBTag/OffshellAC/VBF/VBFToHiggs0Mf05ph0ToZZTo4l_M125_GaSM/ZZ4lAnalysis.root',
    '/eos/user/l/lkang/Active_Research/TaggedTrees/MC_validation_WPsel_non2junderflow_fix/cjlst/RunIILegacy/200205_CutBased/MC_2016_CorrectBTag/OffshellAC/VBF/VBFToHiggs0Mf075ph0ToZZTo4l_M125_GaSM/ZZ4lAnalysis.root',
    '/eos/user/l/lkang/Active_Research/TaggedTrees/MC_validation_WPsel_non2junderflow_fix/cjlst/RunIILegacy/200205_CutBased/MC_2016_CorrectBTag/OffshellAC/VBF/VBFToHiggs0MToZZTo4l_M125_GaSM/ZZ4lAnalysis.root',
    '/eos/user/l/lkang/Active_Research/TaggedTrees/MC_validation_WPsel_non2junderflow_fix/cjlst/RunIILegacy/200205_CutBased/MC_2016_CorrectBTag/OffshellAC/VBF/VBFToHiggs0PHContinToZZTo4l_M125_GaSM/ZZ4lAnalysis.root',
    '/eos/user/l/lkang/Active_Research/TaggedTrees/MC_validation_WPsel_non2junderflow_fix/cjlst/RunIILegacy/200205_CutBased/MC_2016_CorrectBTag/OffshellAC/VBF/VBFToHiggs0PHf025ph0ToZZTo4l_M125_GaSM/ZZ4lAnalysis.root',
    '/eos/user/l/lkang/Active_Research/TaggedTrees/MC_validation_WPsel_non2junderflow_fix/cjlst/RunIILegacy/200205_CutBased/MC_2016_CorrectBTag/OffshellAC/VBF/VBFToHiggs0PHToZZTo4l_M125_GaSM/ZZ4lAnalysis.root'
]

treelist17 = [
    '/eos/user/l/lkang/Active_Research/TaggedTrees/MC_validation_WPsel_non2junderflow_fix/cjlst/RunIILegacy/200205_CutBased/MC_2017/OffshellAC/VBF/VBFToHiggs0PMToZZTo4l_M125_GaSM/ZZ4lAnalysis.root',
    '/eos/user/l/lkang/Active_Research/TaggedTrees/MC_validation_WPsel_non2junderflow_fix/cjlst/RunIILegacy/200205_CutBased/MC_2017/OffshellAC/VBF/VBFToContinToZZTo4l/ZZ4lAnalysis.root',
    '/eos/user/l/lkang/Active_Research/TaggedTrees/MC_validation_WPsel_non2junderflow_fix/cjlst/RunIILegacy/200205_CutBased/MC_2017/OffshellAC/VBF/VBFToHiggs0L1ContinToZZTo4l_M125_GaSM/ZZ4lAnalysis.root',
    '/eos/user/l/lkang/Active_Research/TaggedTrees/MC_validation_WPsel_non2junderflow_fix/cjlst/RunIILegacy/200205_CutBased/MC_2017/OffshellAC/VBF/VBFToHiggs0MContinToZZTo4l_M125_GaSM/ZZ4lAnalysis.root',
    '/eos/user/l/lkang/Active_Research/TaggedTrees/MC_validation_WPsel_non2junderflow_fix/cjlst/RunIILegacy/200205_CutBased/MC_2017/OffshellAC/VBF/VBFToHiggs0Mf025ph0ToZZTo4l_M125_GaSM/ZZ4lAnalysis.root',
    '/eos/user/l/lkang/Active_Research/TaggedTrees/MC_validation_WPsel_non2junderflow_fix/cjlst/RunIILegacy/200205_CutBased/MC_2017/OffshellAC/VBF/VBFToHiggs0Mf05ph0ToZZTo4l_M125_GaSM/ZZ4lAnalysis.root',
    '/eos/user/l/lkang/Active_Research/TaggedTrees/MC_validation_WPsel_non2junderflow_fix/cjlst/RunIILegacy/200205_CutBased/MC_2017/OffshellAC/VBF/VBFToHiggs0Mf075ph0ToZZTo4l_M125_GaSM/ZZ4lAnalysis.root',
    '/eos/user/l/lkang/Active_Research/TaggedTrees/MC_validation_WPsel_non2junderflow_fix/cjlst/RunIILegacy/200205_CutBased/MC_2017/OffshellAC/VBF/VBFToHiggs0MToZZTo4l_M125_GaSM/ZZ4lAnalysis.root',
    '/eos/user/l/lkang/Active_Research/TaggedTrees/MC_validation_WPsel_non2junderflow_fix/cjlst/RunIILegacy/200205_CutBased/MC_2017/OffshellAC/VBF/VBFToHiggs0PHContinToZZTo4l_M125_GaSM/ZZ4lAnalysis.root',
    '/eos/user/l/lkang/Active_Research/TaggedTrees/MC_validation_WPsel_non2junderflow_fix/cjlst/RunIILegacy/200205_CutBased/MC_2017/OffshellAC/VBF/VBFToHiggs0PHf025ph0ToZZTo4l_M125_GaSM/ZZ4lAnalysis.root',
    '/eos/user/l/lkang/Active_Research/TaggedTrees/MC_validation_WPsel_non2junderflow_fix/cjlst/RunIILegacy/200205_CutBased/MC_2017/OffshellAC/VBF/VBFToHiggs0PHf075ph0ToZZTo4l_M125_GaSM/ZZ4lAnalysis.root',
    '/eos/user/l/lkang/Active_Research/TaggedTrees/MC_validation_WPsel_non2junderflow_fix/cjlst/RunIILegacy/200205_CutBased/MC_2017/OffshellAC/VBF/VBFToHiggs0PHToZZTo4l_M125_GaSM/ZZ4lAnalysis.root',
    '/eos/user/l/lkang/Active_Research/TaggedTrees/MC_validation_WPsel_non2junderflow_fix/cjlst/RunIILegacy/200205_CutBased/MC_2017/OffshellAC/VBF/VBFToHiggs0PMToZZTo4l_M125_GaSM/ZZ4lAnalysis.root'
]

treelist18 = [
    '/eos/user/l/lkang/Active_Research/TaggedTrees/MC_validation_WPsel_non2junderflow_fix/cjlst/RunIILegacy/200205_CutBased/MC_2018/OffshellAC/VBF/VBFToHiggs0MToZZTo4l_M125_GaSM/ZZ4lAnalysis.root',
    '/eos/user/l/lkang/Active_Research/TaggedTrees/MC_validation_WPsel_non2junderflow_fix/cjlst/RunIILegacy/200205_CutBased/MC_2018/OffshellAC/VBF/VBFToHiggs0L1ContinToZZTo4l_M125_GaSM/ZZ4lAnalysis.root',
    '/eos/user/l/lkang/Active_Research/TaggedTrees/MC_validation_WPsel_non2junderflow_fix/cjlst/RunIILegacy/200205_CutBased/MC_2018/OffshellAC/VBF/VBFToHiggs0L1f025ph0ToZZTo4l_M125_GaSM/ZZ4lAnalysis.root',
    '/eos/user/l/lkang/Active_Research/TaggedTrees/MC_validation_WPsel_non2junderflow_fix/cjlst/RunIILegacy/200205_CutBased/MC_2018/OffshellAC/VBF/VBFToHiggs0L1f05ph0ToZZTo4l_M125_GaSM/ZZ4lAnalysis.root',
    '/eos/user/l/lkang/Active_Research/TaggedTrees/MC_validation_WPsel_non2junderflow_fix/cjlst/RunIILegacy/200205_CutBased/MC_2018/OffshellAC/VBF/VBFToHiggs0Mf025ph0ToZZTo4l_M125_GaSM/ZZ4lAnalysis.root',
    '/eos/user/l/lkang/Active_Research/TaggedTrees/MC_validation_WPsel_non2junderflow_fix/cjlst/RunIILegacy/200205_CutBased/MC_2018/OffshellAC/VBF/VBFToHiggs0Mf075ph0ToZZTo4l_M125_GaSM/ZZ4lAnalysis.root',
    '/eos/user/l/lkang/Active_Research/TaggedTrees/MC_validation_WPsel_non2junderflow_fix/cjlst/RunIILegacy/200205_CutBased/MC_2018/OffshellAC/VBF/VBFToHiggs0MToZZTo4l_M125_GaSM/ZZ4lAnalysis.root',
    '/eos/user/l/lkang/Active_Research/TaggedTrees/MC_validation_WPsel_non2junderflow_fix/cjlst/RunIILegacy/200205_CutBased/MC_2018/OffshellAC/VBF/VBFToHiggs0PHContinToZZTo4l_M125_GaSM/ZZ4lAnalysis.root',
    '/eos/user/l/lkang/Active_Research/TaggedTrees/MC_validation_WPsel_non2junderflow_fix/cjlst/RunIILegacy/200205_CutBased/MC_2018/OffshellAC/VBF/VBFToHiggs0PHf025ph0ToZZTo4l_M125_GaSM/ZZ4lAnalysis.root'
]

year = '2018'
treelist = treelist18
"""





xsecdict = {
    'ggH115': 0.005194548,
    'ggH120': 0.008663298,
    'ggH124': 0.012327354,
    'ggH125': 0.01333521,
    'ggH126': 0.014371789,
    'ggH130': 0.018685844,
    'ggH135': 0.0236439,
    'ggH140': 0.02750859,
    'ggH145': 0.02942017,
    'ggH150': 0.0285855,
    'ggH155': 0.02386296,
    'ggH160': 0.0125035,
    'ggH165': 0.00626066,
    'ggH170': 0.00623949,
    'ggH175': 0.0080322,
    'ggH180': 0.01402092,
    'ggH190': 0.0432056,
    'ggH200': 0.0471639,
    'ggH210': 0.0454252,
    'ggH230': 0.038969,
    'ggH250': 0.0329896,
    'ggH270': 0.0278953,
    'ggH300': 0.02202813,
    'ggH350': 0.01497465,
    'ggH400': 0.00927108,
    'ggH450': 0.00650136,
    'ggH500': 0.00486805,
    'ggH550': 0.0037638,
    'ggH600': 0.00298052,
    'ggH700': 0.0019343,
    'ggH750': 0.001575595,
    'ggH800': 0.001298815,
    'ggH900': 0.00089466,
    'ggH1000': 0.000630594,
    'ggH1500': 0.0001304814,
    'ggH2000': 3.43E-05,
    'ggH2500': 1.03E-05,
    'ggH3000': 3.36E-06,

    'VBFH115': 0.000392311,
    'VBFH120': 0.0006528165,
    'VBFH124': 0.0009537624,
    'VBFH125': 0.001038159,
    'VBFH126': 0.0011259752,
    'VBFH130': 0.0014998988,
    'VBFH135': 0.002057643,
    'VBFH140': 0.002482812,
    'VBFH145': 0.002746754,
    'VBFH150': 0.00275315,
    'VBFH155': 0.002349105,
    'VBFH160': 0.00127925,
    'VBFH165': 0.0006583,
    'VBFH170': 0.000675282,
    'VBFH175': 0.000891,
    'VBFH180': 0.001598544,
    'VBFH190': 0.0051728,
    'VBFH200': 0.00591038,
    'VBFH210': 0.00594364,
    'VBFH230': 0.00552012,
    'VBFH250': 0.00502369,
    'VBFH270': 0.00452925,
    'VBFH300': 0.00390616,
    'VBFH350': 0.003006126,
    'VBFH400': 0.00206934,
    'VBFH450': 0.001587994,
    'VBFH500': 0.00129108,
    'VBFH550': 0.00107325,
    'VBFH600': 0.000906898,
    'VBFH700': 0.00065975,
    'VBFH750': 0.000564925,
    'VBFH800': 0.000488222,
    'VBFH900': 0.0003658,
    'VBFH1000': 0.0002776776,
    'VBFH1500': 7.53E-05,
    'VBFH2000': 2.34E-05,
    'VBFH2500': 7.86E-06,
    'VBFH3000': 2.75E-06,

    'WplusH115': 0.0001077818,
    'WplusH120': 0.000158601225411,
    'WplusH124': 0.000215471451605,
    'WplusH125': 0.000230556226102,
    'WplusH126': 0.000245615543373,
    'WplusH130': 0.000305723536186,
    'WplusH135': 0.0004018329,
    'WplusH140': 0.0004484988,
    'WplusH145': 0.000459971,
    'WplusH150': 0.000428145,
    'WplusH155': 0.00034155,
    'WplusH160': 0.00017289,
    'WplusH165': 8.29E-05,
    'WplusH170': 8.00E-05,
    'WplusH175': 9.90E-05,
    'WplusH180': 0.0001673208,
    'WplusH190': 0.00048124,
    'WplusH200': 0.000491841,
    'WplusH210': 0.0004448,
    'WplusH230': 0.000338708,
    'WplusH250': 0.0002572647,
    'WplusH270': 0.000196481,
    'WplusH300': 0.0001352228,
    'WplusH350': 7.50E-05,
    'WplusH400': 3.91E-05,
    'WplusH450': 2.35E-05,
    'WplusH500': 1.54E-05,
    'WplusH550': 1.06E-05,
    'WplusH600': 7.50E-06,
    'WplusH700': 4.01E-06,
    'WplusH750': 2.99E-06,
    'WplusH800': 2.27E-06,
    'WplusH900': 1.34E-06,
    'WplusH1000': 8.22E-07,
    'WplusH1500': 9.29E-08,
    'WplusH2000': 1.42E-08,
    'WplusH2500': 0,
    'WplusH3000': 0,

    'WminusH115': 6.89E-05,
    'WminusH120': 0.000101067010642,
    'WminusH124': 0.000136724208781,
    'WminusH125': 0.00014623476298,
    'WminusH126': 0.000155669876077,
    'WminusH130': 0.000192834569494,
    'WminusH135': 0.0002521449,
    'WminusH140': 0.000280134,
    'WminusH145': 0.0002857866,
    'WminusH150': 0.000264945,
    'WminusH155': 0.000207207,
    'WminusH160': 0.000105995,
    'WminusH165': 5.04E-05,
    'WminusH170': 4.86E-05,
    'WminusH175': 6.01E-05,
    'WminusH180': 0.0001007352,
    'WminusH190': 0.00028726,
    'WminusH200': 0.000291116,
    'WminusH210': 0.0002608474,
    'WminusH230': 0.0001956654,
    'WminusH250': 0.0001460753,
    'WminusH270': 0.000109861,
    'WminusH300': 7.39E-05,
    'WminusH350': 3.96E-05,
    'WminusH400': 2.00E-05,
    'WminusH450': 1.16E-05,
    'WminusH500': 7.41E-06,
    'WminusH550': 4.94E-06,
    'WminusH600': 3.41E-06,
    'WminusH700': 1.74E-06,
    'WminusH750': 1.27E-06,
    'WminusH800': 9.43E-07,
    'WminusH900': 5.37E-07,
    'WminusH1000': 3.18E-07,
    'WminusH1500': 3.22E-08,
    'WminusH2000': 4.78E-09,
    'WminusH2500': 0,
    'WminusH3000': 0,

    'ZH115': 0.000252360209622,
    'ZH120': 0.000356286455065,
    'ZH124': 0.000497857666125,
    'ZH125': 0.000536420305232,
    'ZH126': 0.000574393652227,
    'ZH130': 0.000727451403099,
    'ZH135': 0.001095464115337,
    'ZH140': 0.001239610864301,
    'ZH145': 0.001294137598826,
    'ZH150': 0.001227646827457,
    'ZH155': 0.000979838958822,
    'ZH160': 0.000513856945966,
    'ZH165': 0.000274568482557,
    'ZH170': 0.000213632953352,
    'ZH175': 0.000301926401137,
    'ZH180': 0.000495451057082,
    'ZH190': 0.00149070810708,
    'ZH200': 0.001522300155178,
    'ZH210': 0.001367029347461,
    'ZH230': 0.00102592209825,
    'ZH250': 0.000754536802996,
    'ZH270': 0.000558625972363,
    'ZH300': 0.000367211078864,
    'ZH350': 0.000193147556626,
    'ZH400': 9.93E-05,
    'ZH450': 7.50E-05,
    'ZH500': 3.97E-05,
    'ZH550': 2.78E-05,
    'ZH600': 2.01E-05,
    'ZH700': 1.13E-05,
    'ZH750': 8.65E-06,
    'ZH800': 6.73E-06,
    'ZH900': 4.19E-06,
    'ZH1000': 2.69E-06,
    'ZH1500': 3.69E-07,
    'ZH2000': 6.91E-08,
    'ZH2500': 0,
    'ZH3000': 0
}





yeardict = {
    'MC_2016_CorrectBTag':'2016',
    'MC_2017':'2017',
    'MC_2018':'2018'
}


#print( str( sys.argv[1].split('/')[-5] ) )

#print( yeardict[str( sys.argv[1].split('/')[-5] )] )

#print( str( sys.argv[1] ) )

#sys.exit()








#year = yeardict[str( sys.argv[1].split('/')[12] )]

year = ''

for k in yeardict.keys():
    if k in str(sys.argv[1]): 
        year = yeardict[k]
    elif 'AC16' in str(sys.argv[1]): year = '2016'
    elif 'AC17' in str(sys.argv[1]): year = '2017'
    elif 'AC18' in str(sys.argv[1]): year = '2018'



if len(year)==0: 
    print('\nYEAR NOT RECOGNIZED\n')
    sys.exit()

treelist = [str( sys.argv[1] )]


print(year)
print(treelist)


if treelist[0].strip():
    if not os.path.exists(treelist[0]):
        print('sample not FOUND!!!!!!', '\n', treelist[0].strip())
        sys.exit()


#sys.exit()

for ntree, tree in enumerate(tqdm(treelist)):

    #if ntree == 1: break

    print('===== ', tree.split('/')[-2], ' =====\n')

    if os.path.exists('/eos/user/g/gritsan/Write/Corrections/parquet_xsecadded/'+year+'/'+tree.split('/')[-2]+'_lepmc.parquet') and os.path.exists('/eos/user/g/gritsan/Write/Corrections/parquet_xsecadded/'+year+'/'+tree.split('/')[-2]+'_jetmc.parquet') and os.path.exists('/eos/user/g/gritsan/Write/Corrections/parquet_xsecadded/'+year+'/'+tree.split('/')[-2]+'_allmc.parquet'):
        continue

#    if os.path.exists('/eos/user/l/lkang/www/research/OffshellValidation/ReReco/offshell_EW/TemplCorrecEW/parquet/'+year+'/'+tree.split('/')[-2]+'_lepmc.parquet') and os.path.exists('/eos/user/l/lkang/www/research/OffshellValidation/ReReco/offshell_EW/TemplCorrecEW/parquet/'+year+'/'+tree.split('/')[-2]+'_jetmc.parquet') and os.path.exists('/eos/user/l/lkang/www/research/OffshellValidation/ReReco/offshell_EW/TemplCorrecEW/parquet/'+year+'/'+tree.split('/')[-2]+'_allmc.parquet'):
#        continue
    
    if not os.path.exists(tree):
        print("ERROR TREE NOT FOUND\n")
        continue
    
    #===== Load eventTree from file =====#

    f = up.open(tree)
    t = f['eventTree']

    mcweight = '137.4 * 1000 * xsec / {}'.format(t.num_entries)
    evweight = '137.4 * 1000 * xsec * overallEventWeight * L1prefiringWeight / Bin40'

    if 'ToZZTo4l' in tree:
        evweight = '(1.039E+00) * 0.5 * '+evweight
        mcweight = '(1.039E+00) * 0.5 * '+mcweight

#     elif 'VBFTo2e2muJJ_0PMH125_phantom128' in tree:
#         evweight = '(9.806E-01) * '+evweight
#         mcweight = '(9.806E-01) * '+mcweight

#     elif 'VBFTo4eJJ_0PMH125_phantom128' in tree:
#         evweight = '(9.988E-01) * '+evweight
#         mcweight = '(9.988E-01) * '+mcweight

#     elif 'VBFTo4muJJ_0PMH125_phantom128' in tree:
#         evweight = '(9.982E-01) * '+evweight
#         mcweight = '(9.982E-01) * '+mcweight

    wsystup = '(PythiaWeight_fsr_muR4/PythiaWeight_isr_muRoneoversqrt2) * (PythiaWeight_isr_muR4/PythiaWeight_isr_muRoneoversqrt2)'
    wsystdn = '(PythiaWeight_fsr_muR0p25/PythiaWeight_isr_muRoneoversqrt2) * (PythiaWeight_isr_muR0p25/PythiaWeight_isr_muRoneoversqrt2)'

    #===== Saving lepcut dataframe =====#

#    b = t.arrays(t.keys(filter_name='Event*')+t.keys(filter_name='LHEDaughter*')+t.keys(filter_name='LHEMother*')+['EVwgt', 'MCwgt', 'SystUp', 'SystDn']+t.keys(filter_name='p_Gen*'), aliases={'EVwgt': evweight, 'MCwgt': mcweight, 'SystUp': wsystup, 'SystDn': wsystdn})
    b = t.arrays(t.keys(filter_name='Event*')+t.keys(filter_name='LHEDaughter*')+t.keys(filter_name='LHEMother*')+['SystUp', 'SystDn']+t.keys(filter_name='p_Gen*'), aliases={'SystUp': wsystup, 'SystDn': wsystdn})
    lepvec = vec.zip({'EventNumber': b.EventNumber, 'id': b.LHEDaughterId, 'mass': b.LHEDaughterMass, 'pt': b.LHEDaughterPt, 'eta': b.LHEDaughterEta, 'phi': b.LHEDaughterPhi})

    print(lepvec[:,0]['id'])

    print(type(lepvec[:,0]['id']))



    lepmc = ak.to_pandas(b, how='outer').loc[pd.IndexSlice[:, [0,1,2,3]], :]

    print("lepmc saved")

    #===== Saving jetcut dataframe =====#
    
#    b = t.arrays(t.keys(filter_name='Event*')+t.keys(filter_name='LHEAssociated*')+['EVwgt', 'MCwgt', 'SystUp', 'SystDn']+t.keys(filter_name='p_Gen*') + t.keys(filter_name='DiJetMass'), aliases={'EVwgt': evweight, 'MCwgt': mcweight, 'SystUp': wsystup, 'SystDn': wsystdn})
    b = t.arrays(t.keys(filter_name='Event*')+t.keys(filter_name='LHEAssociated*')+['SystUp', 'SystDn']+t.keys(filter_name='p_Gen*') + t.keys(filter_name='DiJetMass'), aliases={'SystUp': wsystup, 'SystDn': wsystdn})
    jetvec = vec.zip({'EventNumber': b.EventNumber, 'id': b.LHEAssociatedParticleId, 'mass': b.LHEAssociatedParticleMass, 'pt': b.LHEAssociatedParticlePt, 'eta': b.LHEAssociatedParticleEta, 'phi': b.LHEAssociatedParticlePhi})

#    LHE2l2Xperm = list(zip(np.array( ((lepvec[:,0]+lepvec[:,1] + jetvec[:,0]+jetvec[:,1]).M) * ((lepvec[:,0]['id']+lepvec[:,1]['id'])==0) * (np.isin(ak.to_numpy(lepvec[:,0]['id']), [-11, 11, -13, 13, -15, 15])) )))

#    LHE2l2Xperm = list(zip(np.array( ((lepvec[:,0]+lepvec[:,1] + jetvec[:,0]+jetvec[:,1]).M) * ((lepvec[:,0]['id']+lepvec[:,1]['id'])==0) * (np.isin(lepvec[:,0]['id'], [-11, 11, -13, 13, -15, 15])) ),\
#            np.array( ((lepvec[:,2]+lepvec[:,3] + jetvec[:,0]+jetvec[:,1]).M) * ((lepvec[:,2]['id']+lepvec[:,3]['id'])==0) * (np.isin(lepvec[:,2]['id'], [-11, 11, -13, 13, -15, 15])) ),\
#            np.array( ((lepvec[:,0]+lepvec[:,3] + jetvec[:,0]+jetvec[:,1]).M) * ((lepvec[:,0]['id']+lepvec[:,3]['id'])==0) * (np.isin(lepvec[:,0]['id'], [-11, 11, -13, 13, -15, 15])) ),\
#            np.array( ((lepvec[:,1]+lepvec[:,2] + jetvec[:,0]+jetvec[:,1]).M) * ((lepvec[:,1]['id']+lepvec[:,2]['id'])==0) * (np.isin(lepvec[:,1]['id'], [-11, 11, -13, 13, -15, 15])) )))
   
    LHE2l2Xperm = np.asarray(list(zip(
        ( np.array( ((lepvec[:,0]+lepvec[:,1] + jetvec[:,0]+jetvec[:,1]).M) * ((lepvec[:,0]['id']+lepvec[:,1]['id'])==0) * ak.from_numpy(np.isin(ak.to_numpy(lepvec[:,0]['id']), np.array([-11, 11, -13, 13, -15, 15]))) ) ), \
        ( np.array( ((lepvec[:,2]+lepvec[:,3] + jetvec[:,0]+jetvec[:,1]).M) * ((lepvec[:,2]['id']+lepvec[:,3]['id'])==0) * ak.from_numpy(np.isin(ak.to_numpy(lepvec[:,2]['id']), np.array([-11, 11, -13, 13, -15, 15]))) ) ), \
        ( np.array( ((lepvec[:,0]+lepvec[:,3] + jetvec[:,0]+jetvec[:,1]).M) * ((lepvec[:,0]['id']+lepvec[:,3]['id'])==0) * ak.from_numpy(np.isin(ak.to_numpy(lepvec[:,0]['id']), np.array([-11, 11, -13, 13, -15, 15]))) ) ), \
        ( np.array( ((lepvec[:,1]+lepvec[:,2] + jetvec[:,0]+jetvec[:,1]).M) * ((lepvec[:,1]['id']+lepvec[:,2]['id'])==0) * ak.from_numpy(np.isin(ak.to_numpy(lepvec[:,1]['id']), np.array([-11, 11, -13, 13, -15, 15]))) ) ), \
        )))
 
    print("permutations checked")
    
    LHEm2l2X = [ min( x[np.nonzero(x)], key=lambda k: abs(k-125) ) for x in map(np.asarray, LHE2l2Xperm) ]

    print("checkpoint reached")

    print(type(LHEm2l2X))

#    print(LHEm2l2X)

    b = ak.with_field(b, LHEm2l2X, where='LHEm2l2X')
    b = ak.with_field(b, ((jetvec[:,0]+jetvec[:,1]).M), where='LHEDiJetMass') #LHEmj1j2
    b = ak.with_field(b, (jetvec[:,0].deltaR(jetvec[:,1])), where='LHEDeltaR')

    Vbosonfile = False
    pm = 0
    
    if any(map(tree.__contains__, ['H0PM', 'H125/', 'H200/', 'H300/', 'H400/', 'H500/', 'H600/', 'H1000/', 'H1500/', 'H2000/', 'H2500/', 'H3000/'])):

        if any(map(tree.__contains__, ['WH', 'WminusH', 'WplusH', 'ZH', 'VBF'])):
            jetvec2 = jetvec[ak.Array(map(len, jetvec)) == 2]
            jetvec3 = jetvec[ak.Array(map(len, jetvec)) == 3]
            jetvec4 = jetvec[ak.Array(map(len, jetvec)) == 4]
            Vbosonfile = True

        if any(map(tree.__contains__, ['WH', 'WminusH', 'WplusH'])):
            pm = 80.379

            jjcombo = np.array(list(( ((jetvec2[:,0]+jetvec2[:,1]).M) * ((jetvec2[:,0]['id']+jetvec2[:,1]['id'])%2==1) * (np.isin(jetvec2[:,0]['id'], [-1, 1, -2, 2, -3, 3, -4, 4, -5, 5])) ))) - pm
            jjtrueV = list(zip( np.array(jetvec2[:,0]["EventNumber"]).astype(int), jjcombo + pm ))
            jjtrueV = [i for i in jjtrueV if i[1]!=0]

            jjjcombo = np.asarray(list(zip(
                ( np.array( ((jetvec3[:,0]+jetvec3[:,1]).M) * ((jetvec3[:,0]['id']+jetvec3[:,1]['id'])%2==1) * (np.isin(jetvec3[:,0]['id'], [-1, 1, -2, 2, -3, 3, -4, 4, -5, 5])) ) - pm ), \
                ( np.array( ((jetvec3[:,0]+jetvec3[:,2]).M) * ((jetvec3[:,0]['id']+jetvec3[:,2]['id'])%2==1) * (np.isin(jetvec3[:,0]['id'], [-1, 1, -2, 2, -3, 3, -4, 4, -5, 5])) ) - pm ), \
                ( np.array( ((jetvec3[:,1]+jetvec3[:,2]).M) * ((jetvec3[:,1]['id']+jetvec3[:,2]['id'])%2==1) * (np.isin(jetvec3[:,1]['id'], [-1, 1, -2, 2, -3, 3, -4, 4, -5, 5])) ) - pm ), \
                )))
            jjjtrueV = list(zip( np.array(jetvec3[:,0]["EventNumber"]).astype(int), np.array(list(map(lambda x,y: x[y], jjjcombo, np.array(list(map(np.argmin, abs(jjjcombo))))))) + pm ))
            jjjtrueV = [i for i in jjjtrueV if i[1]!=0]

            jjjjcombo = np.asarray(list(zip(
                ( np.array( ((jetvec4[:,0]+jetvec4[:,1]).M) * ((jetvec4[:,0]['id']+jetvec4[:,1]['id'])%2==1) * (np.isin(jetvec4[:,0]['id'], [-1, 1, -2, 2, -3, 3, -4, 4, -5, 5])) ) - pm ), \
                ( np.array( ((jetvec4[:,0]+jetvec4[:,2]).M) * ((jetvec4[:,0]['id']+jetvec4[:,2]['id'])%2==1) * (np.isin(jetvec4[:,0]['id'], [-1, 1, -2, 2, -3, 3, -4, 4, -5, 5])) ) - pm ), \
                ( np.array( ((jetvec4[:,1]+jetvec4[:,2]).M) * ((jetvec4[:,1]['id']+jetvec4[:,2]['id'])%2==1) * (np.isin(jetvec4[:,1]['id'], [-1, 1, -2, 2, -3, 3, -4, 4, -5, 5])) ) - pm ), \
                ( np.array( ((jetvec4[:,0]+jetvec4[:,3]).M) * ((jetvec4[:,0]['id']+jetvec4[:,3]['id'])%2==1) * (np.isin(jetvec4[:,0]['id'], [-1, 1, -2, 2, -3, 3, -4, 4, -5, 5])) ) - pm ), \
                ( np.array( ((jetvec4[:,1]+jetvec4[:,3]).M) * ((jetvec4[:,1]['id']+jetvec4[:,3]['id'])%2==1) * (np.isin(jetvec4[:,1]['id'], [-1, 1, -2, 2, -3, 3, -4, 4, -5, 5])) ) - pm ), \
                ( np.array( ((jetvec4[:,2]+jetvec4[:,3]).M) * ((jetvec4[:,2]['id']+jetvec4[:,3]['id'])%2==1) * (np.isin(jetvec4[:,2]['id'], [-1, 1, -2, 2, -3, 3, -4, 4, -5, 5])) ) - pm ), \
                )))
            jjjjtrueV = list(zip( np.array(jetvec4[:,0]["EventNumber"]).astype(int), np.array(list(map(lambda x,y: x[y], jjjjcombo, np.array(list(map(np.argmin, abs(jjjjcombo))))))) + pm ))
            jjjjtrueV = [i for i in jjjjtrueV if i[1]!=0]

            alltrueV = jjtrueV + jjjtrueV + jjjjtrueV

        elif 'ZH' in tree:
            pm = 91.1876

            jjcombo = np.array( ((jetvec2[:,0]+jetvec2[:,1]).M) * ((jetvec2[:,0]['id']+jetvec2[:,1]['id'])==0) * (np.isin(jetvec2[:,0]['id'], [-1, 1, -2, 2, -3, 3, -4, 4, -5, 5])) ) - pm
            jjtrueV = list(zip( np.array(jetvec2[:,0]["EventNumber"]).astype(int), jjcombo + pm ))
            jjtrueV = [i for i in jjtrueV if i[1]!=0]

            jjjcombo = np.asarray(list(zip(
                ( np.array( ((jetvec3[:,0]+jetvec3[:,1]).M) * ((jetvec3[:,0]['id']+jetvec3[:,1]['id'])==0) * (np.isin(jetvec3[:,0]['id'], [-1, 1, -2, 2, -3, 3, -4, 4, -5, 5])) ) - pm ), \
                ( np.array( ((jetvec3[:,0]+jetvec3[:,2]).M) * ((jetvec3[:,0]['id']+jetvec3[:,2]['id'])==0) * (np.isin(jetvec3[:,0]['id'], [-1, 1, -2, 2, -3, 3, -4, 4, -5, 5])) ) - pm ), \
                ( np.array( ((jetvec3[:,1]+jetvec3[:,2]).M) * ((jetvec3[:,1]['id']+jetvec3[:,2]['id'])==0) * (np.isin(jetvec3[:,1]['id'], [-1, 1, -2, 2, -3, 3, -4, 4, -5, 5])) ) - pm ), \
                )))
            jjjtrueV = list(zip( np.array(jetvec3[:,0]["EventNumber"]).astype(int), np.array(list(map(lambda x,y: x[y], jjjcombo, np.array(list(map(np.argmin, abs(jjjcombo))))))) + pm ))
            jjjtrueV = [i for i in jjjtrueV if i[1]!=0]

            jjjjcombo = np.asarray(list(zip(
                ( np.array( ((jetvec4[:,0]+jetvec4[:,1]).M) * ((jetvec4[:,0]['id']+jetvec4[:,1]['id'])==0) * (np.isin(jetvec4[:,0]['id'], [-1, 1, -2, 2, -3, 3, -4, 4, -5, 5])) ) - pm ), \
                ( np.array( ((jetvec4[:,0]+jetvec4[:,2]).M) * ((jetvec4[:,0]['id']+jetvec4[:,2]['id'])==0) * (np.isin(jetvec4[:,0]['id'], [-1, 1, -2, 2, -3, 3, -4, 4, -5, 5])) ) - pm ), \
                ( np.array( ((jetvec4[:,1]+jetvec4[:,2]).M) * ((jetvec4[:,1]['id']+jetvec4[:,2]['id'])==0) * (np.isin(jetvec4[:,1]['id'], [-1, 1, -2, 2, -3, 3, -4, 4, -5, 5])) ) - pm ), \
                ( np.array( ((jetvec4[:,0]+jetvec4[:,3]).M) * ((jetvec4[:,0]['id']+jetvec4[:,3]['id'])==0) * (np.isin(jetvec4[:,0]['id'], [-1, 1, -2, 2, -3, 3, -4, 4, -5, 5])) ) - pm ), \
                ( np.array( ((jetvec4[:,1]+jetvec4[:,3]).M) * ((jetvec4[:,1]['id']+jetvec4[:,3]['id'])==0) * (np.isin(jetvec4[:,1]['id'], [-1, 1, -2, 2, -3, 3, -4, 4, -5, 5])) ) - pm ), \
                ( np.array( ((jetvec4[:,2]+jetvec4[:,3]).M) * ((jetvec4[:,2]['id']+jetvec4[:,3]['id'])==0) * (np.isin(jetvec4[:,2]['id'], [-1, 1, -2, 2, -3, 3, -4, 4, -5, 5])) ) - pm ), \
                )))
            jjjjtrueV = list(zip( np.array(jetvec4[:,0]["EventNumber"]).astype(int), np.array(list(map(lambda x,y: x[y], jjjjcombo, np.array(list(map(np.argmin, abs(jjjjcombo))))))) + pm ))
            jjjjtrueV = [i for i in jjjjtrueV if i[1]!=0]

            alltrueV = jjtrueV + jjjtrueV + jjjjtrueV

        elif 'VBF' in tree:
            jjcombo = np.array( ((jetvec2[:,0]+jetvec2[:,1]).M) * ((jetvec2[:,0]['id']+jetvec2[:,1]['id'])==0) * (np.isin(jetvec2[:,0]['id'], [-1, 1, -2, 2, -3, 3, -4, 4, -5, 5])) )
            jjtrueV = list(zip( np.array(jetvec2[:,0]["EventNumber"]).astype(int), jjcombo ))
            jjtrueV = [i for i in jjtrueV if i[1]!=0]

            jjjcombo = np.asarray(list(zip(
                ( np.array( ((jetvec3[:,0]+jetvec3[:,1]).M) * (np.isin(jetvec3[:,0]['id'], [-1, 1, -2, 2, -3, 3, -4, 4, -5, 5])) * (np.isin(jetvec3[:,1]['id'], [-1, 1, -2, 2, -3, 3, -4, 4, -5, 5])) ) ), \
                ( np.array( ((jetvec3[:,0]+jetvec3[:,2]).M) * (np.isin(jetvec3[:,0]['id'], [-1, 1, -2, 2, -3, 3, -4, 4, -5, 5])) * (np.isin(jetvec3[:,2]['id'], [-1, 1, -2, 2, -3, 3, -4, 4, -5, 5])) ) ), \
                ( np.array( ((jetvec3[:,1]+jetvec3[:,2]).M) * (np.isin(jetvec3[:,1]['id'], [-1, 1, -2, 2, -3, 3, -4, 4, -5, 5])) * (np.isin(jetvec3[:,2]['id'], [-1, 1, -2, 2, -3, 3, -4, 4, -5, 5])) ) ), \
                )))
            jjjtrueV = list(zip( np.array(jetvec3[:,0]["EventNumber"]).astype(int), np.array(list(map(lambda x,y: x[y], jjjcombo, np.array(list(map(np.argmax, abs(jjjcombo))))))) ))
            jjjtrueV = [i for i in jjjtrueV if i[1]!=0]
            
            jjjjcombo = np.asarray(list(zip(
                ( np.array( ((jetvec4[:,0]+jetvec4[:,1]).M) * ((jetvec4[:,0]['id']+jetvec4[:,1]['id'])==0) * (np.isin(jetvec4[:,0]['id'], [-1, 1, -2, 2, -3, 3, -4, 4, -5, 5])) ) - pm ), \
                ( np.array( ((jetvec4[:,0]+jetvec4[:,2]).M) * ((jetvec4[:,0]['id']+jetvec4[:,2]['id'])==0) * (np.isin(jetvec4[:,0]['id'], [-1, 1, -2, 2, -3, 3, -4, 4, -5, 5])) ) - pm ), \
                ( np.array( ((jetvec4[:,1]+jetvec4[:,2]).M) * ((jetvec4[:,1]['id']+jetvec4[:,2]['id'])==0) * (np.isin(jetvec4[:,1]['id'], [-1, 1, -2, 2, -3, 3, -4, 4, -5, 5])) ) - pm ), \
                ( np.array( ((jetvec4[:,0]+jetvec4[:,3]).M) * ((jetvec4[:,0]['id']+jetvec4[:,3]['id'])==0) * (np.isin(jetvec4[:,0]['id'], [-1, 1, -2, 2, -3, 3, -4, 4, -5, 5])) ) - pm ), \
                ( np.array( ((jetvec4[:,1]+jetvec4[:,3]).M) * ((jetvec4[:,1]['id']+jetvec4[:,3]['id'])==0) * (np.isin(jetvec4[:,1]['id'], [-1, 1, -2, 2, -3, 3, -4, 4, -5, 5])) ) - pm ), \
                ( np.array( ((jetvec4[:,2]+jetvec4[:,3]).M) * ((jetvec4[:,2]['id']+jetvec4[:,3]['id'])==0) * (np.isin(jetvec4[:,2]['id'], [-1, 1, -2, 2, -3, 3, -4, 4, -5, 5])) ) - pm ), \
                )))
            jjjjtrueV = list(zip( np.array(jetvec4[:,0]["EventNumber"]).astype(int), np.array(list(map(lambda x,y: x[y], jjjjcombo, np.array(list(map(np.argmax, abs(jjjjcombo))))))) ))
            jjjjtrueV = [i for i in jjjjtrueV if i[1]!=0]
            
            alltrueV = jjtrueV + jjjtrueV + jjjjtrueV
            
    LHEmjj = np.array([0]*len(jetvec))
    if Vbosonfile:
        dictEvLoc = dict(map(lambda sub: (sub[1], sub[0]), list(enumerate(b["EventNumber"]))))
        trueVkey = np.array(alltrueV)[:,0]
        trueVval = np.array(alltrueV)[:,1]
        LHEmjj[[dictEvLoc[i] for i in trueVkey]] = trueVval

    b = ak.with_field(b, LHEmjj, where='LHEmVtoqq')

    jetmc = ak.to_pandas(b, how='outer')
#     jetmc = jetmc.loc[pd.IndexSlice[:, [0,1]], :]

    jetmc['LHETrueDiJetMass'] = jetmc['LHEmVtoqq'][(jetmc['LHEmVtoqq']!=0)].add(jetmc['LHEDiJetMass'][(jetmc['LHEmVtoqq']==0)], fill_value=0)

    print("jetmc saved")

    #===== Saving primary dataframe =====#

#    branch = ['EventNumber', 'EventTag', "xsec", "genxsec", "genBR", 'GenHMass', 'ZZMass', 'Dbsi', 'Dbkg'] + t.keys(filter_name='D2*') + t.keys(filter_name='p_Gen*')
    branch = ['EventNumber', 'EventTag', "xsec", "genxsec", "genBR", 'GenHMass', 'ZZMass', 'Dbsi', 'Dbkg', 'overallEventWeight' , 'L1prefiringWeight' , 'Bin40'] + t.keys(filter_name='D2*') + t.keys(filter_name='p_Gen*')
#    b = t.arrays(branch+['EVwgt', 'MCwgt', 'SystUp', 'SystDn'], aliases={'EVwgt': evweight, 'MCwgt': mcweight, 'SystUp': wsystup, 'SystDn': wsystdn})
    b = t.arrays(branch+['SystUp', 'SystDn'], aliases={'SystUp': wsystup, 'SystDn': wsystdn})

#    YRxsec = [xsecdict[tree.split('/')[-2]]]*t.num_entries
#    b = ak.with_field(b, YRxsec, where='YRxsec')

    allmc = ak.to_pandas(b, how='outer')

    lepcuts = ((lepmc['LHEDaughterPt'].dropna())<3).groupby(lepmc['EventNumber']).sum() \
            + (abs(lepmc['LHEDaughterEta'].dropna())>2.7).groupby(lepmc['EventNumber']).sum()

    jetcuts = ((jetmc.loc[pd.IndexSlice[:,[0,1]],:]['LHEAssociatedParticlePt'].dropna())<15).groupby(jetmc['EventNumber']).sum() \
            + (abs(jetmc.loc[pd.IndexSlice[:,[0,1]],:]['LHEAssociatedParticleEta'].dropna())>6.5).groupby(jetmc['EventNumber']).sum() \
            + ((jetmc.loc[pd.IndexSlice[:,[0,1]],:]['LHEDeltaR'].dropna())<0.3).groupby(jetmc['EventNumber']).sum() \
            + ((jetmc.loc[pd.IndexSlice[:,[0,1]],:]['LHETrueDiJetMass'].dropna())<30).groupby(jetmc['EventNumber']).sum()

    gencuts = lepcuts + jetcuts

    pidcuts = (~(lepmc['LHEDaughterId'].dropna()).isin([-11, 11, -13, 13])).groupby(lepmc['EventNumber']).sum() \
            + (~(lepmc['LHEMotherId'].dropna()).isin([-1, 1, -2, 2, -3, 3, -4, 4, -5, 5, 21])).groupby(lepmc['EventNumber']).sum() \
            + (~(jetmc['LHEAssociatedParticleId'].dropna()).isin([-1, 1, -2, 2, -3, 3, -4, 4, -5, 5, 21])).groupby(jetmc['EventNumber']).sum()

    allmc['lepcuts'] = np.array(lepcuts[allmc['EventNumber']]==0)
    allmc['jetcuts'] = np.array(jetcuts[allmc['EventNumber']]==0)
    allmc['gencuts'] = np.array(gencuts[allmc['EventNumber']]==0)
    allmc['pidcuts'] = np.array(pidcuts[allmc['EventNumber']]==0)

    print("allmc saved")

    lepmc.to_parquet('/eos/user/g/gritsan/Write/Corrections/parquet_xsecadded/'+year+'/'+tree.split('/')[-2]+'_lepmc.parquet')
    jetmc.to_parquet('/eos/user/g/gritsan/Write/Corrections/parquet_xsecadded/'+year+'/'+tree.split('/')[-2]+'_jetmc.parquet')
    allmc.to_parquet('/eos/user/g/gritsan/Write/Corrections/parquet_xsecadded/'+year+'/'+tree.split('/')[-2]+'_allmc.parquet')

    print("parquet saved\n")

    print('SAVED AT: /eos/user/g/gritsan/Write/Corrections/parquet_xsecadded/'+year+'/'+tree.split('/')[-2]+'_*.parquet')

#    lepmc.to_parquet('/eos/user/l/lkang/www/research/OffshellValidation/ReReco/offshell_EW/TemplCorrecEW/parquet/'+year+'/'+tree.split('/')[-2]+'_lepmc.parquet')
#    jetmc.to_parquet('/eos/user/l/lkang/www/research/OffshellValidation/ReReco/offshell_EW/TemplCorrecEW/parquet/'+year+'/'+tree.split('/')[-2]+'_jetmc.parquet')
#    allmc.to_parquet('/eos/user/l/lkang/www/research/OffshellValidation/ReReco/offshell_EW/TemplCorrecEW/parquet/'+year+'/'+tree.split('/')[-2]+'_allmc.parquet')

#    print("parquet saved\n")

#    print('SAVED AT: /eos/user/l/lkang/www/research/OffshellValidation/ReReco/offshell_EW/TemplCorrecEW/parquet/'+year+'/'+tree.split('/')[-2]+'_*.parquet')
 
