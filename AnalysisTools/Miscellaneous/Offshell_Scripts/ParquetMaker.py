
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


yeardict = {
    'MC_2016_CorrectBTag':'2016',
    'MC_2017':'2017',
    'MC_2018':'2018'
}


#print( str( sys.argv[1].split('/')[-5] ) )

#print( yeardict[str( sys.argv[1].split('/')[-5] )] )

#print( str( sys.argv[1] ) )

#sys.exit()


year = yeardict[str( sys.argv[1].split('/')[-5] )]
treelist = [str( sys.argv[1] )]


print(year)
print(treelist)


for ntree, tree in enumerate(tqdm(treelist)):

    #if ntree == 1: break

    print('===== ', tree.split('/')[-2], ' =====\n')

    if os.path.exists('/eos/user/l/lkang/www/research/OffshellValidation/ReReco/offshell_EW/TemplCorrecEW/parquet/'+year+'/'+tree.split('/')[-2]+'_lepmc.parquet') and os.path.exists('/eos/user/l/lkang/www/research/OffshellValidation/ReReco/offshell_EW/TemplCorrecEW/parquet/'+year+'/'+tree.split('/')[-2]+'_jetmc.parquet') and os.path.exists('/eos/user/l/lkang/www/research/OffshellValidation/ReReco/offshell_EW/TemplCorrecEW/parquet/'+year+'/'+tree.split('/')[-2]+'_allmc.parquet'):
        continue
    
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

    b = t.arrays(t.keys(filter_name='Event*')+t.keys(filter_name='LHEDaughter*')+t.keys(filter_name='LHEMother*')+['EVwgt', 'MCwgt', 'SystUp', 'SystDn']+t.keys(filter_name='p_Gen*'), aliases={'EVwgt': evweight, 'MCwgt': mcweight, 'SystUp': wsystup, 'SystDn': wsystdn})
    lepvec = vec.zip({'EventNumber': b.EventNumber, 'id': b.LHEDaughterId, 'mass': b.LHEDaughterMass, 'pt': b.LHEDaughterPt, 'eta': b.LHEDaughterEta, 'phi': b.LHEDaughterPhi})

    print(lepvec[:,0]['id'])

    print(type(lepvec[:,0]['id']))



    lepmc = ak.to_pandas(b, how='outer').loc[pd.IndexSlice[:, [0,1,2,3]], :]

    print("lepmc saved")

    #===== Saving jetcut dataframe =====#
    
    b = t.arrays(t.keys(filter_name='Event*')+t.keys(filter_name='LHEAssociated*')+['EVwgt', 'MCwgt', 'SystUp', 'SystDn']+t.keys(filter_name='p_Gen*') + t.keys(filter_name='DiJetMass'), aliases={'EVwgt': evweight, 'MCwgt': mcweight, 'SystUp': wsystup, 'SystDn': wsystdn})
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

            jjcombo = np.array( ((jetvec2[:,0]+jetvec2[:,1]).M) * ((jetvec2[:,0]['id']+jetvec2[:,1]['id'])%2==1) * (np.isin(jetvec2[:,0]['id'], [-1, 1, -2, 2, -3, 3, -4, 4, -5, 5])) ) - pm
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

    branch = ['EventNumber', 'EventTag', "xsec", "genxsec", "genBR", 'GenHMass', 'ZZMass', 'Dbsi', 'Dbkg'] + t.keys(filter_name='D2*') + t.keys(filter_name='p_Gen*')

    b = t.arrays(branch+['EVwgt', 'MCwgt', 'SystUp', 'SystDn'], aliases={'EVwgt': evweight, 'MCwgt': mcweight, 'SystUp': wsystup, 'SystDn': wsystdn})
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

    lepmc.to_parquet('/eos/user/l/lkang/www/research/OffshellValidation/ReReco/offshell_EW/TemplCorrecEW/parquet/'+year+'/'+tree.split('/')[-2]+'_lepmc.parquet')
    jetmc.to_parquet('/eos/user/l/lkang/www/research/OffshellValidation/ReReco/offshell_EW/TemplCorrecEW/parquet/'+year+'/'+tree.split('/')[-2]+'_jetmc.parquet')
    allmc.to_parquet('/eos/user/l/lkang/www/research/OffshellValidation/ReReco/offshell_EW/TemplCorrecEW/parquet/'+year+'/'+tree.split('/')[-2]+'_allmc.parquet')

    print("parquet saved\n")

    print('SAVED AT: /eos/user/l/lkang/www/research/OffshellValidation/ReReco/offshell_EW/TemplCorrecEW/parquet/'+year+'/'+tree.split('/')[-2]+'_*.parquet')
 
