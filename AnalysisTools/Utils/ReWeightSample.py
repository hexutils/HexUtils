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
    valid_pure = ["0+", "SM", "scalar", "0PM", "a1", "g1",
                 "a2", "0h+", "0PH", "g2",
                 "0-", "a3", "PS", "pseudoscalar", "0M", "g4",
                 "L1", "Lambda1", "0L1",
                 "L1Zg", "0L1Zg", "L1Zgs",
                 "g2Zg", "g2Zgs", "a2Zg", "ghzgs2", "0PHZg",
                 "g4Zg", "g4Zgs", "a3Zg", "ghzgs4", "0MZg",
                 "g2gg", "g2gsgs", "a2gg", "ghgsgs2", "0PHgg",
                 "g4gg", "g4gsgs", "a3gg", "ghgsgs4", "0Mgg"]
    valid_pure_perm = []
    valid_pure.extend(list(permutations(valid_pure, 2)))
    for vp in valid_pure:
      valid_pure_perm.append("".join(vp))
    valid = valid + tuple(valid_pure_perm) + mixturepermutations_4d(valid) + mixturepermutationsEFT(valid)
    
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
        elif ProductionMode in ("qqZZ", "TTZZ", "ZZZ", "WZZ", "WWZ", "TTWW", "TTZJets_M10_MLM", "TTZToLLNuNu_M10", "TTZToLL_M1to10_MLM", "EW","ew_bkg") + tuple(ggZZoffshellproductionmodes):
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
  parsed = False
  print("Hypothesis being parsed: ", Hypothesis)
  if "interf" in Hypothesis:
    print("Interference in hypotheses... stripping from string")
    Hypothesis = Hypothesis.split("-")[0]
  #============ Check if there is a single hypothesis ============#
  if Hypothesis in ("0+", "SM", "scalar", "0PM", "a1", "g1"):
    Coupling_Dict["ghz1"]=1 
    parsed = True
  elif Hypothesis in ("a2", "0h+", "0PH", "g2"):
    Coupling_Dict["ghz2"]=1
    parsed = True
  elif Hypothesis in ("0-", "a3", "PS", "pseudoscalar", "0M", "g4"):
    Coupling_Dict["ghz4"]=1
    parsed = True
  elif Hypothesis in ("L1", "Lambda1", "0L1"):
    Coupling_Dict["ghz1prime2"]=1
    parsed = True
  elif Hypothesis in ("L1Zg", "0L1Zg", "L1Zgs"):
    Coupling_Dict["ghza1prime2"]=1
    parsed = True
  elif Hypothesis in ("g2Zg", "g2Zgs", "a2Zg", "ghzgs2", "0PHZg"):
    Coupling_Dict["ghza2"]=1
    parsed = True
  elif Hypothesis in ("g4Zg", "g4Zgs", "a3Zg", "ghzgs4", "0MZg"):
    Coupling_Dict["ghza4"]=1
    parsed = True
  elif Hypothesis in ("g2gg", "g2gsgs", "a2gg", "ghgsgs2", "0PHgg"):
    Coupling_Dict["gha2"]=1
    parsed = True
  elif Hypothesis in ("g4gg", "g4gsgs", "a3gg", "ghgsgs4", "0Mgg"):
    Coupling_Dict["gha4"]=1
    parsed = True
  # ========= Check of there is a mixed hypothesis ============
  elif Hypothesis in ("fa20.5", "fa2dec0.5", "fa2+0.5", "fa2dec+0.5"):
    Coupling_Dict["ghz1"] = 1
    Coupling_Dict["ghz2"] = 1
    parsed = True
  elif Hypothesis in ("fa30.5", "fa3dec0.5", "fa3+0.5", "fa3dec+0.5"):
    Coupling_Dict["ghz1"] = 1
    Coupling_Dict["ghz4"] = 1
    parsed = True
  elif Hypothesis in ("fL10.5", "fL1dec0.5", "fL1+0.5", "fL1dec+0.5"):
    Coupling_Dict["ghz1"] = 1
    Coupling_Dict["ghz1prime2"] = 1
    parsed = True
  elif Hypothesis in ("fL1Zg0.5", "fL1Zgdec0.5", "fL1Zg+0.5", "fL1Zgdec+0.5"):
    Coupling_Dict["ghz1"] = 1
    Coupling_Dict["ghza1prime2"] = 1
    parsed = True
  elif Hypothesis in ("fa2Zg0.5", "fa2Zgdec0.5", "fa2Zg+0.5", "fa2dec+0.5"):
    Coupling_Dict["ghz1"] = 1
    Coupling_Dict["ghza2"] = 1
    parsed = True
  elif Hypothesis in ("fa2gg0.5", "fa2ggdec0.5", "fa2gg+0.5", "fa2ggdec+0.5"):
    Coupling_Dict["ghz1"] = 1
    Coupling_Dict["gha2"] = 1
    parsed = True
  elif Hypothesis in ("fa3Zg0.5", "fa3Zgdec0.5", "fa3Zg+0.5", "fa3Zgdec+0.5"):
    Coupling_Dict["ghz1"] = 1
    Coupling_Dict["ghza4"] = 1
    parsed = True
  elif Hypothesis in ("fa3gg0.5", "fa3ggdec0.5", "fa3gg+0.5", "fa3ggdec+0.5"):
    Coupling_Dict["ghz1"] = 1
    Coupling_Dict["gha4"] = 1
    parsed = True
  # ========== Sort out if the coupling is not mixed for fai ========= 
  if parsed == True:
    return Coupling_Dict
  elif parsed == False:
    if any(s in Hypothesis for s in ["0+", "SM", "scalar", "0PM", "a1", "g1"]):
      Coupling_Dict["ghz1"]=1 
    if any(s in Hypothesis for s in ["a2", "0h+", "0PH", "g2"]):
      Coupling_Dict["ghz2"]=1
    if any(s in Hypothesis for s in ["0-", "a3", "PS", "pseudoscalar", "0M", "g4"]):
      Coupling_Dict["ghz4"]=1
    if any(s in Hypothesis for s in ["L1Zg", "0L1Zg", "L1Zgs"]):
      Coupling_Dict["ghza1prime2"]=1
    if any(re.match("(^[^.]*)L1(?!Z)", Hypothesis) for s in ["L1", "Lambda1", "0L1"]):
      Coupling_Dict["ghz1prime2"]=1
    if any(s in Hypothesis for s in ["g2Zg", "g2Zgs", "a2Zg", "ghzgs2", "0PHZg"]):
      Coupling_Dict["ghza2"]=1
    if any(s in Hypothesis for s in ["g4Zg", "g4Zgs", "a3Zg", "ghzgs4", "0MZg"]):
      Coupling_Dict["ghza4"]=1
    if any(s in Hypothesis for s in ["g2gg", "g2gsgs", "a2gg", "ghgsgs2", "0PHgg"]):
      Coupling_Dict["gha2"]=1
    if any(s in Hypothesis for s in ["g4gg", "g4gsgs", "a3gg", "ghgsgs4", "0Mgg"]):
      Coupling_Dict["gha4"]=1
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

def ConvertKeyToEWKey(key):
  if key == 'ghz1':
    key = 'ghv1'
  elif key == 'ghz2':
    key = 'ghv2'
  elif key == 'ghz4':
    key = 'ghv4'
  elif key == 'ghz1prime2':
    key = 'ghv1prime2'
  return key

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
    elif ProductionMode in ('VBF'):
      for key in Coupling_Dict.keys():
        if Coupling_Dict[key] != 0:
          prodName.append('JJEW')
          couplname.append(ConvertKeyToEWKey(key))         
          value.append(CouplingValuesDict[key])
          Generator.append('MCFM')
    elif ProductionMode in ('WplusH','WminusH','WH','ZH','VH'):
      for key in Coupling_Dict.keys():
        if Coupling_Dict[key] != 0:
          prodName.append('JJEW')
          couplname.append(ConvertKeyToEWKey(key))         
          value.append(CouplingValuesDict[key])
          Generator.append('MCFM')
    elif ProductionMode in('bbH','ttH'):
      for key in Coupling_Dict.keys():
        if Coupling_Dict[key] != 0:
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

def Sort_Name_Order(List_of_Names):
  def user_sorter(x):
    if x == 'ghz1':
      return 1
    elif x == 'ghz2':
      return 2
    elif x == 'ghz4':
      return 3
    elif x == 'gha2':
      return 4
    elif x == 'gha4':
      return 5
    elif x == 'ghza2':
      return 6
    elif x == 'ghza4':
      return 7
    elif x == 'ghz1prime2':
      return 8
    elif x == 'ghza1prime2':
      return 9 
  return sorted(List_of_Names, key=user_sorter)

def GetMixedMelaConstants(Coupling_Dict,ProductionMode,isData):
  prodName=''
  couplname_plus_value=''
  Generator=''
  CouplingValuesDict=GetCouplingValues()
  MelaMixedConstants = []
  if not isData:
    if ProductionMode == 'ggH':
          prodName='GG'        
          Generator="MCFM"
    elif ProductionMode in ('VBF'):
          prodName = 'JJEW'
          Generator = 'MCFM'
    elif ProductionMode in ('WplusH','WminusH','ZH','VH'):
          prodName = 'JJEW'
          Generator = 'MCFM'
    elif ProductionMode in('bbH'):
          prodName = 'Dec'
          Generator = 'JHUGen'
    elif ProductionMode in('ttH'):
          prodName ='Dec'
          Generator = 'JHUGen'
  #====== Not Implemented Right Now ======
    elif ProductionMode == 'tH':
      return null
  # Sort all permutations of the non zero terms and assign strings #
  Non_Zero_Coupling_String = []
  for Coupling in Coupling_Dict.keys():
    if Coupling_Dict[Coupling] != 0:
        Non_Zero_Coupling_String.append(Coupling)
  Sorted_Names = Sort_Name_Order(Non_Zero_Coupling_String)
  #====== Make coupling names plus values string for 2 term interference =======#
  MELA_Name_String = ''
  for name in Sorted_Names:
    MELA_Name_String += name+"_"+CouplingValuesDict[name]+"_"
  if ProductionMode == 'ggH':
    couplname_plus_value+="kappaTopBot_1_"+MELA_Name_String
  elif ProductionMode in('VBF','WplusH','WminusH','ZH','VH'):
    couplname_plus_value+=MELA_Name_String
  elif ProductionMode in('bbH','ttH'):
    couplname_plus_value+=MELA_Name_String
  #====== Make the Strings to pull from the Trees ======#
  if ProductionMode in 'ggH':
    string = "p_Gen_"+prodName+"_SIG_"+couplname_plus_value+Generator
    MelaMixedConstants.append(string)
  elif ProductionMode in('VBF','WplusH','WminusH','ZH','VH'):
    string = "p_Gen_"+prodName+"_BSI_"+couplname_plus_value+Generator
    MelaMixedConstants.append(string)
  elif ProductionMode in('bbH','ttH'):
    string = "p_Gen_"+prodName+"_SIG_"+couplname_plus_value+Generator
    MelaMixedConstants.append(string)
  return MelaMixedConstants 

def GetIsoHVVCouplingName(IsoTemplateName):
  if "0PM" == IsoTemplateName:
    return "ghz1"
  if "0PH" == IsoTemplateName:
    return "ghz2"
  if "0M" == IsoTemplateName:
    return "ghz4"
  if "0L1Zg" == IsoTemplateName:
    return "ghza1prime2"
  if "0L1" == IsoTemplateName:
    return "ghz1prime2"
  if "0PHZg" == IsoTemplateName:
    return "ghza2"
  if "0MZg" == IsoTemplateName:
    return "ghza4"
  if "0PHgg" == IsoTemplateName:
    return "gha2"
  if "0Mgg" == IsoTemplateName:
    return "gha4"
  raise ValueError("Invalid Iso Template Name")

def GetIntFromTemplateName(IntTemplateName,ProductionMode,isData):
  CouplingDict={} #Stores Coupling Orders  
  CouplingValuesDict=GetCouplingValues()
  print("IntTemplate",IntTemplateName)
  #sort out order of each coupling#
  if re.search("(g1(?P<Order>[1234]))",IntTemplateName):
    CouplingDict["ghz1"] = re.search("(g1(?P<Order>[1234]))",IntTemplateName)["Order"]
  if re.search("(g2(?P<Order>[1234]))",IntTemplateName):
    CouplingDict["ghz2"] = re.search("(g2(?P<Order>[1234]))",IntTemplateName)["Order"]
  if re.search("(g4(?P<Order>[1234]))",IntTemplateName):
    CouplingDict["ghz4"] = re.search("(g4(?P<Order>[1234]))",IntTemplateName)["Order"]
  if re.search("(g1prime2(?P<Order>[1234]))",IntTemplateName):
    CouplingDict["ghz1prime2"] = re.search("(g1prime2(?P<Order>[1234]))",IntTemplateName)["Order"]
  if re.search("(ghzgs1prime2(?P<Order>[1234]))",IntTemplateName):
    CouplingDict["ghza1prime2"] = re.search("(ghzgs1prime2(?P<Order>[1234]))",IntTemplateName)["Order"]
  if re.search("(g2Zg(?P<Order>[1234]))",IntTemplateName):
    CouplingDict["ghza2"] = re.search("(g2Zg(?P<Order>[1234]))",IntTemplateName)["Order"]
  if re.search("(g4Zg(?P<Order>[1234]))",IntTemplateName):
    CouplingDict["ghza4"] = re.search("(g4Zg(?P<Order>[1234]))",IntTemplateName)["Order"]
  if re.search("(g2gg(?P<Order>[1234]))",IntTemplateName):
    CouplingDict["gha2"] = re.search("(g2gg(?P<Order>[1234]))",IntTemplateName)["Order"]
  if re.search("(g4gg(?P<Order>[1234]))",IntTemplateName):
    CouplingDict["gha4"] = re.search("(g4gg(?P<Order>[1234]))",IntTemplateName)["Order"]
  # See how to parse all of the orders #
  print("Parsed Coupling Dict",CouplingDict)
  SumOfOrders = sum(float(CouplingDict[Coupling]) for Coupling in CouplingDict)
  if SumOfOrders == 2:
    Pure_Couplings = []
    Mixed_Couplings = []
    for coupling in CouplingDict:
      # Need to get the pure Couplings 
      if 'gg' in ProductionMode:
        coupl_string = "kappaTopBot_1_"+coupling+"_"+CouplingValuesDict[coupling]
        Pure_Couplings.append("p_Gen_GG_SIG_"+coupl_string+"_MCFM")
    # We need to calculate mixed couplings
    sorted_couplings = Sort_Name_Order(CouplingDict.keys())
    coupl_string = "kappaTopBot_1_"
    for coupling in sorted_couplings:
      coupl_string += coupling+"_"+CouplingValuesDict[coupling]+"_"
    Mixed_Couplings.append("p_Gen_GG_SIG_"+coupl_string+"MCFM")
    # Now make the correct combination of coupling strings # 
    return Mixed_Couplings[0] +"-"+Pure_Couplings[0]+"-"+Pure_Couplings[1]
  elif SumOfOrders == 4: #Not Supported Yet
    raise ValueError("Not supported yet")
  raise ValueError("Invalid Iso Template Name")

def GetPureFromTemplateName(OutputHypothesis,ProductionMode,isData):
  IsoBranchName = ''
  prodName = ''
  coupl_string = ''
  coupling_name= GetIsoHVVCouplingName(OutputHypothesis)
  CouplingValuesDict=GetCouplingValues()
  if not isData:
    if 'gg' in ProductionMode:
      prodName = 'GG'
      coupl_string = 'kappaTopBot_1_'+coupling_name+"_"+CouplingValuesDict[coupling_name]
      Generator = "MCFM"
  return "p_Gen_"+prodName+"_SIG_"+coupl_string+"_"+Generator

# This function will interptret what the hypothesis means and what constants are needed #
def GetConstantsAndMELA(Hypothesis,ProductionMode,isData):
  MelaConstantNames={}
  Coupling_Dict = ParseHypothesis(Hypothesis)
  # This list of tuples will include the names of the branches needed to reweight the event #
  MelaConstantNames["Iso"]=(GetIsoMelaConstants(Coupling_Dict,ProductionMode,isData))
  MelaConstantNames["Mixed"]=(GetMixedMelaConstants(Coupling_Dict,ProductionMode,isData))
  return MelaConstantNames

def GetConstantsAndMELA_From_Template_Name(Template_Name,ProductionMode,isData):
  Branch_Names_String = ''  
  print("Template Names",Template_Name)
  Grouped = re.match("(?:(?P<Hffpure>0(?:PM|M)ff)_)?(?:(?P<HVVpure>0(?:PM|M|PH|L1|L1Zg|Mgg|PHgg|MZg|PHZg))|(?P<HVVint>(?:g(?:1|2|4|1prime2|hzgs1prime2|2gg|4gg|2Zg|4Zg)[1234])*))$",Template_Name)
  grouped_names = Grouped.groupdict()
  print("Grouped names", grouped_names)
  if (grouped_names["HVVpure"] != None):
    Branch_Names_String = GetPureFromTemplateName(grouped_names["HVVpure"],ProductionMode,isData)
  if (grouped_names["HVVint"] != None):
    Branch_Names_String = GetIntFromTemplateName(grouped_names["HVVint"],ProductionMode,isData)
  return Branch_Names_String

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

def Reweight_Branch_NoHff(InputTree,ProductionMode,OutputHypothesis,isData,Analysis_Config,lumi,year,DoInterf,DoMassFilter):
  # Check the input for Input Hypothesis and Output Hypothesis #
  print ("InputTree:",InputTree)
  print ("Production Mode:",ProductionMode)
  print ("OutHypothesis:",OutputHypothesis)
  # If the Prodution mode is bkg we do not incude any hypothesis because we do not reweight bkg 
  doMELA_Reweight = None
  if OutputHypothesis == "bkg":
    Check_Input(ProductionMode,None,None)
    doMELA_Reweight = False
  else:
    if any(prod in ProductionMode for prod in ['VBF','VH','ZH','WplusH','WminusH','bbH']):
      Check_Input(ProductionMode,OutputHypothesis,None)
    else:
      Check_Input(ProductionMode,OutputHypothesis,"Hff0+")
    doMELA_Reweight = True
  if doMELA_Reweight is None:
    raise ValueError('Choose MELA reweight option in reweight failed!')
  # After Checking the validity of request calulate the per event weight for the sample
  eventweight = []
  if Analysis_Config.ReweightProcess == "Calc_Event_Weight_2021_gammaH":
    if 'WH' in InputTree:
      eventweight = Calc_Tree_Weight_2021_gammaH(InputTree,"WH"+"_"+str(year),DoMassFilter)
    elif 'ZH' in InputTree:         
      eventweight = Calc_Tree_Weight_2021_gammaH(InputTree,"ZH"+"_"+str(year),DoMassFilter)
    else:
      eventweight = Calc_Tree_Weight_2021_gammaH(InputTree,ProductionMode+"_"+str(year),DoMassFilter)
  else:
    raise ValueError('Choose Valid Reweighting procedure in Analysis.Config') 
  # Get List of Hypothesis to Reweight By #
  if doMELA_Reweight:
    MelaConstantNames = GetConstantsAndMELA(OutputHypothesis,ProductionMode,isData)
    Branch_Names = ""
    #print("MELACONSTANTNAMES: ",MelaConstantNames)
    if DoInterf and len(MelaConstantNames["Mixed"]) != 0:
      for i in range(len(MelaConstantNames["Mixed"])):
        if i == 0:
          Branch_Names += MelaConstantNames["Mixed"][i]
        else:
          Branch_Names += "+"+MelaConstantNames["Mixed"][i]
      for i in range(len(MelaConstantNames["Iso"])):
          Branch_Names += "-"+MelaConstantNames["Iso"][i]  
      if any(prod in ProductionMode for prod in ['VBF','ZH','WplusH','WminusH','VH']):
          Branch_Names += "-p_Gen_JJEW_BKG_MCFM"
    elif DoInterf and len(MelaConstantNames["Mixed"]) == 0:
      raise ValueError('{} not valid mixed hypothesis'.format(OutputHypothesis))
    elif len(MelaConstantNames["Mixed"]) == 0: # If there are no Mixed Couplings add the single Isolated coupling
      Branch_Names += MelaConstantNames["Iso"][0]
    elif len(MelaConstantNames["Mixed"]) != 0: # If there are Mixed Couplings this means we reweight with the Mixed Coupling
      Branch_Names += MelaConstantNames["Mixed"][0]
    print(Branch_Names)
    return eventweight * tree2array(tree=InputTree,branches=[Branch_Names]).astype(float) * lumi
  if "ZX" in ProductionMode: 
    return np.array(eventweight) 
  else:
    return np.array(eventweight) * lumi 

def Reweight_Branch_NoHff_From_Template_Name(InputTree,template_name,isData,Analysis_Config,lumi,year,DoMassFilter):
  # Check the input for Input Hypothesis and Output Hypothesis #
  print ("InputTree:",InputTree)
  print ("Template:", template_name)
  # Sort out the production mode #
  ProductionMode = template_name
  OutputHypothesis = None
  Grouped = re.match("(?P<production>gg|tt|bb|qq|Z|W|V|gamma)H_(?:(?P<Hffpure>0(?:PM|M)ff)_)?(?:(?P<HVVpure>0(?:PM|M|PH|L1|L1Zg|Mgg|PHgg|MZg|PHZg))|(?P<HVVint>(?:g(?:1|2|4|1prime2|hzgs1prime2|2gg|4gg|2Zg|4Zg)[1234])*))$",template_name)
  if Grouped != None:
    grouped_names = Grouped.groupdict()
    ProductionMode = grouped_names["production"]+"H"
    if (grouped_names["HVVint"] != None):
      OutputHypothesis = grouped_names["HVVint"]
    if (grouped_names["HVVpure"] != None):
      OutputHypothesis = grouped_names["HVVpure"]
  elif "bkg" in template_name:
    OutputHypothesis = "bkg"
  elif "zjets" in template_name:
    OutputHypothesis = "bkg"
  else:
    raise ValueError("Invalid template name")
  print ("Production Mode:",ProductionMode)
  print ("OutHypothesis:",OutputHypothesis)
  # ================== #
  doMELA_Reweight = None
  if OutputHypothesis == "bkg":
    #Check_Input(ProductionMode,None,None)
    doMELA_Reweight = False
  else:
    #if any(prod in ProductionMode for prod in ['VBF','VH','ZH','WplusH','WminusH','bbH','gammaH']):
    #  Check_Input(ProductionMode,OutputHypothesis,None)
    #else:
    #  Check_Input(ProductionMode,OutputHypothesis,"Hff0+")
    doMELA_Reweight = True
  if doMELA_Reweight is None:
    raise ValueError('Choose MELA reweight option in reweight failed!')
  # After Checking the validity of request calulate the per event weight for the sample
  eventweight = []
  if Analysis_Config.ReweightProcess == "Calc_Event_Weight_2021_gammaH":
    if 'WH' in InputTree:
      eventweight = Calc_Tree_Weight_2021_gammaH(InputTree,"WH"+"_"+str(year),DoMassFilter)
    elif 'ZH' in InputTree:
      eventweight = Calc_Tree_Weight_2021_gammaH(InputTree,"ZH"+"_"+str(year),DoMassFilter)
    else:
      eventweight = Calc_Tree_Weight_2021_gammaH(InputTree,ProductionMode+"_"+str(year),DoMassFilter)
  else:
    raise ValueError('Choose Valid Reweighting procedure in Analysis.Config')
  # Get List of Hypothesis to Reweight By #
  if doMELA_Reweight:
    MelaConstantNames = GetConstantsAndMELA_From_Template_Name(OutputHypothesis,ProductionMode,isData)
    print(MelaConstantNames)
    return eventweight * tree2array(tree=InputTree,branches=[MelaConstantNames]).astype(float) * lumi
  if "zjets" in ProductionMode or "ZX" in ProductionMode:
    return np.array(eventweight)
  else:
    return np.array(eventweight) * lumi

