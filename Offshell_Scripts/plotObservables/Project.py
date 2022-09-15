import numpy as np



from ROOT import TCanvas, TFile, TProfile, TNtuple, TH1F, TH3F
#from Class_Templatefiles import tempFile,tempHist


def  projectX(hist):
    xbins = hist.GetNbinsX()
    ybins = hist.GetNbinsY()
    zbins = hist.GetNbinsZ()
    medges = np.array([220, 230, 240, 250, 260, 280, 310, 340, 370, 400, 475, 550, 625, 700, 800, 900, 1000, 1200, 1600, 2000, 3000, 13000], dtype='float64')                                                                                                                                                                           


    temp_pos = TH1F("temp_pos","",len(medges)-1, medges)
    temp_neg = TH1F("temp_neg","dif",len(medges)-1, medges)

    #Unroll Hists
    indk = 0
    has_negative = False
    empty = 0
    for z in range (1,zbins+1):
        for y in range (1,ybins+1):
            for x in range (1,xbins+1):
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
                        empty +=1
                if cont  < 0 :
                    has_negative = True
                    
    if empty > 0:  print ("empty:",hist.GetName(),empty*1.0/(xbins*zbins*ybins))
    
    for y in range (1,ybins+1):
        for z in range (1,zbins+1):
            for x in range (1,xbins+1):
                binx_c = hist.GetXaxis().GetBinCenter(x)
                biny_c = hist.GetYaxis().GetBinCenter(y)
                binz_c = hist.GetZaxis().GetBinCenter(z)
                ibin =  hist.FindBin(binx_c,biny_c,binz_c)
                cont  = hist.GetBinContent(ibin)
                binxx = temp_neg.GetXaxis().GetBinCenter(x)
                #if "back_qqZZ" in hist.GetName() :
                #    print (cont,binxx)
                if cont  < 0 :
                    temp_neg.Fill(binxx,-1*cont)
                else :
                    temp_pos.Fill(binxx,cont)
                
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
    #print temp_pos.Integral(),temp_neg.Integral()    
    return temp_neg,temp_pos


def  projectY(hist):
    xbins = hist.GetNbinsX()
    ybins = hist.GetNbinsY()
    zbins = hist.GetNbinsZ()
    medges = np.array([220, 230, 240, 250, 260, 280, 310, 340, 370, 400, 475, 550, 625, 700, 800, 900, 1000, 1200, 1600, 2000, 3000, 13000], dtype='float64')                                                                                                                                                                           


    temp_pos = hist.ProjectionY()   #TH1F("temp_pos","",len(medges)-1, medges)
    temp_neg = hist.ProjectionY()   #TH1F("temp_neg","dif",len(medges)-1, medges)

    temp_pos.Reset()
    temp_neg.Reset()
    
    #Unroll Hists
    indk = 0
    has_negative = False
    empty = 0
    for z in range (1,zbins+1):
        for y in range (1,ybins+1):
            for x in range (1,xbins+1):
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
                        empty +=1
                if cont  < 0 :
                    has_negative = True
                    
    if empty > 0:  print ("empty:",hist.GetName(),empty*1.0/(xbins*zbins*ybins))


    for x in range (1,xbins+1):
            for z in range (1,zbins+1):
                for y in range (1,ybins+1):

                    binx_c = hist.GetXaxis().GetBinCenter(x)
                    biny_c = hist.GetYaxis().GetBinCenter(y)
                    binz_c = hist.GetZaxis().GetBinCenter(z)
                    ibin =  hist.FindBin(binx_c,biny_c,binz_c)
                    cont  = hist.GetBinContent(ibin)
                    binxx = temp_neg.GetXaxis().GetBinCenter(y)
                    #if "back_qqZZ" in hist.GetName() :
                    #    print (cont,binxx)
                    if cont  < 0 :
                        temp_neg.Fill(binxx,-1*cont)
                    else :
                        temp_pos.Fill(binxx,cont)
                
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
    #print temp_pos.Integral(),temp_neg.Integral()    
    return temp_neg,temp_pos


def  projectZ(hist):
    xbins = hist.GetNbinsX()
    ybins = hist.GetNbinsY()
    zbins = hist.GetNbinsZ()
    medges = np.array([220, 230, 240, 250, 260, 280, 310, 340, 370, 400, 475, 550, 625, 700, 800, 900, 1000, 1200, 1600, 2000, 3000, 13000], dtype='float64')                                                                                                                                                                           


    temp_pos = hist.ProjectionZ()   #TH1F("temp_pos","",len(medges)-1, medges)
    temp_neg = hist.ProjectionZ()   #TH1F("temp_neg","dif",len(medges)-1, medges)

    temp_pos.Reset()
    temp_neg.Reset()
    
    #Unroll Hists
    indk = 0
    has_negative = False
    empty = 0
    for z in range (1,zbins+1):
        for y in range (1,ybins+1):
            for x in range (1,xbins+1):
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
                        empty +=1
                if cont  < 0 :
                    has_negative = True
                    
    if empty > 0:  print ("empty:",hist.GetName(),empty*1.0/(xbins*zbins*ybins))

    for y in range (1,ybins+1):
        for x in range (1,xbins+1):
            for z in range (1,zbins+1):
        
            
                    binx_c = hist.GetXaxis().GetBinCenter(x)
                    biny_c = hist.GetYaxis().GetBinCenter(y)
                    binz_c = hist.GetZaxis().GetBinCenter(z)
                    ibin =  hist.FindBin(binx_c,biny_c,binz_c)
                    cont  = hist.GetBinContent(ibin)
                    binxx = temp_neg.GetXaxis().GetBinCenter(z)
                    #if "back_qqZZ" in hist.GetName() :
                    #    print (cont,binxx)
                    if cont  < 0 :
                        temp_neg.Fill(binxx,-1*cont)
                    else :
                        temp_pos.Fill(binxx,cont)
                
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
    #print temp_pos.Integral(),temp_neg.Integral()    
    return temp_neg,temp_pos



















