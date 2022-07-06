{
  TString LIBCOLLIER = "libcollier.so";
  TString LIBMCFM = "libmcfm_707.so";
  TString LIBJHUGENMELA = "libjhugenmela.so";
  TString LIBMELA = "libJHUGenMELAMELA.so";

  TString loadMELA = __FILE__;
  TString testdir = loadMELA(0, loadMELA.Last('/'));
  if (!testdir.BeginsWith(".") && testdir.EndsWith(".")) testdir = testdir(0, testdir.Last('/'));
  TString LIBPATH = testdir+"/../data/$SCRAM_ARCH/";

  TString LIBMELADIR = LIBPATH;
  if (gSystem->FindDynamicLibrary(LIBMELA)) LIBMELADIR = "";

  gInterpreter->AddIncludePath("$ROOFITSYS/include/");
  gInterpreter->AddIncludePath(testdir+"/../interface/");
  //////////////////////////////////////
  //these explicit loads are required on
  //some machines but not others
  //not entirely sure why
  //either way, they shouldn't hurt
  gSystem->Load("libRooFit");
  gSystem->Load("libPhysics");
  gSystem->Load("libgfortran");
  //////////////////////////////////////
  gSystem->Load(LIBPATH + LIBCOLLIER);
  gSystem->Load(LIBMELADIR + LIBMELA);
  gSystem->Load(LIBPATH + LIBMCFM);
}
