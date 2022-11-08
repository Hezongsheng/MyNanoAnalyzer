#include <TH2.h>
#include <TH2F.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <TGraph.h>
#include <TGraphAsymmErrors.h>
#include "TMultiGraph.h"
#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include <utility>
#include <stdio.h>
#include <TF1.h>
#include <TDirectoryFile.h>
#include <TRandom3.h>
#include "TLorentzVector.h"
#include "TString.h"
#include "TLegend.h"
#include "TH1F.h"
#include "THStack.h"
#include "TKey.h"
#include "THashList.h"
#include "THStack.h"
#include "TPaveLabel.h"
#include "TFile.h"
#include "TTree.h"
#include "TChain.h"
#include "TMath.h"
#include "TLine.h"
#include "TPaveText.h"
#include "tr_Tree.h"

//this code is used to plot data/MC comparison with data-driven estimated bkg with correction (rm not jetfaketau MC
//in anti-isolated region and only consider no jetfaketau MC in signal region )

using namespace std;



int main(int argc, char** argv) {
    gStyle->SetOptStat(0);
    gStyle->SetFrameLineWidth(1);
    gStyle->SetLineWidth(1);
    gStyle->SetOptStat(0);

    
    std::string variable = *(argv + 1);
    double plotmin = atof(*(argv+2));
    double plotmax = atof(*(argv+3));
    int nbins = atoi(*(argv+4));
    int log = atoi(*(argv+5));

    cout << "Try to compare data/MC of variable " << variable << endl;
    cout << "Plot minimum is " << plotmin << endl;
    cout << "Plot maximum is " << plotmax << endl;
    cout << "nbins " << nbins << endl;
    cout << "log scale " << log << endl;

    TFile *fout = new TFile(Form("~/eos/taug-2/nanoplots/mutau/after_sel/histo/histo%s_MT50.root",variable.c_str()),"recreate");


    vector<string> allsamplename = {"DYJetsToLL_M-50","TTTo2L2Nu","TTToHadronic","TTToSemiLeptonic","WJetsToLNu","WW","WZ","ZZTo2L2Nu",
        "ZZTo2Q2L_mllmin4p0","ZZTo4L","ST_t-channel_antitop_5f_InclusiveDecays","ST_t-channel_top_4f_InclusiveDecays","ST_tW_top_5f_inclusiveDecays",
        "ST_tW_antitop_5f_inclusiveDecays","Estbkg"};

    //vector<string> cate = {"DY","WJets","TT","Others"};
    //int catenumber[4][2] = {{0,0},{1,1},{2,4},{5,13}};
    vector<string> cate = {"Others","TT","DY","Estbkg"};
    int catenumber[4][2] = {{4,13},{1,3},{0,0},{14,14}};
    vector<Color_t> color = {kRed,kBlue,kGreen,kCyan};

    TChain *datantuple = new TChain("Events","datatuple");
    datantuple->Add("/afs/cern.ch/user/x/xuqin/eos/taug-2/nanoplots/mutau/after_sel/data*.root");
    TH1F *hdata = new TH1F("hdata","",nbins,plotmin,plotmax);
    fout->cd();
    hdata->Write("data_obs");
    datantuple->Draw(Form("%s>>hdata",variable.c_str()),"MT_muonMET<50","goff");
    int DataEntries = datantuple->GetEntries();
    cout << "Entry of data is " << DataEntries << endl; 
    vector<TChain> bkgMCntuple;
    vector<TH1F*> bkgMChis(cate.size());
    cout << "bkgMChis.size " << bkgMChis.size() << endl;
    THStack *hsMC = new THStack("hsMC","");

    //double bkgMCentries=0;
    /*for (unsigned int i=0; i < allsamplename.size(); i++){
        double xsweight;
        TChain t("Events");
        t.Add(("/afs/cern.ch/user/x/xuqin/eos/taug-2/nanoplots/mutau/" + allsamplename[i] + ".root").c_str());
        t.SetBranchAddress("xsweight",&xsweight);
        t.GetEntry(i);
        cout << "sample is " << allsamplename[i] << " Entries is " << xsweight*t.GetEntries() << endl;
        bkgMCentries += xsweight*t.GetEntries();
        TH1F *hMC = new TH1F(Form("h%s",allsamplename[i].c_str()),"",nbins,plotmin,plotmax);
        t.Draw(Form("%s>>h%s",variable.c_str(),allsamplename[i].c_str()),"xsweight","goff");
        bkgMChis.push_back(hMC);
        hsMC->Add(hMC);
    }*/
    TH1F *hratio = new TH1F("hratio","",nbins,plotmin,plotmax);

    for (unsigned int i=0; i < cate.size(); i++){

        TChain t("Events");
        if (cate[i]!="Estbkg"){
            for (int j = catenumber[i][0];j <= catenumber[i][1]; j++){
                cout << "j= " << j << endl;
                t.Add(("/afs/cern.ch/user/x/xuqin/eos/taug-2/nanoplots/mutau/after_sel/sig_reg_rmjetfaketau/" + allsamplename[j] + "_rmjetfaketau.root").c_str());
            }
            cout << "xixi" << endl;
            bkgMChis[i]=new TH1F(Form("h%s",cate[i].c_str()),"",nbins,plotmin,plotmax);
        //bkgMChis[i]->SetName(Form("h%s",cate[i].c_str()));
        //bkgMChis[i]->SetBins(nbins,plotmin,plotmax);
            cout<< "xixi" << endl;  
            t.Draw(Form("%s>>h%s",variable.c_str(),cate[i].c_str()),"xsweight*muidsf*tauidsf*(MT_muonMET<50)","goff"); 
            fout->cd();
            bkgMChis[i]->Write(cate[i].c_str()); 
        }
        else{ 
            t.Add("/afs/cern.ch/user/x/xuqin/eos/taug-2/nanoplots/mutau/after_sel/Estbkg.root");
            bkgMChis[i]=new TH1F(Form("h%s",cate[i].c_str()),"",nbins,plotmin,plotmax);
        //TH1F *hMC = new TH1F(Form("h%s",cate[i].c_str()),"",nbins,plotmin,plotmax);
            t.Draw(Form("%s>>h%s",variable.c_str(),cate[i].c_str()),"SSFR*(MT_muonMET<50)","goff");  
            fout->cd();
            bkgMChis[i]->Write("Estbkg_beforeCor");
            TH1F * bkgCor=new TH1F("hCor","",nbins,plotmin,plotmax);
            TChain tCor("Events");
            for (int j =0; j< allsamplename.size()-1;j++ ){
                tCor.Add(("/afs/cern.ch/user/x/xuqin/eos/taug-2/nanoplots/mutau/after_sel/anti_iso_notjetfaketau/" + allsamplename[j] + ".root").c_str());
            }
            tCor.Draw(Form("%s>>hCor",variable.c_str()),"xsweight*muidsf*tauidsf*SSFR*(MT_muonMET<50)","goff"); 
            fout->cd();
            bkgCor->Write("anti_isoMC_nojetfaketau");
            bkgMChis[i]->Add(bkgCor,-1); 
            fout->cd();
            bkgMChis[i]->Write("Estbkg_afterCor");

        }  

        cout<< "xixi" << endl;   
        //bkgMChis.push_back(hMC);
        bkgMChis[i]->SetFillColor(color[i]);
        hsMC->Add(bkgMChis[i]);       
    }
    cout << "xuxu" << endl;
    for (unsigned int i=1; i <= nbins; i++){
        double valuedata = hdata->GetBinContent(i);
        double valueMC = 0.;
        for (unsigned int j=0; j < cate.size(); j++){
            valueMC+=bkgMChis[j]->GetBinContent(i);
        }
        double ratio=0;
        if (valueMC!=0){
        ratio = valuedata/valueMC;
        }
        hratio->SetBinContent(i,ratio);
        hratio->SetBinError(i,0);
        fout->cd();
        hratio->Write("ratio");
        cout<< "value of " << i << " is " << hratio->GetBinContent(i) << endl;
    }
    cout << "xuxu" << endl;
    TCanvas *c = new TCanvas("c","",800,600);
    TPad* pad1 = new TPad("pad1","pad1",0,0.30,1,1);
    pad1->Draw();
    pad1->cd();
    pad1->SetFillColor(0);
    pad1->SetBorderMode(0);
    pad1->SetBorderSize(10);
    pad1->SetTickx(1);
    pad1->SetTicky(1);
    pad1->SetLeftMargin(0.10);
    pad1->SetRightMargin(0.05);
    pad1->SetTopMargin(0.122);
    pad1->SetBottomMargin(0.026);
    pad1->SetFrameFillStyle(0);
    pad1->SetFrameLineStyle(0);
    pad1->SetFrameLineWidth(2);
    pad1->SetFrameBorderMode(0);
    pad1->SetFrameBorderSize(10);
    if (log==1){
        pad1->SetLogy();
    }
    //gPad->SetLeftMargin(0.12);
    hdata->GetXaxis()->SetLabelSize(0);
    hdata->GetXaxis()->SetTitle(variable.c_str());
    hdata->GetXaxis()->SetNdivisions(505);
    hdata->GetYaxis()->SetLabelFont(42);
    hdata->GetYaxis()->SetLabelOffset(0.01);
    hdata->GetYaxis()->SetLabelSize(0.04);
    hdata->GetYaxis()->SetTitleSize(0.05);
    hdata->GetYaxis()->SetTitleOffset(1.1);
    hdata->GetYaxis()->SetTickLength(0.012);
    hdata->SetTitle("");
    hdata->GetYaxis()->SetTitle("Events");
    hdata->SetMarkerStyle(20);
    hdata->SetMarkerSize(1);
    hdata->SetLineWidth(1);
    hdata->Draw("e0p");
    hsMC->Draw("histsame");
    hdata->Draw("e0psame");


    if (variable=="taumudelphi"){
        TLegend *leg = new TLegend(0.4,0.55,0.6,0.85);
        leg->AddEntry(hdata, "data", "epl");
        for (int i=cate.size()-1; i>= 0; i--){
            leg->AddEntry(bkgMChis[i], cate[i].c_str(), "f");
        }
        leg->Draw();
    }
    else {
        TLegend *leg = new TLegend(0.7,0.55,0.9,0.85);
        leg->AddEntry(hdata, "data", "epl");
        for (int i=cate.size()-1; i>= 0; i--){
            leg->AddEntry(bkgMChis[i], cate[i].c_str(), "f");
        }
        leg->Draw();
    }


    double lowX=0.11;
    double lowY=0.835;
    TPaveText *CMS = new TPaveText(lowX, lowY+0.06, lowX+0.15, lowY+0.16, "NDC");
    CMS->SetTextFont(61);
    CMS->SetTextSize(0.08);
    CMS->SetBorderSize(   0 );
    CMS->SetFillStyle(    0 );
    CMS->SetTextAlign(   12 );
    CMS->SetTextColor(    1 );
    CMS->AddText("CMS");
    CMS->Draw("same");

    lowX=0.65;
    lowY=0.835;
    TPaveText *lumi  = new TPaveText(lowX, lowY+0.06, lowX+0.30, lowY+0.16, "NDC");
    lumi->SetBorderSize(   0 );
    lumi->SetFillStyle(    0 );
    lumi->SetTextAlign(   12 );
    lumi->SetTextColor(    1 );
    lumi->SetTextSize(0.06);
    lumi->SetTextFont (   42 );
    lumi->AddText("2018, 59.74 fb^{-1} (13 TeV)");
    lumi->Draw("same");

    lowX=0.20;
    lowY=0.835;
    TPaveText *Pre  = new TPaveText(lowX, lowY+0.06, lowX+0.15, lowY+0.16, "NDC");
    Pre->SetTextFont(52);
    Pre->SetTextSize(0.06);
    Pre->SetBorderSize(   0 );
    Pre->SetFillStyle(    0 );
    Pre->SetTextAlign(   12 );
    Pre->SetTextColor(    1 );
    Pre->AddText("Preliminary");
    Pre->Draw("same");

    pad1->RedrawAxis();

    c->cd();
    TPad* pad2 = new TPad("pad2","pad2",0,0.0,1,0.3);
    pad2->SetTopMargin(0.05);
    pad2->SetBottomMargin(0.4);
    pad2->SetLeftMargin(0.10);
    pad2->SetRightMargin(0.05);
    pad2->SetTickx(1);
    pad2->SetTicky(1);
    pad2->SetFrameLineWidth(2);
    //pad2.SetGridx()
    pad2->SetGridy();
    pad2->Draw();
    pad2->cd();


    hratio->SetMaximum(1.6);
    hratio->SetMinimum(0.6);

    hratio->GetXaxis()->SetLabelSize(0.07);
    hratio->GetYaxis()->SetLabelSize(0.08);
    hratio->GetYaxis()->SetTickLength(0.012);
    //hratio->GetYaxis()->SetTitle("#frac{(Obs.-Bkg.)}{#sqrt{Bkg.}}")
    hratio->GetYaxis()->SetTitle("#frac{Obs.}{Exp.}");
    hratio->GetYaxis()->SetNdivisions(5);
    
    hratio->GetXaxis()->SetTitleSize(0.15);
    hratio->GetYaxis()->SetTitleSize(0.10);
    hratio->GetYaxis()->SetTitleOffset(0.4);
    hratio->GetXaxis()->SetTitleOffset(0.8);
    hratio->GetXaxis()->SetLabelSize(0.09);
    hratio->GetXaxis()->SetTitle(variable.c_str());
    hratio->SetMarkerSize(1);
    hratio->SetMarkerStyle(20);
    hratio->SetLineWidth(1);
    hratio->Draw("e0p");
    //hratio->LabelsOption("v","X");

    TLine *line = new TLine(hratio->GetXaxis()->GetXmin(),1,hratio->GetXaxis()->GetXmax(), 1);
    line->SetLineStyle(3);
    line->Draw();



    c->SaveAs(Form("Plotsmutau/Estbkg/%s_log%d_Estbkg_MT50.png",variable.c_str(),log));
    fout->Close();
    //TChain *DYtuple = new TChain("Events");
    //cout << "Entry of MC is " << bkgMCentries << endl;




}

