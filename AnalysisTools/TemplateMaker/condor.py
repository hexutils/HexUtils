#################### DEFINE OPTIONS FOR LOOPS ####################

year = ['2016', '2017', '2018']
state = ['2e2mu', '2e2tau', '2mu2tau', '4e', '4mu', '4tau']
component = ['SIG', 'BSI', 'BKG']
component = ['0', '1', '2', '3', '4', '5']
tag = ['0', '1', '2']
syst = ['btagD', 'btagU', 'jerD', 'jerU', 'jesD', 'jesU']
syst = ['nom', 'kfqcd_up', 'kfqcd_dn', 'kfpdf_up', 'kfpdf_dn', 'kfas_up', 'kfas_dn', 'pdfV_up', 'pdfV_dn', 'AsMZV_up', 'AsMZV_dn', 'QCDmuRV_up', 'QCDmuRV_dn', 'QCDmuFV_up', 'QCDmuFV_dn']

#################### GLUON FUSION BY CATEGORY ####################
'''
for y in year:
    for s in state:
        for c in component:
            for t in tag:
                print("python3 RRtemplates_ggH.py "+y+" "+s+" "+c+" "+t)
'''
#################### GLUON FUSION INCLUSIVE ####################
'''
for y in year:
    for s in state:
        for c in component:
            print("python3 RRtemplates_ggH_inc.py "+y+" "+s+" "+c)
'''
#################### ELECTROWEAK BY CATEGORY ####################
'''
for y in year:
    for c in component:
        for t in tag:
            print("python3 RRtemplates_VBF.py "+y+" "+c+" "+t)
'''
#################### ELECTROWEAK INCLUSIVE ####################
'''
for y in year:
    for c in component:
        print("python3 RRtemplates_VBF.py "+y+" "+c)
'''
#################### QQBAR BACKGROUND BY CATEGORY ####################



#################### QQBAR BACKGROUND INCLUSIVE ####################








#################### POWHEG REWEIGHTING SYST ####################
'''
for y in year:
    for c in component:
        for s in syst:
            for t in tag:
                print("python3 RRtemplates_qqbar.py "+y+" "+c+" "+s+" "+t)
'''
#################### POWHEG REWEIGHTING SHAPES ####################
'''
for y in year:
    for c in component:
        for t in tag:
            print("python3 POWHEGreweight_shape.py "+y+" "+c+" "+t+" nom")
'''

'''
for y in year:
    for c in component:
        for t in tag:
            for s in syst:
                print("python3 POWHEGreweight_shape.py "+y+" "+c+" "+t+" "+s)
'''


for y in year:
    for c in component:
        for t in tag:
            for s in syst:
                print("python3 POWHEGreweight_kappaQ.py "+y+" "+c+" "+t+" "+s)


