import ROOT 
import array
import itertools
import pandas as pd
import numpy as np
from root_numpy import array2tree, tree2array
from ..Utils.ReWeightSample import Reweight_Branch, Reweight_Branch_NoHff, ParseHypothesis, CheckIsIso
from ..Utils.HexMath import weightedaverage, kspoissongaussian

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

def Convert_Hypothesis_And_Prodution_Mode_To_Template_Name(hypothesis,production_mode): #This function takes as input a given hypothesis and returns the correct naming convention for the combine physics model

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
  print(Coupling_Dict,CheckIsIso(Coupling_Dict))
  if CheckIsIso(Coupling_Dict):
    print("here")
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
    if production_mode == 'ttH': #Need to include Hff couplings???#
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
      print(bin_edges)
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
  if category == 0: #Untagged 
    Discriminants = Analysis_Config.Untagged_Discriminants
  elif category == 1: #VBF1jTagged
    Discriminants = Analysis_Config.VBF1jTagged_Discriminants
  elif category == 2: #VBF2jTagged
    Discriminants = Analysis_Config.VBF2jTagged_Discriminants
  elif category == 3: #VHLeptTagged
    Discriminants = Analysis_Config.VHLeptTagged_Discriminants
  elif category == 4: #VHHadrTagged
    Discriminants = Analysis_Config.VHHadrTagged_Discriminants
  elif category == 5: #ttHLeptTagged
    Discriminants = Analysis_Config.ttHLeptTagged_Discriminants
  elif category == 6: #ttHHadrTagged
    Discriminants = Analysis_Config.ttHHadrTagged_Discriminants
  elif category == 7: #VHMETTagged
    Discriminants = Analysis_Config.VHMETTagged_Discriminants
  elif category == 8: #Boosted
    Discriminants = Analysis_Config.Boosted_Discriminants
  elif category == 9: #gammaH
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

  if len(Discriminants) == 2: # This will make a 2D histogram to unroll #
    # This is where we process categories with two discriminants #
    nx = len(Discriminants[D_Name[0]])-1
    ny = len(Discriminants[D_Name[1]])-1
    xbins = array.array('d',Discriminants[D_Name[0]])
    ybins = array.array('d',Discriminants[D_Name[1]])

    # Now need to reweight each sample and add Fill the histograms #
    # Loop over the input trees and return the new weights #
       
    Histogram_Dict = {} # Initialize the Dictionary for Histograms (Each histogram is for the AC Hypothesis you want)
    for hypothesis in Hypothesis_List:
      name = Convert_Hypothesis_And_Prodution_Mode_To_Template_Name(hypothesis,targetprod)
      Histogram_Dict[hypothesis] = ROOT.TH2F(name,name,nx,xbins,ny,ybins) # Initialize the Histogram Dictionary with with each AC hypothesis you need
 
    for h in Hypothesis_List: # Choose which hypothesis to reweight to
      DoInterf, hypothesis = IsInterf(h)# Check if the hypothesis has interference or not # 
      Temporary_Histogram_List = [] # store the reweighted histogram for each sample in Samples to Reweight
      for sample in Samples_To_Reweight: # Loop over all samples with input production mode
        f = ROOT.TFile(sample, 'READ')
        t = f.Get("eventTree") # This name could change but overall processed CJLST trees for this analysis should have eventTree as the name
        New_Weights = Reweight_Branch_NoHff(t,targetprod,hypothesis,isData,Analysis_Config,lumi,year,DoInterf,DoMassFilter) # Returns New Weights for each event
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
          Histogram_Dict[h].SetBinContent(x,y,val)
          Histogram_Dict[h].SetBinError(x,y,err)
      print("Saving :",Histogram_Dict[h].GetName(),Histogram_Dict[h].Integral())         
    # Make the Output File and return the output #
    for hist in Histogram_Dict.keys():
      hlist.append(Histogram_Dict[hist])
    return Output_Name

  if len(Discriminants) != 2:
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
    for hypothesis in Hypothesis_List:
      name = Convert_Hypothesis_And_Prodution_Mode_To_Template_Name(hypothesis,targetprod)
      Histogram_Dict[hypothesis] = ROOT.TH3F(name,name,nx,xbins,ny,ybins,nz,zbins) # Initialize the Histogram Dictionary with with each AC hypothesis you need

    for h in Hypothesis_List: # Choose which hypothesis to reweight to
      DoInterf, hypothesis = IsInterf(h)# Check if the hypothesis has interference or not #
      Temporary_Histogram_List = [] # store the reweighted histogram for each sample in Samples to Reweight
      for sample in Samples_To_Reweight: # Loop over all samples with input production mode
        f = ROOT.TFile(sample, 'READ')
        t = f.Get("eventTree") # This name could change but overall processed CJLST trees for this analysis should have eventTree as the name
        print(sample)
        New_Weights = Reweight_Branch_NoHff(t,targetprod,hypothesis,isData,Analysis_Config,lumi,year,DoInterf,DoMassFilter) # Returns New Weights for each event
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
            Histogram_Dict[h].SetBinContent(x,y,z,val)
            Histogram_Dict[h].SetBinError(x,y,z,err)
      print("Saving :",Histogram_Dict[h].GetName(),Histogram_Dict[h].Integral())
    # Make the Output File and return the output #
    for hist in Histogram_Dict.keys():
      hlist.append(Histogram_Dict[hist])
    return Output_Name

