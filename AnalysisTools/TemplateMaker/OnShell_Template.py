import ROOT 
import array
import itertools
import pandas as pd
from root_numpy import array2tree, tree2array
from ..Utils.ReWeightSample import Reweight_Branch, Reweight_Branch_NoHff

def Parse_Tagged_Mode(Tag,Analysis_Config):
  # Get the Categorization from Analysis Config #
  Categorization = Analysis_Config.TaggingProcess
  cat_num = -999
  # Parse the Categorization and return  the number for the tag #
  if Categorization == "Tag_AC_19_Scheme_2":
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
  try:
    cat_num != -999 
  except ValueError:
    print("Please select valid Tagged Mode!")

  return cat_num 

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
  print(len(Tuples_Of_Bin_Num))
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

def FillHistOnShellNoSyst(targetprod,targetcateg,hlist,yeardict,Analysis_Config,year):
  # This should take an empty h_list and then fill with the templates 
  # target production will return which ever production that will be used to make the template ex (ggH,VBF etc) 
  # targetcateg is which tagged category is used to make the template 
  # h_list is an input dictionary 
  # year dict has paths and years attatched to each samples
  # year is an array of years to use#

  # First We nee to parse the input category which tells us exactly which discriminants are needed #
  category = Parse_Tagged_Mode(targetcateg,Analysis_Config)
  
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
  else:
    print("No category found")
  
  if "Data" not in targetprod: # Need for input to get th new weights
    isData = False
  else:
    isData = True

  Trees_Dict = yeardict[year] # Returns dictionary of all the samples for a given year
  Samples_To_Reweight = Trees_Dict[targetprod] #Returns the list of all samples of a given production mode 
  if len(Samples_To_Reweight) == 1:
    Samples_To_Reweight = Samples_To_Reweight[0] 
  lumi = Analysis_Config.lumi[year]
  Coupling_Name = Analysis_Config.Coupling_Name # Returns name of couplings used for analysis (what do we need to reweight to?)  
  Output_Name = "templates_"+str(targetprod)+"_"+Coupling_Name+"_"+"2e2mu"+"_"+Analysis_Config.TreeFile+"_"+year+".root" #NEED to fix decay mode#
  Hypothesis_List = Analysis_Config.Hypothesis_List # Returns a list of all the hyptothesis to reweight to 

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
      Histogram_Dict[hypothesis] = ROOT.TH2F(hypothesis,hypothesis,nx,xbins,ny,ybins) # Initialize the Histogram Dictionary with with each AC hypothesis you need
 
    for hypothesis in Hypothesis_List: # Choose which hypothesis to reweight to
      for sample in Samples_To_Reweight: # Loop over all samples with input production mode
        print(sample)
        f = ROOT.TFile(sample, 'READ')
        t = f.Get("eventTree") # This name could change but overall processed CJLST trees for this analysis should have eventTree as the name
        New_Weights = Reweight_Branch_NoHff(t,targetprod,hypothesis,isData,Analysis_Config,lumi,year) # Returns New Weights for each event
        for Discriminant in D_Name:
          Discriminant_Values[Discriminant] = tree2array(tree=t,branches=[Discriminant]).astype(float)
        # Fill the histogram with the Discriminants for each template #
        Tag = tree2array(tree=t,branches=["EventTag"]).astype(int) # Need to know what category each event falls into
        for i in range(len(New_Weights)):
          if Tag[i] == category:
            Histogram_Dict[hypothesis].Fill(Discriminant_Values[D_Name[0]][i],Discriminant_Values[D_Name[1]][i],New_Weights[i])
          
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
    nz = 0
    zbins = []
    for i in range(2,len(Discriminants)):
      num_bins *= len(Discriminants[D_Name[i]]) - 1
    for i in range(0,num_bins + 1):
      zbins.append(i)
    nz = len(zbins) - 1
    zbins = array.array('d',zbins)
    Histogram_Dict = {} # Initialize the Dictionary for Histograms (Each histogram is for the AC Hypothesis you want)
    for hypothesis in Hypothesis_List:
      Histogram_Dict[hypothesis] = ROOT.TH3F(hypothesis,hypothesis,nx,xbins,ny,ybins,nz,zbins) # Initialize the Histogram Dictionary with with each AC hypothesis you need

    for hypothesis in Hypothesis_List: # Choose which hypothesis to reweight to
      for sample in Samples_To_Reweight: # Loop over all samples with input production mode
        print(sample)
        f = ROOT.TFile(sample, 'READ')
        t = f.Get("eventTree") # This name could change but overall processed CJLST trees for this analysis should have eventTree as the name
        New_Weights = Reweight_Branch_NoHff(t,targetprod,hypothesis,isData,Analysis_Config,lumi,year) # Returns New Weights for each event
        for Discriminant in D_Name:
          Discriminant_Values[Discriminant] = tree2array(tree=t,branches=[Discriminant]).astype(float)
        # Fill the histogram with the Discriminants for each template #
        Tag = tree2array(tree=t,branches=["EventTag"]).astype(int) # Need to know what category each event falls into
        # Trim the x and y axis Discriminants from the dictionary
        Discriminant_Values_Trimmed = Trim_Dict(Discriminant_Values,[D_Name[0],D_Name[1]])
        Discriminant_Trimmed = Trim_Dict(Discriminants,[D_Name[0],D_Name[1]])
        Z_bin = Get_Z_Value(Discriminant_Values_Trimmed,Discriminant_Trimmed)
        for i in range(len(New_Weights)):
          if Tag[i] == category:
            Histogram_Dict[hypothesis].Fill(Discriminant_Values[D_Name[0]][i],Discriminant_Values[D_Name[1]][i],Z_bin[i],New_Weights[i]) 
    # Make the Output File and return the output #
    for hist in Histogram_Dict.keys():
      hlist.append(Histogram_Dict[hist])
    return Output_Name

