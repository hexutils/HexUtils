'''
CMS official style
To get test plots, just do:
 
    python -i test_tdrstyle.py

To set up the plotting style do the following in your python macro:

    import tdrstyle 
    
To print the CMS luminosity information, use the tdrstyle.cmsPrel function. For more information, do 

    help(tdrstyle.cmsPrel)
'''

import ROOT as rt



def cmsPrel(lumi,  energy=None,  simOnly=True,  onLeft=True,  sp=0, textScale=1., xoffset=0., thisIsPrelim=False):
  '''Overlay CMS information text: 
    CMS
    Simulation, if applicable
    luminosity and sqrt(s) 

  Parameters:
  - lumi: luminosity, in pb 
  - energy: sqrt(s), in TeV
  - simOnly: if set to True, print Simulation below CMS
  - onLeft: print CMS (Simulation) on the left side of the pad. 
    otherwise, print it on the right side. 
  - spacing for text in the top margin, do not touch.
  - textScale: set to 1 by default. You might want to use a larger 
    factor to scale up all texts in case your plots are small in your paper.
  '''
  if energy: 
    energy = int(energy)

  latex = rt.TLatex()
  
  t = rt.gStyle.GetPadTopMargin()
  tmpTextSize=0.75*t
  latex.SetTextSize(tmpTextSize)
  latex.SetNDC()
  textSize=latex.GetTextSize()
  latex.SetName("lumiText")
  latex.SetTextFont(42)
    
  lumyloc = 0.965
  cmsyloc = 0.893
  simyloc = 0.858
  if sp!=0:
    lumyloc = 0.945
    cmsyloc = 0.85
    simyloc = 0.8
  cmsalign = 31
  cmsxloc = 0.924
  cmsyloc = lumyloc
  cmsxloc = rt.gStyle.GetPadLeftMargin()
  if onLeft:
    cmsalign = 11
    cmsxloc = 0.204
    cmsxloc = rt.gStyle.GetPadLeftMargin()
 
  xlumi = 1-rt.gStyle.GetPadRightMargin() - xoffset
  if (lumi > 0.):
    latex.SetTextAlign(31) # align left, right=31
    latex.SetTextSize(textSize*0.6/0.75)
    if lumi > 1000. :
        latex.DrawLatex(xlumi,lumyloc,
                        " {lumi} fb^{{-1}} ({energy} TeV)".format(
                        lumi=lumi/1000.,
                        energy=energy
                        ))
    elif lumi < 0.01:
        latex.DrawLatex(xlumi,lumyloc,
                        " {lumi} nb^{{-1}} ({energy} TeV)".format(
                        lumi=lumi*1000.,
                        energy=energy
                        ))        
    else:
      latex.DrawLatex(xlumi,lumyloc,
                      " {lumi} pb^{{-1}} ({energy} TeV)".format(
                      lumi=lumi,
                      energy=energy
                      ))
  
  else:
    if energy: 
      latex.SetTextAlign(31) # align right=31
      latex.SetTextSize(textSize*0.6/0.75)
      latex.DrawLatex(xlumi,lumyloc," {energy} TeV".format(energy=energy))
  
 
  latex.SetTextAlign(cmsalign) # align left / right
  latex.SetTextFont(61)
  latex.SetTextSize(textSize)
  latex.DrawLatex(cmsxloc, cmsyloc,"CMS")
  
  latex.SetTextFont(52)
  latex.SetTextSize(textSize*0.76)
  
  if(simOnly):
    latex.DrawLatex(cmsxloc, simyloc,"Simulation")
  elif thisIsPrelim:
    latex.DrawLatex(cmsxloc, simyloc, "Preliminary")


def tdrGrid( gridOn):
  tdrStyle.SetPadGridX(gridOn)
  tdrStyle.SetPadGridY(gridOn)

#fixOverlay: Redraws the axis
def fixOverlay(): gPad.RedrawAxis()

def setTDRStyle(square=True):
  tdrStyle =  rt.TStyle("tdrStyle","Style for P-TDR")

   #for the canvas:
  tdrStyle.SetCanvasBorderMode(0)
  tdrStyle.SetCanvasColor(rt.kWhite)
  if square:    
    tdrStyle.SetCanvasDefH(600) #Height of canvas
    tdrStyle.SetCanvasDefW(600) #Width of canvas
    tdrStyle.SetCanvasDefX(0)   #POsition on screen
    tdrStyle.SetCanvasDefY(0)

  tdrStyle.SetPadBorderMode(0)
  #tdrStyle.SetPadBorderSize(Width_t size = 1)
  tdrStyle.SetPadColor(rt.kWhite)
  tdrStyle.SetPadGridX(False)
  tdrStyle.SetPadGridY(False)
  tdrStyle.SetGridColor(0)
  tdrStyle.SetGridStyle(3)
  tdrStyle.SetGridWidth(1)

#For the frame:
  tdrStyle.SetFrameBorderMode(0)
  tdrStyle.SetFrameBorderSize(1)
  tdrStyle.SetFrameFillColor(0)
  tdrStyle.SetFrameFillStyle(0)
  tdrStyle.SetFrameLineColor(1)
  tdrStyle.SetFrameLineStyle(1)
  tdrStyle.SetFrameLineWidth(1)

#For the histo:
  #tdrStyle.SetHistFillColor(1)
  #tdrStyle.SetHistFillStyle(0)
  tdrStyle.SetHistLineColor(1)
  tdrStyle.SetHistLineStyle(0)
  tdrStyle.SetHistLineWidth(2)
  #tdrStyle.SetLegoInnerR(Float_t rad = 0.5)
  #tdrStyle.SetNumberContours(Int_t number = 20)

  tdrStyle.SetEndErrorSize(2)
  #tdrStyle.SetErrorMarker(20)
  #tdrStyle.SetErrorX(0.)

  tdrStyle.SetMarkerStyle(20)

#For the fit/function:
  tdrStyle.SetOptFit(1)
  tdrStyle.SetFitFormat("5.4g")
  tdrStyle.SetFuncColor(2)
  tdrStyle.SetFuncStyle(1)
  tdrStyle.SetFuncWidth(1)

#For the date:
  tdrStyle.SetOptDate(0)
  # tdrStyle.SetDateX(Float_t x = 0.01)
  # tdrStyle.SetDateY(Float_t y = 0.01)

# For the statistics box:
  tdrStyle.SetOptFile(0)
  tdrStyle.SetOptStat(0) # To display the mean and RMS:   SetOptStat("mr")
  tdrStyle.SetStatColor(rt.kWhite)
  tdrStyle.SetStatFont(42)
  tdrStyle.SetStatFontSize(0.025)
  tdrStyle.SetStatTextColor(1)
  tdrStyle.SetStatFormat("6.4g")
  tdrStyle.SetStatBorderSize(1)
  tdrStyle.SetStatH(0.1)
  tdrStyle.SetStatW(0.15)
  # tdrStyle.SetStatStyle(Style_t style = 1001)
  # tdrStyle.SetStatX(Float_t x = 0)
  # tdrStyle.SetStatY(Float_t y = 0)

# Margins:
  tdrStyle.SetPadTopMargin(0.05)
  tdrStyle.SetPadBottomMargin(0.15)
  tdrStyle.SetPadLeftMargin(0.16)
  tdrStyle.SetPadRightMargin(0.04)

# For the Global title:

  tdrStyle.SetOptTitle(0)
  tdrStyle.SetTitleFont(42)
  tdrStyle.SetTitleColor(1)
  tdrStyle.SetTitleTextColor(1)
  tdrStyle.SetTitleFillColor(10)
  tdrStyle.SetTitleFontSize(0.05)
  # tdrStyle.SetTitleH(0) # Set the height of the title box
  # tdrStyle.SetTitleW(0) # Set the width of the title box
  # tdrStyle.SetTitleX(0) # Set the position of the title box
  # tdrStyle.SetTitleY(0.985) # Set the position of the title box
  # tdrStyle.SetTitleStyle(Style_t style = 1001)
  # tdrStyle.SetTitleBorderSize(2)

# For the axis titles:

  tdrStyle.SetTitleColor(1, "XYZ")
  tdrStyle.SetTitleFont(42, "XYZ")
  tdrStyle.SetTitleSize(0.06, "XYZ")
  # tdrStyle.SetTitleXSize(Float_t size = 0.02) # Another way to set the size?
  # tdrStyle.SetTitleYSize(Float_t size = 0.02)
  if square:
    tdrStyle.SetTitleYOffset(1.4)
  else:
    tdrStyle.SetTitleYOffset(1.1)
  # tdrStyle.SetTitleOffset(1.1, "Y") # Another way to set the Offset

# For the axis labels:

  tdrStyle.SetLabelColor(1, "XYZ")
  tdrStyle.SetLabelFont(42, "XYZ")
  tdrStyle.SetLabelOffset(0.007, "XYZ")
  tdrStyle.SetLabelSize(0.05, "XYZ")

# For the axis:

  tdrStyle.SetAxisColor(1, "XYZ")
  tdrStyle.SetStripDecimals(True)
  tdrStyle.SetTickLength(0.03, "XYZ")
  # tdrStyle.SetNdivisions(510, "XYZ")
  tdrStyle.SetPadTickX(1)  # To get tick marks on the opposite side of the frame
  tdrStyle.SetPadTickY(1)
  # tdrStyle.SetMaxDigits(3)
  
# Change for log plots:
  tdrStyle.SetOptLogx(0)
  tdrStyle.SetOptLogy(0)
  tdrStyle.SetOptLogz(0)

# Postscript options:
  tdrStyle.SetPaperSize(20.,20.)
  # tdrStyle.SetLineScalePS(Float_t scale = 3)
  # tdrStyle.SetLineStyleString(Int_t i, const char* text)
  # tdrStyle.SetHeaderPS(const char* header)
  # tdrStyle.SetTitlePS(const char* pstitle)

  # tdrStyle.SetBarOffset(Float_t baroff = 0.5)
  # tdrStyle.SetBarWidth(Float_t barwidth = 0.5)
  # tdrStyle.SetPaintTextFormat(const char* format = "g")
  # tdrStyle.SetPalette(Int_t ncolors = 0, Int_t* colors = 0)
  # tdrStyle.SetTimeOffset(Double_t toffset)
  # tdrStyle.SetHistMinimumZero(kTRUE)

#  tdrStyle.SetHatchesLineWidth(5)
#  tdrStyle.SetHatchesSpacing(0.05)

  tdrStyle.SetLegendBorderSize(0)


  tdrStyle.cd()

setTDRStyle()  

if __name__ == "__main__":

  from ROOT import gStyle, TH1F, gPad, TLegend, TF1, TCanvas
  
  c1 = TCanvas("c1", "c1")
  
  h = TH1F("h", "; p_{T}^{Bar} (TeV); Events / 2 TeV (10^{3})", 50, -50, 50)
  gaus1 = TF1('gaus1', 'gaus')
  gaus1.SetParameters(1, 0, 5)
  h.FillRandom("gaus1", 50000)
  h.Scale(0.001)
  # h.GetXaxis().SetNdivisions(5)
  # h.GetXaxis().SetRangeUser(-70,70)
  h.Draw()
  
  legend_args = (0.645, 0.79, 0.985, 0.91, '', 'NDC')

  legend = TLegend(*legend_args)
  legend.SetFillStyle(0)
  legend.AddEntry(h, "h1", "l")
  legend.AddEntry(h, "h1 again", "l")
  legend.Draw()

  cmsPrel(25000., 8., True)
  
  gPad.Update()
  gPad.SaveAs('tdrstyle.png')
