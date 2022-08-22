# paramters should be taken from the corrections study in 
#/afs/cern.ch/work/s/skyriaco/Offshell_trees/TreeEditor/testCat/cat_jul20/EWcatfit
#/afs/cern.ch/user/s/skyriaco/www/public_html/Offshel/Results/CategorizationStudy/shapesggMC2017/inclusive_fix/cateff/correctionsEW




def EWcor(category,m4l,parvh,parvbf,parevh,parevbf): 
    correction  = 1
    if int(category) == 0 : 

        fvh   = parvh[0] + parvh[1]*m4l + parvh[2]*m4l*m4l + parvh[3]*m4l*m4l*m4l + parvh[4]*m4l*m4l*m4l*m4l    
        fvbf  = parvbf[0] + parvbf[1]*m4l + parvbf[2]*m4l*m4l + parvbf[3]*m4l*m4l*m4l + parvbf[4]*m4l*m4l*m4l*m4l
        
        eJvh  = parevh[0] + parevh[1]*m4l + parevh[2]*m4l*m4l + parevh[3]*m4l*m4l*m4l + parevh[4]*m4l*m4l*m4l*m4l
        eJvbf = parevbf[0] + parevbf[1]*m4l + parevbf[2]*m4l*m4l + parevbf[3]*m4l*m4l*m4l + parevbf[4]*m4l*m4l*m4l*m4l
        
        correction  = (1. - fvh*eJvh - fvbf*eJvbf) /(1. - eJvh - eJvbf) 
    if int(category) == 1 : 
        fvbf  = parvbf[0] + parvbf[1]*m4l + parvbf[2]*m4l*m4l + parvbf[3]*m4l*m4l*m4l + parvbf[4]*m4l*m4l*m4l*m4l
        correction  = fvbf
    if int(category) == 2 : 
        fvh   = parvh[0] + parvh[1]*m4l + parvh[2]*m4l*m4l + parvh[3]*m4l*m4l*m4l + parvh[4]*m4l*m4l*m4l*m4l    
        correction  = fvbf

    return correction















