from ROOT import TCanvas, TFile, TProfile, TNtuple, TH1F, TH3F
#from Class_Templatefiles import tempFile,tempHist

def Unroll(hist):
    xbins = hist.GetNbinsX()
    ybins = hist.GetNbinsY()
    
    is2d = False
    is3d = False
    
    if "TH2" in str(type(hist)) :
        is2d = True 
        temp_pos = TH1F("temp_pos","",xbins*ybins,0,xbins*ybins)
        temp_neg = TH1F("temp_neg","dif",xbins*ybins,0,xbins*ybins)

    if "TH3" in str(type(hist)) :
        is3d = True 
        zbins = hist.GetNbinsZ()
        temp_pos = TH1F("temp_pos","",xbins*ybins*zbins,0,xbins*ybins*zbins)
        temp_neg = TH1F("temp_neg","dif",xbins*ybins*zbins,0,xbins*ybins*zbins)

        
    
    #Unroll Hists
    indk = 0
    has_negative = False 
    for y in range (1,ybins+1):
        for x in range (1,xbins+1):
            if is3d : 
             zbins = hist.GetNbinsZ()

             for z in range (1,zbins+1):
                binx_c = hist.GetXaxis().GetBinCenter(x)
                biny_c = hist.GetYaxis().GetBinCenter(y)
                binz_c = hist.GetZaxis().GetBinCenter(z)
                ibin =  hist.FindBin(binx_c,biny_c,binz_c)
                cont  = hist.GetBinContent(ibin)

                #put small values in empty background bins
                if cont == 0 : 
                    if "back" in hist.GetName():
                        intt = hist.Integral()
                        nb = ybins*xbins*zbins
                        contt = 0.1*intt*1.0/nb
                        #print ("found empty bin",contt)
                        hist.SetBinContent(ibin,contt)
                        #print (cont)
                if cont  < 0 :
                    has_negative = True
            else :
                binx_c = hist.GetXaxis().GetBinCenter(x)
                biny_c = hist.GetYaxis().GetBinCenter(y)
                ibin =  hist.FindBin(binx_c,biny_c)
                cont  = hist.GetBinContent(ibin)

                #put small values in empty background bins
                if cont == 0 : 
                    if "back" in hist.GetName():
                        intt = hist.Integral()
                        nb = ybins*xbins
                        contt = 0.1*intt*1.0/nb
                        #print ("found empty bin",contt)
                        hist.SetBinContent(ibin,contt)
                        #print (cont)
                if cont  < 0 :
                    has_negative = True

                 
    for y in range (1,ybins+1):
        for x in range (1,xbins+1):
            if is3d : 
              zbins = hist.GetNbinsZ()  
              for z in range (1,zbins+1):
                binx_c = hist.GetXaxis().GetBinCenter(x)
                biny_c = hist.GetYaxis().GetBinCenter(y)
                binz_c = hist.GetZaxis().GetBinCenter(z)
                ibin =  hist.FindBin(binx_c,biny_c,binz_c)
                cont  = hist.GetBinContent(ibin)
                if cont  < 0 :
                    temp_neg.Fill(indk,-1*cont)
                else :
                    temp_pos.Fill(indk,cont)
                indk = indk +1
            else :
                  
                binx_c = hist.GetXaxis().GetBinCenter(x)
                biny_c = hist.GetYaxis().GetBinCenter(y)
                
                ibin =  hist.FindBin(binx_c,biny_c)
                cont  = hist.GetBinContent(ibin)
                if cont  < 0 :
                    temp_neg.Fill(indk,-1*cont)
                else :
                    temp_pos.Fill(indk,cont)
                indk = indk +1
                 
                
    temp_name = hist.GetName()
    
    tpname = temp_name
    tnname = temp_name

    '''  
    tnname = tnname.replace("0HPlus","0PH")
    tnname = tnname.replace("0Plus","0PM")
    tnname = tnname.replace("0Minus","0M")
    tpname = tpname.replace("0HPlus","0PH")
    tpname = tpname.replace("0Plus","0PM")
    tpname = tpname.replace("0Minus","0M")
    tnname = tnname.replace("background","bkg")
    tpname = tpname.replace("background","bkg")
    tpname = tnname.replace("qqZZ","qqzz")
    tpname = tpname.replace("ggZZ","ggzz")
    tpname = tpname.replace("ZX","zjets")
    tnname = tpname.replace("VBF","qqH")
    tpname = tpname.replace("VBF","qqH")
    '''
    

    
    if (has_negative or not ( "bkg" in tnname or "Data" in tnname  or "0PH" in tnname or "0PM" in tnname or "L1" in tnname or "0M" in tnname) ):
    

        if "up" in tpname or "dn" in tpname :
            tpnm = tpname.split("_")
            tpnm.insert(2,"positive")
            tpname= tpnm[0]
            for ist in range(1,len(tpnm)):
              tpname = tpname+"_"+tpnm[ist]  
              
        else :     
            tpname = tpname+"_positive"


        if "up" in tnname or "dn" in tnname :
            tnnm = tnname.split("_")
            tnnm.insert(2,"negative")
            tnname= tnnm[0]
            for ist in range(1,len(tnnm)):
              tnname = tnname+"_"+tnnm[ist]  
              
        else :     
            tnname = tnname+"_negative"



            
        temp_neg.SetName(tnname)
        temp_pos.SetName(tpname)
    else:
    
        tnname = tnname.replace("0Xff_","0Mff_")
        tpname = tpname.replace("0Xff_","0Mff_")

        #if ( not ( "0Mff" in tnname )  )  and ("ggH" in tnname or "ttH" in tnname): 

     #       print tpname
        
            #tnsplit =tnname.split("_") 
            #tpsplit =tpname.split("_")
            
            #tpname = tpsplit[0] + "_0PMff_"
            #tnname = tnsplit[0] + "_0PMff_"             
            #take care of syst by adding all the full ending 
            #for nitem in range(1,len(tpsplit)):
            #    tpname = tpname+"_"+tpsplit[nitem]
            #for nitem in range(1,len(tnsplit)):
            #    tnname = tnname+"_"+tnsplit[nitem]
            #tpname = tpname.replace("__","_")
            #tnname = tpname.replace("__","_")
                
        
        temp_neg.SetName(tnname)
        temp_pos.SetName(tpname)

    if "data" in  tnname or "Data" in tnname : 
        

        temp_neg.SetName("data_obs")
        temp_pos.SetName("data_obs")

    return temp_neg,temp_pos

def Unroll_2D_OnShell(hist):
    xbins = hist.GetNbinsX()
    ybins = hist.GetNbinsY()

    temp_pos = TH1F("temp_pos","",xbins*ybins,0,xbins*ybins)
    temp_neg = TH1F("temp_neg","dif",xbins*ybins,0,xbins*ybins)

    #Unroll Hists

    indk = 0
    has_negative = False 
    for y in range (1,ybins+1):
        for x in range (1,xbins+1):
                binx_c = hist.GetXaxis().GetBinCenter(x)
                biny_c = hist.GetYaxis().GetBinCenter(y)
                ibin =  hist.FindBin(binx_c,biny_c)
                cont  = hist.GetBinContent(ibin)

                #put small values in empty background bins
                if cont == 0 : 
                    if "bkg" in hist.GetName():
                        intt = hist.Integral()
                        nb = ybins*xbins
                        contt = 0.1*intt*1.0/nb
                        print ("found empty bin",contt)
                        hist.SetBinContent(ibin,contt)
                        print (cont)
                if cont  < 0 :
                    has_negative = True
                
    for y in range (1,ybins+1):
        for x in range (1,xbins+1):
                binx_c = hist.GetXaxis().GetBinCenter(x)
                biny_c = hist.GetYaxis().GetBinCenter(y)
                ibin =  hist.FindBin(binx_c,biny_c)
                cont  = hist.GetBinContent(ibin)
                if cont  < 0 :
                    temp_neg.Fill(indk,-1*cont)
                else :
                    temp_pos.Fill(indk,cont)
                indk = indk +1

    temp_name = hist.GetName()
    
    tpname = temp_name
    tnname = temp_name

    if (has_negative and ( "bkg" in tnname or "Data" in tnname  or "0PH" in tnname or "0PM" in tnname or "L1" in tnname or "0M" in tnname)):
      for y in range (1,ybins+1):
        for x in range (1,xbins+1):
                binx_c = hist.GetXaxis().GetBinCenter(x)
                biny_c = hist.GetYaxis().GetBinCenter(y)
                ibin =  hist.FindBin(binx_c,biny_c)
                cont  = hist.GetBinContent(ibin)

                #put small values in negtative background bins
                #Also put 0 in negative signal bins
                if cont  < 0 :
                    hist.SetBinContent(ibin,0)
                    print ("found negative bin",cont)
                    cont = 0
                if cont == 0 :
                    if "bkg" in hist.GetName():
                        intt = hist.Integral()
                        nb = ybins*xbins*zbins
                        contt = 0.1*intt*1.0/nb
                        print ("found empty bin",contt)
                        hist.SetBinContent(ibin,contt)
                        print (cont)

      temp_neg.SetName(tnname)
      temp_pos.SetName(tpname)

    elif (has_negative or not ( "bkg" in tnname or "Data" in tnname  or "0PH" in tnname or "0PM" in tnname or "L1" in tnname or "0M" in tnname) ):
    

        if "up" in tpname or "dn" in tpname :
            tpnm = tpname.split("_")
            tpnm.insert(2,"positive")
            tpname= tpnm[0]
            for ist in range(1,len(tpnm)):
              tpname = tpname+"_"+tpnm[ist]  
              
        else :     
            tpname = tpname+"_positive"


        if "up" in tnname or "dn" in tnname :
            tnnm = tnname.split("_")
            tnnm.insert(2,"negative")
            tnname= tnnm[0]
            for ist in range(1,len(tnnm)):
              tnname = tnname+"_"+tnnm[ist]  
              
        else :     
            tnname = tnname+"_negative"

            
        temp_neg.SetName(tnname)
        temp_pos.SetName(tpname)
 
    else:
    
        tnname = tnname.replace("0Xff_","0Mff_")
        tpname = tpname.replace("0Xff_","0Mff_")   
        
        temp_neg.SetName(tnname)
        temp_pos.SetName(tpname)

    if "data" in  tnname or "Data" in tnname : 
        
        temp_neg.SetName("data_obs")
        temp_pos.SetName("data_obs")

    return temp_neg,temp_pos                   

def Unroll_3D_OnShell(hist):
    xbins = hist.GetNbinsX()
    ybins = hist.GetNbinsY()
    zbins = hist.GetNbinsZ()


    temp_pos = TH1F("temp_pos","",xbins*ybins*zbins,0,xbins*ybins*zbins)
    temp_neg = TH1F("temp_neg","dif",xbins*ybins*zbins,0,xbins*ybins*zbins)

    #Unroll Hists
    indk = 0
    has_negative = False 
    for y in range (1,ybins+1):
        for x in range (1,xbins+1):
            for z in range (1,zbins+1):
                binx_c = hist.GetXaxis().GetBinCenter(x)
                biny_c = hist.GetYaxis().GetBinCenter(y)
                binz_c = hist.GetZaxis().GetBinCenter(z)
                ibin =  hist.FindBin(binx_c,biny_c,binz_c)
                cont  = hist.GetBinContent(ibin)

                #put small values in empty background bins
                if cont == 0 : 
                    if "bkg" in hist.GetName():
                        intt = hist.Integral()
                        nb = ybins*xbins*zbins
                        contt = 0.1*intt*1.0/nb
                        print ("found empty bin",contt)
                        hist.SetBinContent(ibin,contt)
                        print (cont)
                if cont  < 0 :
                    has_negative = True

                    
    for y in range (1,ybins+1):
        for x in range (1,xbins+1):
            for z in range (1,zbins+1):
                binx_c = hist.GetXaxis().GetBinCenter(x)
                biny_c = hist.GetYaxis().GetBinCenter(y)
                binz_c = hist.GetZaxis().GetBinCenter(z)
                ibin =  hist.FindBin(binx_c,biny_c,binz_c)
                cont  = hist.GetBinContent(ibin)
                if cont  < 0 :
                    temp_neg.Fill(indk,-1*cont)
                else :
                    temp_pos.Fill(indk,cont)
                indk = indk +1
    temp_name = hist.GetName()
    
    tpname = temp_name
    tnname = temp_name
   
    if (has_negative and ( "bkg" in tnname or "Data" in tnname  or "0PH" in tnname or "0PM" in tnname or "L1" in tnname or "0M" in tnname) ):
      xbins = hist.GetNbinsX()
      ybins = hist.GetNbinsY()
      zbins = hist.GetNbinsZ()
      for x in range (1,xbins+1):
        for y in range (1,ybins+1):
          for z in range (1,zbins+1):
                binx_c = hist.GetXaxis().GetBinCenter(x)
                biny_c = hist.GetYaxis().GetBinCenter(y)
                binz_c = hist.GetZaxis().GetBinCenter(z)
                ibin =  hist.FindBin(binx_c,biny_c,binz_c)
                cont  = hist.GetBinContent(ibin)

                #put small values in negtative background bins
                #Also put 0 in negative signal bins
                if cont  < 0 :
                    hist.SetBinContent(ibin,0)
                    print ("found negative bin",cont)
                    cont = 0
                if cont == 0 :
                    if "bkg" in hist.GetName():
                        intt = hist.Integral()
                        nb = ybins*xbins*zbins
                        contt = 0.1*intt*1.0/nb
                        print ("found empty bin",contt)
                        hist.SetBinContent(ibin,contt)
                        print (cont)
      temp_neg.SetName(tnname)
      temp_pos.SetName(tpname)
      
    elif (has_negative or not ( "bkg" in tnname or "Data" in tnname  or "0PH" in tnname or "0PM" in tnname or "L1" in tnname or "0M" in tnname) ):
    

        if "up" in tpname or "dn" in tpname :
            tpnm = tpname.split("_")
            tpnm.insert(2,"positive")
            tpname= tpnm[0]
            for ist in range(1,len(tpnm)):
              tpname = tpname+"_"+tpnm[ist]  
              
        else :     
            tpname = tpname+"_positive"


        if "up" in tnname or "dn" in tnname :
            tnnm = tnname.split("_")
            tnnm.insert(2,"negative")
            tnname= tnnm[0]
            for ist in range(1,len(tnnm)):
              tnname = tnname+"_"+tnnm[ist]  
              
        else :     
            tnname = tnname+"_negative"

           
        temp_neg.SetName(tnname)
        temp_pos.SetName(tpname)


    else:
    
        tnname = tnname.replace("0Xff_","0Mff_")
        tpname = tpname.replace("0Xff_","0Mff_")

        #if ( not ( "0Mff" in tnname )  )  and ("ggH" in tnname or "ttH" in tnname): 

     #       print tpname
        
            #tnsplit =tnname.split("_") 
            #tpsplit =tpname.split("_")
            
            #tpname = tpsplit[0] + "_0PMff_"
            #tnname = tnsplit[0] + "_0PMff_"             
            #take care of syst by adding all the full ending 
            #for nitem in range(1,len(tpsplit)):
            #    tpname = tpname+"_"+tpsplit[nitem]
            #for nitem in range(1,len(tnsplit)):
            #    tnname = tnname+"_"+tnsplit[nitem]
            #tpname = tpname.replace("__","_")
            #tnname = tpname.replace("__","_")
                
        
        temp_neg.SetName(tnname)
        temp_pos.SetName(tpname)

    if "data" in  tnname or "Data" in tnname : 
        

        temp_neg.SetName("data_obs")
        temp_pos.SetName("data_obs")

    return temp_neg,temp_pos                   

def Unroll(hist):
    xbins = hist.GetNbinsX()
    ybins = hist.GetNbinsY()
    zbins = hist.GetNbinsZ()


    temp_pos = TH1F("temp_pos","",xbins*ybins*zbins,0,xbins*ybins*zbins)
    temp_neg = TH1F("temp_neg","dif",xbins*ybins*zbins,0,xbins*ybins*zbins)

    #Unroll Hists
    indk = 0
    has_negative = False 
    for y in range (1,ybins+1):
        for x in range (1,xbins+1):
            for z in range (1,zbins+1):
                binx_c = hist.GetXaxis().GetBinCenter(x)
                biny_c = hist.GetYaxis().GetBinCenter(y)
                binz_c = hist.GetZaxis().GetBinCenter(z)
                ibin =  hist.FindBin(binx_c,biny_c,binz_c)
                cont  = hist.GetBinContent(ibin)

                #put small values in empty background bins
                if cont == 0 : 
                    if "back" in hist.GetName():
                        intt = hist.Integral()
                        nb = ybins*xbins*zbins
                        contt = 0.1*intt*1.0/nb
                        print ("found empty bin",contt)
                        hist.SetBinContent(ibin,contt)
                        print (cont)
                if cont  < 0 :
                    has_negative = True

                    
    for y in range (1,ybins+1):
        for x in range (1,xbins+1):
            for z in range (1,zbins+1):
                binx_c = hist.GetXaxis().GetBinCenter(x)
                biny_c = hist.GetYaxis().GetBinCenter(y)
                binz_c = hist.GetZaxis().GetBinCenter(z)
                ibin =  hist.FindBin(binx_c,biny_c,binz_c)
                cont  = hist.GetBinContent(ibin)
                if cont  < 0 :
                    temp_neg.Fill(indk,-1*cont)
                else :
                    temp_pos.Fill(indk,cont)
                indk = indk +1
    temp_name = hist.GetName()
    
    tpname = temp_name
    tnname = temp_name

    '''  
    tnname = tnname.replace("0HPlus","0PH")
    tnname = tnname.replace("0Plus","0PM")
    tnname = tnname.replace("0Minus","0M")

    tpname = tpname.replace("0HPlus","0PH")
    tpname = tpname.replace("0Plus","0PM")
    tpname = tpname.replace("0Minus","0M")

    tnname = tnname.replace("background","bkg")
    tpname = tpname.replace("background","bkg")

    tpname = tnname.replace("qqZZ","qqzz")
    tpname = tpname.replace("ggZZ","ggzz")
    tpname = tpname.replace("ZX","zjets")

    tnname = tpname.replace("VBF","qqH")
    tpname = tpname.replace("VBF","qqH")
    '''
    

    
    if (has_negative or not ( "bkg" in tnname or "Data" in tnname  or "0PH" in tnname or "0PM" in tnname or "L1" in tnname or "0M" in tnname) ):
    

        if "up" in tpname or "dn" in tpname :
            tpnm = tpname.split("_")
            tpnm.insert(2,"positive")
            tpname= tpnm[0]
            for ist in range(1,len(tpnm)):
              tpname = tpname+"_"+tpnm[ist]  
              
        else :     
            tpname = tpname+"_positive"


        if "up" in tnname or "dn" in tnname :
            tnnm = tnname.split("_")
            tnnm.insert(2,"negative")
            tnname= tnnm[0]
            for ist in range(1,len(tnnm)):
              tnname = tnname+"_"+tnnm[ist]  
              
        else :     
            tnname = tnname+"_negative"


            
        temp_neg.SetName(tnname)
        temp_pos.SetName(tpname)
    else:
    
        tnname = tnname.replace("0Xff_","0Mff_")
        tpname = tpname.replace("0Xff_","0Mff_")

        #if ( not ( "0Mff" in tnname )  )  and ("ggH" in tnname or "ttH" in tnname): 

     #       print tpname
        
            #tnsplit =tnname.split("_") 
            #tpsplit =tpname.split("_")
            
            #tpname = tpsplit[0] + "_0PMff_"
            #tnname = tnsplit[0] + "_0PMff_"             
            #take care of syst by adding all the full ending 
            #for nitem in range(1,len(tpsplit)):
            #    tpname = tpname+"_"+tpsplit[nitem]
            #for nitem in range(1,len(tnsplit)):
            #    tnname = tnname+"_"+tnsplit[nitem]
            #tpname = tpname.replace("__","_")
            #tnname = tpname.replace("__","_")
                
        
        temp_neg.SetName(tnname)
        temp_pos.SetName(tpname)

    if "data" in  tnname or "Data" in tnname : 
        

        temp_neg.SetName("data_obs")
        temp_pos.SetName("data_obs")

    return temp_neg,temp_pos
