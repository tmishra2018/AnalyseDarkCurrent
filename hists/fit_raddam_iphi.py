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
#zoomTS2=False
#zoomNov=False
inputdir = ""
runs=[]
doses= []
doseserr= []
days=[]
dayserr=[]

#### Break apart the linear fit into 3 distinct regions, independent fits
fitRange = [[0,23], ### fb-1
[23.19,30.968],[30.9,53.86],[54,66.0]] #adjust lumi in LumiList.txt by hand for first run at start of TS2 to put it in this range
#[25,49]]
#fitRange = [[0,23],[23.19,66.44]] ### fb-1
if timeMode:
    fitRange=[[0,49],[49,70],[72,209]]

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


#### holders for mean dark currents
#### 3.3 mm and 2.8 mm channels are treated separately
means_3p3 = []
means_3p30 = []
means_3p31 = []
means_3p32 = []
meanse_3p3 = []
meanse_3p30 = []
meanse_3p31 = []
meanse_3p32 = []
means_3p3_oth = []
means_3p30_oth = []
means_3p31_oth = []
means_3p32_oth = []
meanse_3p3_oth = []
meanse_3p30_oth = []
meanse_3p31_oth = []
meanse_3p32_oth = []

##### This makes a summary table of the currents and luminosities
##### Also loads the currents into memory for making the TGraph later
csvFile = open("dark_current_lumi_time.csv","w")
csvFile.write("Run Number,Time [days since June 18],Integrated luminosity [/fb],Average 2.8mm dark current [uA],uncertainty,Average 3.3mm dark current [uA],uncertainty\n")
for i,run in enumerate(runs):
    #filename = inputdir+"hists_sub_HcalTupleMaker_run"+run+"_posieta_iphi.root"
    filename = inputdir+"hists_sub_HcalTupleMaker_run"+run+"_negieta_iphi.root"

    file = ROOT.TFile(filename,"READ")
    #print filename
    h_3p3 = file.Get("h1_3p3_"+run)
    h_3p30 = file.Get("h1_3p30_"+run)
    h_3p31 = file.Get("h1_3p31_"+run)
    h_3p32 = file.Get("h1_3p32_"+run)
    h_3p3_oth = file.Get("h1_3p3_oth_"+run)
    h_3p30_oth = file.Get("h1_3p30_oth_"+run)
    h_3p31_oth = file.Get("h1_3p31_oth_"+run)
    h_3p32_oth = file.Get("h1_3p32_oth_"+run)

    #print h_3p30.GetMean()
    means_3p3.append(h_3p3.GetMean()/200.)
    means_3p30.append(h_3p30.GetMean()/200.)
    means_3p31.append(h_3p31.GetMean()/200.)
    means_3p32.append(h_3p32.GetMean()/200.)
    means_3p3_oth.append(h_3p3_oth.GetMean()/200.)
    means_3p30_oth.append(h_3p30_oth.GetMean()/200.)
    means_3p31_oth.append(h_3p31_oth.GetMean()/200.)
    means_3p32_oth.append(h_3p32_oth.GetMean()/200.)

    meanse_3p3.append(h_3p3.GetMeanError()/200.)
    meanse_3p30.append(h_3p30.GetMeanError()/200.)
    meanse_3p31.append(h_3p31.GetMeanError()/200.)
    meanse_3p32.append(h_3p32.GetMeanError()/200.)
    meanse_3p3_oth.append(h_3p3_oth.GetMeanError()/200.)
    meanse_3p30_oth.append(h_3p30_oth.GetMeanError()/200.)
    meanse_3p31_oth.append(h_3p31_oth.GetMeanError()/200.)
    meanse_3p32_oth.append(h_3p32_oth.GetMeanError()/200.)
    

    csvFile.write(",".join([run,str(int(days[i])),str(round(doses[i],1)),str(round(means_3p3[i],3)),str(round(meanse_3p3[i],3)),str(round(means_3p30[i],3)),str(round(meanse_3p30[i],3)), str(round(means_3p3_oth[i],3)), str(round(meanse_3p3_oth[i],3)),str(round(means_3p30_oth[i],3)), str(round(meanse_3p30_oth[i],3)),str(round(means_3p31[i],3)),str(round(meanse_3p31[i],3)),str(round(means_3p31_oth[i],3)),str(round(meanse_3p31_oth[i],3)),str(round(means_3p32[i],3)),str(round(meanse_3p32[i],3)),str(round(means_3p32_oth[i],3)),str(round(meanse_3p32_oth[i],3))]))
    csvFile.write("\n")


csvFile.close()

graph_3p3 = ROOT.TGraphErrors(len(doses),array("d",doses),array("d",means_3p3),array("d",doseserr),array("d",meanse_3p3))
graph_3p30 = ROOT.TGraphErrors(len(doses),array("d",doses),array("d",means_3p30),array("d",doseserr),array("d",meanse_3p30))
graph_3p31 = ROOT.TGraphErrors(len(doses),array("d",doses),array("d",means_3p31),array("d",doseserr),array("d",meanse_3p31))
graph_3p32 = ROOT.TGraphErrors(len(doses),array("d",doses),array("d",means_3p32),array("d",doseserr),array("d",meanse_3p32))
graph_3p3_oth = ROOT.TGraphErrors(len(doses),array("d",doses),array("d",means_3p3_oth),array("d",doseserr),array("d",meanse_3p3_oth))
graph_3p30_oth = ROOT.TGraphErrors(len(doses),array("d",doses),array("d",means_3p30_oth),array("d",doseserr),array("d",meanse_3p30_oth))
graph_3p31_oth = ROOT.TGraphErrors(len(doses),array("d",doses),array("d",means_3p31_oth),array("d",doseserr),array("d",meanse_3p31_oth))
graph_3p32_oth = ROOT.TGraphErrors(len(doses),array("d",doses),array("d",means_3p32_oth),array("d",doseserr),array("d",meanse_3p32_oth))

#graph_2p8.SetTitle(";Integrated luminosity [fb^{-1}];Average SiPM dark current [#muA]")
graph_3p3.SetTitle(";Integrated luminosity [fb^{-1}];Average SiPM dark current [#muA]")
graph_3p30.SetTitle(";Integrated luminosity [fb^{-1}];Average SiPM dark current [#muA]")
graph_3p31.SetTitle(";Integrated luminosity [fb^{-1}];Average SiPM dark current [#muA]")
graph_3p32.SetTitle(";Integrated luminosity [fb^{-1}];Average SiPM dark current [#muA]")
graph_3p3_oth.SetTitle(";Integrated luminosity [fb^{-1}];Average SiPM dark current [#muA]")
graph_3p30_oth.SetTitle(";Integrated luminosity [fb^{-1}];Average SiPM dark current [#muA]")
graph_3p31_oth.SetTitle(";Integrated luminosity [fb^{-1}];Average SiPM dark current [#muA]")
graph_3p32_oth.SetTitle(";Integrated luminosity [fb^{-1}];Average SiPM dark current [#muA]")



graph_3p3.SetLineColor(colors[1])
graph_3p3.SetLineStyle(2)
graph_3p3.SetMarkerColor(colors[1])
graph_3p3.SetMarkerSize(1)
graph_3p3.SetMarkerStyle(20)

graph_3p30.SetLineColor(colors[1])
graph_3p30.SetLineStyle(2)
graph_3p30.SetMarkerColor(colors[1])
graph_3p30.SetMarkerSize(1)
graph_3p30.SetMarkerStyle(20)

graph_3p31.SetLineColor(colors[6])
graph_3p31.SetLineStyle(2)
graph_3p31.SetMarkerColor(colors[6])
graph_3p31.SetMarkerSize(1)
graph_3p31.SetMarkerStyle(20)

graph_3p32.SetLineColor(colors[7])
graph_3p32.SetLineStyle(2)
graph_3p32.SetMarkerColor(colors[7])
graph_3p32.SetMarkerSize(1)
graph_3p32.SetMarkerStyle(20)

graph_3p3_oth.SetLineColor(colors[2])
graph_3p3_oth.SetLineStyle(2)
graph_3p3_oth.SetMarkerColor(colors[2])
graph_3p3_oth.SetMarkerSize(1)
graph_3p3_oth.SetMarkerStyle(20)

graph_3p30_oth.SetLineColor(colors[2])
graph_3p30_oth.SetLineStyle(2)
graph_3p30_oth.SetMarkerColor(colors[2])
graph_3p30_oth.SetMarkerSize(1)
graph_3p30_oth.SetMarkerStyle(20)

graph_3p31_oth.SetLineColor(colors[3])
graph_3p31_oth.SetLineStyle(2)
graph_3p31_oth.SetMarkerColor(colors[3])
graph_3p31_oth.SetMarkerSize(1)
graph_3p31_oth.SetMarkerStyle(20)

graph_3p32_oth.SetLineColor(colors[4])
graph_3p32_oth.SetLineStyle(2)
graph_3p32_oth.SetMarkerColor(colors[4])
graph_3p32_oth.SetMarkerSize(1)
graph_3p32_oth.SetMarkerStyle(20)


c = ROOT.TCanvas()
c.SetGridx()
c.SetGridy()
graph_3p3.SetMinimum(0)
graph_3p30.SetMinimum(0)
graph_3p31.SetMinimum(0)
graph_3p32.SetMinimum(0)
graph_3p3_oth.SetMinimum(0)
graph_3p30_oth.SetMinimum(0)
graph_3p31_oth.SetMinimum(0)
graph_3p32_oth.SetMinimum(0)

c = ROOT.TCanvas()
c.SetGridx()
c.SetGridy()
#graph_3p30.Draw("AELPZ")
graph_3p3.Draw("AELPZ")
#graph_3p32.Draw("AELPZ")
#graph_3p30_oth.Draw("ELPZ same")
graph_3p3_oth.Draw("ELPZ same")
#graph_3p32_oth.Draw("ELPZ same")


#if (not timeMode):
funcs=[]
for i,range in enumerate(fitRange):
#     #if i!=1:
    name = "f3p30_"+str(i)
    #print name
    f1 = ROOT.TF1(name,"pol1",range[0],range[1])
    f1.SetParameter(0,0.01)
    f1.SetParameter(1,2.90919e-02)
    f1.SetLineStyle(9)
    f1.SetLineColor(colors[1])
    print("SiPMs, range "+str(i))
    graph_3p3.Fit(name,"R")
    print 'NDF ' +str(f1.GetNDF())
    funcs.append(f1)
    print -1./f1.GetParameter(1),-1./(f1.GetParameter(1)+f1.GetParError(1))+1./f1.GetParameter(1),-1./(f1.GetParameter(1)-f1.GetParError(1))+1./f1.GetParameter(1)
                
    name = "f3p3_"+str(i)
    f2 = ROOT.TF1(name,"pol1",range[0],range[1])
    f2.SetParameter(0,0.01)
    f2.SetParameter(1,2.90919e-02)
    f2.SetLineStyle(9)
    f2.SetLineColor(colors[2])
    print("SiPMs, range "+str(i))
    graph_3p3_oth.Fit(name,"R")
    print 'NDF ' +str(f2.GetChisquare())
    funcs.append(f2)
    print -1./f2.GetParameter(1),-1./(f2.GetParameter(1)+f2.GetParError(1))+1./f2.GetParameter(1),-1./(f2.GetParameter(1)-f2.GetParError(1))+1./f2.GetParameter(1)
        
# #     elif i==1:
# #         name = "f2p8_expo_"+str(i)
# #         f3 = ROOT.TF1(name,"expo",range[0],range[1])
# #         f3.SetParameter(0,0.01)
# #         f3.SetParameter(1,2.90919e-02)
# #         f3.SetLineStyle(9)
# #         f3.SetLineColor(colors[1])
# #         graph_2p8.Fit(name,"R")
# #         funcs.append(f3)
    
# #         name = "f3p3_expo_"+str(i)
# #         f4 = ROOT.TF1(name,"expo",range[0],range[1])
# #         f4.SetParameter(0,0.01)
# #         f4.SetParameter(1,2.90919e-02)
# #         f4.SetLineStyle(9)
# #         f4.SetLineColor(20002)
# #         graph_3p3.Fit(name,"R")
# #         funcs.append(f4)
        

    for f in funcs:
        f.Draw("same")
        
tla = ROOT.TLatex()
tla.SetTextSize(0.05)
tla.DrawLatexNDC(0.14,0.91,"#font[62]{CMS} #scale[0.8]{#font[52]{Preliminary 2018}}")

outname="fit_raddam_gsel0_ieta_negative_iphi.pdf"
#outname="fit_raddam_gsel0_ieta_positive.pdf"

c.Print(outname)
c.Close()
