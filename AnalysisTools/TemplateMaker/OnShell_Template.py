import ROOT 
import array
import itertools
import pandas as pd
import numpy as np
import re
import pickle
from root_numpy import array2tree, tree2array
from ..Utils.ReWeightSample import Reweight_Branch, Reweight_Branch_NoHff, ParseHypothesis, CheckIsIso, Reweight_Branch_NoHff_From_Template_Name
from ..Utils.HexMath import weightedaverage, kspoissongaussian
from collections import Counter

def IsInterf(Hypothesis):
  IsInterf = False
  temp_hypothesis = Hypothesis
  if "interf" in Hypothesis:
    IsInterf = True
    temp_hypothesis = Hypothesis.split("-")[0]
  return IsInterf, temp_hypothesis

def Parse_Tagged_Mode(Tag,Analysis_Config):
  # Get the Categorization from Analysis Config #
  Categorization = Analysis_Config.TaggingProcess
  print (Tag,Categorization)
  cat_num = -999
  # Parse the Categorization and return  the number for the tag #
  if Categorization in("Tag_AC_19_Scheme_2"):
    if Tag == "Untagged":
      cat_num =  0
    elif Tag == "VBF1jTagged":
      cat_num =  1
    elif Tag == "VBF2jTagged":
      cat_num =  2
    elif Tag == "VHLeptTagged": 
      cat_num =  3
    elif Tag == "VHHadrTagged":
      cat_num =  4
    elif Tag == "ttHLeptTagged": 
      cat_num =  5
    elif Tag == "ttHHadrTagged":
      cat_num =  6
    elif Tag == "VHMETTagged":
      cat_num =  7
    elif Tag == "Boosted":
      cat_num =  8  
  elif Categorization in("Tag_Untagged_and_gammaH"):
    if Tag == "Untagged":
      cat_num =  0
    elif Tag == "gammaH":
      cat_num = 9
  try:
    cat_num != -999 
  except ValueError:
    print("Please select valid Tagged Mode!")

  return cat_num 

def Parse_Final_States(fs): 
  # Return the absolute value of |Z1Flav * Z2Flav|
  if fs == '4l':
    return False, null 
  elif fs == '2e2mu':
    return True, 11*11*13*13
  elif fs == '4mu':
    return True, 13*13*13*13
  elif fs == '4e':
    return True, 11*11*11*11
  else:
    raise ValueError("Please select a valid final state")

def Sort_Coupling_Order(couplings):
  #print("Here",couplings)
  def user_sorter(x):
    if x == 'g1':
      return 1
    elif x == 'g2':
      return 2
    elif x == 'g4':
      return 3
    elif x == 'g2gg':
      return 4
    elif x == 'g4gg':
      return 5
    elif x == 'g2Zg':
      return 6
    elif x == 'g4Zg':
      return 7
    elif x == 'g1prime2':
      return 8
    elif x == 'ghzgs1prime2':
      return 9
  return sorted(couplings, key=user_sorter)

def Filter_SMAC_Only(Template_Names):
  filtered_names = []
  for name in Template_Names:
    Grouped = re.match("(?P<production>gg|tt|bb|qq|Z|W|V|gamma)H_(?:(?P<Hffpure>0(?:PM|M)ff)_)?(?:(?P<HVVpure>0(?:PM|M|PH|L1|L1Zg|Mgg|PHgg|MZg|PHZg))|(?P<HVVint>(?:g(?:1|2|4|1prime2|hzgs1prime2|2gg|4gg|2Zg|4Zg)[1234])*))$",name)
    if Grouped != None:
      print("Matched",Grouped.groups())
      grouped_dict = Grouped.groupdict()
      if (grouped_dict["HVVint"] != None):
        Interf_String=grouped_dict["HVVint"]
        print("Int",name)
        if re.match("(g11g(?:1|2|4|1prime2|hzgs1prime2|2gg|4gg|2Zg|4Zg)[1])*$",Interf_String) or re.match("(g12g(?:1|2|4|1prime2|hzgs1prime2|2gg|4gg|2Zg|4Zg)[2])*$",Interf_String):
          filtered_names.append(name)
      if (grouped_dict["HVVpure"] != None):
        filtered_names.append(name)
  print("filtered",filtered_names)
  return filtered_names

def Filter_HZZ_Only(Template_Names):
  filtered_names = []
  for name in Template_Names:
    Grouped = re.match("(?P<production>gg|tt|bb|qq|Z|W|V|gamma)H_(?:(?P<Hffpure>0(?:PM|M)ff)_)?(?:(?P<HVVpure>0(?:PM|M|PH|L1|L1Zg|Mgg|PHgg|MZg|PHZg))|(?P<HVVint>(?:g(?:1|2|4|1prime2|hzgs1prime2|2gg|4gg|2Zg|4Zg)[1234])*))$",name)
    if Grouped != None:
      grouped_dict = Grouped.groupdict()
      if (grouped_dict["HVVint"] != None):
        Interf_String=grouped_dict["HVVint"]
        if (re.match("(?P<HVVint>(?:g(?:1|2|4|1prime2|hzgs1prime2)[1234])*)$",Interf_String)) and not (re.match("(?P<HVVint>(?:g(?:2gg|4gg|2Zg|4Zg)[1234])*)$",Interf_String)):
          filtered_names.append(name)
      if (grouped_dict["HVVpure"] != None):
        if (re.search("(?P<HVVpure>0(?:PM|M|PH|L1|L1Zg)*)$",name)):
          filtered_names.append(name)
  print("HZZ Filtered",filtered_names)
  return filtered_names

def Filter_Photons_Only(Template_Names):
  filtered_names = []
  for name in Template_Names:
    Grouped = re.match("(?P<production>gg|tt|bb|qq|Z|W|V|gamma)H_(?:(?P<Hffpure>0(?:PM|M)ff)_)?(?:(?P<HVVpure>0(?:PM|M|PH|L1|L1Zg|Mgg|PHgg|MZg|PHZg))|(?P<HVVint>(?:g(?:1|2|4|1prime2|hzgs1prime2|2gg|4gg|2Zg|4Zg)[1234])*))$",name)
    if Grouped != None:
      grouped_dict = Grouped.groupdict()
      if (grouped_dict["HVVint"] != None):
        Interf_String=grouped_dict["HVVint"]
        if not (re.match("(?P<HVVint>(?:g(?:2|4|1prime2|hzgs1prime2)[1234])*)$",Interf_String)) and (re.match("(?P<HVVint>(?:g(?:1|2gg|4gg|2Zg|4Zg)[1234])*)$",Interf_String)):
          filtered_names.append(name)
      if (grouped_dict["HVVpure"] != None):
        if not (re.search("(?P<HVVpure>0(?:M|PH|L1|L1Zg)*)$",name)):
          filtered_names.append(name)
  print("Photon Filtered",filtered_names)
  return filtered_names

def Convert_Hypothesis_And_Prodution_Mode_To_Template_Name(hypothesis_list,prod):
  Name_List = []
  Options = hypothesis_list["Options"]
  couplings = hypothesis_list["Hypothesis"]
  production_mode = prod
  #print("Here",production_mode)
  if ('ggH' in production_mode):
    production_mode = 'ggH'
  elif ('VBF' in production_mode):
    production_mode = 'qqH'
  elif any(prod in production_mode for prod in ['ZH','WH','Wplus','Wminus','VH']):
    production_mode = 'VH'
  elif any(prod in production_mode for prod in ['tqH','tWH','ttH']):
    production_mode = 'ttH'
  elif ('bbH' in production_mode):
    production_mode = 'bbH'
  elif("ggZZ" in production_mode): 
    Name_List.append("bkg_ggzz")
    return Name_List
  elif("qqZZ" in production_mode):
    Name_List.append("bkg_qqzz")
    return Name_List
  elif("ew_bkg" in production_mode):
    Name_List.append("bkg_ew")
    return Name_List
  elif("ZX" in production_mode):
    Name_List.append("bkg_zjets")
    return Name_List
  
  if production_mode in ['ggH']:
    All_Combinations = [p for p in itertools.product(couplings, repeat=2)]
    for combo in All_Combinations:
      counted = Counter(combo)
      #print(combo)
      coupling_names = []
      for key in counted.keys():
        coupling_names.append(key)
      sorted_names = Sort_Coupling_Order(coupling_names)
      temp_str = production_mode+"_"
      for name in sorted_names:
        if counted[name] == 2: # Sort out the pure samples 
          if name == "g1":
            temp_str+="0PM"
          elif name == "g2":
            temp_str+="0PH"
          elif name == "g4":
            temp_str+="0M"
          elif name == "g1prime2":
            temp_str+="0L1"
          elif name == "ghzgs1prime2":
            temp_str+="0L1Zg"
          elif name == "g2gg":
            temp_str+="0PHgg"
          elif name == "g4gg":
            temp_str+="0Mgg"
          elif name == "g2Zg":
            temp_str+="0PHZg"
          elif name == "g4Zg":
            temp_str+="0MZg"
        else:
          temp_str += name+str(counted[name])
      Name_List.append(temp_str)
  elif production_mode in ['gammaH']:
    All_Combinations = [p for p in itertools.product(couplings, repeat=4)]
    for combo in All_Combinations:
      counted = Counter(combo)
      coupling_names = []
      for key in counted.keys():
        coupling_names.append(key)
      sorted_names = Sort_Coupling_Order(coupling_names)
      temp_str = production_mode+"_"
      for name in sorted_names:
        if counted[name] == 4: # Sort out the pure samples 
          if name == "g1":
            temp_str+="0PM"
          elif name == "g2":
            temp_str+="0PH"
          elif name == "g2":
            temp_str+="0M"
          elif name == "g1prime2":
            temp_str+="0L1"
          elif name == "ghzgs1prime2":
            temp_str+="0L1Zg"
          elif name == "g2gg":
            temp_str+="0PHgg"
          elif name == "g4gg":
            temp_str+="0Mgg"
          elif name == "g2zg":
            temp_str+="0PHZg"
          elif name == "g4zg":
            temp_Str+="0MZg"
          else:
            temp_str += name+str(counted[name])
      Name_List.append(temp_str)
  print("Here SM",Name_List)
  if "SM+AC_Only" in Options:
    Name_List = Filter_SMAC_Only(Name_List)
  if "HZZ_Only" in Options:
    Name_List = Filter_HZZ_Only(Name_List)
  if "Photons_Only" in Options:
    Name_List = Filter_Photons_Only(Name_List)
  return Name_List

def Convert_Hypothesis_And_Prodution_Mode(hypothesis,production_mode): #This function takes as input a given hypothesis and returns the correct naming convention for the combine physics model

  # establish naming convention for production mode#
  if ('ggH' in production_mode):
    production_mode = 'ggH'
  elif ('VBF' in production_mode):
    production_mode = 'qqH'
  elif any(prod in production_mode for prod in ['ZH','WH','Wplus','Wminus','VH']):
    production_mode = 'VH'
  elif any(prod in production_mode for prod in ['tqH','tWH','ttH']):
    production_mode = 'ttH'
  elif ('bbH' in production_mode):
    production_mode = 'bbH'
  elif("ggZZ" in production_mode):
    return "bkg_ggzz"
  elif("qqZZ" in production_mode):
    return "bkg_qqzz"
  elif("ew_bkg" in production_mode):
    return "bkg_ew"
  elif("ZX" in production_mode):
    return "bkg_zjets"
  Coupling_Dict = ParseHypothesis(hypothesis) # Needed to parse out the naming conventions
  if CheckIsIso(Coupling_Dict):
    if Coupling_Dict["ghz1"] != 0:
      return production_mode+"_"+"0PM"
    elif Coupling_Dict["ghz2"] != 0:
      return production_mode+"_"+"0PH"
    elif Coupling_Dict["ghz4"] != 0:
      return production_mode+"_"+"0M"
    elif Coupling_Dict["ghz1prime2"] != 0:
      return production_mode+"_"+"0L1"
    elif Coupling_Dict["ghza1prime2"] != 0:
      return production_mode+"_"+"0L1Zg"
    elif Coupling_Dict["ghza2"] != 0:
      return production_mode+"_"+"0PHZg"
    elif Coupling_Dict["ghza4"] != 0:
      return production_mode+"_"+"0MZg"
    elif Coupling_Dict["gha2"] != 0:
      return production_mode+"_"+"0PHgg"
    elif Coupling_Dict["gha4"] != 0:
      return production_mode+"_"+"0Mgg"
  else:
    if any(prod in production_mode for prod in ['ggH',"qqH","VH","bbH"]):
      coupling_string = ''
      for key in Coupling_Dict.keys():
        if Coupling_Dict[key] != 0:
          if key == "ghz1":
            coupling_string += 'g11'
          elif key == "ghz2":
            coupling_string += 'g21'
          elif key == "ghz4" != 0:
            coupling_string += 'g41'
          elif key == "ghz1prime2":
            coupling_string += 'g1prime21'
          elif key == "ghza1prime2" != 0:
            coupling_string += 'ghzgs1prime21'
          elif key == "ghza2":
            coupling_string += 'g2za1'
          elif key == "ghza4":
            coupling_string += 'g4za1'
          elif key == "gha2":
            coupling_string += 'g2gg1'
          elif key == "gha4":
            coupling_string += 'g4gg1'
    if any(prod in production_mode for prod in ['gammaH']):
      coupling_string = ''
      for key in Coupling_Dict.keys():
        if Coupling_Dict[key] != 0:
          if key == "ghz1":
            coupling_string += 'g11'
          elif key == "ghz2":
            coupling_string += 'g21'
          elif key == "ghz4" != 0:
            coupling_string += 'g41'
          elif key == "ghz1prime2":
            coupling_string += 'g1prime21'
          elif key == "ghza1prime2" != 0:
            coupling_string += 'ghzgs1prime21'
          elif key == "ghza2":
            coupling_string += 'g2za1'
          elif key == "ghza4":
            coupling_string += 'g4za1'
          elif key == "gha2":
            coupling_string += 'g2gg1'
          elif key == "gha4":
            coupling_string += 'g4gg1'
    elif production_mode == 'ttH': #Need to include Hff couplings???#
      coupling_string = ''
      for key in Coupling_Dict.keys():
        if Coupling_Dict[key] != 0:
          print(key)
          if key == "ghz1":
            coupling_string += 'g11'
          elif key == "ghz2":
            coupling_string += 'g21'
          elif key == "ghz4" != 0:
            coupling_string += 'g41'
          elif key == "ghz1prime2":
            coupling_string += 'g1prime21'
          elif key == "ghza1prime2" != 0:
            coupling_string += 'ghzgs1prime21'
          elif key == "ghza2":
            coupling_string += 'g2za1'
          elif key == "ghza4":
            coupling_string += 'g4za1'
          elif key == "gha2":
            coupling_string += 'g2gg1'
          elif key == "gha4":
            coupling_string += 'g4gg1'
  return production_mode + "_" + coupling_string

def Trim_Dict(d,keys):
  n = d.copy()
  for key in keys:
    del n[key]
  return n

def Get_Bin_Num(value,bin_edges):
  for i in range(1, len(bin_edges)):
    if bin_edges[i-1] <= value <= bin_edges[i]:
      #print(bin_edges)
      #print(bin_edges[i])
      return i 
  #print(value)
  return 0 

def Convert_Tuple_To_Bin(Tuples,Discriminants):
  # Input should be a tuple of the discriminant values
  # And the Discrminant Names with binning 
  # Make sure that the length of the tuple is the number of input discriminants 

  New_Tuples = []
  for t in Tuples:
    tup_list = list(t)
    index = 0
    for key in Discriminants.keys():
      bin_edges = Discriminants[key]
      tup_list[index] = Get_Bin_Num(t[index],bin_edges)
      #if tup_list[index] < 1:
      #  print(key)
      index += 1
    New_Tuples.append(tuple(tup_list))

  return New_Tuples

def Get_Z_Value(Discriminant_Values,Discriminants):
  # Input should be 2 dictionaries with keys of the names of the discriminants
  # The expected binning is with integer bins (0,1,2,3,4 etc) and the length must equal the 
  # number of bins for each discriminants multiplied together
  # Once the bin index is decided assign a value between the two bin edges and return that value for the Z_Value
   # each iteration is assigned an integer bin number. Then we return the bin number - .5 
  Binning_Num = []
  for key in Discriminants.keys():
    Binning_Num.append(list(range(1, len(Discriminants[key]))))
  Tuples_Of_Bin_Num = list(itertools.product(*Binning_Num))
  df = pd.DataFrame.from_dict(Discriminant_Values)
  # Convert the input Discriminats values to a Tuple of Values

  Tuple_Of_Discriminant_Values=list(df.itertuples(index=False, name=None))  
  Binned_Tuples = Convert_Tuple_To_Bin(Tuple_Of_Discriminant_Values,Discriminants)
  Index_Of_Match=[]
  # Sort through the new tuples to return a list of bins for each event 
  for tup in Binned_Tuples:
    try:
      Index_Of_Match.append(Tuples_Of_Bin_Num.index(tup))
    except ValueError:
      Index_Of_Match.append(-999)
  # Add .5 to ach index to push into the correct bin
  Index_Of_Match = [i + .5 for i in Index_Of_Match]
  return Index_Of_Match

def Calculate_Average_And_Unc_From_Template_Bins(val,err):
  # Expects a list of values and error from a set of n histograms
  # We need to take the weighted average while also protecting against weird bin values/low statistics
  # first step is to remove values with 0 and save them separatley
  temp_val = []
  temp_err = []
  temp_zeros_val = []
  temp_zeros_err = []
  maxerr = max(err)
  for i in range(len(val)): # Only apply outlier procedure to non zero values
    if val[i] != 0 and err[i] != 0:
      temp_val.append(val[i])
      temp_err.append(err[i])
    else:
      temp_zeros_val.append(val[i])
      temp_zeros_err.append(maxerr)
  val = temp_val
  err = temp_err
  #print("Start: ",val,err)
  #if len(val) == 0:
  #  return 0,0
  # Protect against all zeros 
  if all(entries == 0 for entries in val):
    return 0,0
  #for i in range(len(val)): # Loop over all bins check if bin is empty
  #  if err[i] == 0: 
  #    err[i] = max(err)
  maxerrorratio, errortoset = max((err[x]/val[x],err[x]) for x in range(len(err)) if err[x] !=0)
  for i in range(len(val)):
    if err[i] == 0:
      err[i] = errortoset
  for i in range(len(val)):
    errortoset = None
    for j in range(len(val)): # Check if a bin is an outlier:
      if err[j] <= err[i]: continue
      if err[j] == 0: continue 
      relative_error_1 = err[i]/val[i]
      relative_error_2 = err[j]/val[j]
      #print("Relative Error",relative_error_1,relative_error_2)
      if val[i] == 0 or relative_error_2 <= relative_error_1 * ((1 + 1.5 * np.log10(err[j]/err[i]) * kspoissongaussian(1/relative_error_1**2))):
        #print ("here")
        if errortoset is None: errortoset = 0 
        errortoset = max(errortoset, err[j])
    if errortoset is not None:
      err[i] = errortoset
  #print("End: ",val,err)
  #combine the values and the values that were set aside earlier
  val = val + temp_zeros_val 
  err = err + temp_zeros_err
  return weightedaverage(val,err)

def GetBinOptimalDiscriminant1D(Discriminant_Values,Optimal_Discriminants,dct):
  # Find the bin number and then shift by 0.5 to make sure the 
  #value returned is between the 
  Bin_Value = []
  for i in range(len(Discriminant_Values[list(Discriminant_Values.keys())[0]])):
    Bin_Per_Discriminant = []
    for name in Optimal_Discriminants.keys():
      if name in Discriminant_Values:
        Bin_Per_Discriminant.append(Get_Bin_Num(Discriminant_Values[name][i],Optimal_Discriminants[name]))
    ns = {"temp_bin_num":None,"dct":dct}
    str_exec = "temp_bin_num = dct["
    for j in range(len(Bin_Per_Discriminant)):
      if j != len(Bin_Per_Discriminant) - 1:
        str_exec += str(Bin_Per_Discriminant[j]) +","
      else:
        str_exec += str(Bin_Per_Discriminant[j]) +"]"
    try:
      exec(str_exec,ns)
    except:
      raise ValueError("Failed to get bin if optimal discriminant")
    Bin_Value.append(ns["temp_bin_num"] + 0.5)
  return Bin_Value

def GetBinOptimalDiscriminantND(Discriminant_Values,Discriminants,Optimal_Discriminants,nbins,dct):
  # The expected input is a list of all discriminants not used on x or y axis
  Bin_Value = []
  # Make Binning for Optimal_Discriminants
  Optimal_Bin_Edges = []
  for i in range(nbins + 1):
    Optimal_Bin_Edges.append(i)
  Optimal_Value = GetBinOptimalDiscriminant1D(Discriminant_Values,Optimal_Discriminants,dct) # Value to put optimal bin in correct position
  Combined_Discriminant_Values = {}
  Combined_Discriminant_Bins = {}
  for name in Discriminant_Values.keys():
    if name not in Optimal_Discriminants:
      Combined_Discriminant_Values[name] = Discriminant_Values[name]
      Combined_Discriminant_Bins[name] = Discriminants[name]
  Combined_Discriminant_Values["optimal"] = Optimal_Value
  Combined_Discriminant_Bins["optimal"] = Optimal_Bin_Edges
  Bin_Value = Get_Z_Value(Combined_Discriminant_Values,Combined_Discriminant_Bins)
  return Bin_Value

def FillHistOnShellNoSyst(targetprod,targetcateg,hlist,yeardict,Analysis_Config,year,final_state):
  # This should take an empty h_list and then fill with the templates 
  # target production will return which ever production that will be used to make the template ex (ggH,VBF etc) 
  # targetcateg is which tagged category is used to make the template 
  # h_list is an input dictionary 
  # year dict has paths and years attatched to each samples
  # year is an array of years to use#

  # First We nee to parse the input category which tells us exactly which discriminants are needed #
  category = Parse_Tagged_Mode(targetcateg,Analysis_Config)
  print("Category ",category)
  UseOptimal = False
  if category == 0: #Untagged 
    if Analysis_Config.UseOptimal["Untagged"]==True:
      Discriminants_Optimal = Analysis_Config.Optimal_Discriminants_Untagged
      UseOptimal = True
    Discriminants = Analysis_Config.Untagged_Discriminants
  elif category == 1: #VBF1jTagged
    if Analysis_Config.UseOptimal["VBF1jTagged"]==True:
      Discriminants_Optimal = Analysis_Config.Optimal_Discriminants_VBF1jTagged
      UseOptimal = True
    Discriminants = Analysis_Config.VBF1jTagged_Discriminants
  elif category == 2: #VBF2jTagged
    if Analysis_Config.UseOptimal["VBF2jTagged"]==True:
      Discriminants_Optimal = Analysis_Config.Optimal_Discriminants_VBF2jTagged
      UseOptimal = True
    Discriminants = Analysis_Config.VBF2jTagged_Discriminants
  elif category == 3: #VHLeptTagged
    if Analysis_Config.UseOptimal["VHLeptTagged"]==True:
      Discriminants_Optimal = Analysis_Config.Optimal_Discriminants_VHLeptTagged
      UseOptimal = True
    Discriminants = Analysis_Config.VHLeptTagged_Discriminants
  elif category == 4: #VHHadrTagged
    if Analysis_Config.UseOptimal["VHHadrTagged"]==True:
      Discriminants_Optimal = Analysis_Config.Optimal_Discriminants_VHHadrTagged
      UseOptimal = True
    Discriminants = Analysis_Config.VHHadrTagged_Discriminants
  elif category == 5: #ttHLeptTagged
    if Analysis_Config.UseOptimal["ttHLeptTagged"]==True:
      Discriminants_Optimal = Analysis_Config.Optimal_Discriminants_ttHLeptTagged
      UseOptimal = True
    Discriminants = Analysis_Config.ttHLeptTagged_Discriminants
  elif category == 6: #ttHHadrTagged
    if Analysis_Config.UseOptimal["ttHHadrTagged"]==True:
      Discriminants_Optimal = Analysis_Config.Optimal_Discriminants_ttHHadrTagged
      UseOptimal = True
    Discriminants = Analysis_Config.ttHHadrTagged_Discriminants
  elif category == 7: #VHMETTagged
    if Analysis_Config.UseOptimal["VHMETTagged"]==True:
      Discriminants_Optimal = Analysis_Config.Optimal_Discriminants_VHMETTagged
      UseOptimal = True
    Discriminants = Analysis_Config.VHMETTagged_Discriminants
  elif category == 8: #Boosted
    if Analysis_Config.UseOptimal["Boosted"]==True:
      Discriminants_Optimal = Analysis_Config.Optimal_Discriminants_Boosted
      UseOptimal = True
    Discriminants = Analysis_Config.Boosted_Discriminants
  elif category == 9: #gammaH
    if Analysis_Config.UseOptimal["gammaH"]==True:
      Discriminants_Optimal = Analysis_Config.Optimal_Discriminants_gammaH
      UseOptimal = True
    Discriminants = Analysis_Config.gammaH_Discriminants
  else:
    print("No category found")
  
  if "Data" not in targetprod: # Need for input to get the new weights
    isData = False
  else:
    isData = True

  Trees_Dict = yeardict[year] # Returns dictionary of all the samples for a given year
  Samples_To_Reweight = Trees_Dict[targetprod] #Returns the list of all samples of a given production mode 
  if len(Samples_To_Reweight) == 1:
    Samples_To_Reweight = Samples_To_Reweight[0] 
  lumi = Analysis_Config.lumi[year]
  Coupling_Name = Analysis_Config.Coupling_Name # Returns name of couplings used for analysis (what do we need to reweight to?)  
  Output_Name = "templates_"+str(targetprod)+"_"+str(targetcateg)+"_"+Coupling_Name+"_"+final_state+"_"+Analysis_Config.TreeFile+"_"+year+".root" #NEED to fix decay mode#
  Hypothesis_List = Analysis_Config.Hypothesis_List # Returns a list of all the hyptothesis to reweight to 
  Template_Names = Convert_Hypothesis_And_Prodution_Mode_To_Template_Name(Hypothesis_List,targetprod)
  DoMassFilter = Analysis_Config.DoMassFilter
  #Parse the final state to filter at the end#
  filter_final_state, final_state = Parse_Final_States(final_state)

  print("Samples To Reweight",Samples_To_Reweight)
  # Added a catch to check if the production mode is background #
  # Then this sets the Hypothesis List to only include SM #
  if any(x in targetprod for x in ["ggZZ","qqZZ","ew_bkg","ZX"]):
    Hypothesis_List = ["bkg"]  

  #Get name of discriminants and save them to a list of strings#
  D_Name=[]
  for key in Discriminants.keys():
    D_Name.append(key)

  Discriminant_Values = {}
  for name in D_Name:
    Discriminant_Values[name] = []
  
  # This part here will check if we need to use optimal discriminants for a given 
  # Category, we need to if each optimal observable is 
  if UseOptimal == True:  
    # This sorts which discriminant is optimal or not
    D_Name_NotOptimal = []
    D_Name_Optimal = []
    for name in D_Name: 
      if(name in Discriminants) and (name in Discriminants_Optimal):
        D_Name_Optimal.append(name)
      else:
        D_Name_NotOptimal.append(name)
    optpkl = Discriminants_Optimal["Path_To_Pickle"] 
    nbins = Discriminants_Optimal["nbins"] 
    print(optpkl)
    with open(optpkl, "rb") as f:
     binning = sorted(pickle.load(f)[-nbins], key=lambda x: min(x))
     dct = {bin: i for i, bins in enumerate(binning) for bin in bins}
    # Sort if we make a 1D,2D,or 3D histogram 
    if len(D_Name_NotOptimal) == 0:
      nx = Discriminants_Optimal["nbins"]
      xbins = []  
      for i in range(nx):
        xbins.append(i)

      Histogram_Dict = {} # Initialize the Dictionary for Histograms (Each histogram is for the AC Hypothesis you want)
      for name in Template_Names:
        Histogram_Dict[name] = ROOT.TH2F(name,name,nx,xbins,ny,ybins) # Initialize the Histogram Dictionary with with each AC hypothesis you need
        
      for tn in Template_Names: # Choose which hypothesis to reweight to
        Temporary_Histogram_List = [] # store the reweighted histogram for each sample in Samples to Reweight
        for sample in Samples_To_Reweight: # Loop over all samples with input production mode
          f = ROOT.TFile(sample, 'READ')
          t = f.Get("eventTree") # This name could change but overall processed CJLST trees for this analysis should have eventTree as the name
          New_Weights = Reweight_Branch_NoHff_From_Template_Name(t,tn,isData,Analysis_Config,lumi,year,DoMassFilter) # Returns New Weights for each event
          for Discriminant in D_Name:
            Discriminant_Values[Discriminant] = tree2array(tree=t,branches=[Discriminant]).astype(float);
          # Fill the histogram with the Discriminants for each template #
          Tag = tree2array(tree=t,branches=["EventTag"]).astype(int); # Need to know what category each event falls into
          Z1Flav = tree2array(tree=t,branches=["Z1Flav"]).astype(int); # Need to know flavor of Z1
          Z2Flav = tree2array(tree=t,branches=["Z2Flav"]).astype(int); # Need to know flavor of Z2
          # Make the temporary histogram for this specific sample input
          Temp_Hist = ROOT.TH1F(sample,sample,nx,xbins)
          Temp_Hist.Sumw2(True)
          xbin = GetBinOptimalDiscriminant1D(Discriminant_Values,Optimal_Discriminants,dct)
          #print("Category:",category)
          for i in range(len(New_Weights)):
            if Tag[i] == category:
              if filter_final_state:
                if abs(Z1Flav[i] * Z2Flav[i]) == final_state:
                  Temp_Hist.Fill(xbin[i],New_Weights[i])
              else:
                Temp_Hist.Fill(xbin[i],New_Weights[i])
          Temporary_Histogram_List.append(Temp_Hist)
          print("Saving :",Temp_Hist.GetName(),Temp_Hist.Integral())
        # Apply the logic for filling the combined histogram #
        # Loop over each bin and calculate the weighted average of each bin #
        for x in range(1,nx+1):
            binval=[] # list of bin values
            binerr=[] # list of error on each bin
            for hist in Temporary_Histogram_List:
              binval.append(hist.GetBinContent(x))
              binerr.append(hist.GetBinError(x))
            if "bkg" in Hypothesis_List:
              val = sum(binval)
              err = sum(i*i for i in binerr)
            else:
              val, err = Calculate_Average_And_Unc_From_Template_Bins(binval,binerr)
            Histogram_Dict[tn].SetBinContent(x,val)
            Histogram_Dict[tn].SetBinError(x,err)
        print("Saving :",Histogram_Dict[tn].GetName(),Histogram_Dict[tn].Integral())
      # Make the Output File and return the output #
      for hist in Histogram_Dict.keys():
        hlist.append(Histogram_Dict[hist])
      return Output_Name

    elif len(D_Name_NotOptimal) == 1:
      nx = len(Discriminants[D_Name_NotOptimal[0]])
      xbins = array.array('d',Discriminants[D_Name_NotOptimal[0]])
      ny = Discriminants_Optimal["nbins"]
      for i in range(ny):
        ybins.append(i)
      Histogram_Dict = {} # Initialize the Dictionary for Histograms (Each histogram is for the AC Hypothesis you want)
      for name in Template_Names:
        Histogram_Dict[name] = ROOT.TH2F(name,name,nx,xbins,ny,ybins) # Initialize the Histogram Dictionary with with each AC hypothesis you need

      for tn in Template_Names: # Choose which hypothesis to reweight to
        Temporary_Histogram_List = [] # store the reweighted histogram for each sample in Samples to Reweight
        for sample in Samples_To_Reweight: # Loop over all samples with input production mode
          f = ROOT.TFile(sample, 'READ')
          t = f.Get("eventTree") # This name could change but overall processed CJLST trees for this analysis should have eventTree as the name
          New_Weights = Reweight_Branch_NoHff_From_Template_Name(t,tn,isData,Analysis_Config,lumi,year,DoMassFilter) # Returns New Weights for each event
          for Discriminant in D_Name:
            Discriminant_Values[Discriminant] = tree2array(tree=t,branches=[Discriminant]).astype(float);
          # Fill the histogram with the Discriminants for each template #
          Tag = tree2array(tree=t,branches=["EventTag"]).astype(int); # Need to know what category each event falls into
          Z1Flav = tree2array(tree=t,branches=["Z1Flav"]).astype(int); # Need to know flavor of Z1
          Z2Flav = tree2array(tree=t,branches=["Z2Flav"]).astype(int); # Need to know flavor of Z2
          # Make the temporary histogram for this specific sample input
          Temp_Hist = ROOT.TH1F(sample,sample,nx,xbins)
          Temp_Hist.Sumw2(True)
          ybin = GetBinOptimalDiscriminant1D(Discriminant_Values,Discriminants_Optimal,dct)
          #print("Category:",category)
          for i in range(len(New_Weights)):
            if Tag[i] == category:
              if filter_final_state:
                if abs(Z1Flav[i] * Z2Flav[i]) == final_state:
                  Temp_Hist.Fill(Discriminant_Values[D_Name_NotOptimal[0]][i],ybin[i],New_Weights[i])
              else:
                Temp_Hist.Fill(Discriminant_Values[D_Name_NotOptimal[0]][i],ybin[i],New_Weights[i])
          Temporary_Histogram_List.append(Temp_Hist)
          print("Saving :",Temp_Hist.GetName(),Temp_Hist.Integral())
        # Apply the logic for filling the combined histogram #
        # Loop over each bin and calculate the weighted average of each bin #
        for x in range(1,nx+1):
          for y in range(1,ny+1):
            binval=[] # list of bin values
            binerr=[] # list of error on each bin
            for hist in Temporary_Histogram_List:
              binval.append(hist.GetBinContent(x,y))
              binerr.append(hist.GetBinError(x,y))
            if "bkg" in Hypothesis_List:
              val = sum(binval)
              err = sum(i*i for i in binerr)
            else:
              val, err = Calculate_Average_And_Unc_From_Template_Bins(binval,binerr)
            Histogram_Dict[tn].SetBinContent(x,y,val)
            Histogram_Dict[tn].SetBinError(x,y,err)
        print("Saving :",Histogram_Dict[tn].GetName(),Histogram_Dict[tn].Integral())
      # Make the Output File and return the output #
      for hist in Histogram_Dict.keys():
        hlist.append(Histogram_Dict[hist])
      return Output_Name


    elif len(D_Name_NotOptimal) >= 2:
      nx = len(Discriminants[D_Name_NotOptimal[0]])-1
      ny = len(Discriminants[D_Name_NotOptimal[1]])-1
      nz = None
      xbins = array.array('d',Discriminants[D_Name_NotOptimal[0]])
      ybins = array.array('d',Discriminants[D_Name_NotOptimal[1]])
      zbins = array.array('d')
      # Choose the z-axis to hold the rest of the discriminants
      num_bins=1
      for i in range(2,len(D_Name_NotOptimal)):
        num_bins *= len(Discriminants[D_Name_NotOptimal[i]]) - 1
      num_bins *= Discriminants_Optimal["nbins"]
      for i in range(0,num_bins + 1):
        zbins.append(i)
      nz = len(zbins) - 1
      Histogram_Dict = {} # Initialize the Dictionary for Histograms (Each histogram is for the AC Hypothesis you want)
      
      for name in Template_Names:
        Histogram_Dict[name] = ROOT.TH3F(name,name,nx,xbins,ny,ybins,nz,zbins) # Initialize the Histogram Dictionary with with each AC hypothesis you need

      for tn in Template_Names: # Choose which hypothesis to reweight to
        Temporary_Histogram_List = [] # store the reweighted histogram for each sample in Samples to Reweight
        for sample in Samples_To_Reweight: # Loop over all samples with input production mode
          f = ROOT.TFile(sample, 'READ')
          t = f.Get("eventTree") # This name could change but overall processed CJLST trees for this analysis should have eventTree as the name
          print(sample)
          New_Weights = Reweight_Branch_NoHff_From_Template_Name(t,tn,isData,Analysis_Config,lumi,year,DoMassFilter) # Returns New Weights for each event
          for Discriminant in D_Name:
            Discriminant_Values[Discriminant] = tree2array(tree=t,branches=[Discriminant]).astype(float)
          # Fill the histogram with the Discriminants for each template #
          Tag = tree2array(tree=t,branches=["EventTag"]).astype(int) # Need to know what category each event falls into
          Z1Flav = tree2array(tree=t,branches=["Z1Flav"]).astype(int); # Need to know flavor of Z1
          Z2Flav = tree2array(tree=t,branches=["Z2Flav"]).astype(int); # Need to know flavor of Z2
          # Make the temporary histogram for this specific sample input
          Temp_Hist = ROOT.TH3F(sample,sample,nx,xbins,ny,ybins,nz,zbins)
          Temp_Hist.Sumw2(True)
          # Trim the x and y axis Discriminants from the dictionary
          Discriminant_Values_Trimmed = Trim_Dict(Discriminant_Values,[D_Name_NotOptimal[0],D_Name_NotOptimal[1]])
          Discriminant_Trimmed = Trim_Dict(Discriminants,[D_Name_NotOptimal[0],D_Name_NotOptimal[1]])
          Z_bin = GetBinOptimalDiscriminantND(Discriminant_Values_Trimmed,Discriminant_Trimmed,Discriminants_Optimal,nbins,dct)
          sum_weight = 0
          for i in range(len(New_Weights)):
            if Tag[i] == category:
              if filter_final_state:
                if abs(Z1Flav[i] * Z2Flav[i]) == final_state:
                  Temp_Hist.Fill(Discriminant_Values[D_Name_NotOptimal[0]][i],Discriminant_Values[D_Name_NotOptimal[1]][i],Z_bin[i],New_Weights[i])
                  sum_weight += New_Weights[i]
              else:
                Temp_Hist.Fill(Discriminant_Values[D_Name_NotOptimal[0]][i],Discriminant_Values[D_Name_NotOptimal[1]][i],Z_bin[i],New_Weights[i])
                sum_weight += New_Weights[i]
          print("Saving :",Temp_Hist.GetName(),Temp_Hist.Integral(),sum_weight)
          Temporary_Histogram_List.append(Temp_Hist)
        # Apply the logic for filling the combined histogram #
        # Loop over each bin and calculate the weighted average of each bin #
        for x in range (1,nx+1):
          for y in range(1,ny+1):
            for z in range(1,nz+1):
              binval=[] # list of bin values
              binerr=[] # list of error on each bin
              for hist in Temporary_Histogram_List:
                binval.append(hist.GetBinContent(x,y,z))
                binerr.append(hist.GetBinError(x,y,z))
              if "bkg" in Hypothesis_List:
                val = sum(binval)
                err = sum(i*i for i in binerr)
              else:
                val, err = Calculate_Average_And_Unc_From_Template_Bins(binval,binerr)
              Histogram_Dict[tn].SetBinContent(x,y,z,val)
              Histogram_Dict[tn].SetBinError(x,y,z,err)
        print("Saving :",Histogram_Dict[tn].GetName(),Histogram_Dict[tn].Integral())
      # Make the Output File and return the output #
      for hist in Histogram_Dict.keys():
        hlist.append(Histogram_Dict[hist])
      return Output_Name

      
  elif len(Discriminants) == 2: # This will make a 2D histogram to unroll #
    # This is where we process categories with two discriminants #
    nx = len(Discriminants[D_Name[0]])-1
    ny = len(Discriminants[D_Name[1]])-1
    xbins = array.array('d',Discriminants[D_Name[0]])
    ybins = array.array('d',Discriminants[D_Name[1]])

    # Now need to reweight each sample and add Fill the histograms #
    # Loop over the input trees and return the new weights #
       
    Histogram_Dict = {} # Initialize the Dictionary for Histograms (Each histogram is for the AC Hypothesis you want)
    for name in Template_Names:
      Histogram_Dict[name] = ROOT.TH2F(name,name,nx,xbins,ny,ybins) # Initialize the Histogram Dictionary with with each AC hypothesis you need
 
    for tn in Template_Names: # Choose which hypothesis to reweight to
      Temporary_Histogram_List = [] # store the reweighted histogram for each sample in Samples to Reweight
      for sample in Samples_To_Reweight: # Loop over all samples with input production mode
        f = ROOT.TFile(sample, 'READ')
        t = f.Get("eventTree") # This name could change but overall processed CJLST trees for this analysis should have eventTree as the name
        New_Weights = Reweight_Branch_NoHff_From_Template_Name(t,tn,isData,Analysis_Config,lumi,year,DoMassFilter) # Returns New Weights for each event
        for Discriminant in D_Name:
          Discriminant_Values[Discriminant] = tree2array(tree=t,branches=[Discriminant]).astype(float);
        # Fill the histogram with the Discriminants for each template #
        Tag = tree2array(tree=t,branches=["EventTag"]).astype(int); # Need to know what category each event falls into
        Z1Flav = tree2array(tree=t,branches=["Z1Flav"]).astype(int); # Need to know flavor of Z1
        Z2Flav = tree2array(tree=t,branches=["Z2Flav"]).astype(int); # Need to know flavor of Z2
        # Make the temporary histogram for this specific sample input
        Temp_Hist = ROOT.TH2F(sample,sample,nx,xbins,ny,ybins)
        Temp_Hist.Sumw2(True)
        #print("Category:",category)
        for i in range(len(New_Weights)):
          if Tag[i] == category:
            if filter_final_state:
              if abs(Z1Flav[i] * Z2Flav[i]) == final_state:
                Temp_Hist.Fill(Discriminant_Values[D_Name[0]][i],Discriminant_Values[D_Name[1]][i],New_Weights[i])
            else:
              Temp_Hist.Fill(Discriminant_Values[D_Name[0]][i],Discriminant_Values[D_Name[1]][i],New_Weights[i])
        Temporary_Histogram_List.append(Temp_Hist)
        print("Saving :",Temp_Hist.GetName(),Temp_Hist.Integral())
      # Apply the logic for filling the combined histogram #
      # Loop over each bin and calculate the weighted average of each bin #
      for x in range(1,nx+1):
        for y in range(1,ny+1):
          binval=[] # list of bin values
          binerr=[] # list of error on each bin
          for hist in Temporary_Histogram_List:
            binval.append(hist.GetBinContent(x,y))
            binerr.append(hist.GetBinError(x,y))
          if "bkg" in Hypothesis_List:
            val = sum(binval)
            err = sum(i*i for i in binerr)
          else:
            val, err = Calculate_Average_And_Unc_From_Template_Bins(binval,binerr)
          Histogram_Dict[tn].SetBinContent(x,y,val)
          Histogram_Dict[tn].SetBinError(x,y,err)
      print("Saving :",Histogram_Dict[tn].GetName(),Histogram_Dict[tn].Integral())         
    # Make the Output File and return the output #
    for hist in Histogram_Dict.keys():
      hlist.append(Histogram_Dict[hist])
    return Output_Name

  elif len(Discriminants) != 2:
    # Choose the first discriminant in the list to be the x axis
    nx = len(Discriminants[D_Name[0]]) - 1
    xbins = array.array('d',Discriminants[D_Name[0]])
    # Choose the second discriminant in the list to be the y axis 
    ny = len(Discriminants[D_Name[1]]) - 1 
    ybins = array.array('d',Discriminants[D_Name[1]])
    # Choose the z-axis to hold the rest of the discriminants  
    num_bins=1
    zbins = []

    for i in range(2,len(Discriminants)):
      num_bins *= len(Discriminants[D_Name[i]]) - 1
    for i in range(0,num_bins + 1):
      zbins.append(i)

    nz = len(zbins) - 1
    zbins = array.array('d',zbins)
    Histogram_Dict = {} # Initialize the Dictionary for Histograms (Each histogram is for the AC Hypothesis you want)

    for name in Template_Names:
      Histogram_Dict[name] = ROOT.TH3F(name,name,nx,xbins,ny,ybins,nz,zbins) # Initialize the Histogram Dictionary with with each AC hypothesis you need

    for tn in Template_Names: # Choose which hypothesis to reweight to
      Temporary_Histogram_List = [] # store the reweighted histogram for each sample in Samples to Reweight
      for sample in Samples_To_Reweight: # Loop over all samples with input production mode
        f = ROOT.TFile(sample, 'READ')
        t = f.Get("eventTree") # This name could change but overall processed CJLST trees for this analysis should have eventTree as the name
        print(sample,"tn:",tn)
        New_Weights = Reweight_Branch_NoHff_From_Template_Name(t,tn,isData,Analysis_Config,lumi,year,DoMassFilter) # Returns New Weights for each event
        for Discriminant in D_Name:
          Discriminant_Values[Discriminant] = tree2array(tree=t,branches=[Discriminant]).astype(float)
        # Fill the histogram with the Discriminants for each template #
        Tag = tree2array(tree=t,branches=["EventTag"]).astype(int) # Need to know what category each event falls into
        Z1Flav = tree2array(tree=t,branches=["Z1Flav"]).astype(int); # Need to know flavor of Z1
        Z2Flav = tree2array(tree=t,branches=["Z2Flav"]).astype(int); # Need to know flavor of Z2
        # Make the temporary histogram for this specific sample input
        Temp_Hist = ROOT.TH3F(sample,sample,nx,xbins,ny,ybins,nz,zbins)
        Temp_Hist.Sumw2(True)
        # Trim the x and y axis Discriminants from the dictionary
        Discriminant_Values_Trimmed = Trim_Dict(Discriminant_Values,[D_Name[0],D_Name[1]])
        Discriminant_Trimmed = Trim_Dict(Discriminants,[D_Name[0],D_Name[1]])
        Z_bin = Get_Z_Value(Discriminant_Values_Trimmed,Discriminant_Trimmed)
        sum_weight = 0
        for i in range(len(New_Weights)):
          if Tag[i] == category:
            if filter_final_state:
              if abs(Z1Flav[i] * Z2Flav[i]) == final_state:
                Temp_Hist.Fill(Discriminant_Values[D_Name[0]][i],Discriminant_Values[D_Name[1]][i],Z_bin[i],New_Weights[i])
                sum_weight += New_Weights[i]
            else:
              Temp_Hist.Fill(Discriminant_Values[D_Name[0]][i],Discriminant_Values[D_Name[1]][i],Z_bin[i],New_Weights[i])
              sum_weight += New_Weights[i]
        print("Saving :",Temp_Hist.GetName(),Temp_Hist.Integral(),sum_weight)
        Temporary_Histogram_List.append(Temp_Hist)
      # Apply the logic for filling the combined histogram #
      # Loop over each bin and calculate the weighted average of each bin #
      for x in range (1,nx+1):
        for y in range(1,ny+1):
          for z in range(1,nz+1):
            binval=[] # list of bin values
            binerr=[] # list of error on each bin
            for hist in Temporary_Histogram_List:
              binval.append(hist.GetBinContent(x,y,z))
              binerr.append(hist.GetBinError(x,y,z))
            if "bkg" in Hypothesis_List:
              val = sum(binval)
              err = sum(i*i for i in binerr)
            else:
              val, err = Calculate_Average_And_Unc_From_Template_Bins(binval,binerr)
            Histogram_Dict[tn].SetBinContent(x,y,z,val)
            Histogram_Dict[tn].SetBinError(x,y,z,err)
      print("Saving :",Histogram_Dict[tn].GetName(),Histogram_Dict[tn].Integral())
    # Make the Output File and return the output #
    for hist in Histogram_Dict.keys():
      hlist.append(Histogram_Dict[hist])
    return Output_Name

