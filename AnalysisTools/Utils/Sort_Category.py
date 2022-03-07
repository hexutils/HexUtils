def sort_category(Analysis_Config,prod):
   if Analysis_Config.name == "OnShell_HVV_Photons_2021":
     p_sorted = False
     if "ZZTo4l" in prod: 
       prod = "ZZTo4l"
       p_sorted = True
     if 'ggH' in prod:
       prod = "ggH"
       p_sorted = True
     elif 'VBF' in prod:
       prod = "VBF"
       p_sorted = True
     elif 'Wplus' in prod:
       prod = "Wplus"
       p_sorted = True
     elif 'Wminus' in prod:
       prod = "Wminus"
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
     elif 'tHW' in prod:
       prod = 'tHW'
       p_sorted = True
     elif 'tqH' in prod:
       prod = 'tqH'
       p_sorted = True
     return prod,p_sorted 
   return prod,p_sorted 
