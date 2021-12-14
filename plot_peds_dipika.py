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
    subname = sys.argv[2]

if len(sys.argv) >=3:
    subtractQIE=True
    qieRun=sys.argv[2]


inputdir = "/Users/chandiprasadkar/work/HCALWORK/"

#nieta = 14
#minieta = 16

nieta = 14
minieta = -29

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

def printTH2(h2,name,min=None,max=None):
    c = ROOT.TCanvas()
    c.SetRightMargin(0.2)
    c.SetLeftMargin(0.16)
    h2.SetStats(0)
    h2.SetLabelSize(0.04,"y")
    if(h2.GetNbinsY()==niphi*ndepth):
        for iphi in range(miniphi,miniphi+niphi):
            for idepth in range(mindepth,mindepth+ndepth):
                index = 1 + niphi*(idepth-1) + iphi-miniphi
                h2.GetYaxis().SetBinLabel(index,"Depth "+str(idepth)+", iPhi "+str(iphi))
                #h2.GetYaxis().ChangeLabel(index,-1,-1,12)
    if min is None:
        h2.SetMinimum(0.95*h2.GetMinimum(0.000001))
        
    else:
        h2.SetMaximum(max)
        h2.SetMinimum(min)
        
    h2.Draw("colz")
    c.Print("peds/h2_"+name+".pdf") 
    if not subtractQIE:
        c.Print("peds/h2_"+name+".pdf") 
    else:
        c.Print("peds/h2_sub"+name+".pdf")
    
def printTH1(h1,name):
    c = ROOT.TCanvas()
    c.SetGrid()
    
    #h1.SetStats(0)

    h1.SetLineWidth(2)
    h1.Draw("hist")
    c.Print("peds/h1_"+name+".pdf")
    if not subtractQIE:
        c.Print("peds/h1_"+name+".pdf")
    else:
        c.Print("peds/h1_sub"+name+".pdf")

ch = ROOT.TChain("hcalTupleTree/tree")
ch.Add(inputdir+filename)
ents=str(ch.GetEntries())
print(ents)

run = filename.split(".root")[0][-6:]
filename=filename.replace(".root","")#.split("/")[-1]
subname=subname.replace(".root","")
if not subtractQIE:
    outFile=ROOT.TFile("hists/hists_"+filename+".root","RECREATE")
else: 
    outFile=ROOT.TFile("hists/hists_sub_"+filename+"_negieta.root","RECREATE")
    #outFile=ROOT.TFile("hists/hists_sub_"+filename+"_ieta23.root","RECREATE")
print 'filename: ' +filename
print 'run '+run
#outFile=ROOT.TFile("hists_"+filename+".root","RECREATE")
print(ch.GetEntries())




h2 = ROOT.TH2F("h2","",nieta,minieta,minieta+nieta,ndepth*niphi,niphi*mindepth+miniphi,niphi*mindepth+miniphi+ndepth*niphi)
h2.Sumw2()
if subtractQIE:
    q_ch = ROOT.TChain("hcalTupleTree/tree")
    q_ch.Add(qieRun)
    q_ents=str(q_ch.GetEntries())
    q_h2 = ROOT.TH2F("h2_qie","",nieta,minieta,minieta+nieta,ndepth*niphi,niphi*mindepth+miniphi,niphi*mindepth+miniphi+ndepth*niphi)
    q_h2.Sumw2()

nbins = 50
minx=0
maxx=500
unit="fC"

h1_3p3 = ROOT.TH1F("h1_3p3_"+run,";Mean 8TS pedestal sum ["+unit+"]; Number of channels",nbins,minx,maxx)
h1_2p8 = ROOT.TH1F("h1_2p8_"+run,";Mean 8TS pedestal sum ["+unit+"]; Number of channels",nbins,minx,maxx)
h1e_2p8 = ROOT.TH1F("h1e_2p8_"+run,";Error on mean 8TS pedestal sum ["+unit+"]; Number of channels",12,0,6)
h1e_3p3 = ROOT.TH1F("h1e_3p3_"+run,";Error on mean 8TS pedestal sum ["+unit+"]; Number of channels",12,0,6)

h1_2p8.StatOverflows(True)
h1_3p3.StatOverflows(True)
h1e_2p8.StatOverflows(True)
h1e_3p3.StatOverflows(True)

if unit=="fC": unit="FC"

ch.Project("h2","72*QIE11DigiDepth+QIE11DigiIPhi:QIE11DigiIEta","1/("+ents+".)*(QIE11DigiFC[][0]+QIE11DigiFC[][1]+QIE11DigiFC[][2]+QIE11DigiFC[][3]+QIE11DigiFC[][4]+QIE11DigiFC[][5]+QIE11DigiFC[][6]+QIE11DigiFC[][7])")

printTH2(h2,filename+"_"+unit+"")
q_ch.Project("h2_qie","72*QIE11DigiDepth+QIE11DigiIPhi:QIE11DigiIEta","1/("+ents+".)*(QIE11DigiFC[][0]+QIE11DigiFC[][1]+QIE11DigiFC[][2]+QIE11DigiFC[][3]+QIE11DigiFC[][4]+QIE11DigiFC[][5]+QIE11DigiFC[][6]+QIE11DigiFC[][7])")

for x in range(1,1+h2.GetNbinsX()):
    for y in range(1,1+h2.GetNbinsY()):
        if(h2.GetBinContent(x,y)>0):
            mean = h2.GetBinContent(x,y)
            meanerr= h2.GetBinError(x,y)
            if subtractQIE:
                mean = mean - q_h2.GetBinContent(x,y)
                meanerr = pow(pow(meanerr,2)+pow(q_h2.GetBinError(x,y),2),0.5)

            eta=x+minieta-1
            yvalue = niphi*mindepth+miniphi+y-1
            iphi = (yvalue-miniphi)%niphi+miniphi
            depth = (yvalue-iphi)/72
            #if(mean<100):
            #print ' Eta' +str(eta) +' phi '+ str(iphi)+ ' depth ' + str(depth)+ ' mean ' + str(mean)
            isiphi=(iphi>30 and iphi<40)
            is3p3 = (eta>=-17 or (eta==-18 and depth==5))
            if is3p3:
                if(isiphi): print '3.3mm SiPM Eta '+str(eta)+ ' iphi '+ str(iphi)+ ' depth ' +str(depth)+ ' charge '+str(mean)
                h1_3p3.Fill(mean)
            else:
                if(isiphi): print '2.8mm SiPM Eta '+str(eta)+ ' iphi '+ str(iphi)+ ' depth ' +str(depth)+ ' charge '+str(mean)
                h1_2p8.Fill(mean)

printTH1(h1_2p8,filename+"_"+unit+"_2p8")
printTH1(h1_3p3,filename+"_"+unit+"_3p3")
h1_3p3.Write()
h1_2p8.Write()
outFile.Save()
outFile.Close()









