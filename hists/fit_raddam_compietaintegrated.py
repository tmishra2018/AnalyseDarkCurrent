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

#### Time mode: change X axis from
timeMode=False
zoomTS2=False
zoomNov=False
inputdir = ""
runs=[]
doses= []
doseserr= []
days=[]
dayserr=[]

#### Break apart the linear fit into 3 distinct regions, independent fits
fitRange = [[0,23], 
[23.7,31]] #adjust lumi in LumiList.txt by hand for first run at start of TS2 to put it in this range
#[25,49.5]]
#fitRange = [[0,7.3]] ### fb-1

##### Load the luminosity information
with open("LumiList.txt") as lumilist:
    for line in lumilist:
        runs.append(line.split()[0])
        doses.append(float(line.split()[1]))
        doseserr.append(0.01*float(line.split()[1]))
        days.append(float(line.split()[3]))
        dayserr.append(0.2)


one = ROOT.TColor(20001,0.906,0.153,0.094)
two = ROOT.TColor(20002,0.906,0.533,0.094)
three = ROOT.TColor(20003,0.086,0.404,0.576)
four =ROOT.TColor(20004,0.071,0.694,0.18)
five =ROOT.TColor(20005,0.388,0.098,0.608)
six=ROOT.TColor(20006,0.906,0.878,0.094)
colors = [1,20003,20001,20002,20004,20005,20006,2,3,4,6,7,5,1,8,9,29,38,46]

nieta = 14
minieta = 16
niphi = 4
miniphi= 63
ndepth = 7
mindepth = 1

#### holders for mean dark currents
#### 3.3 mm and 2.8 mm channels are treated separately
means_3p30 = []
means_3p31 = []
means_3p32 = []
meanse_3p30 = []
meanse_3p31 = []
meanse_3p32 = []

##### This makes a summary table of the currents and luminosities
##### Also loads the currents into memory for making the TGraph later
csvFile = open("dark_current_lumi_time.csv","w")
csvFile.write("Run Number,Time [days since June 9],Integrated luminosity [/fb],Average 3.3mm dark current depth1 [uA],uncertainty,Average 3.3mm dark current depth3[uA],uncertainty,Average 3.3mm dark current depth5[uA],uncertainty\n")
for i,run in enumerate(runs):
    #filename = inputdir+"hists_sub_SPE_gsel0_"+run+".root"
    #filename = inputdir+"hists_sub_HcalTupleMaker_run"+run+"_sp17.root"
    filename = inputdir+"hists_sub_HcalTupleMaker_run"+run+"_ietaintegrated.root"

    file = ROOT.TFile(filename,"READ")
    print filename
    h_3p30 = file.Get("h1_3p30_"+run)
    h_3p31 = file.Get("h1_3p31_"+run)
    h_3p32 = file.Get("h1_3p32_"+run)

    means_3p30.append(h_3p30.GetMean()/200.)
    means_3p31.append(h_3p31.GetMean()/200.)
    means_3p32.append(h_3p32.GetMean()/200.)

    meanse_3p30.append(h_3p30.GetMeanError()/200.)
    meanse_3p31.append(h_3p31.GetMeanError()/200.)
    meanse_3p32.append(h_3p32.GetMeanError()/200.)

    csvFile.write(",".join([run,str(int(days[i])),str(round(doses[i],1)),str(round(means_3p30[i],3)),str(round(meanse_3p30[i],3)),str(round(means_3p31[i],3)),str(round(meanse_3p31[i],3)),str(round(means_3p31[i],3)),str(round(meanse_3p32[i],3))]))
    csvFile.write("\n")


csvFile.close()



#graph_2p8 = ROOT.TGraphErrors(len(doses),array("d",doses),array("d",means_2p8),array("d",doseserr),array("d",meanse_2p8))
graph_3p30 = ROOT.TGraphErrors(len(doses),array("d",doses),array("d",means_3p30),array("d",doseserr),array("d",meanse_3p30))
graph_3p31 = ROOT.TGraphErrors(len(doses),array("d",doses),array("d",means_3p31),array("d",doseserr),array("d",meanse_3p31))
graph_3p32 = ROOT.TGraphErrors(len(doses),array("d",doses),array("d",means_3p32),array("d",doseserr),array("d",meanse_3p32))
#graph_2p8.SetTitle(";Integrated luminosity [fb^{-1}];Average SiPM dark current [#muA]")
graph_3p30.SetTitle(";Integrated luminosity [fb^{-1}];Average SiPM dark current [#muA]")
graph_3p31.SetTitle(";Integrated luminosity [fb^{-1}];Average SiPM dark current [#muA]")
graph_3p32.SetTitle(";Integrated luminosity [fb^{-1}];Average SiPM dark current [#muA]")



graph_3p30.SetLineColor(colors[1])
graph_3p30.SetLineStyle(2)
graph_3p30.SetMarkerColor(colors[1])
graph_3p30.SetMarkerSize(1)
graph_3p30.SetMarkerStyle(20)

graph_3p31.SetLineColor(20002)
graph_3p31.SetLineStyle(2)
graph_3p31.SetMarkerColor(20002)
graph_3p31.SetMarkerSize(1)
graph_3p31.SetMarkerStyle(20)

graph_3p32.SetLineColor(20004)
graph_3p32.SetLineStyle(2)
graph_3p32.SetMarkerColor(20004)
graph_3p32.SetMarkerSize(1)
graph_3p32.SetMarkerStyle(20)

c = ROOT.TCanvas()
c.SetGridx()
c.SetGridy()
graph_3p30.SetMinimum(0)
graph_3p31.SetMinimum(0)
graph_3p32.SetMinimum(0)

graph_3p30.Draw("AELPZ")
graph_3p31.Draw("ELPZ same")
graph_3p32.Draw("ELP same")
#if (not timeMode) or zoomTS2 or zoomNov:
funcs=[]
for i,range in enumerate(fitRange):
    name = "f3p30_"+str(i)
    print name
    f1 = ROOT.TF1(name,"pol1",range[0],range[1])
    f1.SetParameter(0,0.01)
    f1.SetParameter(1,2.90919e-02)
    f1.SetLineStyle(9)
    f1.SetLineColor(colors[1])
    print("3.3 mm SiPMs, range "+str(i))
    graph_3p30.Fit(name,"R")
    print 'NDF ' +str(f1.GetNDF())
    funcs.append(f1)
    print -1./f1.GetParameter(1),-1./(f1.GetParameter(1)+f1.GetParError(1))+1./f1.GetParameter(1),-1./(f1.GetParameter(1)-f1.GetParError(1))+1./f1.GetParameter(1)

    name = "f3p31_"+str(i)
    f2 = ROOT.TF1(name,"pol1",range[0],range[1])
    f2.SetParameter(0,0.01)
    f2.SetParameter(1,2.90919e-02)
    f2.SetLineStyle(9)
    f2.SetLineColor(20002)
    print("3.3 mm SiPMs, range "+str(i))
    graph_3p31.Fit(name,"R")
    print 'NDF ' +str(f2.GetChisquare())
    funcs.append(f2)
    print -1./f2.GetParameter(1),-1./(f2.GetParameter(1)+f2.GetParError(1))+1./f2.GetParameter(1),-1./(f2.GetParameter(1)-f2.GetParError(1))+1./f2.GetParameter(1)

    name = "f3p32_"+str(i)
    f3 = ROOT.TF1(name,"pol1",range[0],range[1])
    f3.SetParameter(0,0.01)
    f3.SetParameter(1,2.90919e-02)
    f3.SetLineStyle(9)
    f3.SetLineColor(20004)
    print("3.3 mm SiPMs, range "+str(i))
    graph_3p32.Fit(name,"R")
    print 'NDF ' +str(f3.GetChisquare())
    funcs.append(f3)

for f in funcs:
    f.Draw("same")

tla = ROOT.TLatex()
tla.SetTextSize(0.05)
tla.DrawLatexNDC(0.14,0.91,"#font[62]{CMS} #scale[0.8]{#font[52]{Preliminary 2018}}")

outname="fit_raddam_gsel0_ietaintegrated.pdf"
#outname="fit_raddam_gsel0_ieta17.pdf"

c.Print(outname)
c.Close()
