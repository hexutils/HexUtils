def sort_category(Analysis_Config,prod):
   if Analysis_Config.name in("OnShell_HVV_Photons_2021","gammaH_Photons_Decay_Only"):
     p_sorted = False
     print(prod)
     if "ZZTo4l" in prod: 
       prod = "qqZZ"
       p_sorted = True
     elif any(x in prod for x in ["ggTo4e","ggTo2e2mu","ggTo2e2tau","ggTo2mu2tau","ggTo4mu","ggTo4tau"]): 
       prod = "ggZZ"
       p_sorted = True
     elif all(x in prod for x in ["VBF","Contin"]) or prod in ["TTLToLL_M1to0_MLM","TTZToLLNuNu_M10","TTZJets_M10_MLM","TTZZ","TTWW","ZZZ","WWZ","WZZ"] or prod in ["OffshellAC"]: 
       prod = "ew_bkg"
       p_sorted = True
     elif 'Data' in prod:
       prod = "ZX"
       p_sorted = True
     elif 'ggH' in prod:
       prod = "ggH"
       p_sorted = True
     elif 'VBF' in prod:
       prod = "VBF"
       p_sorted = True
     elif 'Wplus' in prod:
       prod = "WplusH"
       p_sorted = True
     elif 'Wminus' in prod:
       prod = "WminusH"
       p_sorted = True
     elif 'ZH' in prod and not 'ggZH' in prod:
       prod = "ZH"
       p_sorted = True
     elif 'ggZH' in prod:
       prod = "ggZH"
       p_sorted = True
     elif 'bbH' in prod:
       prod = 'bbH'
       p_sorted = True
     elif 'ttH' in prod:
       prod = 'ttH'
       p_sorted = True
     elif ('tHW' in prod) or ('tqH' in prod):
       prod = 'tH'
       p_sorted = True
     return prod,p_sorted 
   return prod,p_sorted 
