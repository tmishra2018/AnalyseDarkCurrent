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
inputdir = "/afs/cern.ch/work/c/ckar/HCALWORK/hcal_noise_analysis/src/"; 
runs=[]
doses= []
doseserr= []
days=[]
dayserr=[]

#### Break apart the linear fit into 3 distinct regions, independent fits
fitRange = [[0,15.6], ### fb-1
			[15.6,24.115], #adjust lumi in LumiList.txt by hand for first run at start of TS2 to put it in this range
			[25,49.5]]
if timeMode:
	fitRange=[[0,180]]
	if zoomTS2: fitRange=[[97,106]]
	if zoomNov: fitRange =[[159,180]]


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
means_3p3 = []
means_2p8 = []
meanse_3p3 = []
meanse_2p8 = []

##### This makes a summary table of the currents and luminosities
##### Also loads the currents into memory for making the TGraph later
csvFile = open("dark_current_lumi_time.csv","w")
csvFile.write("Run Number,Time [days since June 9],Integrated luminosity [/fb],Average 2.8mm dark current [uA],uncertainty,Average 3.3mm dark current [uA],uncertainty\n")
for i,run in enumerate(runs):
	filename = inputdir+"hists_sub_SPE_gsel0_"+run+".root"
	file = ROOT.TFile(filename,"READ")
	h_3p3 = file.Get("h1_3p3_"+run)
	h_2p8 = file.Get("h1_2p8_"+run)

	means_3p3.append(h_3p3.GetMean()/200.)
	means_2p8.append(h_2p8.GetMean()/200.)

	print(means_2p8[-1],doses[i])
	meanse_3p3.append(h_3p3.GetMeanError()/200.)
	meanse_2p8.append(h_2p8.GetMeanError()/200.)

	csvFile.write(",".join([run,str(int(days[i])),str(round(doses[i],1)),str(round(means_2p8[i],3)),str(round(meanse_2p8[i],3)),str(round(means_3p3[i],3)),str(round(meanse_3p3[i],3))]))
	csvFile.write("\n")


csvFile.close()




if timeMode:
	graph_2p8 = ROOT.TGraphErrors(len(days),array("d",days),array("d",means_2p8),array("d",dayserr),array("d",meanse_2p8))
	graph_3p3 = ROOT.TGraphErrors(len(days),array("d",days),array("d",means_3p3),array("d",dayserr),array("d",meanse_3p3))
	graph_2p8.SetTitle(";Time [Days since June 9];Average SiPM dark current [#muA]")
	graph_3p3.SetTitle(";Time [Days since June 9];Average SiPM dark current [#muA]")

	graph_lvt = ROOT.TGraphErrors(len(days),array("d",days),array("d",[0.02*x for x in doses]),array("d",dayserr),array("d",[0.02*x for x in doseserr]))
	graph_lvt.SetTitle(";Time [Days since June 9]; Integrated luminosity [100 fb^{-1}]")
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



graph_2p8.SetLineColor(colors[1])
graph_2p8.SetLineStyle(2)
graph_2p8.SetMarkerColor(colors[1])
graph_2p8.SetMarkerSize(1)
graph_2p8.SetMarkerStyle(20)
graph_3p3.SetLineColor(20002)
graph_3p3.SetLineStyle(2)
graph_3p3.SetMarkerColor(20002)
graph_3p3.SetMarkerSize(1)
graph_3p3.SetMarkerStyle(20)



c = ROOT.TCanvas()
c.SetGridx()
c.SetGridy()
graph_3p3.SetMinimum(0)
if timeMode:
	graph_3p3.GetXaxis().SetLimits(-1,180)
	graph_lvt.Draw("AELPZ")
	c.Print("lumi_vs_time.pdf")
if zoomTS2 or zoomNov:
	graph_3p3.GetXaxis().SetLimits(fitRange[0][0]-1,fitRange[0][1]+1)

graph_3p3.Draw("AELPZ")
graph_2p8.Draw("ELPZ same")
if timeMode and not (zoomNov or zoomTS2):
	graph_lvt.Draw("ELPZ same")

if (not timeMode) or zoomTS2 or zoomNov:
	funcs=[]
	for i,range in enumerate(fitRange):
		name = "f2p8_"+str(i)
		if not zoomTS2 and not zoomNov: 
			f1 = ROOT.TF1(name,"pol1",range[0],range[1])
			f1.SetParameter(0,0.01)
			f1.SetParameter(1,2.90919e-02)
		elif zoomTS2:
			#f1 = ROOT.TF1(name,"exp([0]+[1]*x)",range[0],range[1])
			f1 = ROOT.TF1(name,"[0]*(0.45*exp([1]*(x-98))+0.55)",range[0],range[1])
			f1.SetParameter(0,0.45)
			f1.SetParameter(1,-1e-01)
			#f1.SetParameter(2,0.2)
			#f1.SetParLimits(2,0,0.25)
		elif zoomNov:
			#f1 = ROOT.TF1(name,"exp([0]+[1]*x)",range[0],range[1])
			f1 = ROOT.TF1(name,"[0]*(0.45*exp([1]*(x-160))+0.55)",range[0],range[1])
			f1.SetParameter(0,0.85)
			f1.SetParameter(1,-5e-03)
			#f1.SetParameter(2,0.2)
			#f1.SetParLimits(2,0,0.25)

		f1.SetLineStyle(9)
		f1.SetLineColor(colors[1])
		print("2.8 mm SiPMs, range "+str(i))
		graph_2p8.Fit(name,"R")
		funcs.append(f1)
		print -1./f1.GetParameter(1),-1./(f1.GetParameter(1)+f1.GetParError(1))+1./f1.GetParameter(1),-1./(f1.GetParameter(1)-f1.GetParError(1))+1./f1.GetParameter(1)

		name = "f3p3_"+str(i)
		if not zoomTS2 and not zoomNov: 
			f2 = ROOT.TF1(name,"pol1",range[0],range[1])
			f2.SetParameter(0,0.01)
			f2.SetParameter(1,2.90919e-02)
		elif zoomTS2:
			#f2 = ROOT.TF1(name,"exp([0]+[1]*x)",range[0],range[1])
			f2 = ROOT.TF1(name,"[0]*(0.45*exp([1]*(x-98))+0.55)",range[0],range[1])
			f2.SetParameter(0,0.65)
			f2.SetParameter(1,-1e-01)
			#f2.SetParameter(2,0.3)
			#f2.SetParLimits(2,0,0.35)
		elif zoomNov:
			#f2 = ROOT.TF1(name,"exp([0]+[1]*x)",range[0],range[1])
			f2 = ROOT.TF1(name,"[0]*(0.45*exp([1]*(x-160))+0.55)",range[0],range[1])
			f2.SetParameter(0,0.65)
			f2.SetParameter(1,-1e-01)
			#f2.SetParameter(2,0.3)
			#f2.SetParLimits(2,0,0.35)
			

		f2.SetLineStyle(9)
		f2.SetLineColor(20002)
		print("3.3 mm SiPMs, range "+str(i))
		graph_3p3.Fit(name,"R")
		funcs.append(f2)
		print -1./f2.GetParameter(1),-1./(f2.GetParameter(1)+f2.GetParError(1))+1./f2.GetParameter(1),-1./(f2.GetParameter(1)-f2.GetParError(1))+1./f2.GetParameter(1)

	for f in funcs:
		f.Draw("same")

tla = ROOT.TLatex()
tla.SetTextSize(0.05)
tla.DrawLatexNDC(0.14,0.91,"#font[62]{CMS} #scale[0.8]{#font[52]{Preliminary 2018}}")

outname="fit_raddam_gsel0_sub_range_3range.pdf"
if timeMode: outname = "fit_raddam_gsel0_sub_vs_time.pdf"
if zoomTS2: outname = "fit_raddam_gsel0_sub_vs_time_zoomTS2_const.pdf"
if zoomNov: outname = "fit_raddam_gsel0_sub_vs_time_zoomNov_const.pdf"

c.Print(outname)
c.Close()






