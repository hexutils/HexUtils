import ROOT

def IsCrossFeed(event): 

    iscrossf = False



    vj1 = ROOT.TLorentzVector()
    vj2 = ROOT.TLorentzVector()
    vjj = ROOT.TLorentzVector()
    
    vl1 = ROOT.TLorentzVector()
    vl2 = ROOT.TLorentzVector()
    vl3 = ROOT.TLorentzVector()
    vl4 = ROOT.TLorentzVector()
    
    vll1 = ROOT.TLorentzVector()
    vll2 = ROOT.TLorentzVector()
    
    v2l2qa = ROOT.TLorentzVector()
    v2l2qb = ROOT.TLorentzVector()
    

    
    m1 = event.LHEAssociatedParticleMass[0]
    phi1 = event.LHEAssociatedParticlePhi[0]
    pt1 = event.LHEAssociatedParticlePt[0]
    eta1 = event.LHEAssociatedParticleEta[0]
    
    m2 = event.LHEAssociatedParticleMass[1]
    phi2 = event.LHEAssociatedParticlePhi[1]
    pt2 = event.LHEAssociatedParticlePt[1]
    eta2 = event.LHEAssociatedParticleEta[1]
    
    ml1 = event.LHEDaughterMass[0]
    phil1 = event.LHEDaughterPhi[0]
    ptl1 = event.LHEDaughterPt[0]
    etal1 = event.LHEDaughterEta[0]
    
    ml2 = event.LHEDaughterMass[1]
    phil2 = event.LHEDaughterPhi[1]
    ptl2 = event.LHEDaughterPt[1]
    etal2 = event.LHEDaughterEta[1]
    
    ml3 = event.LHEDaughterMass[2]
    phil3 = event.LHEDaughterPhi[2]
    ptl3 = event.LHEDaughterPt[2]
    etal3 = event.LHEDaughterEta[2]
    
    ml4 = event.LHEDaughterMass[3]
    phil4 = event.LHEDaughterPhi[3]
    ptl4 = event.LHEDaughterPt[3]
    etal4 = event.LHEDaughterEta[3]
    
    vl1.SetPtEtaPhiM(ptl1,etal1,phil1,ml1)
    vl2.SetPtEtaPhiM(ptl2,etal2,phil2,ml2)
    vl3.SetPtEtaPhiM(ptl3,etal3,phil3,ml3)
    vl4.SetPtEtaPhiM(ptl4,etal4,phil4,ml4)
    
    
    
    vj1.SetPtEtaPhiM(pt1,eta1,phi1,m1)
    vj2.SetPtEtaPhiM(pt2,eta2,phi2,m2)
    vjj = vj1 + vj2
    
    
    if event.LHEDaughterId[0] == - event.LHEDaughterId[1] :
        vll1 = vl1 + vl2
        vll2 = vl3 + vl4
    if event.LHEDaughterId[0] == - event.LHEDaughterId[2] :
        vll1 = vl1 + vl3
        vll2 = vl2 + vl4
            
    if event.LHEDaughterId[0] == - event.LHEDaughterId[3] :
        vll1 = vl1 + vl4
        vll2 = vl2 + vl3




    v2l2qa = vll1 + vjj
    v2l2qb = vll2 + vjj

    mv2l2qa = v2l2qa.Mag()
    mv2l2qb = v2l2qb.Mag()

        #print mv2l2qa, mv2l2qb                                                                                                                                                                                                                                                          
    if abs(mv2l2qa - 125.0) < 0.1  or abs(mv2l2qb - 125.0) < 0.1 : iscrossf = True
    
    if abs(event.LHEDaughterId[0]) == abs(event.LHEDaughterId[1]) and abs(event.LHEDaughterId[0]) == abs(event.LHEDaughterId[2])  and abs(event.LHEDaughterId[0]) == abs(event.LHEDaughterId[3]):

        if event.LHEDaughterId[0] == - event.LHEDaughterId[1] :
            vll1 = vl1 + vl2
            vll2 = vl3 + vl4
            
            v2l2qa = vll1 + vjj
            v2l2qb = vll2 + vjj
            
            mv2l2qa = v2l2qa.Mag()
            mv2l2qb = v2l2qb.Mag()
            if abs(mv2l2qa - 125.0) < 0.1  or abs(mv2l2qb - 125.0) < 0.1 : iscrossf = True
        
        if event.LHEDaughterId[0] == - event.LHEDaughterId[2] :
            vll1 = vl1 + vl3
            vll2 = vl2 + vl4
            
            v2l2qa = vll1 + vjj
            v2l2qb = vll2 + vjj
            
            mv2l2qa = v2l2qa.Mag()
            mv2l2qb = v2l2qb.Mag()
            if abs(mv2l2qa - 125.0) < 0.1  or abs(mv2l2qb - 125.0) < 0.1 :  iscrossf = True            

        if event.LHEDaughterId[0] == - event.LHEDaughterId[3] :
            vll1 = vl1 + vl4
            vll2 = vl2 + vl3
            
            v2l2qa = vll1 + vjj
            v2l2qb = vll2 + vjj
            
            mv2l2qa = v2l2qa.Mag()
            mv2l2qb = v2l2qb.Mag()
            if abs(mv2l2qa - 125.0) < 0.1  or abs(mv2l2qb - 125.0) < 0.1 : iscrossf = True


    #if iscrossf : print ("res ",iscrossf)        
        
    return iscrossf
