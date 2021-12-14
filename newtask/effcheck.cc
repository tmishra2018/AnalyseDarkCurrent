#include<iostream>
#include <vector>
#include <set>
#include <cmath>
#include <string>
#include <stdio.h>
#include <cstring>
#include "TString.h"
#include "TFile.h"
#include "TTree.h"
#include "TH1.h"
#include "THStack.h"
#include <stdlib.h>
#include <map>
#include "TH2.h"
using namespace std;
void effcheck(){

  TFile *fmc=new TFile("Reduce_BsToJpsiPhi_mc2016_private.root");
  TFile *fdata=new TFile("test_Reduce_BsTojpsiphi.root");
  TTree *tmc=(TTree*)fmc->Get("tr");
  TTree *tmc1=(TTree*)fmc->Get("tr1");
  
  TTree *t=(TTree*)fdata->Get("tr1");


  int nentry=tmc->GetEntries();
  cout<<"Entry;"<<nentry<<endl;
  Double_t m=0,treco,trecoe;
  double m3=0,mkk=0,psipt=0,phipt=0,chi2=0,tau=0,taue=0,pvip=0;
  float gt;
  double iso=0,pvips=0,chi2dof=0,docatrk=0,alpha=0,fls3d=0;
  int closetrk=0;
  Bool_t hlt=false;
  //  t->SetBranchAddress("*",0);
  t->SetBranchStatus("m",1);
  t->SetBranchAddress("m",&m);
  t->SetBranchAddress("m3",&m3);
  t->SetBranchAddress("mkk",&mkk);
  t->SetBranchAddress("psipt",&psipt);
  t->SetBranchAddress("phipt",&phipt);
  t->SetBranchAddress("chi2",&chi2);
  t->SetBranchAddress("tau",&tau);
  t->SetBranchAddress("taue",&taue);
  t->SetBranchAddress("iso",&iso);
  t->SetBranchAddress("pvips",&pvips);
  t->SetBranchAddress("chi2dof",&chi2dof);
  t->SetBranchAddress("docatrk",&docatrk);
  t->SetBranchAddress("alpha",&alpha);
  t->SetBranchAddress("fls3d",&fls3d);
  t->SetBranchAddress("pvip",&pvip);
  t->SetBranchAddress("closetrk",&closetrk);
  t->SetBranchAddress("hlt",&hlt);

  //  tmc1->SetBranchAddress("m",&m);
  tmc1->SetBranchAddress("m3",&m3);
  tmc1->SetBranchAddress("mkk",&mkk);
  tmc1->SetBranchAddress("psipt",&psipt);
  tmc1->SetBranchAddress("phipt",&phipt);
  tmc1->SetBranchAddress("chi2",&chi2);
  tmc1->SetBranchAddress("treco",&treco);
  tmc->SetBranchAddress("gt",&gt);
  tmc1->SetBranchAddress("trecoe",&trecoe);
  tmc1->SetBranchAddress("iso",&iso);
  tmc1->SetBranchAddress("pvips",&pvips);
  tmc1->SetBranchAddress("chi2dof",&chi2dof);
  tmc1->SetBranchAddress("docatrk",&docatrk);
  tmc1->SetBranchAddress("alpha",&alpha);
  tmc1->SetBranchAddress("fls3d",&fls3d);
  tmc1->SetBranchAddress("pvip",&pvip);
  tmc1->SetBranchAddress("closetrk",&closetrk);
  tmc1->SetBranchAddress("hlt",&hlt);            
  
  TH1D* htau=new TH1D("htau"," bfrhlt",50,0,10);
  htau->Sumw2();
  TH1D* htauwotct=new TH1D("htauwotct","tau_without_cut",50,0,10);
  htauwotct->Sumw2();

  TH1D* hsidebnd=new TH1D("hsidebnd"," Side band",50,0,10);
  hsidebnd->Sumw2();
  TH1D* hsignal=new TH1D("hsignal"," signal region",50,0,10);
  hsignal->Sumw2();



  TH1D* htauwthlt=new TH1D("htauwthlt","tau_withhlt_ cut",50,0,10);
  htauwthlt->Sumw2();
  TH1D* htaumc=new TH1D("htaumc","tau_mc",50,0,10);
  htaumc->Sumw2();
  TH1D* htauwotctmc=new TH1D("htauwtctmc","without_cut _mc",50,0,10);
  htauwotctmc->Sumw2();
  TH1D* htauwthltmc=new TH1D("htauwthltmc","with hlt mc",50,0,10);
  htauwthltmc->Sumw2();
  TH1D* hmcgtau=new TH1D("hmcgtau","gtau nocut",50,0,10);
  hmcgtau->Sumw2();
  TH1D* hltratiomc=new TH1D("hltratiomc","hlt ratio MC",50,0,10);
  TH1D* tauratio=new TH1D("tauratio","tau ratio",50,0,10);
  TH1D* tauwtctrat=new TH1D("tauwtctrat","hlt aftrcut/bfr cut Data~MC",50,0,10);
  TH1D* hltratio=new TH1D("hltratio","All cut after/bfr Data~Mc",50,0,10);
  TH1D* efficiency=new TH1D("efficiency","efficiency",50,0,10);
 
  
  for(Int_t i=0;i<nentry;i++){
       t->GetEntry(i);
    htau->Fill(tau);
    //    cout<<"bfr hlt"<<tau<<endl;
    if(hlt){
      //cout<<"after hlt"<<tau<<endl;
      htauwotct->Fill(tau);
         if(m3>3.05 &&m3<3.14 && mkk>1.01 &&mkk <1.03&&pvips<2 && docatrk > 0.015 && iso >0.80 && pvip <0.008 && closetrk <2.00 && chi2>0.02  && alpha<0.050 && fls3d >13 && psipt>7 && phipt >0.7)continue;

	 htauwthlt->Fill(tau);
	 if((m > 5.2 && m<5.26)||(m > 5.46 && m<5.52)){
	   //	   cout<<tau<<endl;
	   hsidebnd->Fill(tau);
	   //	   hsidebnd->Draw()
	 }
	 if((m > 5.30 && m<5.42)){
	   hsignal->Fill(tau);
	 }
	 

	 ///hsidebnd->Draw();
		//  cout<<"wirk "<<tau<<endl;
    }
  }
  hsignal->Add(hsidebnd,-1);
  ////.......................
  ////....MC.................
  ////.......................
  for(Int_t j=0;j<tmc1->GetEntries();j++){
    tmc1->GetEntry(j);
    htaumc->Fill(treco);
    if(hlt){
      htauwotctmc->Fill(treco);
      if(m3>3.05 &&m3<3.14 && mkk>1.01 &&mkk <1.03 && psipt>7 && phipt >0.7)continue;//&&pvips<2 && docatrk > 0.015 && iso >0.80 && pvip <0.008 && closetrk <2.00 && chi2>0.02  && alpha<0.050 && fls3d >13 )continue;
       htauwthltmc->Fill(treco);
      // cout<<"wirk "<<t<<endl;
      }
  }
  for(Int_t k=0 ;k<tmc->GetEntries();k++){
    tmc->GetEntry(k);
    hmcgtau->Fill(gt);
  }
  /*
  hsidebnd->Draw();
  //  tauratio->Divide(hsignal,htau,1,1,"B");
  tauwtctrat->Divide(htauwotctmc,htaumc,1,1,"B");
  //  htauwothlt->Add(htauwothltg,-1);
  hltratiomc->Divide(htauwthltmc,htaumc,1,1,"B");
  ////////////// hltratio->Divide(htauwthlt,htauwotct,1,1,"B");
  htauwthltmc->Draw();
  */
  TH1D* new=(TH1D*)hmcgtau->Clone("new");
  htauwthltmc->Add(hmcgtau,-1);
  efficiency->Divide(htauwthltmc,hmcgtau,1,1,"B");
  double taumc=htauwthltmc->Integral();  
  double gtauk=hmcgtau->Integral();
  tauratio->Divide(htauwthltmc,new,1,1,"B");

  //  hmcgtau->Scale(taumc/gtauk);
  //  hmcgtau->(htauwthltmc,-1); 
  //  double hltdata=hltratio->Integral();
  //double hltmc=hltratiomc->Integral();
  //  hmcgtau->Draw();
  //hltratiomc->Scale(hltdata/hltmc);
  /*
  hltratio->Draw();
  hltratiomc->SetLineColor(kGreen);
  hltratiomc->GetYaxis()->SetRange(0.4,1);
  hltratio->GetYaxis()->SetRange(0.4,1);
  hltratiomc->Draw("same");  
  *


  double dat= htauwthlt->Integral();
  double dat1=htauwthltmc->Integral();
  // htauwthltmc->Scale(dat/dat1);
  */
  htauwthltmc->Draw();
  //efficiency->Draw();
  TCanvas* cta=new TCanvas("cta","efficiency plot",600,600);
  //  hltratiomc->Draw();
  efficiency->Draw();
  //tauratio->SetLineColor(kRed);
  // htauwthltmc->SetAxisRange(0,7,"X");
  // htauwthlt->SetAxisRange(0,7,"X");
  //tauratio->Draw("same");


  cta->SaveAs("efficiency.pdf");



  cout<<"area"<<hltratio->GetEntries()<<endl;
  cout<<"areamc"<<hltratiomc->GetEntries()<<endl;
  
  /*  TEfficiency* pEff=0;
  if(TEfficiency::CheckConsistency(htauwothlt,htauwothltg))
    {
      pEff=new TEfficiency (htauwothlt,htauwothltg);
    }
  */
  TCanvas* chlt=new TCanvas("chlt","tau_cut/gtauNo_cuts",600,600);
  hltratiomc->Draw();
  // tauratio->Draw();
   //   tauratio->SetAxisRange(0,1,"Y");
   //tauwtctrat->SetLineColor(kRed);
   // tauwtctrat->SetAxisRange(0,1,"Y");
   //tauwtctrat->Draw("same");
   chlt->SaveAs("hlt ratio_plot.pdf");
   /*   TCanvas* chlt1=new TCanvas("chlt1","after allcuts/bfr allcuts",600,600);
   hltratio->Draw();
   hltratiomc->SetLineColor(kRed);
   hltratiomc->SetAxisRange(0.4,1,"Y");
   hltratio->SetAxisRange(0.4,1,"Y");
   hltratiomc->Draw("same");
   chlt1->SaveAs("Mc_data after cut/bfrcut.pdf");
   /*
  TFile f1("histo.root","recreate"); //Open file, then write histo to it.
  htau->Write();
  h->Write();
  htauwthlt->Write();
  h4->Write();
  htauwothlt->Write();
   */
  }
