#include <TROOT.h>
#include "TMath.h"
#include <iostream>

#include "RooFit.h"
#include "TPaveText.h"
#include "TLegend.h"
#include "TLatex.h"
#include "TCut.h"

#include "TCanvas.h"
#include "TAxis.h"
#include "THStack.h"
#include "TStyle.h"
#include <map>
#include <string>

void plot_hist(){

  gStyle->SetOptTitle(0);
  //  gStyle->SetOptStat(0);
  gStyle->SetOptFit(1);

  using namespace std;

  TFile *priv=new TFile("hists_sub_HcalTupleMaker_run315992_posieta.root");
  TH1F * priv3p3431=(TH1F*)priv->Get("h1_3p3_315992");

  Int_t bin=priv3p3431->FindBin(400);
  priv3p3431->GetXaxis()->SetRange(0,bin);
  priv3p3431->GetXaxis()->SetTitle("Mean 8TS SiPM current[fC]");
  //priv3p3431->Draw();

  // TAxis *xold   = priv3p3431->GetXaxis();
//   Float_t xmin  = xold->GetXmin();
//   Float_t xmax  = xold->GetXmax();

//   TH1F *hnew =(TH1F*)priv3p3431->Clone();

//   // change name and axis specs
//   hnew->SetName("hnew");
//   TAxis *xnew   = hnew->GetXaxis();
//   xnew->Set(20,xmin,xmax);
//   hnew->Set(22);
  //  hnew->Draw();
  //return;
  TFile *priv2=new TFile("hists_sub_HcalTupleMaker_run317722_posieta.root");
  TH1F * priv3p3992=(TH1F*)priv2->Get("h1_3p3_317722");

  Int_t bin1=priv3p3992->FindBin(400);
  priv3p3992->GetXaxis()->SetRange(0,bin1);
  priv3p3992->SetLineColor(kRed);
  priv3p3992->GetXaxis()->SetTitle("Mean 8TS SiPM current[fC]");
  //priv3p3992->Draw();

  TFile *priv3=new TFile("hists_sub_HcalTupleMaker_run322239_posieta.root");
  TH1F * priv3p3104=(TH1F*)priv3->Get("h1_3p3_322239");

  Int_t bin2=priv3p3104->FindBin(400);
  priv3p3104->GetXaxis()->SetRange(0,bin2);
  priv3p3104->SetLineColor(kBlue);
  priv3p3104->GetXaxis()->SetTitle("Mean 8TS SiPM current[fC]");
  //priv3p3104->Draw();

  TH1F * priv2p8431=(TH1F*)priv->Get("h1_2p8_315992");
  Int_t bin3=priv2p8431->FindBin(400);
  priv2p8431->GetXaxis()->SetRange(0,bin3);
  //priv2p8431->Draw();                                                                                                                
  TH1F * priv2p8992=(TH1F*)priv2->Get("h1_2p8_317722");
  Int_t bin4=priv2p8992->FindBin(400);
  priv2p8992->GetXaxis()->SetRange(0,bin4);
  priv2p8992->SetLineColor(kRed);
  TH1F * priv2p8104=(TH1F*)priv3->Get("h1_2p8_322239");
  Int_t bin5=priv2p8104->FindBin(400);
  priv2p8104->GetXaxis()->SetRange(0,bin5);
  priv2p8104->SetLineColor(kBlue);

  priv2p8431->GetXaxis()->SetTitle("Mean 8TS SiPM current[fC]");
  priv2p8992->GetXaxis()->SetTitle("Mean 8TS SiPM current[fC]");
  priv2p8104->GetXaxis()->SetTitle("Mean 8TS SiPM current[fC]");

  priv2p8431->GetYaxis()->SetTitleOffset(1.25);
  priv2p8992->GetYaxis()->SetTitleOffset(1.25);
  priv2p8104->GetYaxis()->SetTitleOffset(1.25);
  priv3p3431->GetYaxis()->SetTitleOffset(1.25);
  priv3p3992->GetYaxis()->SetTitleOffset(1.25);
  priv3p3104->GetYaxis()->SetTitleOffset(1.25);

  priv2p8431->GetXaxis()->SetTitleOffset(1.0);
  //priv2p8431->GetXaxis()->SetLabelOffset(0.01);
  //priv2p8431->GetXaxis()->SetTitleSize(0.043);
  //priv2p8431->GetYaxis()->SetTitleSize(0.043);
  
  TCanvas* c=new TCanvas("c","canvas",1000,800);
  c->SetMargin(0.16,0.09,0.13,0.07);
  c->Divide(3,2);
  c->cd(1);
  priv3p3431->Draw();
  c->cd(2);
  priv3p3992->Draw();
  c->cd(3);
  priv3p3104->Draw();
  c->cd(4);
  priv2p8431->Draw();
  c->cd(5);
  priv2p8992->Draw();
  c->cd(6);
  priv2p8104->Draw();



//   THStack *hs = new THStack("hs","");
//   hs->Add(priv3p3431);
//   hs->Add(priv3p3992);
//   hs->Add(priv3p3104);
//   //  hs->GetXaxis()->SetTitle("Mean 8TS SIPM Current[fC]");
//   //hs->GetXaxis()->SetRange(0,bin2);
//   hs->Draw();
}
