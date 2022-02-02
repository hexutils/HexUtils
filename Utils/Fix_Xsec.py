def update_xsec(name, xsec):
  new_xsec = 0
  # All of these will sync the xsec with the YR 4 xsec #
  # Currently Only works for 125 GeV #
  if ("bbH120" in name): new_xsec = 0.5534*0.0001659; 
  elif ("bbH124" in name):  new_xsec = 0.4999*0.0002502 
  elif ("bbH125" in name):  new_xsec = 0.4880*0.0002745 
  elif ("bbH126" in name):  new_xsec = 0.4760*0.0003001 
  elif ("bbH130" in name):  new_xsec = 0.4304*0.0004124 

  elif ("ttH120" in name): new_xsec = 0.5697*0.00042015426186342315 
  elif ("ttH124" in name): new_xsec = 0.5193*0.000649581819587205 
  elif ("ttH125" in name) or ("ttH125_tuneup" in name) or ("ttH125_tunedown" in name): new_xsec = 0.5071*0.0007176792246182684
  elif ("ttH126" in name): new_xsec = 0.4964*0.000788372579311756 
  elif ("ttH130" in name): new_xsec = 0.4539*0.0010947747168867862 

  elif ("ggZH125" in name): new_xsec =  new_xsec = 0.1227*0.0006991275831543255# Assuming some scale factor is included 

  # qqZH xsec as total ZH xsec - ggZH. Numbers from https://twiki.cern.ch/twiki/bin/view/LHCPhysics/CERNYellowReportPageAt13TeV#ZH_Process
  elif ("ZH120" in name): new_xsec = 0.864*0.0004106877051958817
  elif ("ZH124" in name): new_xsec = 0.7809*0.0006322344128856341
  elif (("ZH125" in name) or ("ZH125_tuneup" in name) or ("ZH125_tunedown" in name)): new_xsec = 0.7612*0.0006991275831543255 
  elif ("ZH126" in name): new_xsec = 0.7431*0.0007650556125370585
  elif ("ZH130" in name): new_xsec = 0.6735*0.0010674878938974918
        
  else: new_xsec = xsec
    
  return new_xsec
