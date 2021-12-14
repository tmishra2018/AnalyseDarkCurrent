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
inputdir = "iphi/"
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
niphi = 72
miniphi= 1
#h2 = ROOT.TH2F("h2","",niphi,miniphi,miniphi+niphi,len(doses),array("d",doses),array("d",means_2p8))
#h3 = ROOT.TH2F("h3","",niphi,miniphi,miniphi+niphi,len(doses),array("d",doses),array("d",means_3p3))

for iphi_l in range(miniphi, miniphi+niphi):
    means_3p3 = []
    meanse_3p3 = []
    means_2p8 = []
    meanse_2p8 = []

##### This makes a summary table of the currents and luminosities
##### Also loads the currents into memory for making the TGraph later
    csvFile = open("dark_current_lumi_time_posieta_all_iphi.csv","w")
    #csvFile = open("dark_current_lumi_time_negieta_all_iphi.csv","w")
    csvFile.write("Run Number,Time [days since June 18],Integrated luminosity [/fb],Average 2.8mm dark current [uA],uncertainty,Average 3.3mm dark current [uA],uncertainty\n")
    for i,run in enumerate(runs):

        #filename = inputdir+"hists_sub_HcalTupleMaker_run"+run+"_negieta_iphi_"+str(iphi_l)+".root"
        filename = inputdir+"hists_sub_HcalTupleMaker_run"+run+"_posieta_iphi_"+str(iphi_l)+".root"

        file = ROOT.TFile(filename,"READ")

        h_3p3 = file.Get("h1_3p3_"+str(iphi_l)+"_"+run)
        h_2p8 = file.Get("h1_2p8_"+str(iphi_l)+"_"+run)

        means_3p3.append(h_3p3.GetMean()/200.)
        means_2p8.append(h_2p8.GetMean()/200.)
        meanse_3p3.append(h_3p3.GetMeanError()/200.)
        meanse_2p8.append(h_2p8.GetMeanError()/200.)
        print 'SiPM run '+str(run)+' mean '+str(h_3p3.GetMean())+ ' mean/200 '+str(h_3p3.GetMean()/200.)
        
        csvFile.write(",".join([run,str(int(days[i])),str(round(doses[i],1)),str(round(means_3p3[i],3)),str(round(meanse_3p3[i],3)),str(round(means_2p8[i],3)),str(round(meanse_2p8[i],3))]))
        csvFile.write("\n")

    csvFile.close()
    
    print("doses, "+str(len(doses)))#+" range "+(*means_3p3))
    #print(*means_3p3)
    graph_3p3 = ROOT.TGraphErrors(len(doses),array("d",doses),array("d",means_3p3),array("d",doseserr),array("d",meanse_3p3))
    graph_2p8 = ROOT.TGraphErrors(len(doses),array("d",doses),array("d",means_2p8),array("d",doseserr),array("d",meanse_2p8))
    
    graph_2p8.SetTitle(";Integrated luminosity [fb^{-1}];Average SiPM dark current [#muA]")
    graph_3p3.SetTitle(";Integrated luminosity [fb^{-1}];Average SiPM dark current [#muA]")
    
    graph_3p3.SetLineColor(colors[1])
    graph_3p3.SetLineStyle(2)
    graph_3p3.SetMarkerColor(colors[1])
    graph_3p3.SetMarkerSize(1)
    graph_3p3.SetMarkerStyle(20)

    graph_2p8.SetLineColor(colors[2])
    graph_2p8.SetLineStyle(2)
    graph_2p8.SetMarkerColor(colors[2])
    graph_2p8.SetMarkerSize(1)
    graph_2p8.SetMarkerStyle(20)
    
    c = ROOT.TCanvas()
    c.SetGridx()
    c.SetGridy()
    graph_3p3.SetMinimum(0)
    graph_2p8.SetMinimum(0)
    
    c = ROOT.TCanvas()
    c.SetGridx()
    c.SetGridy()

    graph_3p3.Draw("AELPZ")
    graph_2p8.Draw("ELPZ same")

    funcs=[]
    for i,range in enumerate(fitRange):
        name = "f3p30_"+str(i)

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
        graph_2p8.Fit(name,"R")
        print 'NDF ' +str(f2.GetChisquare())
        funcs.append(f2)
        print -1./f2.GetParameter(1),-1./(f2.GetParameter(1)+f2.GetParError(1))+1./f2.GetParameter(1),-1./(f2.GetParameter(1)-f2.GetParError(1))+1./f2.GetParameter(1)
        

        for f in funcs:
            f.Draw("same")
        
    tla = ROOT.TLatex()
    tla.SetTextSize(0.05)
    tla.DrawLatexNDC(0.14,0.91,"#font[62]{CMS} #scale[0.8]{#font[52]{Preliminary 2018}}")
    tla.DrawLatexNDC(0.64,0.91,"ieta=+ve and iphi="+str(iphi_l))

    leg3 = ROOT.TLegend(0.30,0.70,0.56,0.91)
    leg3.SetTextFont(43)
    leg3.SetTextSize(16)
    leg3.SetFillColor(0)
    leg3.SetBorderSize(0)
    leg3.SetFillStyle(0)
    leg3.AddEntry(f1,"3.3 mm SiPM","l")
    leg3.AddEntry(f2,"2.8 mm SiPM","l")

    leg3.Draw()
    outname="plots_iphi/fit_raddam_gsel0_ieta_positive_iphi_"+str(iphi_l)+".pdf"
    #outname="plots_iphi/fit_raddam_gsel0_ieta_negitive_iphi_"+str(iphi_l)+".pdf"
    

    c.Print(outname)
    c.Close()
