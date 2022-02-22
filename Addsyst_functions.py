def addlumi(lines,processes):
    line = "lumi_13TeV lnN"
    for pr in processes :
        line =  line + " 1.025/0.975" 
    #line = line + " \n"    
    lines.append(line)    

def addQCDscale_muR_ggH(lines,processes):
    line = "QCDscale_muF_qqH lnN"
    for pr in processes :
        if "ggH" in pr : 
            line =  line + " 1.07110716651/0.906525580474"
        else :
             line = line + " -"
    #line = line + " \n"    
    lines.append(line)


    
def addQCDscale_muR_qqH(lines,processes):
    line = "QCDscale_muR_qqH lnN"
    for pr in processes :
        if "qqH" in pr : 
            line =  line + " 0.990706673021/1.00745328795"
        else :
             line = line + " -"
    #line = line + " \n"    
    lines.append(line)

def addQCDscale_muF_ggH(lines,processes):
    line = "QCDscale_muF_ggH lnN"
    for pr in processes :
        if "ggH" in pr : 
            line =  line + " 0.980003776978/1.01624735028"
        else :
             line = line + " -"
    #line = line + " \n"    
    lines.append(line)


    
def addQCDscale_muF_qqH(lines,processes):
    line = "QCDscale_muF_qqH lnN"
    for pr in processes :
        if "qqH" in pr : 
            line =  line + " 1.003290476/1.00409718125"
        else :
             line = line + " -"
    #line = line + " \n"    
    lines.append(line)



def addEWcorr_qqZZ(lines,processes):
    line = "EWcorr_qqZZ lnN"
    for pr in processes :
        if "back_qqZZ" in pr : 
            line =  line + " 0.99900110477/1.0009987799"
        else :
            line = line + " -"
    #line = line + " \n"    
    lines.append(line)


