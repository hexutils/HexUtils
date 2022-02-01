#!/usr/bin/env python

from uncertainties import ufloat
from uncertainties.umath import sqrt


class Conventions:
  def __init__(self):
	self.M_Z = 91.1876
	self.Ga_Z = 2.4952
	self.aL = -0.53762
	self.aR = 0.46238
	self.e = 0.8431872482432357  # = cL_lep = cR_lep from mod_Parameters
	self.L1 = 10000.

	self.g2HZZ = 1.65684
	self.g4HZZ = 2.55052
	self.g1prime2HZZ = -12100.42
	self.ghzgs1prime2HZZ = -7613.351302119843
	self.ghzgs2HZZ = 0.0477547
	self.ghzgs4HZZ = 0.0529487
	self.ghgsgs2HZZ = 0.0530640
	self.ghgsgs4HZZ = 0.0536022
	self.eLHZZ = sqrt(7.2310297E+00 / 1.4347981E+01)
	self.eRHZZ = sqrt(7.2310297E+00 / 1.3952140E+00)

	self.g2HWW = 1.133582
	self.g4HWW = 1.76132
	self.g1prime2HWW = -13752.22
	self.ghzgs1prime2HWW = -1000

	self.g2VBF = 0.27196538
	self.g4VBF = 0.297979018705
	self.g1prime2VBF = -2158.21307286
	self.ghzgs1prime2VBF = -4091.051456694223
	self.ghzgs2VBF = 0.200460
	self.ghzgs4VBF = 0.206536
	self.ghgsgs2VBF = 0.123994
	self.ghgsgs4VBF = 0.124727

	self.g2ZH = 0.112481
	self.g4ZH = 0.144057
	self.g1prime2ZH = -517.788
	self.ghzgs1prime2ZH = -642.9534550379002
	self.ghzgs2ZH = 0.140705
	self.ghzgs4ZH = 0.175403
	self.ghgsgs2ZH = 0.655141
	self.ghgsgs4ZH = 0.747376

	self.g2WH = 0.0998956
	self.g4WH = 0.1236136
	self.g1prime2WH = -525.274

	self.g2VH = 0.10430356645812816 #sqrt((JHUXSZHa1 + JHUXSWHa1*normalize_WH_to_ZH) / (JHUXSZHa2 + JHUXSWHa2*normalize_WH_to_ZH))
	self.g4VH = 0.13053750671388425 #sqrt((JHUXSZHa1 + JHUXSWHa1*normalize_WH_to_ZH) / (JHUXSZHa3 + JHUXSWHa3*normalize_WH_to_ZH))
	self.g1prime2VH = -522.3034453633128 #-sqrt((JHUXSZHa1 + JHUXSWHa1*normalize_WH_to_ZH) / (JHUXSZHL1 + JHUXSWHL1*normalize_WH_to_ZH))
	self.ghzgs1prime2VH = -1027.387141119873 #-sqrt((JHUXSZHa1 + JHUXSWHa1*normalize_WH_to_ZH) / (JHUXSZHL1Zg + JHUXSWHL1Zg*normalize_WH_to_ZH))
	self.nominal_normalize_WH_to_ZH = 0.15070409765374365

	self.ghg4HJJ = 1.0062
	self.kappa_tilde_ttH = 1.6

	self.g1prime2ggZH = -219.641
	self.ghzgs1prime2ggZH = -57787
	self.kappa_tilde_ggZH = 0.9475

	#https://twiki.cern.ch/twiki/pub/LHCPhysics/LHCHXSWG/Higgs_XSBR_YR4_update.xlsx
	self.SMXSggH   = (44.14      #'YR4 SM 13TeV'!B24   (ggH cross section, m=125)
        	      *1000)    #                     (pb to fb)
	self.SMBR2e2mu =  5.897E-05  #'YR4 SM BR'!CO25     (2e2mu BR, m=125)
	self.SMBR4l    =  2.745E-04  #'YR4 SM BR'!CL25     (4l BR including taus, m=125)
	self.SMXSVBF   = (3.782E+00  #'YR4 SM 13TeV'!B24   (VBF cross section, m=125)
        	      *1000)    #                     (pb to fb)
	self.SMXSWH    = (1.373E+00  #'YR4 SM 13TeV'!R24   (WH cross section, m=125)
	              *1000)    #                     (pb to fb)
	self.SMXSWpH   = (8.400E-01  #'YR4 SM 13TeV'!X24   (W+H cross section, m=125)
        	      *1000)    #                     (pb to fb)
	self.SMXSWmH   = (5.328E-01  #'YR4 SM 13TeV'!X24   (W-H cross section, m=125)
        	      *1000)    #                     (pb to fb)
	self.SMXSZH    = (8.839E-01  #'YR4 SM 13TeV'!AB24  (ZH cross section, m=125)
        	      *1000)    #                     (pb to fb)
	self.SMXSttH   = (5.071E-01  #'YR4 SM 13TeV'!AK24  (ttH cross section, m=125)
        	      *1000)    #                     (pb to fb)
	self.SMXSbbH   = (4.880E-01  #'YR4 SM 13TeV'!BB24  (bbH cross section, m=125)
        	      *1000)    #                     (pb to fb)
	self.SMXStqHt  = (7.425E-02  #'YR4 SM 13TeV'!BJ24  (tqH t channel cross section, m=125)
        	      *1000)    #                     (pb to fb)
	self.SMXStqHs  = (2.879E-03  #'YR4 SM 13TeV'!BT24  (tqH s channel cross section, m=125)
        	      *1000)    #                     (pb to fb)

	self.SMXStqH  = self.SMXStqHt + self.SMXStqHs

	self.SMXSggH2e2mu = self.SMXSggH * self.SMBR2e2mu
	self.SMXSVBF2e2mu = self.SMXSVBF * self.SMBR2e2mu
	self.SMXSZH2e2mu  = self.SMXSZH  * self.SMBR2e2mu
	self.SMXSWH2e2mu  = self.SMXSWH  * self.SMBR2e2mu
	self.SMXSWpH2e2mu = self.SMXSWpH * self.SMBR2e2mu
	self.SMXSWmH2e2mu = self.SMXSWmH * self.SMBR2e2mu
	self.SMXSttH2e2mu = self.SMXSttH * self.SMBR2e2mu
	self.SMXSbbH2e2mu = self.SMXSbbH * self.SMBR2e2mu
	self.SMXStqH2e2mu = self.SMXStqH * self.SMBR2e2mu

	self.SMXSggH4l = self.SMXSggH * self.SMBR4l
	self.SMXSVBF4l = self.SMXSVBF * self.SMBR4l
	self.SMXSZH4l  = self.SMXSZH  * self.SMBR4l
	self.SMXSWH4l  = self.SMXSWH  * self.SMBR4l
	self.SMXSWpH4l = self.SMXSWpH * self.SMBR4l
	self.SMXSWmH4l = self.SMXSWmH * self.SMBR4l
	self.SMXSttH4l = self.SMXSttH * self.SMBR4l
	self.SMXSbbH4l = self.SMXSbbH * self.SMBR4l
	self.SMXStqH4l = self.SMXStqH * self.SMBR4l
