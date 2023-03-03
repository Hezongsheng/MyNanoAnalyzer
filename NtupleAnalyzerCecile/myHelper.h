#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <utility>
#include <map>
#include <string>
#include "TH1F.h"
#include "TH2F.h"
#include "TTree.h"
#include "TFile.h"
#include "TSystem.h"
#include "TMath.h" //M_PI is in TMath
#include "TRandom3.h"
#include <TLorentzVector.h>


float TMass_F(float pt3lep, float px3lep, float py3lep, float met, float metPhi) {
    return sqrt(pow(pt3lep + met, 2) - pow(px3lep + met * cos(metPhi), 2) - pow(py3lep + met * sin(metPhi), 2));
}


void WriteHistToFileETau(TFile* myfile, std::vector<TH1F*> hist, std::string name, TString dir_name, TString uncertainties[27], TString fake_uncertainties[1], bool isMC, int nbhist, int nbhist_offset, bool write_uncertainties){
    TString postfix="";
    TDirectory *dir =myfile->mkdir(dir_name);
    dir->cd();
    if (!write_uncertainties) nbhist=1;
    for (int k=0; k<nbhist; ++k){
       for (int j=0; j<hist[k]->GetSize()-1; ++j){
         if (hist[k]->GetBinContent(j)<0) hist[k]->SetBinContent(j,0);
       }
       if (k<(27-nbhist_offset)) postfix=uncertainties[k];
       else postfix=fake_uncertainties[k-(27-nbhist_offset)];
       hist[k]->SetName(name.c_str()+postfix);
       hist[k]->Write();
    }
}

void WriteHistToFileMuTau(TFile* myfile, std::vector<TH1F*> hist, std::string name, TString dir_name, TString uncertainties[27], TString fake_uncertainties[1], bool isMC, int nbhist, int nbhist_offset, bool write_uncertainties){
    TString postfix="";
    TDirectory *dir =myfile->mkdir(dir_name);
    dir->cd();
    if (!write_uncertainties) nbhist=1;
    for (int k=0; k<nbhist; ++k){
       for (int j=0; j<hist[k]->GetSize()-1; ++j){
         if (hist[k]->GetBinContent(j)<0) hist[k]->SetBinContent(j,0);
       }
       if (k<(27-nbhist_offset)) postfix=uncertainties[k];
       else postfix=fake_uncertainties[k-(27-nbhist_offset)];
       hist[k]->SetName(name.c_str()+postfix);
       hist[k]->Write();
    }
}

void WriteHistToFileEMu(TFile* myfile, std::vector<TH1F*> hist, std::string name, TString dir_name, TString uncertainties[1], TString fake_uncertainties[1], bool isMC, int nbhist, int nbhist_offset, bool write_uncertainties){
    TString postfix="";
    TDirectory *dir =myfile->mkdir(dir_name);
    dir->cd();
    if (!write_uncertainties) nbhist=1;
    for (int k=0; k<nbhist; ++k){
       for (int j=0; j<hist[k]->GetSize()-1; ++j){
         if (hist[k]->GetBinContent(j)<0) hist[k]->SetBinContent(j,0);
       }
       if (k<(1-nbhist_offset)) postfix=uncertainties[k];
       else postfix=fake_uncertainties[k-(1-nbhist_offset)];
       hist[k]->SetName(name.c_str()+postfix);
       hist[k]->Write();
    }
}
