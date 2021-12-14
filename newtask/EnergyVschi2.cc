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
void EnergyVschi2(){
  TFile *file=new TFile("HcalTupleMaker_323997_chi15.root");
  TTree *tmc=(TTree*)file->Get("hcalTupleTree/tree");

  TH2D* hEVsChi2=new TH2D("hEVschi2","",100,0.,100.,100,0.,100.);
  double HBHERecHitEnergy,HBHERecHitChi2;
  TH1D* HE=new TH1D("HE",";Enregy",100,0.,100.);
  TH1D* Hchi2=new TH1D("Hchi2",";Chi2",100,0.,100.);
  tmc->SetBranchAddress("HBHERecHitEnergy",&HBHERecHitEnergy);
  tmc->SetBranchAddress("HBHERecHitChi2",&HBHERecHitChi2);

  for(int k=0;k<tmc->GetEntries();k++){
    tmc->GetEntry(k);
    hEVsChi2->Fill(HBHERecHitChi2,HBHERecHitEnergy);
    HE->Fill(HBHERecHitEnergy);
    Hchi2->Fill(HBHERecHitChi2);
    //tmc->Draw("HBHERecHitEnergy:HBHERecHitChi2>>hEVsChi2");
  }
  //Hchi2->Draw();
  hEVsChi2->Draw();
}
