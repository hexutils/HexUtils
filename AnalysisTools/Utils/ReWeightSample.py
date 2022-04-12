import ROOT
from itertools import combinations, permutations
import re
from .Calc_Weight import *
from root_numpy import array2tree, tree2array

### Useful Functions to use with the main reweight samples function ###a

ggZZoffshellproductionmodes = "ggTo2e2mu_0MH125Contin_10GaSM_MCFM701 ggTo2e2mu_0MH125Contin_MCFM701 ggTo2e2mu_0MH125_MCFM701 ggTo2e2mu_0Mf05ph0H125Contin_10GaSM_MCFM701 ggTo2e2mu_0Mf05ph0H125Contin_MCFM701 ggTo2e2mu_0Mf05ph0H125_MCFM701 ggTo2e2mu_0PHH125Contin_10GaSM_MCFM701 ggTo2e2mu_0PHH125Contin_MCFM701 ggTo2e2mu_0PHH125_MCFM701 ggTo2e2mu_0PHf05ph0H125Contin_10GaSM_MCFM701 ggTo2e2mu_0PHf05ph0H125Contin_MCFM701 ggTo2e2mu_0PHf05ph0H125_MCFM701 ggTo2e2mu_0PL1H125Contin_10GaSM_MCFM701 ggTo2e2mu_0PL1H125Contin_MCFM701 ggTo2e2mu_0PL1H125_MCFM701 ggTo2e2mu_0PL1f05ph0H125Contin_10GaSM_MCFM701 ggTo2e2mu_0PL1f05ph0H125Contin_MCFM701 ggTo2e2mu_0PL1f05ph0H125_MCFM701 ggTo2e2mu_0PMH125Contin_10GaSM_MCFM701 ggTo2e2mu_0PMH125Contin_MCFM701 ggTo2e2mu_0PMH125_MCFM701 ggTo2e2mu_ContinDefaultShower_MCFM701 ggTo2e2mu_Contin_MCFM701 ggTo2e2tau_0MH125Contin_10GaSM_MCFM701 ggTo2e2tau_0MH125Contin_MCFM701 ggTo2e2tau_0MH125_MCFM701 ggTo2e2tau_0Mf05ph0H125Contin_10GaSM_MCFM701 ggTo2e2tau_0Mf05ph0H125Contin_MCFM701 ggTo2e2tau_0Mf05ph0H125_MCFM701 ggTo2e2tau_0PHH125Contin_10GaSM_MCFM701 ggTo2e2tau_0PHH125Contin_MCFM701 ggTo2e2tau_0PHH125_MCFM701 ggTo2e2tau_0PHf05ph0H125Contin_10GaSM_MCFM701 ggTo2e2tau_0PHf05ph0H125Contin_MCFM701 ggTo2e2tau_0PHf05ph0H125_MCFM701 ggTo2e2tau_0PL1H125Contin_10GaSM_MCFM701 ggTo2e2tau_0PL1H125Contin_MCFM701 ggTo2e2tau_0PL1H125_MCFM701 ggTo2e2tau_0PL1f05ph0H125Contin_10GaSM_MCFM701 ggTo2e2tau_0PL1f05ph0H125Contin_MCFM701 ggTo2e2tau_0PL1f05ph0H125_MCFM701 ggTo2e2tau_0PMH125Contin_10GaSM_MCFM701 ggTo2e2tau_0PMH125Contin_MCFM701 ggTo2e2tau_0PMH125_MCFM701 ggTo2e2tau_Contin_MCFM701 ggTo2mu2tau_0MH125Contin_10GaSM_MCFM701 ggTo2mu2tau_0MH125Contin_MCFM701 ggTo2mu2tau_0MH125_MCFM701 ggTo2mu2tau_0Mf05ph0H125Contin_10GaSM_MCFM701 ggTo2mu2tau_0Mf05ph0H125Contin_MCFM701 ggTo2mu2tau_0Mf05ph0H125_MCFM701 ggTo2mu2tau_0PHH125Contin_10GaSM_MCFM701 ggTo2mu2tau_0PHH125Contin_MCFM701 ggTo2mu2tau_0PHH125_MCFM701 ggTo2mu2tau_0PHf05ph0H125Contin_10GaSM_MCFM701 ggTo2mu2tau_0PHf05ph0H125Contin_MCFM701 ggTo2mu2tau_0PHf05ph0H125_MCFM701 ggTo2mu2tau_0PL1H125Contin_10GaSM_MCFM701 ggTo2mu2tau_0PL1H125Contin_MCFM701 ggTo2mu2tau_0PL1H125_MCFM701 ggTo2mu2tau_0PL1f05ph0H125Contin_10GaSM_MCFM701 ggTo2mu2tau_0PL1f05ph0H125Contin_MCFM701 ggTo2mu2tau_0PL1f05ph0H125_MCFM701 ggTo2mu2tau_0PMH125Contin_10GaSM_MCFM701 ggTo2mu2tau_0PMH125Contin_MCFM701 ggTo2mu2tau_0PMH125_MCFM701 ggTo2mu2tau_Contin_MCFM701 ggTo4e_0MH125Contin_10GaSM_MCFM701 ggTo4e_0MH125Contin_MCFM701 ggTo4e_0MH125_MCFM701 ggTo4e_0Mf05ph0H125Contin_10GaSM_MCFM701 ggTo4e_0Mf05ph0H125Contin_MCFM701 ggTo4e_0Mf05ph0H125_MCFM701 ggTo4e_0PHH125Contin_10GaSM_MCFM701 ggTo4e_0PHH125Contin_MCFM701 ggTo4e_0PHH125_MCFM701 ggTo4e_0PHf05ph0H125Contin_10GaSM_MCFM701 ggTo4e_0PHf05ph0H125Contin_MCFM701 ggTo4e_0PHf05ph0H125_MCFM701 ggTo4e_0PL1H125Contin_10GaSM_MCFM701 ggTo4e_0PL1H125Contin_MCFM701 ggTo4e_0PL1H125_MCFM701 ggTo4e_0PL1f05ph0H125Contin_10GaSM_MCFM701 ggTo4e_0PL1f05ph0H125Contin_MCFM701 ggTo4e_0PL1f05ph0H125_MCFM701 ggTo4e_0PMH125Contin_10GaSM_MCFM701 ggTo4e_0PMH125Contin_MCFM701 ggTo4e_0PMH125_MCFM701 ggTo4e_ContinDefaultShower_MCFM701 ggTo4e_Contin_MCFM701 ggTo4mu_0MH125Contin_10GaSM_MCFM701 ggTo4mu_0MH125Contin_MCFM701 ggTo4mu_0MH125_MCFM701 ggTo4mu_0Mf05ph0H125Contin_10GaSM_MCFM701 ggTo4mu_0Mf05ph0H125Contin_MCFM701 ggTo4mu_0Mf05ph0H125_MCFM701 ggTo4mu_0PHH125Contin_10GaSM_MCFM701 ggTo4mu_0PHH125Contin_MCFM701 ggTo4mu_0PHH125_MCFM701 ggTo4mu_0PHf05ph0H125Contin_10GaSM_MCFM701 ggTo4mu_0PHf05ph0H125Contin_MCFM701 ggTo4mu_0PHf05ph0H125_MCFM701 ggTo4mu_0PL1H125Contin_10GaSM_MCFM701 ggTo4mu_0PL1H125Contin_MCFM701 ggTo4mu_0PL1H125_MCFM701 ggTo4mu_0PL1f05ph0H125Contin_10GaSM_MCFM701 ggTo4mu_0PL1f05ph0H125Contin_MCFM701 ggTo4mu_0PL1f05ph0H125_MCFM701 ggTo4mu_0PMH125Contin_10GaSM_MCFM701 ggTo4mu_0PMH125Contin_MCFM701 ggTo4mu_0PMH125_MCFM701 ggTo4mu_ContinDefaultShower_MCFM701 ggTo4mu_Contin_MCFM701 ggTo4tau_0MH125Contin_10GaSM_MCFM701 ggTo4tau_0MH125Contin_MCFM701 ggTo4tau_0MH125_MCFM701 ggTo4tau_0Mf05ph0H125Contin_10GaSM_MCFM701 ggTo4tau_0Mf05ph0H125Contin_MCFM701 ggTo4tau_0Mf05ph0H125_MCFM701 ggTo4tau_0PHH125Contin_10GaSM_MCFM701 ggTo4tau_0PHH125Contin_MCFM701 ggTo4tau_0PHH125_MCFM701 ggTo4tau_0PHf05ph0H125Contin_10GaSM_MCFM701 ggTo4tau_0PHf05ph0H125Contin_MCFM701 ggTo4tau_0PHf05ph0H125_MCFM701 ggTo4tau_0PL1H125Contin_10GaSM_MCFM701 ggTo4tau_0PL1H125Contin_MCFM701 ggTo4tau_0PL1H125_MCFM701 ggTo4tau_0PL1f05ph0H125Contin_10GaSM_MCFM701 ggTo4tau_0PL1f05ph0H125Contin_MCFM701 ggTo4tau_0PL1f05ph0H125_MCFM701 ggTo4tau_0PMH125Contin_10GaSM_MCFM701 ggTo4tau_0PMH125Contin_MCFM701 ggTo4tau_0PMH125_MCFM701 ggTo4tau_Contin_MCFM701".split()

def mixturepermutations_4d(enumitemsalreadythere):
  def inner():
    pures = "a3", "a2", "L1", "L1Zg", "a3Zg", "a2Zg", "a3gg", "a2gg"

    #pure hypotheses
    yield "0+",
    for _ in pures:
      yield _,

    for proddec in "dec", "prod", "proddec":
      kwargs = {"proddec": proddec, "sign": "-" if proddec == "proddec" else ""}
      #mixtures with SM
      for kwargs["ai"] in pures:
        yield "f{ai}{proddec}{sign}0.5".format(**kwargs),
      #mixtures with each other
      for kwargs["ai"], kwargs["aj"] in combinations(pures, 2):
        yield (
          "f{ai}{proddec}0.5f{aj}{proddec}{sign}0.5".format(**kwargs),
          "f{aj}{proddec}{sign}0.5f{ai}{proddec}0.5".format(**kwargs),
        )

      if proddec == "dec": yield None, "decay is done"

      #to get the terms with 3 unique couplings:
      #  there are 3 different new terms for each set of 3 couplings,
      #  since exactly one of the couplings is squared
      #  so we need 3 more mixtures
      #  prod, dec, proddec (with a minus sign somewhere for variety) will work
      for kwargs["ai"], kwargs["aj"] in combinations(pures, 2):
        yield (
          "f{ai}{proddec}0.33f{aj}{proddec}{sign}0.33".format(**kwargs),
          "f{aj}{proddec}{sign}0.33f{ai}{proddec}0.33".format(**kwargs),
        )

      for kwargs["ai"], kwargs["aj"], kwargs["ak"] in combinations(pures, 3):
        yield tuple(
          "".join(permutation).format(**kwargs)
            for permutation
            in permutations(("f{ai}{proddec}0.33", "f{aj}{proddec}0.33", "f{ak}{proddec}{sign}0.33"))
        )

    #for each set of 4 couplings, there's only one possible new term
    #proddec is the way to go, since it includes both
    #I'll keep it general using combinations, just in case that ever becomes necessary
    #it's not clear that a minus sign would help, so I'll leave it out
    kwargs = {}
    for kwargs["ai"], kwargs["aj"], kwargs["ak"] in combinations(pures, 3):
      yield tuple(
        "".join(permutation).format(**kwargs)
          for permutation
          in permutations(("f{ai}proddec0.25", "f{aj}proddec0.25", "f{ak}proddec0.25"))
      )
    for kwargs["ai"], kwargs["aj"], kwargs["ak"], kwargs["al"] in combinations(pures, 4):
      yield tuple(
        "".join(permutation).format(**kwargs)
          for permutation
          in permutations(("f{ai}proddec0.25", "f{aj}proddec0.25", "f{ak}proddec0.25", "f{al}proddec0.25"))
      )

  result = []
  allofthem = 0
  for enumitemnames in inner():
    if enumitemnames == (None, "decay is done"):
      assert allofthem == len(list(combinations(range(10), 2))), (allofthem, len(list(combinations(range(10), 2))))
      continue

    allofthem += 1
    enumitemnames_modified = [_ for _ in enumitemnames]
    enumitemnames_modified += [re.sub("(?<!prod)dec", "", _) for _ in enumitemnames_modified]
    if any(_ in enumitemsalreadythere for _ in enumitemnames_modified):
      continue
    result.append(enumitemnames_modified)

  assert allofthem == len(list(combinations(range(12), 4))), (allofthem, len(list(combinations(range(12), 4))))
  return tuple(result)

def mixturepermutationsEFT(enumitemsalreadythere):
  def inner():
    pures = "a3EFT", "a2EFT", "L1EFT"

    #pure hypotheses
    yield "0+",
    for _ in pures:
      yield _,

    for proddec in "dec", "prod", "proddec":
      kwargs = {"proddec": proddec, "sign": "-" if proddec == "proddec" else ""}
      #mixtures with SM
      for kwargs["ai"] in pures:
        yield "f{ai}{proddec}{sign}0.5".format(**kwargs),
      #mixtures with each other
      for kwargs["ai"], kwargs["aj"] in combinations(pures, 2):
        yield (
          "f{ai}{proddec}0.5f{aj}{proddec}{sign}0.5".format(**kwargs),
          "f{aj}{proddec}{sign}0.5f{ai}{proddec}0.5".format(**kwargs),
        )

      if proddec == "dec": yield None, "decay is done"

      #to get the terms with 3 unique couplings:
      #  there are 3 different new terms for each set of 3 couplings,
      #  since exactly one of the couplings is squared
      #  so we need 3 more mixtures
      #  prod, dec, proddec (with a minus sign somewhere for variety) will work
      for kwargs["ai"], kwargs["aj"] in combinations(pures, 2):
        yield (
          "f{ai}{proddec}0.33f{aj}{proddec}{sign}0.33".format(**kwargs),
          "f{aj}{proddec}{sign}0.33f{ai}{proddec}0.33".format(**kwargs),
        )

      for kwargs["ai"], kwargs["aj"], kwargs["ak"] in combinations(pures, 3):
        yield tuple(
          "".join(permutation).format(**kwargs)
            for permutation
            in permutations(("f{ai}{proddec}0.33", "f{aj}{proddec}0.33", "f{ak}{proddec}{sign}0.33"))
        )

    #for each set of 4 couplings, there's only one possible new term
    #proddec is the way to go, since it includes both
    #I'll keep it general using combinations, just in case that ever becomes necessary
    #it's not clear that a minus sign would help, so I'll leave it out
    kwargs = {}
    for kwargs["ai"], kwargs["aj"], kwargs["ak"] in combinations(pures, 3):
      yield tuple(
        "".join(permutation).format(**kwargs)
          for permutation
          in permutations(("f{ai}proddec0.25", "f{aj}proddec0.25", "f{ak}proddec0.25"))
      )
    for kwargs["ai"], kwargs["aj"], kwargs["ak"], kwargs["al"] in combinations(pures, 4):
      yield tuple(
        "".join(permutation).format(**kwargs)
          for permutation
          in permutations(("f{ai}proddec0.25", "f{aj}proddec0.25", "f{ak}proddec0.25", "f{al}proddec0.25"))
      )

  result = []
  allofthem = 0
  for enumitemnames in inner():
    if enumitemnames == (None, "decay is done"):
      assert allofthem == len(list(combinations(range(5), 2))), (allofthem, len(list(combinations(range(5), 2))))
      continue

    allofthem += 1
    enumitemnames_modified = [_ for _ in enumitemnames]
    enumitemnames_modified += [re.sub("(?<!prod)dec", "", _) for _ in enumitemnames_modified]
    if any(_ in enumitemsalreadythere for _ in enumitemnames_modified):
      continue
    result.append(enumitemnames_modified)

  assert allofthem == len(list(combinations(range(7), 4))), (allofthem, len(list(combinations(range(7), 4))))
  return tuple(result)

def Valid_Hypothesis(hypothesis):
    valid = (    "0+", "SM", "scalar", "0PM", "a1", "g1",
                 "a2", "0h+", "0PH", "g2",
                 "0-", "a3", "PS", "pseudoscalar", "0M", "g4",
                 "L1", "Lambda1", "0L1",
                 "L1Zg", "0L1Zg", "L1Zgs",
                 "fa20.5", "fa2dec0.5", "fa2+0.5", "fa2dec+0.5",
                 "fa30.5", "fa3dec0.5", "fa3+0.5", "fa3dec+0.5",
                 "fL10.5", "fL1dec0.5", "fL1+0.5", "fL1dec+0.5",
                 "fL1Zg0.5", "fL1Zgdec0.5", "fL1Zg+0.5", "fL1Zgdec+0.5",
                 "fa2prod0.5", "fa2prod+0.5",
                 "fa3prod0.5", "fa3prod+0.5",
                 "fL1prod0.5", "fL1prod+0.5",
                 "fL1Zgprod0.5", "fL1Zgprod+0.5",
                 "fa2proddec0.5", "fa2proddec+0.5",
                 "fa3proddec0.5", "fa3proddec+0.5",
                 "fL1proddec0.5", "fL1proddec+0.5",
                 "fL1Zgproddec0.5", "fL1Zgproddec+0.5",
                 "fa2dec-0.5", "fa2-0.5",
                 "fa3dec-0.5", "fa3-0.5",
                 "fL1dec-0.5", "fL1-0.5",
                 "fL1Zgdec-0.5", "fL1Zg-0.5",
                 "fa2prod-0.5",
                 "fa3prod-0.5",
                 "fL1prod-0.5",
                 "fL1Zgprod-0.5",
                 "fa2proddec-0.5",
                 "fa3proddec-0.5",
                 "fL1proddec-0.5",
                 "fL1Zgproddec-0.5",
                 "fa2dec-0.9", "fa2-0.9",
                 "fa2VBF0.5", "fa2VBF+0.5",
                 "fa3VBF0.5", "fa3VBF+0.5",
                 "fL1VBF0.5", "fL1VBF+0.5",
                 "fa2VH0.5", "fa2VH+0.5",
                 "fa3VH0.5", "fa3VH+0.5",
                 "fL1VH0.5", "fL1VH+0.5",
                 "BestFit19009",
                 "g2Zg", "g2Zgs", "a2Zg", "ghzgs2", "0PHZg",
                 "g4Zg", "g4Zgs", "a3Zg", "ghzgs4", "0MZg",
                 "g2gg", "g2gsgs", "a2gg", "ghgsgs2", "0PHgg",
                 "g4gg", "g4gsgs", "a3gg", "ghgsgs4", "0Mgg",
                 "fg2Zg0.5", "fa2Zg0.5", "fg2Zgdec0.5", "fa2Zgdec0.5",
                 "fg4Zg0.5", "fa3Zg0.5", "fg4Zgdec0.5", "fa3Zgdec0.5",
                 "fg2gg0.5", "fa2gg0.5", "fg2ggdec0.5", "fa2ggdec0.5",
                 "fg4gg0.5", "fa3gg0.5", "fg4ggdec0.5", "fa3ggdec0.5",
                 "fg2Zg-0.5", "fa2Zg-0.5", "fg2Zgdec-0.5", "fa2Zgdec-0.5",
                 "fg4Zg-0.5", "fa3Zg-0.5", "fg4Zgdec-0.5", "fa3Zgdec-0.5",
                 "fg2gg-0.5", "fa2gg-0.5", "fg2ggdec-0.5", "fa2ggdec-0.5",
                 "fg4gg-0.5", "fa3gg-0.5", "fg4ggdec-0.5", "fa3ggdec-0.5",
                 "fg2Zgprod0.5", "fa2Zgprod0.5",
                 "fg4Zgprod0.5", "fa3Zgprod0.5",
                 "fg2ggprod0.5", "fa2ggprod0.5",
                 "fg4ggprod0.5", "fa3ggprod0.5",
                 "fg2Zgprod-0.5", "fa2Zgprod-0.5",
                 "fg4Zgprod-0.5", "fa3Zgprod-0.5",
                 "fg2ggprod-0.5", "fa2ggprod-0.5",
                 "fg4ggprod-0.5", "fa3ggprod-0.5",
                 "fg2Zgproddec0.5", "fa2Zgproddec0.5",
                 "fg4Zgproddec0.5", "fa3Zgproddec0.5",
                 "fg2ggproddec0.5", "fa2ggproddec0.5",
                 "fg4ggproddec0.5", "fa3ggproddec0.5",
                 "fg2Zgproddec-0.5", "fa2Zgproddec-0.5",
                 "fg4Zgproddec-0.5", "fa3Zgproddec-0.5",
                 "fg2ggproddec-0.5", "fa2ggproddec-0.5",
                 "fg4ggproddec-0.5", "fa3ggproddec-0.5",
                )
    valid = valid + mixturepermutations_4d(valid) + mixturepermutationsEFT(valid)
    if hypothesis in valid:
      return True
    return False

def Check_Input(ProductionMode,Hypothesis,HffHypothesis):
        if ProductionMode is None:
            raise ValueError("No option provided for productionmode")
        elif ProductionMode in ("ggH", "VBF", "ZH", "WH", "WplusH", "WminusH", "ttH", "bbH", "tqH", "VH"):
            if Hypothesis is None:
                raise ValueError("No hypothesis provided for {} productionmode\n{}".format(ProductionMode))
            if not Valid_Hypothesis(Hypothesis):
                raise ValueError("{} hypothesis can't be {}\n{}".format(ProductionMode, Hypothesis))
            if ProductionMode in ("ggH", "ttH", "tqH"):
                if HffHypothesis is None:
                    if ProductionMode == "ggH":
                        HffHypothesis = HffHypothesis("Hff0+")
                    else:
                        raise ValueError("Hff hypothesis not provided for {} productionmode\n{}".format(ProductionMode))
                if ProductionMode == "tqH" and HffHypothesis != "Hff0+":
                    raise ValueError("Bad hffhypothesis {} for {} productionmode\n{}".format(HffHypothesis, ProductionMode))
            else:
                if HffHypothesis is not None:
                    raise ValueError("Hff hypothesis provided for {} productionmode\n".format(ProductionMode))
        elif ProductionMode in ("ggZZ", "VBF_bkg"):
            if Hypothesis is not None:
                raise ValueError("Hypothesis provided for {} productionmode\n".format(ProductionMode))
            if HffHypothesis is not None:
                raise ValueError("Hff hypothesis provided for {} productionmode\n".format(ProductionMode))
        elif ProductionMode in ("qqZZ", "TTZZ", "ZZZ", "WZZ", "WWZ", "TTWW", "TTZJets_M10_MLM", "TTZToLLNuNu_M10", "TTZToLL_M1to10_MLM", "EW") + tuple(ggZZoffshellproductionmodes):
            if Hypothesis is not None:
                raise ValueError("Hypothesis provided for {} productionmode\n".format(ProductionMode))
            if HffHypothesis is not None:
                raise ValueError("Hff hypothesis provided for {} productionmode\n".format(ProductionMode))
        elif ProductionMode in ("ZX", "data"):
            if Hypothesis is not None:
                raise ValueError("Hypothesis provided for {} productionmode\n".format(ProductionMode))
            if HffHypothesis is not None:
                raise ValueError("Hff hypothesis provided for {} productionmode\n".format(ProductionMode))
        else:
            raise ValueError("Bad productionmode {}\n{}".format(ProductionMode))

# This function will parse the couplings from the Hypothesis and return them separately #
def ParseHypothesis(Hypothesis):
  Coupling_Dict = dict({'ghz1': 0, 'ghz2': 0, 'ghz4': 0, 'ghz1prime2': 0, 'ghza1prime2': 0, 'ghza2': 0, 'ghza4': 0, 'gha2': 0, 'gha4': 0})
  print("Hypothesis being parsed: ",Hypothesis)
  if "interf" in Hypothesis:
    print("Interference in hypotheses... stripping from string")
    Hypothesis = Hypothesis.split("-")[0]
  #============ Check if there is a single hypothesis ============#
  if Hypothesis in ("0+", "SM", "scalar", "0PM", "a1", "g1"):
    Coupling_Dict["ghz1"]=1 
  elif Hypothesis in ("a2", "0h+", "0PH", "g2"):
    Coupling_Dict["ghz2"]=1
  elif Hypothesis in ("0-", "a3", "PS", "pseudoscalar", "0M", "g4"):
    Coupling_Dict["ghz4"]=1
  elif Hypothesis in ("L1", "Lambda1", "0L1"):
    Coupling_Dict["ghz1prime2"]=1
  elif Hypothesis in ("L1Zg", "0L1Zg", "L1Zgs"):
    Coupling_Dict["ghza1prime2"]=1
  elif Hypothesis in ("g2Zg", "g2Zgs", "a2Zg", "ghzgs2", "0PHZg"):
    Coupling_Dict["ghza2"]=1
  elif Hypothesis in ("g4Zg", "g4Zgs", "a3Zg", "ghzgs4", "0MZg"):
    Coupling_Dict["ghza4"]=1
  elif Hypothesis in ("g2gg", "g2gsgs", "a2gg", "ghgsgs2", "0PHgg"):
    Coupling_Dict["gha2"]=1
  elif Hypothesis in ("g4gg", "g4gsgs", "a3gg", "ghgsgs4", "0Mgg"):
    Coupling_Dict["gha4"]=1
  # ========= Check of there is a mixed hypothesis ============
  elif Hypothesis in ("fa20.5", "fa2dec0.5", "fa2+0.5", "fa2dec+0.5"):
    Coupling_Dict["ghz1"] = 1
    Coupling_Dict["ghz2"] = 1
  elif Hypothesis in ("fa30.5", "fa3dec0.5", "fa3+0.5", "fa3dec+0.5"):
    Coupling_Dict["ghz1"] = 1
    Coupling_Dict["ghz4"] = 1
  elif Hypothesis in ("fL10.5", "fL1dec0.5", "fL1+0.5", "fL1dec+0.5"):
    Coupling_Dict["ghz1"] = 1
    Coupling_Dict["ghz1prime2"] = 1
  elif Hypothesis in ("fL1Zg0.5", "fL1Zgdec0.5", "fL1Zg+0.5", "fL1Zgdec+0.5"):
    Coupling_Dict["ghz1"] = 1
    Coupling_Dict["ghza1prime2"] = 1
  elif Hypothesis in ("fa2Zg0.5", "fa2Zgdec0.5", "fa2Zg+0.5", "fa2dec+0.5"):
    Coupling_Dict["ghz1"] = 1
    Coupling_Dict["ghza2"] = 1
  elif Hypothesis in ("fa2gg0.5", "fa2ggdec0.5", "fa2gg+0.5", "fa2ggdec+0.5"):
    Coupling_Dict["ghz1"] = 1
    Coupling_Dict["gha2"] = 1
  elif Hypothesis in ("fa3Zg0.5", "fa3Zgdec0.5", "fa3Zg+0.5", "fa3Zgdec+0.5"):
    Coupling_Dict["ghz1"] = 1
    Coupling_Dict["ghza4"] = 1
  elif Hypothesis in ("fa3gg0.5", "fa3ggdec0.5", "fa3gg+0.5", "fa3ggdec+0.5"):
    Coupling_Dict["ghz1"] = 1
    Coupling_Dict["gha4"] = 1
  return Coupling_Dict

def CheckIsIso(Coupling_Dict):
  iso = False
  for key in Coupling_Dict.keys():
    if Coupling_Dict[key] != 0 and iso == False:
      iso = True
    elif Coupling_Dict[key] != 0:
      return False
  return True

def GetCouplingValues():
  CouplingValuesDict=dict({'ghz1': '1', 'ghz2': '1', 'ghz4': '1', 'ghz1prime2': '1E4', 'ghza1prime2': '1E4', 'ghza2': '1', 'ghza4': '1', 'gha2': '1', 'gha4': '1'})
  return CouplingValuesDict

def GetIsoMelaConstants(Coupling_Dict,ProductionMode,isData):
  prodName=[]
  couplname=[]
  value=[]
  Generator=[]
  CouplingValuesDict=GetCouplingValues()
  MelaIsoConstants = []
  if not isData:
    if ProductionMode == 'ggH':
      for key in Coupling_Dict.keys():
        if Coupling_Dict[key] != 0:
          prodName.append('GG')
          couplname.append('kappaTopBot_1_'+key)         
          value.append(CouplingValuesDict[key])
          Generator.append("MCFM")
    elif ProductionMode in ('VBF','WplusH','WminusH','ZH'):
      for key in Coupling_Dict.keys():
          prodName.append('JJEW')
          couplname.append(key)         
          value.append(CouplingValuesDict[key])
          Generator.append('MCFM')
    elif ProductionMode in('bbH','ttH'):
      for key in Coupling_Dict.keys():
          prodName.append('Dec')
          couplname.append(key)
          value.append(CouplingValuesDict[key])
          Generator.append('JHUGen')
  #====== Not Implemented Right Now ======
    elif ProductionMode == 'tqH':
      return null
  #====== Make the Strings to pull from the Trees ======#
  for i in range(len(prodName)):
    string = "p_Gen_"+prodName[i]+"_SIG_"+couplname[i]+"_"+value[i]+"_"+Generator[i]
    MelaIsoConstants.append(string)
  return MelaIsoConstants 

def GetMixedMelaConstants(Coupling_Dict,ProductionMode,isData):
  prodName=[]
  couplname_plus_value=[]
  Generator=[]
  CouplingValuesDict=GetCouplingValues()
  MelaMixedConstants = []
  if not isData:
    if ProductionMode == 'ggH':
          prodName.append('GG')        
          Generator.append("MCFM")
    elif ProductionMode in ('VBF','WplusH','WminusH','ZH'):
          prodName.append('JJEW')
          Generator.append('MCFM')
    elif ProductionMode in('bbH','ttH'):
          prodName.append('Dec')
          Generator.append('JHUGen')
  #====== Not Implemented Right Now ======
    elif ProductionMode == 'tqH':
      return null
  # Sort all permutations of the non zero terms and assign strings #
  Non_Zero_Coupling_String = []
  for Coupling in Coupling_Dict.keys():
    if Coupling_Dict[Coupling] != 0:
      Non_Zero_Coupling_String.append(Coupling)
  Mixed_Combos = list(combinations(Non_Zero_Coupling_String, 2))
  #====== Make coupling names plus values string =======#
  for combo in Mixed_Combos:
    name_1 = combo[0]
    name_2 = combo[1]
    first = 0
    second = 1
    if "ghz1" in name_1 and not "prime" in name_1:
      first = 0
      second = 1
    else:
      first = 1
      second = 0
    if ProductionMode == 'ggH':
      couplname_plus_value.append("kappaTopBot_1_"+name_1+"_"+CouplingValuesDict[name_1]+"_"+name_2+"_"+CouplingValuesDict[name_2])
    else:
      couplname_plus_value.append(name_1+"_"+CouplingValuesDict[name_1]+"_"+name_2+"_"+CouplingValuesDict[name_2])


  #====== Make the Strings to pull from the Trees ======#
  for i in range(len(couplname_plus_value)):
    string = "p_Gen_"+prodName[i]+"_SIG_"+couplname_plus_value[i]+"_"+Generator[i]
    MelaMixedConstants.append(string)
  return MelaMixedConstants 

# This function will interptret what the hypothesis means and what constants are needed #
def GetConstantsAndMELA(Hypothesis,ProductionMode,isData):
  MelaConstantNames={}
  Coupling_Dict = ParseHypothesis(Hypothesis)
  # This list of tuples will include the names of the branches needed to reweight the event # 
  MelaConstantNames["Iso"]=(GetIsoMelaConstants(Coupling_Dict,ProductionMode,isData))
  MelaConstantNames["Mixed"]=(GetMixedMelaConstants(Coupling_Dict,ProductionMode,isData))
  return MelaConstantNames

def Reweight_Event(InputEvent,ProductionMode,InputHypothesis,OutputHypothesis,HffHypothesis,isData,Analysis_Config,lumi,year):
  # Check the input for Input Hypothesis and Output Hypothesis #
  Check_Input(ProductionMode,InputHypothesis,HffHypothesis)
  Check_Input(ProductionMode,OutputHypothesis,HffHypothesis)
  # Get List of Hypothesis to Reweight By #
  MelaConstantNames = GetConstantsAndMELA(OutputHypothesis,ProductionMode,isData)
  # Calculate the weight to reweight by #
  namespace = {'MELA_Weight': 1.,'InputEvent':InputEvent,'MelaConstantNames':MelaConstantNames}
  for i in range(len(MelaConstantNames)):
    exec("MELA_Weight = MELA_Weight * InputEvent."+MelaConstantNames[i],namespace)
  # Get the Nominal event weight #
  eventweight = 1
  if Analysis_Config.ReweightProcess == "Calc_Event_Weight_2021_gammaH": 
    eventweight = Calc_Event_Weight_2021_gammaH(InputEvent,InputHypothesis+"_"+str(year))
  return eventweight * namespace['MELA_Weight'] * lumi

### This function returns an array of the new event weights ### 
def Reweight_Branch(InputTree,ProductionMode,OutputHypothesis,HffHypothesis,isData,Analysis_Config,lumi,year):
  # Check the input for Input Hypothesis and Output Hypothesis #
  Check_Input(ProductionMode,OutputHypothesis,HffHypothesis)
  # Get List of Hypothesis to Reweight By #
  MelaConstantNames = GetConstantsAndMELA(OutputHypothesis,ProductionMode,isData)
  Branch_Names = ""
  if len(MelaConstantNames) == 1:
    Branch_Names += MelaConstantNames[0]
  # Note that there is no option right now to support reweighting to non isolated hypothesis
  # Get the Nominal event weight #
  eventweight = 1
  if Analysis_Config.ReweightProcess == "Calc_Event_Weight_2021_gammaH": 
    eventweight = Calc_Tree_Weight_2021_gammaH(InputTree,ProductionMode+"_"+str(year))
  return eventweight * tree2array(tree=InputTree,branches=[Branch_Names]).astype(float) *lumi

def Reweight_Branch_NoHff(InputTree,ProductionMode,OutputHypothesis,isData,Analysis_Config,lumi,year,DoInterf):
  # Check the input for Input Hypothesis and Output Hypothesis #
  print (ProductionMode,OutputHypothesis)
  # If the Prodution mode is bkg we do not incude any hypothesis because we do not reweight bkg 
  doMELA_Reweight = None
  if OutputHypothesis == "bkg":
    Check_Input(ProductionMode,None,None)
    doMELA_Reweight = False
  else:
    Check_Input(ProductionMode,OutputHypothesis,"Hff0+")
    doMELA_Reweight = True
  if doMELA_Reweight is None:
    raise ValueError('Choose MELA reweight opiton in reweight failed!')
  # After Checking the validity of request calulate the per event weight for the sample
  eventweight = []
  if Analysis_Config.ReweightProcess == "Calc_Event_Weight_2021_gammaH":
    eventweight = Calc_Tree_Weight_2021_gammaH(InputTree,ProductionMode+"_"+str(year))
  else:
    raise ValueError('Choose Valid Reweighting procedure in Analysis.Config') 
  # Get List of Hypothesis to Reweight By #
  if doMELA_Reweight:
    MelaConstantNames = GetConstantsAndMELA(OutputHypothesis,ProductionMode,isData)
    Branch_Names = ""
    if DoInterf and len(MelaConstantNames["Mixed"]) != 0:
      for i in range(len(MelaConstantNames["Mixed"])):
        if i == 0:
          Branch_Names += MelaConstantNames["Mixed"][i]
        else:
          Branch_Names += "+"+MelaConstantNames["Mixed"][i]
      for i in range(len(MelaConstantNames["Iso"])):
          Branch_Names += "-"+MelaConstantNames["Iso"][i]  
    elif DoInterf and len(MelaConstantNames["Mixed"]) == 0:
      raise ValueError('{} not valid mixed hypothesis'.format(OutputHypothesis))
    elif len(MelaConstantNames["Mixed"]) == 0: # If there are no Mixed Couplings add the single Isolated coupling
      Branch_Names += MelaConstantNames["Iso"][0]
    elif len(MelaConstantNames["Mixed"]) != 0: # If there are Mixed Couplings this means we reweight with the Mixed Coupling
      Branch_Names += MelaConstantNames["Mixed"][0]
    # Note that there is no option right now to support reweighting to non isolated hypothesis
    return eventweight * tree2array(tree=InputTree,branches=[Branch_Names]).astype(float) * lumi
  else:
    return eventweight 
