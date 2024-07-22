//C, C++
#include <stdio.h>
#include <assert.h>
#include <stdlib.h>
#include <iostream>
#include <fstream>
#include <string>
#include <iomanip>
#include <math.h>

#include <time.h>

using namespace std;

void read_dose( TString dose_map_file_name, TH1D *h1_x, TH1D *h1_y, TH1D *h1_d, TH2D *h2_dose);

Int_t plots_dose(){

  Double_t x_l = 0.0;
  Double_t x_r = 100;
  Int_t nbinsx = 10000;

  Double_t y_l = 0.0;
  Double_t y_r = 100;
  Int_t nbinsy = 100;

  Double_t d_l = -3.0;
  Double_t d_r = 30;
  Int_t nbinsd = 1000;

  Double_t dose_binx = 1080;
  Double_t dose_pitch_x = 0.08477;
  Double_t dose_x0 = 0.0;
  Double_t dose_x_l = dose_x0 - dose_pitch_x/2.0;
  Double_t dose_x_r = dose_x0 + dose_pitch_x*(dose_binx-1) + dose_pitch_x/2.0;
  //
  Double_t dose_biny = 840;
  Double_t dose_pitch_y = 0.08477;
  Double_t dose_y0 = 0.0;
  Double_t dose_y_l = dose_y0 - dose_pitch_y/2.0;
  Double_t dose_y_r = dose_y0 + dose_pitch_y*(dose_biny-1) + dose_pitch_y/2.0;

  
  TH1D *h1_x = new TH1D("h1_x","h1_x",nbinsx, x_l, x_r);
  TH1D *h1_y = new TH1D("h1_y","h1_y",nbinsy, y_l, y_r);
  TH1D *h1_d = new TH1D("h1_d","h1_d",nbinsd, d_l, d_r);
  TH2D *h2_dose = new TH2D("h2_dose","h2_dose", dose_binx, dose_x_l, dose_x_r, dose_biny, dose_y_l, dose_y_r);
  
  read_dose( "2024-07-17_gafchromic_x_y_D.txt", h1_x, h1_y, h1_d, h2_dose);

  //h1_x->Draw();
  //h1_y->Draw();
  //h1_d->Draw();
  h2_dose->Draw("ZCOLOR");
  
  return 0;
}

void read_dose( TString dose_map_file_name, TH1D *h1_x, TH1D *h1_y, TH1D *h1_d, TH2D *h2_dose){
  cout<<" Reading --> "<<dose_map_file_name<<endl;
  ifstream myfile(dose_map_file_name.Data());
  Double_t x;
  Double_t y;
  Double_t d;
  string mot;
  if(myfile.is_open()){
    myfile>>mot>>mot>>mot>>mot;
    myfile>>mot>>mot>>mot;
    while(myfile>>x>>y>>d){
      h1_x->Fill(x);
      h1_y->Fill(y);
      h1_d->Fill(d);
      h2_dose->Fill(x,y,d);
    }
    myfile.close();
  }
}
