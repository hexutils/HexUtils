/*
Simple fast c++ script to skimm trees to only specific branches
 */







void filterTree(char* filename,char *foutname)
{
 
  //TFile *f1 = new TFile("/eos/user/g/gritsan/Write/TaggedTrees/OffshellTemplateTrees20220923/nominal/cjlst/RunIILegacy/200205_CutBased/MC_2017/OffshellAC/gg/ggTo4e_0PL1H125_MCFM701/ZZ4lAnalysis.root");

  TFile *f1 = TFile::Open(filename);



  TTree *oldtree; f1->GetObject("eventTree", oldtree);


  oldtree->SetBranchStatus("*", 0);
 
  // Activate only four of them
  for (auto activeBranchName : {"GenHMass","LHEDaughterPt","LHEDaughterPhi" ,"LHEDaughterEta","LHEDaughterMass","LHEDaughterId","KFactor_QCD_ggZZ_Nominal","xsec","p_Gen_GG_SIG_kappaTopBot_1_ghz1_1_MCFM","p_Gen_GG_BSI_kappaTopBot_1_ghz1_1_MCFM","p_Gen_GG_BKG_MCFM"}) {
    oldtree->SetBranchStatus(activeBranchName, 1);
  }
  
  //"LHEAssociatedParticleMass","LHEAssociatedParticlePhi","LHEAssociatedParticlePt","LHEAssociatedParticleEta"



  // Create a new file + a clone of old tree header. Do not copy events
  TFile newfile(foutname, "recreate");
  auto newtree = oldtree->CloneTree();
  
  
  cout<<"here"<<endl;
 
  // Divert branch fH to a separate file and copy all events
  //newtree->GetBranch("LHEDaughterPhi")->SetFile("small_fH.root");
  //newtree->CopyEntries(oldtree);
 
  newtree->Print();

  newfile.Write();
  gApplication->Terminate();
}

