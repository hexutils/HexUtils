import os
import sys

ifile = int(sys.argv[1])


files =["/eos/user/g/gritsan/Write/TaggedTrees/OffshellTemplateTrees20220923/nominal/cjlst/RunIILegacy/200205_CutBased/MC_2017/OffshellAC/gg/ggTo2e2mu_0MH125Contin_MCFM701/ZZ4lAnalysis.root",
"/eos/user/g/gritsan/Write/TaggedTrees/OffshellTemplateTrees20220923/nominal/cjlst/RunIILegacy/200205_CutBased/MC_2017/OffshellAC/gg/ggTo2e2mu_0MH125_MCFM701/ZZ4lAnalysis.root",
"/eos/user/g/gritsan/Write/TaggedTrees/OffshellTemplateTrees20220923/nominal/cjlst/RunIILegacy/200205_CutBased/MC_2017/OffshellAC/gg/ggTo2e2mu_0Mf05ph0H125Contin_MCFM701/ZZ4lAnalysis.root",
"/eos/user/g/gritsan/Write/TaggedTrees/OffshellTemplateTrees20220923/nominal/cjlst/RunIILegacy/200205_CutBased/MC_2017/OffshellAC/gg/ggTo2e2mu_0Mf05ph0H125_MCFM701/ZZ4lAnalysis.root",
"/eos/user/g/gritsan/Write/TaggedTrees/OffshellTemplateTrees20220923/nominal/cjlst/RunIILegacy/200205_CutBased/MC_2017/OffshellAC/gg/ggTo2e2mu_0PHH125Contin_MCFM701/ZZ4lAnalysis.root",
"/eos/user/g/gritsan/Write/TaggedTrees/OffshellTemplateTrees20220923/nominal/cjlst/RunIILegacy/200205_CutBased/MC_2017/OffshellAC/gg/ggTo2e2mu_0PHH125_MCFM701/ZZ4lAnalysis.root",
"/eos/user/g/gritsan/Write/TaggedTrees/OffshellTemplateTrees20220923/nominal/cjlst/RunIILegacy/200205_CutBased/MC_2017/OffshellAC/gg/ggTo2e2mu_0PHf05ph0H125Contin_MCFM701/ZZ4lAnalysis.root",
"/eos/user/g/gritsan/Write/TaggedTrees/OffshellTemplateTrees20220923/nominal/cjlst/RunIILegacy/200205_CutBased/MC_2017/OffshellAC/gg/ggTo2e2mu_0PHf05ph0H125_MCFM701/ZZ4lAnalysis.root",
"/eos/user/g/gritsan/Write/TaggedTrees/OffshellTemplateTrees20220923/nominal/cjlst/RunIILegacy/200205_CutBased/MC_2017/OffshellAC/gg/ggTo2e2mu_0PL1H125Contin_MCFM701/ZZ4lAnalysis.root",
"/eos/user/g/gritsan/Write/TaggedTrees/OffshellTemplateTrees20220923/nominal/cjlst/RunIILegacy/200205_CutBased/MC_2017/OffshellAC/gg/ggTo2e2mu_0PL1H125_MCFM701/ZZ4lAnalysis.root",
"/eos/user/g/gritsan/Write/TaggedTrees/OffshellTemplateTrees20220923/nominal/cjlst/RunIILegacy/200205_CutBased/MC_2017/OffshellAC/gg/ggTo2e2mu_0PL1f05ph0H125Contin_MCFM701/ZZ4lAnalysis.root",
"/eos/user/g/gritsan/Write/TaggedTrees/OffshellTemplateTrees20220923/nominal/cjlst/RunIILegacy/200205_CutBased/MC_2017/OffshellAC/gg/ggTo2e2mu_0PL1f05ph0H125_MCFM701/ZZ4lAnalysis.root",
"/eos/user/g/gritsan/Write/TaggedTrees/OffshellTemplateTrees20220923/nominal/cjlst/RunIILegacy/200205_CutBased/MC_2017/OffshellAC/gg/ggTo2e2mu_0PMH125Contin_MCFM701/ZZ4lAnalysis.root",
"/eos/user/g/gritsan/Write/TaggedTrees/OffshellTemplateTrees20220923/nominal/cjlst/RunIILegacy/200205_CutBased/MC_2017/OffshellAC/gg/ggTo2e2mu_0PMH125_MCFM701/ZZ4lAnalysis.root",
"/eos/user/g/gritsan/Write/TaggedTrees/OffshellTemplateTrees20220923/nominal/cjlst/RunIILegacy/200205_CutBased/MC_2017/OffshellAC/gg/ggTo2e2mu_Contin_MCFM701/ZZ4lAnalysis.root",
"/eos/user/g/gritsan/Write/TaggedTrees/OffshellTemplateTrees20220923/nominal/cjlst/RunIILegacy/200205_CutBased/MC_2017/OffshellAC/gg/ggTo2e2tau_0PMH125_MCFM701/ZZ4lAnalysis.root",
"/eos/user/g/gritsan/Write/TaggedTrees/OffshellTemplateTrees20220923/nominal/cjlst/RunIILegacy/200205_CutBased/MC_2017/OffshellAC/gg/ggTo2mu2tau_0PMH125_MCFM701/ZZ4lAnalysis.root",
"/eos/user/g/gritsan/Write/TaggedTrees/OffshellTemplateTrees20220923/nominal/cjlst/RunIILegacy/200205_CutBased/MC_2017/OffshellAC/gg/ggTo4e_0MH125Contin_MCFM701/ZZ4lAnalysis.root",
"/eos/user/g/gritsan/Write/TaggedTrees/OffshellTemplateTrees20220923/nominal/cjlst/RunIILegacy/200205_CutBased/MC_2017/OffshellAC/gg/ggTo4e_0MH125_MCFM701/ZZ4lAnalysis.root",
"/eos/user/g/gritsan/Write/TaggedTrees/OffshellTemplateTrees20220923/nominal/cjlst/RunIILegacy/200205_CutBased/MC_2017/OffshellAC/gg/ggTo4e_0Mf05ph0H125Contin_MCFM701/ZZ4lAnalysis.root",
"/eos/user/g/gritsan/Write/TaggedTrees/OffshellTemplateTrees20220923/nominal/cjlst/RunIILegacy/200205_CutBased/MC_2017/OffshellAC/gg/ggTo4e_0Mf05ph0H125_MCFM701/ZZ4lAnalysis.root",
"/eos/user/g/gritsan/Write/TaggedTrees/OffshellTemplateTrees20220923/nominal/cjlst/RunIILegacy/200205_CutBased/MC_2017/OffshellAC/gg/ggTo4e_0PHH125Contin_MCFM701/ZZ4lAnalysis.root",
"/eos/user/g/gritsan/Write/TaggedTrees/OffshellTemplateTrees20220923/nominal/cjlst/RunIILegacy/200205_CutBased/MC_2017/OffshellAC/gg/ggTo4e_0PHH125_MCFM701/ZZ4lAnalysis.root",
"/eos/user/g/gritsan/Write/TaggedTrees/OffshellTemplateTrees20220923/nominal/cjlst/RunIILegacy/200205_CutBased/MC_2017/OffshellAC/gg/ggTo4e_0PHf05ph0H125Contin_MCFM701/ZZ4lAnalysis.root",
"/eos/user/g/gritsan/Write/TaggedTrees/OffshellTemplateTrees20220923/nominal/cjlst/RunIILegacy/200205_CutBased/MC_2017/OffshellAC/gg/ggTo4e_0PHf05ph0H125_MCFM701/ZZ4lAnalysis.root",
"/eos/user/g/gritsan/Write/TaggedTrees/OffshellTemplateTrees20220923/nominal/cjlst/RunIILegacy/200205_CutBased/MC_2017/OffshellAC/gg/ggTo4e_0PL1H125Contin_MCFM701/ZZ4lAnalysis.root",
"/eos/user/g/gritsan/Write/TaggedTrees/OffshellTemplateTrees20220923/nominal/cjlst/RunIILegacy/200205_CutBased/MC_2017/OffshellAC/gg/ggTo4e_0PL1H125_MCFM701/ZZ4lAnalysis.root",
"/eos/user/g/gritsan/Write/TaggedTrees/OffshellTemplateTrees20220923/nominal/cjlst/RunIILegacy/200205_CutBased/MC_2017/OffshellAC/gg/ggTo4e_0PL1H125_MCFM701/small_fH.root",
"/eos/user/g/gritsan/Write/TaggedTrees/OffshellTemplateTrees20220923/nominal/cjlst/RunIILegacy/200205_CutBased/MC_2017/OffshellAC/gg/ggTo4e_0PL1f05ph0H125Contin_MCFM701/ZZ4lAnalysis.root",
"/eos/user/g/gritsan/Write/TaggedTrees/OffshellTemplateTrees20220923/nominal/cjlst/RunIILegacy/200205_CutBased/MC_2017/OffshellAC/gg/ggTo4e_0PL1f05ph0H125_MCFM701/ZZ4lAnalysis.root",
"/eos/user/g/gritsan/Write/TaggedTrees/OffshellTemplateTrees20220923/nominal/cjlst/RunIILegacy/200205_CutBased/MC_2017/OffshellAC/gg/ggTo4e_0PMH125Contin_MCFM701/ZZ4lAnalysis.root",
"/eos/user/g/gritsan/Write/TaggedTrees/OffshellTemplateTrees20220923/nominal/cjlst/RunIILegacy/200205_CutBased/MC_2017/OffshellAC/gg/ggTo4e_0PMH125_MCFM701/ZZ4lAnalysis.root",
"/eos/user/g/gritsan/Write/TaggedTrees/OffshellTemplateTrees20220923/nominal/cjlst/RunIILegacy/200205_CutBased/MC_2017/OffshellAC/gg/ggTo4e_Contin_MCFM701/ZZ4lAnalysis.root",
"/eos/user/g/gritsan/Write/TaggedTrees/OffshellTemplateTrees20220923/nominal/cjlst/RunIILegacy/200205_CutBased/MC_2017/OffshellAC/gg/ggTo4mu_0MH125Contin_MCFM701/ZZ4lAnalysis.root",
"/eos/user/g/gritsan/Write/TaggedTrees/OffshellTemplateTrees20220923/nominal/cjlst/RunIILegacy/200205_CutBased/MC_2017/OffshellAC/gg/ggTo4mu_0MH125_MCFM701/ZZ4lAnalysis.root",
"/eos/user/g/gritsan/Write/TaggedTrees/OffshellTemplateTrees20220923/nominal/cjlst/RunIILegacy/200205_CutBased/MC_2017/OffshellAC/gg/ggTo4mu_0Mf05ph0H125Contin_MCFM701/ZZ4lAnalysis.root",
"/eos/user/g/gritsan/Write/TaggedTrees/OffshellTemplateTrees20220923/nominal/cjlst/RunIILegacy/200205_CutBased/MC_2017/OffshellAC/gg/ggTo4mu_0Mf05ph0H125_MCFM701/ZZ4lAnalysis.root",
"/eos/user/g/gritsan/Write/TaggedTrees/OffshellTemplateTrees20220923/nominal/cjlst/RunIILegacy/200205_CutBased/MC_2017/OffshellAC/gg/ggTo4mu_0PHH125Contin_MCFM701/ZZ4lAnalysis.root",
"/eos/user/g/gritsan/Write/TaggedTrees/OffshellTemplateTrees20220923/nominal/cjlst/RunIILegacy/200205_CutBased/MC_2017/OffshellAC/gg/ggTo4mu_0PHH125_MCFM701/ZZ4lAnalysis.root",
"/eos/user/g/gritsan/Write/TaggedTrees/OffshellTemplateTrees20220923/nominal/cjlst/RunIILegacy/200205_CutBased/MC_2017/OffshellAC/gg/ggTo4mu_0PHf05ph0H125Contin_MCFM701/ZZ4lAnalysis.root",
"/eos/user/g/gritsan/Write/TaggedTrees/OffshellTemplateTrees20220923/nominal/cjlst/RunIILegacy/200205_CutBased/MC_2017/OffshellAC/gg/ggTo4mu_0PHf05ph0H125_MCFM701/ZZ4lAnalysis.root",
"/eos/user/g/gritsan/Write/TaggedTrees/OffshellTemplateTrees20220923/nominal/cjlst/RunIILegacy/200205_CutBased/MC_2017/OffshellAC/gg/ggTo4mu_0PL1H125Contin_MCFM701/ZZ4lAnalysis.root",
"/eos/user/g/gritsan/Write/TaggedTrees/OffshellTemplateTrees20220923/nominal/cjlst/RunIILegacy/200205_CutBased/MC_2017/OffshellAC/gg/ggTo4mu_0PL1H125_MCFM701/ZZ4lAnalysis.root",
"/eos/user/g/gritsan/Write/TaggedTrees/OffshellTemplateTrees20220923/nominal/cjlst/RunIILegacy/200205_CutBased/MC_2017/OffshellAC/gg/ggTo4mu_0PL1f05ph0H125Contin_MCFM701/ZZ4lAnalysis.root",
"/eos/user/g/gritsan/Write/TaggedTrees/OffshellTemplateTrees20220923/nominal/cjlst/RunIILegacy/200205_CutBased/MC_2017/OffshellAC/gg/ggTo4mu_0PL1f05ph0H125_MCFM701/ZZ4lAnalysis.root",
"/eos/user/g/gritsan/Write/TaggedTrees/OffshellTemplateTrees20220923/nominal/cjlst/RunIILegacy/200205_CutBased/MC_2017/OffshellAC/gg/ggTo4mu_0PMH125Contin_MCFM701/ZZ4lAnalysis.root",
"/eos/user/g/gritsan/Write/TaggedTrees/OffshellTemplateTrees20220923/nominal/cjlst/RunIILegacy/200205_CutBased/MC_2017/OffshellAC/gg/ggTo4mu_0PMH125_MCFM701/ZZ4lAnalysis.root",
"/eos/user/g/gritsan/Write/TaggedTrees/OffshellTemplateTrees20220923/nominal/cjlst/RunIILegacy/200205_CutBased/MC_2017/OffshellAC/gg/ggTo4mu_Contin_MCFM701/ZZ4lAnalysis.root",
"/eos/user/g/gritsan/Write/TaggedTrees/OffshellTemplateTrees20220923/nominal/cjlst/RunIILegacy/200205_CutBased/MC_2017/OffshellAC/gg/ggTo4tau_0PMH125_MCFM701/ZZ4lAnalysis.root"]


finname = files[ifile]

finname  = finname.split("/")

foutname = "/eos/user/g/gritsan/Write/LHCWG/gg/"+finname[-2]+"_"+finname[-1]


print foutname
os.system("root -l \'filterTree.C(\""+files[ifile]+"\",\""+foutname+"\")\'")


