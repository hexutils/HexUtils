import utilities
import downloadfromCJLST
import os
import ROOT

CJLSTscriptsfolder = os.path.dirname(os.path.abspath(__file__))

#have to be in order of who includes whose header file
scripts = ["cConstants", "Discriminants", "Category", "bitops", "FinalStates", "LeptonSFHelper"]

downloader = downloadfromCJLST.Downloader("09326dd9a646711b576c26b07b592dbaf75200f1")
for script in scripts:
    downloader.add("AnalysisStep/src/{}.cc".format(script))
    downloader.add("AnalysisStep/interface/{}.h".format(script))

downloader.add("AnalysisStep/test/ZpXEstimation/include/FakeRates.h")
downloader.add("AnalysisStep/test/ZpXEstimation/src/FakeRates.cpp")
for cconstant in "Dbkgkin_2e2mu", "Dbkgkin_4e", "Dbkgkin_4mu", "DjVBF", "DjjVBF", "DjjWH", "DjjZH", "DbkgjjEWQCD_4l_HadVHTagged_", "DbkgjjEWQCD_4l_JJVBFTagged_", "DbkgjjEWQCD_2l2l_HadVHTagged_", "DbkgjjEWQCD_2l2l_JJVBFTagged_":
    downloader.add("AnalysisStep/data/cconstants/SmoothKDConstant_m4l_{}13TeV.root".format(cconstant))
for rootfile in "FakeRates_SS_2016_Legacy.root", "FakeRates_SS_2017_Legacy.root", "FakeRates_SS_2018_Legacy.root":
    downloader.add(os.path.join("AnalysisStep/data/FakeRates", rootfile), sha1="7f4ba82b5f36db82350d0f64ba48b85d56067709")
for rootfile in "newData_FakeRates_SS_2016.root", "newData_FakeRates_SS_2017.root", "newData_FakeRates_SS_2018.root":
    downloader.add(os.path.join("AnalysisStep/data/FakeRates", rootfile))
for rootfile in "ElectronSF_Legacy_2016_NoGap.root", "ElectronSF_Legacy_2016_Gap.root", "Ele_Reco_2016.root", "Ele_Reco_LowEt_2016.root", "ElectronSF_Legacy_2017_NoGap.root", "ElectronSF_Legacy_2017_Gap.root", "Ele_Reco_2017.root", "Ele_Reco_LowEt_2017.root", "ElectronSF_Legacy_2018_NoGap.root", "ElectronSF_Legacy_2018_Gap.root", "Ele_Reco_2018.root", "Ele_Reco_LowEt_2018.root", "final_HZZ_muon_SF_2016RunB2H_legacy_newLoose_newIso_paper.root", "ScaleFactors_mu_Moriond2017_v2.root", "ScaleFactors_mu_Moriond2018_final.root", "final_HZZ_muon_SF_2018RunA2D_ER_newLoose_newIso_paper.root", "final_HZZ_muon_SF_2018RunA2D_ER_2702.root", "final_HZZ_SF_2017_rereco_mupogsysts_3010.root", "final_HZZ_muon_SF_2017_newLooseIso_mupogSysts_paper.root":
    downloader.add(os.path.join("AnalysisStep/data/LeptonEffScaleFactors/", rootfile))

with utilities.cd(CJLSTscriptsfolder):
    downloader.download()

for script in scripts:
    utilities.LoadMacro(os.path.join(CJLSTscriptsfolder, script+".cc+"))
utilities.LoadMacro(os.path.join(CJLSTscriptsfolder, "FakeRates.cpp+"))

from ROOT import categoryAC19, UntaggedAC19, VBF1jTaggedAC19, VBF2jTaggedAC19, VHLeptTaggedAC19, VHHadrTaggedAC19, ttHLeptTaggedAC19, ttHHadrTaggedAC19, VHMETTaggedAC19, BoostedAC19, categoryMor18

from ROOT import getDVBF2jetsConstant, getDVBF1jetConstant, getDWHhConstant, getDZHhConstant, getDbkgkinConstant, getDbkgConstant
from ROOT import getDVBF2jetsWP, getDVBF1jetWP, getDWHhWP, getDZHhWP
from ROOT import getDVBF2jetsConstant_shiftWP, getDVBF1jetConstant_shiftWP, getDWHhConstant_shiftWP, getDZHhConstant_shiftWP

from ROOT import D_bkg_VBFdec, D_bkg_VHdec, DVBF1j_ME

utilities.LoadMacro(os.path.join(CJLSTscriptsfolder, "updated_xsec.cc+"))
from ROOT import update_xsec
