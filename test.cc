mm_kin_pt>6.5 && mm_kin_vtx_chi2dof<2.2&& mm_doca<0.1 && mm_kin_sl3d>13&& mm_kin_slxy>3&& mm_kin_alpha<0.05&&mm_kin_pvip<0.008&&mm_kin_pvlip<99.0&&abs(mm_kin_pvip/mm_kin_pvipErr)<2.0&&abs(mm_kin_pvlip/mm_kin_pvlipErr)<99.0&&mm_docatrk>0.015&&mm_closetrk<2&&mm_iso>0.8&&mm_m1iso>0.8&&mm_m2iso>0.8&&mm_bdt>0.3&&mm_kin_mu1pt>4&&mm_kin_mu2pt>4&&abs(mm_kin_mu1eta)<1.4&&abs(mm_kin_mu2eta)<1.4

void test()
{
  TCanvas *c = new TCanvas("c","c",600, 400);

  TMultiGraph * mg = new TMultiGraph("mg","mg");

  const Int_t size = 10;
          
  double x[size];
  double y1[size];
  double y2[size];
  double y3[size];

  for ( int i = 0; i <  size ; ++i ) {
    x[i] = i;
    y1[i] = size - i;
    y2[i] = size - 0.5 * i;
    y3[i] = size - 0.6 * i;
  }

  TGraph * gr1 = new TGraph( size, x, y1 );
  gr1->SetName("gr1");
  gr1->SetTitle("graph 1");
  gr1->SetMarkerStyle(21);
  gr1->SetDrawOption("AP");
  gr1->SetLineColor(2);
  gr1->SetLineWidth(4);
  gr1->SetFillStyle(0);

  TGraph * gr2 = new TGraph( size, x, y2 );
  gr2->SetName("gr2");
  gr2->SetTitle("graph 2");
  gr2->SetMarkerStyle(22);
  gr2->SetMarkerColor(2);
  gr2->SetDrawOption("P");
  gr2->SetLineColor(3);
  gr2->SetLineWidth(4);
  gr2->SetFillStyle(0);

  TGraph * gr3 = new TGraph( size, x, y3 );
  gr3->SetName("gr3");
  gr3->SetTitle("graph 3");
  gr3->SetMarkerStyle(23);
  gr3->SetLineColor(4);
  gr3->SetLineWidth(4);
  gr3->SetFillStyle(0);

  mg->Add( gr1 );
  mg->Add( gr2 );

  gr3->Draw("ALP");
  mg->Draw("LP");
  c->BuildLegend();

  c->Print("multigraphleg.gif");
}
