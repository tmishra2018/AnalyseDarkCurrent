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
#timeMode=False
timeMode=True
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
    fitRange=[[72,600]]
    #fitRange=[[0,49],[49,70],[72,600]]
    
##### Load the luminosity information
#with open("LumiList_ex.txt") as lumilist:
with open("LumiList_new.txt") as lumilist:
    for line in lumilist:
        runs.append(line.split()[0])
        doses.append(float(line.split()[1]))
        doseserr.append(0.01*float(line.split()[1]))
        days.append(float(line.split()[3]))
        dayserr.append(0.2)




#### holders for mean dark currents
#### 3.3 mm and 2.8 mm channels are treated separately
means_3p3 = []
means_2p8 = []
meanse_3p3 = []
meanse_2p8 = []

##### This makes a summary table of the currents and luminosities
##### Also loads the currents into memory for making the TGraph later

#csvFile = open("dark_current_lumi_time_newsub_pos_315068.csv","w")
csvFile = open("dark_current_lumi_time_newsub_neg_315068.csv","w")
#csvFile = open("dark_current_lumi_time_newsub_330853.csv","w")
#csvFile = open("dark_current_lumi_time_newsub_neg_331425.csv","w")
#csvFile = open("dark_current_lumi_time_newsub_neg_330959.csv","w")
#csvFile = open("dark_current_lumi_time_newsub_po_331425.csv","w")
#csvFile = open("dark_current_lumi_time_newsub_pos_330959.csv","w")
#csvFile = open("dark_current_lumi_time_oldsub.csv","w")
csvFile.write("Run Number,Time [days since June 18],Integrated luminosity [/fb],Average 2.8mm dark current [uA],uncertainty,Average 3.3mm dark current [uA],uncertainty\n")
for i,run in enumerate(runs):

    #print("looping ",loop," sub ",sub, " i ",i )
    if i < 54:
        filename = inputdir+"hists_sub_HcalTupleMaker_run"+run+"_posieta_sub_315068.root"
    else:
        filename = inputdir+"hists_sub_HcalTupleMaker_run"+run+"_posieta_sub_330506.root"

    #filename = inputdir+"hists_sub_HcalTupleMaker_run"+run+"_posieta_sub_315068.root"
    #filename = inputdir+"hists_sub_HcalTupleMaker_run"+run+"_posieta_sub_331425.root"

    #filename = inputdir+"hists_sub_HcalTupleMaker_run"+run+"_negieta_sub_315068.root"
    #filename = inputdir+"hists_sub_HcalTupleMaker_run"+run+"_posieta_oldsub.root"
    #filename = inputdir+"hists_sub_HcalTupleMaker_run"+run+"_posieta_sub_330959.root"
    #filename = inputdir+"hists_sub_HcalTupleMaker_run"+run+"_posieta_sub_330319.root"
    #filename = inputdir+"hists_sub_HcalTupleMaker_run"+run+"_posieta_sub_331425.root"
    #filename = inputdir+"hists_sub_HcalTupleMaker_run"+run+"_negieta_sub_331425.root"
    #filename = inputdir+"hists_sub_HcalTupleMaker_run"+run+"_negieta_sub_330959.root"
    #filename = inputdir+"hists_sub_HcalTupleMaker_run"+run+"_posieta.root"
    #filename = inputdir+"hists_sub_HcalTupleMaker_run"+run+"_negieta.root"
    #filename = inputdir+"hists_sub_HcalTupleMaker_run"+run+"_negieta_sub_331425.root"
    #filename = inputdir+"hists_sub_HcalTupleMaker_run"+run+"_negieta_sub_330959.root"
    file = ROOT.TFile(filename,"READ")
    print filename
    h_3p3 = file.Get("h1_3p3_"+run)
    h_2p8 = file.Get("h1_2p8_"+run)
    print ("3p3 mean "+str(h_3p3.GetMean()))
    print ("2p8 mean "+str(h_2p8.GetMean()))
    means_3p3.append(h_3p3.GetMean()/200.)
    means_2p8.append(h_2p8.GetMean()/200.)
    #means_3p3.append(h_3p3.GetMean())
    #means_2p8.append(h_2p8.GetMean())
    print(means_2p8[-1],doses[i])
    meanse_3p3.append(h_3p3.GetMeanError()/200.)
    meanse_2p8.append(h_2p8.GetMeanError()/200.)
    #meanse_3p3.append(h_3p3.GetMeanError())
    #meanse_2p8.append(h_2p8.GetMeanError())

    csvFile.write(",".join([run,str(int(days[i])),str(round(doses[i],1)),str(round(means_2p8[i],3)),str(round(meanse_2p8[i],3)),str(round(means_3p3[i],3)),str(round(meanse_3p3[i],3))]))
    csvFile.write("\n")


csvFile.close()

if timeMode:
    graph_2p8 = ROOT.TGraphErrors(len(days),array("d",days),array("d",means_2p8),array("d",dayserr),array("d",meanse_2p8))
    graph_3p3 = ROOT.TGraphErrors(len(days),array("d",days),array("d",means_3p3),array("d",dayserr),array("d",meanse_3p3))
    graph_2p8.SetTitle(";Time [Days since Jan 29];Average SiPM dark current [#muA]")
    graph_3p3.SetTitle(";Time [Days since Jan 29];Average SiPM dark current [#muA]")

    graph_lvt = ROOT.TGraphErrors(len(days),array("d",days),array("d",[0.02*x for x in doses]),array("d",dayserr),array("d",[0.02*x for x in doseserr]))
    graph_lvt.SetTitle(";Time [Days since Jan 29]; Integrated luminosity [100 fb^{-1}]")
    graph_lvt.SetMarkerColor(922)
    graph_lvt.SetLineColor(922)
    graph_lvt.SetLineStyle(2)
    graph_lvt.SetMarkerSize(1)
    graph_lvt.SetMarkerStyle(20)

else:
    graph_2p8 = ROOT.TGraphErrors(len(doses),array("d",doses),array("d",means_2p8),array("d",doseserr),array("d",meanse_2p8))
    graph_3p3 = ROOT.TGraphErrors(len(doses),array("d",doses),array("d",means_3p3),array("d",doseserr),array("d",meanse_3p3))
    graph_2p8.SetTitle(";Integrated luminosity [fb^{-1}];Average SiPM dark current [#muA]")
    graph_3p3.SetTitle(";Integrated luminosity [fb^{-1}];Average SiPM dark current [#muA]")

one = ROOT.TColor(20001,0.906,0.153,0.094)
two = ROOT.TColor(20002,0.906,0.533,0.094)
three = ROOT.TColor(20003,0.086,0.404,0.576)
four =ROOT.TColor(20004,0.071,0.694,0.18)
five =ROOT.TColor(20005,0.388,0.098,0.608)
six=ROOT.TColor(20006,0.906,0.878,0.094)
colors = [1,20003,20001,20002,20004,20005,20006,2,3,4,6,7,5,1,8,9,29,38,46]


graph_2p8.SetLineStyle(2)
graph_2p8.SetLineColor(2)#red
graph_2p8.SetMarkerColor(2)
graph_2p8.SetMarkerSize(1)
graph_2p8.SetMarkerStyle(20)


graph_3p3.SetLineStyle(4)
graph_3p3.SetLineColor(4)#blue
graph_3p3.SetMarkerColor(4)
graph_3p3.SetMarkerSize(1)
graph_3p3.SetMarkerStyle(20)

c = ROOT.TCanvas()
c.SetGridx()
c.SetGridy()
graph_3p3.SetMinimum(0)
graph_3p3.SetMaximum(6)
# if timeMode:
#     graph_3p3.GetXaxis().SetLimits(-1,110)
#     graph_lvt.Draw("AELPZ")
#     c.Print("lumi_vs_time.pdf")

graph_3p3.Draw("AELPZ")
graph_2p8.Draw("ELPZ same")
#graph_2p8.Draw("AELPZ")
#if timeMode:
    #graph_lvt.Draw("ELPZ same")
#
if (not timeMode):
    funcs=[]
    for i,range in enumerate(fitRange):
        name = "f2p8_"+str(i)
        print name
        f1 = ROOT.TF1(name,"pol1",range[0],range[1])
        f1.SetParameter(0,0.01)
        f1.SetParameter(1,2.90919e-02)
        f1.SetLineStyle(1)
        f1.SetLineColor(2)
        print("2.8 mm SiPMs, range "+str(i))
        graph_2p8.Fit(name,"R")
        print 'NDF ' +str(f1.GetNDF())
        funcs.append(f1)
        print -1./f1.GetParameter(1),-1./(f1.GetParameter(1)+f1.GetParError(1))+1./f1.GetParameter(1),-1./(f1.GetParameter(1)-f1.GetParError(1))+1./f1.GetParameter(1)
        
        
        name = "f3p3_"+str(i)
        f2 = ROOT.TF1(name,"pol1",range[0],range[1])
        f2.SetParameter(0,0.01)
        f2.SetParameter(1,2.90919e-02)
        f2.SetLineStyle(1)
        f2.SetLineColor(4)
        print("3.3 mm SiPMs, range "+str(i))
        graph_3p3.Fit(name,"R")
        print 'NDF ' +str(f2.GetChisquare())
        funcs.append(f2)
        print -1./f2.GetParameter(1),-1./(f2.GetParameter(1)+f2.GetParError(1))+1./f2.GetParameter(1),-1./(f2.GetParameter(1)-f2.GetParError(1))+1./f2.GetParameter(1)
        
#     elif i==1:
#         name = "f2p8_expo_"+str(i)
#         f3 = ROOT.TF1(name,"expo",range[0],range[1])
#         f3.SetParameter(0,0.01)
#         f3.SetParameter(1,2.90919e-02)
#         f3.SetLineStyle(9)
#         f3.SetLineColor(colors[1])
#         graph_2p8.Fit(name,"R")
#         funcs.append(f3)
    
#         name = "f3p3_expo_"+str(i)
#         f4 = ROOT.TF1(name,"expo",range[0],range[1])
#         f4.SetParameter(0,0.01)
#         f4.SetParameter(1,2.90919e-02)
#         f4.SetLineStyle(9)
#         f4.SetLineColor(20002)
#         graph_3p3.Fit(name,"R")
#         funcs.append(f4)
        

       # for f in funcs:
        #    f.Draw("same")
        
tla = ROOT.TLatex()
tla.SetTextSize(0.05)
tla.DrawLatexNDC(0.14,0.91,"#font[62]{CMS} #scale[0.8]{#font[52]{Preliminary 2019}}")
#if timeMode: outname = "fit_raddam_gsel0_sub_vs_time_pos_newsub_331425.pdf"
#if timeMode: outname = "fit_raddam_gsel0_sub_vs_time_pos_newsub_330959.pdf"
#if timeMode: outname = "fit_raddam_gsel0_sub_vs_time_pos_newsub_330853.pdf"
#if timeMode: outname = "fit_raddam_gsel0_sub_vs_time_pos_newsub_330319.pdf"
#if timeMode: outname = "fit_raddam_gsel0_sub_vs_time_neg_newsub_331425.pdf"
#if timeMode: outname = "fit_raddam_gsel0_sub_vs_time_neg_newsub_330959.pdf"
#if timeMode: outname = "fit_raddam_gsel0_sub_vs_time_neg_newsub_315068.pdf"
#if timeMode: outname = "fit_raddam_gsel0_sub_vs_time_neg_newsub_330506.pdf"
if timeMode: outname = "fit_raddam_gsel0_sub_vs_time_pos_newsub_330506.pdf"
#if timeMode: outname = "fit_raddam_gsel0_sub_vs_time_pos_newsub_315068.pdf"


#if timeMode: outname = "fit_raddam_gsel0_sub_vs_time_pos_oldsub.pdf"

#outname="fit_raddam_gsel0_ieta17_odddepth.pdf"
#else: outname="fit_raddam_gsel0_ieta_negative.pdf"
#else: outname="fit_raddam_gsel0_ieta_positive.pdf"
else: outname="fit_raddam_gsel0_ieta_positive_newsub.pdf"
#outname="fit_raddam_gsel0_ieta17.pdf"

c.Print(outname)
c.Close()
