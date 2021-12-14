#!/usr/bin/env python
import os, sys, re
import ROOT
import os
from array import array
from set_palette import set_palette

ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.gStyle.SetLabelFont(42,"xyz")
ROOT.gStyle.SetLabelSize(0.05,"xyz")
#ROOT.gStyle.SetTitleFont(42)
ROOT.gStyle.SetTitleFont(42,"xyz")
ROOT.gStyle.SetTitleFont(42,"t")
#ROOT.gStyle.SetTitleSize(0.05)
ROOT.gStyle.SetTitleSize(0.06,"xyz")
ROOT.gStyle.SetTitleSize(0.06,"t")
ROOT.gStyle.SetPadBottomMargin(0.14)
ROOT.gStyle.SetPadLeftMargin(0.14)
ROOT.gStyle.SetTitleOffset(1,'y')
#ROOT.gStyle.SetLegendTextSize(0.05)
ROOT.gStyle.SetGridStyle(3)
ROOT.gStyle.SetGridColor(13)
#ROOT.gStyle.SetOptStat(1001101)

subtractQIE=False
qieRun=0

if len(sys.argv) < 2:
    sys.exit('Please provide an input file') 

else:
    filename = sys.argv[1]


if len(sys.argv) >=3:
    subtractQIE=True
    qieRun=sys.argv[2]


inputdir = "/Users/chandiprasadkar/work/HCALWORK/hists/"

nieta = 14
minieta = 16
niphi = 70
miniphi= 0
ndepth = 7
mindepth = 1

dsub=inputdir+"hists_sub_"+filename+".root"
filr=ROOT.TFile(dsub,"READ")
print filr
h_3p3= filr.Get("h1_3p3_run315431")
h_3p3.Draw()
