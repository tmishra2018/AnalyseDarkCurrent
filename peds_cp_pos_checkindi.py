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

if len(sys.argv) < 1:
    sys.exit('Please provide an input file') 

else:
    filename = sys.argv[1]

inputdir = "/Users/chandiprasadkar/work/HCALWORK/"

#nieta = 14
#minieta = 16

nieta = 14
minieta = 16

niphi = 72
miniphi= 1

ndepth = 7
mindepth = 1

set_palette()
if not os.path.exists("peds/"):
    os.makedirs("peds/")

one = ROOT.TColor(20001,0.906,0.153,0.094)
two = ROOT.TColor(20002,0.906,0.533,0.094)
three = ROOT.TColor(20003,0.086,0.404,0.576)
four =ROOT.TColor(20004,0.071,0.694,0.18)
five =ROOT.TColor(20005,0.388,0.098,0.608)
six=ROOT.TColor(20006,0.906,0.878,0.094)
colors = [1,20001,20002,20003,20004,20005,20006,2,3,4,6,7,5,1,8,9,29,38,46]
ch = ROOT.TChain("hcalTupleTree/tree")
ch.Add(inputdir+filename)
ents=str(ch.GetEntries())
print(ents)

run = filename.split(".root")[0][-6:]
filename=filename.replace(".root","")#.split("/")[-1]

outFile=ROOT.TFile("hists/hists_sub_"+filename+"_posieta_nosub.root","RECREATE")

print 'filename: ' +filename
print 'run '+run
#outFile=ROOT.TFile("hists_"+filename+".root","RECREATE")
print(ch.GetEntries())




h2 = ROOT.TH2F("h2","",nieta,minieta,minieta+nieta,ndepth*niphi,niphi*mindepth+miniphi,niphi*mindepth+miniphi+ndepth*niphi)
h2.Sumw2()

nbins = 50
minx=0
maxx=500
unit="fC"

h1 = ROOT.TH1F("h1_"+run,";Mean 8TS pedestal sum ["+unit+"]; Number of channels",nbins,minx,maxx)
#h1_2p8 = ROOT.TH1F("h1_2p8_"+run,";Mean 8TS pedestal sum ["+unit+"]; Number of channels",10,0,400)
h1_3p3 = ROOT.TH1F("h1_3p3_"+run,";Mean 8TS pedestal sum ["+unit+"]; Number of channels",nbins,minx,maxx)
h1_2p8 = ROOT.TH1F("h1_2p8_"+run,";Mean 8TS pedestal sum ["+unit+"]; Number of channels",nbins,minx,maxx)
h1_3p30 = ROOT.TH1F("h1_3p30_"+run,";Mean 8TS pedestal sum ["+unit+"]; Number of channels",nbins,minx,maxx)
h1_3p31 = ROOT.TH1F("h1_3p31_"+run,";Mean 8TS pedestal sum ["+unit+"]; Number of channels",nbins,minx,maxx)
h1_3p32 = ROOT.TH1F("h1_3p32_"+run,";Mean 8TS pedestal sum ["+unit+"]; Number of channels",nbins,minx,maxx)


h1e = ROOT.TH1F("h1e_"+run,";Error on mean 8TS pedestal sum ["+unit+"]; Number of channels",12,0,6)
h1e_2p8 = ROOT.TH1F("h1e_2p8_"+run,";Error on mean 8TS pedestal sum ["+unit+"]; Number of channels",12,0,6)
h1e_3p3 = ROOT.TH1F("h1e_3p3_"+run,";Error on mean 8TS pedestal sum ["+unit+"]; Number of channels",12,0,6)

h1.StatOverflows(True) 
h1_2p8.StatOverflows(True)
h1_3p3.StatOverflows(True)

h1_3p30.StatOverflows(True)
h1_3p31.StatOverflows(True)
h1_3p32.StatOverflows(True)

h1e.StatOverflows(True)
h1e_2p8.StatOverflows(True)
h1e_3p3.StatOverflows(True)

if unit=="fC": unit="FC"

ch.Project("h2","72*QIE11DigiDepth+QIE11DigiIPhi:QIE11DigiIEta","1/("+ents+".)*(QIE11DigiFC[][0]+QIE11DigiFC[][1]+QIE11DigiFC[][2]+QIE11DigiFC[][3]+QIE11DigiFC[][4]+QIE11DigiFC[][5]+QIE11DigiFC[][6]+QIE11DigiFC[][7])")


for x in range(1,1+h2.GetNbinsX()):
    for y in range(1,1+h2.GetNbinsY()):
        if(h2.GetBinContent(x,y)>0):
            mean = h2.GetBinContent(x,y)
            meanerr= h2.GetBinError(x,y)
            
            h1.Fill(mean)
            h1e.Fill(meanerr)
            
            eta=x+minieta-1
            yvalue = niphi*mindepth+miniphi+y-1
            iphi = (yvalue-miniphi)%niphi+miniphi
            depth = (yvalue-iphi)/72
            
            
            is3p3 = (eta<=17 or (eta ==18 and depth==5))
            if is3p3:
                h1_3p3.Fill(mean)
            else:
                h1_2p8.Fill(mean)

h1.Write()
h1e.Write()
h1_3p3.Write()
#h1_3p31.Write()
#h1_3p32.Write()
h1_2p8.Write()
h2.Write()
outFile.Save()
outFile.Close()









