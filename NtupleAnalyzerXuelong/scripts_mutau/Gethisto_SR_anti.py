from ROOT import RDataFrame, TFile, TChain, TTree, TFile, TH1D, TLorentzVector,TCanvas,TH1, TH2, TH1F
import numpy as np
from ROOT.RDF import TH1DModel, TH2DModel
import sys
from math import cos,sin,sqrt,pi
import ROOT
import time as timer
sys.path.append("..")
from pyFunc.gethisto_SR_mutau import df_withFR_anti, gethisto, df_withFR_anti_sys, gethisto_anti,DY_rescale
time_start=timer.time()
ROOT.gInterpreter.AddIncludePath('/afs/cern.ch/user/x/xuqin/work/taug-2/taug-2wkdir/CMSSW_10_6_27/src/MyNanoAnalyzer/NtupleAnalyzerXuelong/lib')
ROOT.gInterpreter.Declare('#include "basic_sel.h"')
ROOT.gInterpreter.Declare('#include "GetPFtrk.h"')
ROOT.gInterpreter.Declare('#include "Correction.h"')
ROOT.gInterpreter.Declare('#include "ApplyFR.h"')
ROOT.gSystem.Load('/afs/cern.ch/user/x/xuqin/work/taug-2/taug-2wkdir/CMSSW_10_6_27/src/MyNanoAnalyzer/NtupleAnalyzerXuelong/lib/RDFfunc.so')


TH1.SetDefaultSumw2(True)
TH2.SetDefaultSumw2(True)


nbins = int(8)
binning = np.array([40,55,70,85,100,150,200,350,500],dtype=float)


year = sys.argv[1]
sample = sys.argv[2]
name = sys.argv[3]

realcut = " && LepCand_gen[tauindex]!=0"
if "SingleMuon" in sample:
    realcut = ""

weight = "xsweight*SFweight*Acoweight*npvs_weight*nPUtrkweight*nHStrkweight*eeSF"
if year!="2018":
    weight = "xsweight*SFweight*Acoweight*npvs_weight*nPUtrkweight*nHStrkweight*eeSF*L1PreFiringWeight_Nom"

fake_uncertainty = ["CMS_jetfake_tauptextrap_qcd_mt_dm0_yearDown", "CMS_jetfake_tauptextrap_qcd_mt_dm0_yearUp", \
    "CMS_jetfake_tauptextrap_qcd_mt_dm1_yearDown", "CMS_jetfake_tauptextrap_qcd_mt_dm1_yearUp", \
    "CMS_jetfake_tauptextrap_qcd_mt_dm10_yearDown", "CMS_jetfake_tauptextrap_qcd_mt_dm10_yearUp", \
    "CMS_jetfake_tauptextrap_qcd_mt_dm11_yearDown", "CMS_jetfake_tauptextrap_qcd_mt_dm11_yearUp", \
    "CMS_jetfake_ntracksextrap_qcd_mt_dm0_yearDown", "CMS_jetfake_ntracksextrap_qcd_mt_dm0_yearUp", \
    "CMS_jetfake_ntracksextrap_qcd_mt_dm1_yearDown", "CMS_jetfake_ntracksextrap_qcd_mt_dm1_yearUp", \
    "CMS_jetfake_ntracksextrap_qcd_mt_dm10_yearDown", "CMS_jetfake_ntracksextrap_qcd_mt_dm10_yearUp", \
    "CMS_jetfake_ntracksextrap_qcd_mt_dm11_yearDown", "CMS_jetfake_ntracksextrap_qcd_mt_dm11_yearUp", \
    "CMS_jetfake_tauptextrap_w_mt_dm0_yearDown", "CMS_jetfake_tauptextrap_w_mt_dm0_yearUp", \
    "CMS_jetfake_tauptextrap_w_mt_dm1_yearDown", "CMS_jetfake_tauptextrap_w_mt_dm1_yearUp", \
    "CMS_jetfake_tauptextrap_w_mt_dm10_yearDown", "CMS_jetfake_tauptextrap_w_mt_dm10_yearUp", \
    "CMS_jetfake_tauptextrap_w_mt_dm11_yearDown", "CMS_jetfake_tauptextrap_w_mt_dm11_yearUp", \
    "CMS_jetfake_ntracksextrap_w_mt_dm0_yearDown", "CMS_jetfake_ntracksextrap_w_mt_dm0_yearUp", \
    "CMS_jetfake_ntracksextrap_w_mt_dm1_yearDown", "CMS_jetfake_ntracksextrap_w_mt_dm1_yearUp", \
    "CMS_jetfake_ntracksextrap_w_mt_dm10_yearDown", "CMS_jetfake_ntracksextrap_w_mt_dm10_yearUp", \
    "CMS_jetfake_ntracksextrap_w_mt_dm11_yearDown", "CMS_jetfake_ntracksextrap_w_mt_dm11_yearUp", \
    ]


fake_func = ["GetFR_mutau_qcd_sys_taupt(qcdFR,taupt,0,LepCand_DecayMode[tauindex],true)",\
    "GetFR_mutau_qcd_sys_taupt(qcdFR,taupt,0,LepCand_DecayMode[tauindex],false)",\
    "GetFR_mutau_qcd_sys_taupt(qcdFR,taupt,1,LepCand_DecayMode[tauindex],true)",\
    "GetFR_mutau_qcd_sys_taupt(qcdFR,taupt,1,LepCand_DecayMode[tauindex],false)",\
    "GetFR_mutau_qcd_sys_taupt(qcdFR,taupt,10,LepCand_DecayMode[tauindex],true)",\
    "GetFR_mutau_qcd_sys_taupt(qcdFR,taupt,10,LepCand_DecayMode[tauindex],false)",\
    "GetFR_mutau_qcd_sys_taupt(qcdFR,taupt,11,LepCand_DecayMode[tauindex],true)",\
    "GetFR_mutau_qcd_sys_taupt(qcdFR,taupt,11,LepCand_DecayMode[tauindex],false)",\
    "GetFR_mutau_qcd_sys_ntrk_dm(qcdFR,0,LepCand_DecayMode[tauindex],true,\"{}\")".format(year),\
    "GetFR_mutau_qcd_sys_ntrk_dm(qcdFR,0,LepCand_DecayMode[tauindex],false,\"{}\")".format(year),\
    "GetFR_mutau_qcd_sys_ntrk_dm(qcdFR,1,LepCand_DecayMode[tauindex],true,\"{}\")".format(year),\
    "GetFR_mutau_qcd_sys_ntrk_dm(qcdFR,1,LepCand_DecayMode[tauindex],false,\"{}\")".format(year),\
    "GetFR_mutau_qcd_sys_ntrk_dm(qcdFR,10,LepCand_DecayMode[tauindex],true,\"{}\")".format(year),\
    "GetFR_mutau_qcd_sys_ntrk_dm(qcdFR,10,LepCand_DecayMode[tauindex],false,\"{}\")".format(year),\
    "GetFR_mutau_qcd_sys_ntrk_dm(qcdFR,11,LepCand_DecayMode[tauindex],true,\"{}\")".format(year),\
    "GetFR_mutau_qcd_sys_ntrk_dm(qcdFR,11,LepCand_DecayMode[tauindex],false,\"{}\")".format(year),\
    "GetFR_mutau_w_sys_taupt(wFR,taupt,0,LepCand_DecayMode[tauindex],true)",\
    "GetFR_mutau_w_sys_taupt(wFR,taupt,0,LepCand_DecayMode[tauindex],false)",\
    "GetFR_mutau_w_sys_taupt(wFR,taupt,1,LepCand_DecayMode[tauindex],true)",\
    "GetFR_mutau_w_sys_taupt(wFR,taupt,1,LepCand_DecayMode[tauindex],false)",\
    "GetFR_mutau_w_sys_taupt(wFR,taupt,10,LepCand_DecayMode[tauindex],true)",\
    "GetFR_mutau_w_sys_taupt(wFR,taupt,10,LepCand_DecayMode[tauindex],false)",\
    "GetFR_mutau_w_sys_taupt(wFR,taupt,11,LepCand_DecayMode[tauindex],true)",\
    "GetFR_mutau_w_sys_taupt(wFR,taupt,11,LepCand_DecayMode[tauindex],false)",\
    "GetFR_mutau_w_sys_ntrk_dm(wFR,0,LepCand_DecayMode[tauindex],true,\"{}\")".format(year),\
    "GetFR_mutau_w_sys_ntrk_dm(wFR,0,LepCand_DecayMode[tauindex],false,\"{}\")".format(year),\
    "GetFR_mutau_w_sys_ntrk_dm(wFR,1,LepCand_DecayMode[tauindex],true,\"{}\")".format(year),\
    "GetFR_mutau_w_sys_ntrk_dm(wFR,1,LepCand_DecayMode[tauindex],false,\"{}\")".format(year),\
    "GetFR_mutau_w_sys_ntrk_dm(wFR,10,LepCand_DecayMode[tauindex],true,\"{}\")".format(year),\
    "GetFR_mutau_w_sys_ntrk_dm(wFR,10,LepCand_DecayMode[tauindex],false,\"{}\")".format(year),\
    "GetFR_mutau_w_sys_ntrk_dm(wFR,11,LepCand_DecayMode[tauindex],true,\"{}\")".format(year),\
    "GetFR_mutau_w_sys_ntrk_dm(wFR,11,LepCand_DecayMode[tauindex],false,\"{}\")".format(year)\
    ]


'''fake_uncertainty_qcd = [ "CMS_jetfake_qcd_invertOSDown","CMS_jetfake_qcd_invertOSUp",\
    "CMS_jetfake_tauptextrap_qcd_mt_dm0_yearDown", "CMS_jetfake_tauptextrap_qcd_mt_dm0_yearUp", \
    "CMS_jetfake_tauptextrap_qcd_mt_dm1_yearDown", "CMS_jetfake_tauptextrap_qcd_mt_dm1_yearUp", \
    "CMS_jetfake_tauptextrap_qcd_mt_dm10_yearDown", "CMS_jetfake_tauptextrap_qcd_mt_dm10_yearUp", \
    "CMS_jetfake_tauptextrap_qcd_mt_dm11_yearDown", "CMS_jetfake_tauptextrap_qcd_mt_dm11_yearUp", \
    "CMS_jetfake_ntracksextrap_qcd_mt_dm0_yearDown", "CMS_jetfake_ntracksextrap_qcd_mt_dm0_yearUp", \
    "CMS_jetfake_ntracksextrap_qcd_mt_dm1_yearDown", "CMS_jetfake_ntracksextrap_qcd_mt_dm1_yearUp", \
    "CMS_jetfake_ntracksextrap_qcd_mt_dm10_yearDown", "CMS_jetfake_ntracksextrap_qcd_mt_dm10_yearUp", \
    "CMS_jetfake_ntracksextrap_qcd_mt_dm11_yearDown", "CMS_jetfake_ntracksextrap_qcd_mt_dm11_yearUp", \
    "CMS_jetfake_ntracksextrap_qcd_mt_yearDown", "CMS_jetfake_ntracksextrap_qcd_mt_yearUp",\
    ]

fake_uncertainty_w = ["CMS_jetfake_w_invertMTDown","CMS_jetfake_w_invertMTUp",\
    "CMS_jetfake_tauptextrap_w_mt_dm0_yearDown", "CMS_jetfake_tauptextrap_w_mt_dm0_yearUp", \
    "CMS_jetfake_tauptextrap_w_mt_dm1_yearDown", "CMS_jetfake_tauptextrap_w_mt_dm1_yearUp", \
    "CMS_jetfake_tauptextrap_w_mt_dm10_yearDown", "CMS_jetfake_tauptextrap_w_mt_dm10_yearUp", \
    "CMS_jetfake_tauptextrap_w_mt_dm11_yearDown", "CMS_jetfake_tauptextrap_w_mt_dm11_yearUp", \
    "CMS_jetfake_ntracksextrap_w_mt_dm0_yearDown", "CMS_jetfake_ntracksextrap_w_mt_dm0_yearUp", \
    "CMS_jetfake_ntracksextrap_w_mt_dm1_yearDown", "CMS_jetfake_ntracksextrap_w_mt_dm1_yearUp", \
    "CMS_jetfake_ntracksextrap_w_mt_dm10_yearDown", "CMS_jetfake_ntracksextrap_w_mt_dm10_yearUp", \
    "CMS_jetfake_ntracksextrap_w_mt_dm11_yearDown", "CMS_jetfake_ntracksextrap_w_mt_dm11_yearUp", \
    "CMS_jetfake_ntracksextrap_w_mt_yearDown", "CMS_jetfake_ntracksextrap_w_mt_yearUp",\
]

fake_uncertainty_wfraction = ["CMS_jetfake_wfractionDown", "CMS_jetfake_wfractionUp"]

func_qcd = ["GetFR_mutau_qcd_sys_invertOS(qcdFR,0.9)",\
    "GetFR_mutau_qcd_sys_invertOS(qcdFR,1.1)",\
    "GetFR_mutau_qcd_sys_taupt(qcdFR,taupt,0,LepCand_DecayMode[tauindex],true)",\
    "GetFR_mutau_qcd_sys_taupt(qcdFR,taupt,0,LepCand_DecayMode[tauindex],false)",\
    "GetFR_mutau_qcd_sys_taupt(qcdFR,taupt,1,LepCand_DecayMode[tauindex],true)",\
    "GetFR_mutau_qcd_sys_taupt(qcdFR,taupt,1,LepCand_DecayMode[tauindex],false)",\
    "GetFR_mutau_qcd_sys_taupt(qcdFR,taupt,10,LepCand_DecayMode[tauindex],true)",\
    "GetFR_mutau_qcd_sys_taupt(qcdFR,taupt,10,LepCand_DecayMode[tauindex],false)",\
    "GetFR_mutau_qcd_sys_taupt(qcdFR,taupt,11,LepCand_DecayMode[tauindex],true)",\
    "GetFR_mutau_qcd_sys_taupt(qcdFR,taupt,11,LepCand_DecayMode[tauindex],false)",\
    "GetFR_mutau_qcd_sys_ntrk_dm(qcdFR,0,LepCand_DecayMode[tauindex],true)",\
    "GetFR_mutau_qcd_sys_ntrk_dm(qcdFR,0,LepCand_DecayMode[tauindex],false)",\
    "GetFR_mutau_qcd_sys_ntrk_dm(qcdFR,1,LepCand_DecayMode[tauindex],true)",\
    "GetFR_mutau_qcd_sys_ntrk_dm(qcdFR,1,LepCand_DecayMode[tauindex],false)",\
    "GetFR_mutau_qcd_sys_ntrk_dm(qcdFR,10,LepCand_DecayMode[tauindex],true)",\
    "GetFR_mutau_qcd_sys_ntrk_dm(qcdFR,10,LepCand_DecayMode[tauindex],false)",\
    "GetFR_mutau_qcd_sys_ntrk_dm(qcdFR,11,LepCand_DecayMode[tauindex],true)",\
    "GetFR_mutau_qcd_sys_ntrk_dm(qcdFR,11,LepCand_DecayMode[tauindex],false)",\
    "GetFR_mutau_qcd_sys_ntrk(qcdFR,0.9)",\
    "GetFR_mutau_qcd_sys_ntrk(qcdFR,1.1)",\
]

func_w = ["GetFR_mutau_w_sys_invertmT(wFR,0.9)",\
    "GetFR_mutau_w_sys_invertmT(wFR,1.1)",\
    "GetFR_mutau_w_sys_taupt(wFR,taupt,0,LepCand_DecayMode[tauindex],true)",\
    "GetFR_mutau_w_sys_taupt(wFR,taupt,0,LepCand_DecayMode[tauindex],false)",\
    "GetFR_mutau_w_sys_taupt(wFR,taupt,1,LepCand_DecayMode[tauindex],true)",\
    "GetFR_mutau_w_sys_taupt(wFR,taupt,1,LepCand_DecayMode[tauindex],false)",\
    "GetFR_mutau_w_sys_taupt(wFR,taupt,10,LepCand_DecayMode[tauindex],true)",\
    "GetFR_mutau_w_sys_taupt(wFR,taupt,10,LepCand_DecayMode[tauindex],false)",\
    "GetFR_mutau_w_sys_taupt(wFR,taupt,11,LepCand_DecayMode[tauindex],true)",\
    "GetFR_mutau_w_sys_taupt(wFR,taupt,11,LepCand_DecayMode[tauindex],false)",\
    "GetFR_mutau_w_sys_ntrk_dm(wFR,0,LepCand_DecayMode[tauindex],true)",\
    "GetFR_mutau_w_sys_ntrk_dm(wFR,0,LepCand_DecayMode[tauindex],false)",\
    "GetFR_mutau_w_sys_ntrk_dm(wFR,1,LepCand_DecayMode[tauindex],true)",\
    "GetFR_mutau_w_sys_ntrk_dm(wFR,1,LepCand_DecayMode[tauindex],false)",\
    "GetFR_mutau_w_sys_ntrk_dm(wFR,10,LepCand_DecayMode[tauindex],true)",\
    "GetFR_mutau_w_sys_ntrk_dm(wFR,10,LepCand_DecayMode[tauindex],false)",\
    "GetFR_mutau_w_sys_ntrk_dm(wFR,11,LepCand_DecayMode[tauindex],true)",\
    "GetFR_mutau_w_sys_ntrk_dm(wFR,11,LepCand_DecayMode[tauindex],false)",\
    "GetFR_mutau_w_sys_ntrk(wFR,0.9)",\
    "GetFR_mutau_w_sys_ntrk(wFR,1.1)",\
]

func_wfraction = ["Getwfraction_sys(wfraction, true)",\
    "Getwfraction_sys(wfraction, false)",
]
'''

print ("year is ", year , " sample is ", sample, " name is ", name)
df= RDataFrame("Events","/eos/cms/store/cmst3/group/taug2/AnalysisXuelong/ntuples_mutau_{}_basicsel/{}.root".format(year,sample))
df = df.Define("totalweight",weight)
fout=0

if sample == "DY":
    fout = TFile("Histo/HistoSR_anti_{}/{}.root".format(year,name),"recreate")
else:
    fout = TFile("Histo/HistoSR_anti_{}/{}.root".format(year,sample),"recreate")
    
mt_0cut = "(nTrk==0) && (Acopl<0.015) && ((taupt>30 && isSingleMuonTrigger && LepCand_trgmatch[muindex])||(taupt>32 && isMuonTauTrigger && LepCand_trgmatch[muindex])) && mvis>40 && mtrans<75 "
mt_1cut = "(nTrk==1) && (Acopl<0.015) && ((taupt>30 && isSingleMuonTrigger && LepCand_trgmatch[muindex])||(taupt>32 && isMuonTauTrigger && LepCand_trgmatch[muindex])) && mvis>40 && mtrans<75"

DYshapecut = "(nTrk<10) && (Acopl<0.015) && ((taupt>30 && isSingleMuonTrigger && LepCand_trgmatch[muindex])||(taupt>32 && isMuonTauTrigger && LepCand_trgmatch[muindex])) && mvis>40 && mtrans<75"

if year=="2016pre" or year=="2016post":
    mt_0cut = "(nTrk==0) && (Acopl<0.015) && ((taupt>30 && isSingleMuonTrigger && LepCand_trgmatch[muindex])||(taupt>30 && isMuonTauTrigger && LepCand_trgmatch[muindex])) && mvis>40 && mtrans<75 "
    mt_1cut = "(nTrk==1) && (Acopl<0.015) && ((taupt>30 && isSingleMuonTrigger && LepCand_trgmatch[muindex])||(taupt>30 && isMuonTauTrigger && LepCand_trgmatch[muindex])) && mvis>40 && mtrans<75"
    DYshapecut = "(nTrk<10) && (Acopl<0.015) && ((taupt>30 && isSingleMuonTrigger && LepCand_trgmatch[muindex])||(taupt>30 && isMuonTauTrigger && LepCand_trgmatch[muindex])) && mvis>40 && mtrans<75"

if year=="2017":
    mt_0cut = "(nTrk==0) && (Acopl<0.015) && ((taupt>30 && isSingleMuonTrigger && LepCand_trgmatch[muindex] )||(taupt>32 && isMuonTauTrigger && LepCand_trgmatch[muindex] && LepCand_trgmatch[tauindex])) && mvis>40 && mtrans<75 "
    mt_1cut = "(nTrk==1) && (Acopl<0.015) && ((taupt>30 && isSingleMuonTrigger && LepCand_trgmatch[muindex])||(taupt>32 && isMuonTauTrigger && LepCand_trgmatch[muindex] && LepCand_trgmatch[tauindex])) && mvis>40 && mtrans<75"
    DYshapecut = "(nTrk<10) && (Acopl<0.015) && ((taupt>30 && isSingleMuonTrigger && LepCand_trgmatch[muindex])||(taupt>32 && isMuonTauTrigger && LepCand_trgmatch[muindex] && LepCand_trgmatch[tauindex])) && mvis>40 && mtrans<75"


isocut = "&& isOS && is_isolated"
anticut = "&& isOS && !is_isolated"

cutZTT = " && LepCand_gen[tauindex]==5"
cutZLL = " && LepCand_gen[tauindex]!=5"
dir0 = fout.mkdir("mt_0")
dir1 = fout.mkdir("mt_1")

mt_0cut = mt_0cut + realcut
mt_1cut = mt_1cut + realcut
DYshapecut = DYshapecut + realcut

if (name=="ZTT"):
    DYshapecut = DYshapecut+cutZTT
    mt_0cut = mt_0cut + cutZTT
    mt_1cut = mt_1cut + cutZTT
if (name=="ZLL"):
    DYshapecut = DYshapecut+cutZLL
    mt_0cut = mt_0cut + cutZLL 
    mt_1cut = mt_1cut + cutZLL

histo_mt0_anti=0
histo_mt1_anti=0

if sample == "DY":
    df_DYhigh_anti = df_withFR_anti(df.Filter(DYshapecut+anticut),year)
    df_mt0_anti = df_withFR_anti(df.Filter(mt_0cut+anticut),year)
    df_mt1_anti = df_withFR_anti(df.Filter(mt_1cut+anticut),year)
    
    histoDYhigh_anti = gethisto_anti(df_DYhigh_anti,"DYhigh_anti", nbins, binning)
    histoDY_mt0_anti = gethisto_anti(df_mt0_anti,"mt0_anti", nbins, binning)
    histoDY_mt1_anti = gethisto_anti(df_mt1_anti,"mt1_anti", nbins, binning)

    histo_mt0_anti = DY_rescale(histoDYhigh_anti,histoDY_mt0_anti)
    histo_mt1_anti = DY_rescale(histoDYhigh_anti,histoDY_mt1_anti)

    print ("mt_0 basic ", histo_mt0_anti.Integral())
    print ("mt_1 basic ", histo_mt1_anti.Integral())
    dir0.cd()
    histo_mt0_anti.SetName("{}_anti".format(name))
    histo_mt0_anti.Write()
    dir1.cd()
    histo_mt1_anti.SetName("{}_anti".format(name))
    histo_mt1_anti.Write()
    
    ### now systematic part
    for i in range(len(fake_uncertainty)):
        uncertainty_name = str.replace(fake_uncertainty[i],"year",year)
        if ("qcd" in uncertainty_name):
            sysflag = 0
        else:
            sysflag = 1
        df_DYhigh_anti_sys = df_withFR_anti_sys(df_DYhigh_anti, sysflag, fake_func[i])
        df_mt0_anti_sys = df_withFR_anti_sys(df_mt0_anti, sysflag, fake_func[i])
        df_mt1_anti_sys = df_withFR_anti_sys(df_mt1_anti, sysflag, fake_func[i])
        histoDYhigh_anti_sys = gethisto_anti(df_DYhigh_anti_sys,"DYhigh_anti_{}".format(uncertainty_name), nbins, binning)
        histoDY_mt0_anti_sys = gethisto_anti(df_mt0_anti_sys,"mt0_anti_{}".format(uncertainty_name), nbins, binning)
        histoDY_mt1_anti_sys = gethisto_anti(df_mt1_anti_sys,"mt1_anti_{}".format(uncertainty_name), nbins, binning)
        histo_mt0_anti_sys = DY_rescale(histoDYhigh_anti_sys,histoDY_mt0_anti_sys)
        histo_mt1_anti_sys = DY_rescale(histoDYhigh_anti_sys,histoDY_mt1_anti_sys)
        print ("mt_0 ", uncertainty_name, " ", histo_mt0_anti_sys.Integral())
        print ("mt_1 ", uncertainty_name, " ", histo_mt1_anti_sys.Integral())
        dir0.cd()
        histo_mt0_anti_sys.SetName("{}_anti_{}".format(name,uncertainty_name))
        histo_mt0_anti_sys.Write()
        dir1.cd()
        histo_mt1_anti_sys.SetName("{}_anti_{}".format(name,uncertainty_name))
        histo_mt1_anti_sys.Write()
        
    
    
    '''
    for i in range(len(fake_uncertainty_qcd)):
        uncertainty_name = str.replace(fake_uncertainty_qcd[i],"year","2018")
        df_DYhigh_anti_sys = df_withFR_anti_sys(df_DYhigh_anti, 0, func_qcd[i])
        df_mt0_anti_sys = df_withFR_anti_sys(df_mt0_anti, 0, func_qcd[i])
        df_mt1_anti_sys = df_withFR_anti_sys(df_mt1_anti, 0, func_qcd[i])
        histoDYhigh_anti_sys = gethisto_anti(df_DYhigh_anti_sys,"DYhigh_anti_{}".format(uncertainty_name), nbins, binning)
        histoDY_mt0_anti_sys = gethisto_anti(df_mt0_anti_sys,"mt0_anti_{}".format(uncertainty_name), nbins, binning)
        histoDY_mt1_anti_sys = gethisto_anti(df_mt1_anti_sys,"mt1_anti_{}".format(uncertainty_name), nbins, binning)
        histo_mt0_anti_sys = DY_rescale(histoDYhigh_anti_sys,histoDY_mt0_anti_sys)
        histo_mt1_anti_sys = DY_rescale(histoDYhigh_anti_sys,histoDY_mt1_anti_sys)
        dir0.cd()
        histo_mt0_anti_sys.SetName("{}_anti_{}".format(name,uncertainty_name))
        histo_mt0_anti_sys.Write()
        dir1.cd()
        histo_mt1_anti_sys.SetName("{}_anti_{}".format(name,uncertainty_name))
        histo_mt1_anti_sys.Write()

    for i in range(len(fake_uncertainty_w)):
        uncertainty_name = str.replace(fake_uncertainty_w[i],"year","2018")
        df_DYhigh_anti_sys = df_withFR_anti_sys(df_DYhigh_anti, 1, func_w[i])
        df_mt0_anti_sys = df_withFR_anti_sys(df_mt0_anti, 1, func_w[i])
        df_mt1_anti_sys = df_withFR_anti_sys(df_mt1_anti, 1, func_w[i])
        histoDYhigh_anti_sys = gethisto_anti(df_DYhigh_anti_sys,"DYhigh_anti_{}".format(uncertainty_name), nbins, binning)
        histoDY_mt0_anti_sys = gethisto_anti(df_mt0_anti_sys,"mt0_anti_{}".format(uncertainty_name), nbins, binning)
        histoDY_mt1_anti_sys = gethisto_anti(df_mt1_anti_sys,"mt1_anti_{}".format(uncertainty_name), nbins, binning)
        histo_mt0_anti_sys = DY_rescale(histoDYhigh_anti_sys,histoDY_mt0_anti_sys)
        histo_mt1_anti_sys = DY_rescale(histoDYhigh_anti_sys,histoDY_mt1_anti_sys)
        dir0.cd()
        histo_mt0_anti_sys.SetName("{}_anti_{}".format(name,uncertainty_name))
        histo_mt0_anti_sys.Write()
        dir1.cd()
        histo_mt1_anti_sys.SetName("{}_anti_{}".format(name,uncertainty_name))
        histo_mt1_anti_sys.Write()
        
    for i in range(len(fake_uncertainty_wfraction)):
        uncertainty_name = str.replace(fake_uncertainty_wfraction[i],"year","2018")
        df_DYhigh_anti_sys = df_withFR_anti_sys(df_DYhigh_anti, 2, func_wfraction[i])
        df_mt0_anti_sys = df_withFR_anti_sys(df_mt0_anti, 2, func_wfraction[i])
        df_mt1_anti_sys = df_withFR_anti_sys(df_mt1_anti, 2, func_wfraction[i])
        histoDYhigh_anti_sys = gethisto_anti(df_DYhigh_anti_sys,"DYhigh_anti_{}".format(uncertainty_name), nbins, binning)
        histoDY_mt0_anti_sys = gethisto_anti(df_mt0_anti_sys,"mt0_anti_{}".format(uncertainty_name), nbins, binning)
        histoDY_mt1_anti_sys = gethisto_anti(df_mt1_anti_sys,"mt1_anti_{}".format(uncertainty_name), nbins, binning)
        histo_mt0_anti_sys = DY_rescale(histoDYhigh_anti_sys,histoDY_mt0_anti_sys)
        histo_mt1_anti_sys = DY_rescale(histoDYhigh_anti_sys,histoDY_mt1_anti_sys)
        dir0.cd()
        histo_mt0_anti_sys.SetName("{}_anti_{}".format(name,uncertainty_name))
        histo_mt0_anti_sys.Write()
        dir1.cd()
        histo_mt1_anti_sys.SetName("{}_anti_{}".format(name,uncertainty_name))
        histo_mt1_anti_sys.Write()
    '''

else:
    df_mt0_anti = df_withFR_anti(df.Filter(mt_0cut+anticut),year)
    df_mt1_anti = df_withFR_anti(df.Filter(mt_1cut+anticut),year)
    histo_mt0_anti = gethisto_anti(df_mt0_anti,"mt0_anti", nbins, binning)
    histo_mt1_anti = gethisto_anti(df_mt1_anti,"mt1_anti", nbins, binning)
    print ("mt_0 basic ", histo_mt0_anti.Integral())
    print ("mt_1 basic ", histo_mt1_anti.Integral())
    dir0.cd()
    histo_mt0_anti.SetName("{}_anti".format(name))
    histo_mt0_anti.Write()
    dir1.cd()
    histo_mt1_anti.SetName("{}_anti".format(name))
    histo_mt1_anti.Write()
    
    ### now systematic part
    for i in range(len(fake_uncertainty)):
        uncertainty_name = str.replace(fake_uncertainty[i],"year",year)
        if ("qcd" in uncertainty_name):
            sysflag = 0
        elif ("wfraction" in uncertainty_name):
            sysflag = 2
        else:
            sysflag = 1
        df_mt0_anti_sys = df_withFR_anti_sys(df_mt0_anti, sysflag, fake_func[i])
        df_mt1_anti_sys = df_withFR_anti_sys(df_mt1_anti, sysflag, fake_func[i])
        histo_mt0_anti_sys = gethisto_anti(df_mt0_anti_sys,"mt0_anti_{}".format(uncertainty_name), nbins, binning)
        histo_mt1_anti_sys = gethisto_anti(df_mt1_anti_sys,"mt1_anti_{}".format(uncertainty_name), nbins, binning)
        print ("mt_0 ", uncertainty_name, " ", histo_mt0_anti_sys.Integral())
        print ("mt_1 ", uncertainty_name, " ", histo_mt1_anti_sys.Integral())
        dir0.cd()
        histo_mt0_anti_sys.SetName("{}_anti_{}".format(name,uncertainty_name))
        histo_mt0_anti_sys.Write()
        dir1.cd()
        histo_mt1_anti_sys.SetName("{}_anti_{}".format(name,uncertainty_name))
        histo_mt1_anti_sys.Write()
    
    
    '''for i in range(len(fake_uncertainty_qcd)):
        uncertainty_name = str.replace(fake_uncertainty_qcd[i],"year","2018")
        df_mt0_anti_sys = df_withFR_anti_sys(df_mt0_anti, 0, func_qcd[i])
        df_mt1_anti_sys = df_withFR_anti_sys(df_mt1_anti, 0, func_qcd[i])
        histo_mt0_anti_sys = gethisto_anti(df_mt0_anti_sys,"mt0_anti_{}".format(uncertainty_name), nbins, binning)
        histo_mt1_anti_sys = gethisto_anti(df_mt1_anti_sys,"mt1_anti_{}".format(uncertainty_name), nbins, binning)
        dir0.cd()
        histo_mt0_anti_sys.SetName("{}_anti_{}".format(name,uncertainty_name))
        histo_mt0_anti_sys.Write()
        dir1.cd()
        histo_mt1_anti_sys.SetName("{}_anti_{}".format(name,uncertainty_name))
        histo_mt1_anti_sys.Write()

    for i in range(len(fake_uncertainty_w)):
        uncertainty_name = str.replace(fake_uncertainty_w[i],"year","2018")
        df_mt0_anti_sys = df_withFR_anti_sys(df_mt0_anti, 0, func_w[i])
        df_mt1_anti_sys = df_withFR_anti_sys(df_mt1_anti, 0, func_w[i])
        histo_mt0_anti_sys = gethisto_anti(df_mt0_anti_sys,"mt0_anti_{}".format(uncertainty_name), nbins, binning)
        histo_mt1_anti_sys = gethisto_anti(df_mt1_anti_sys,"mt1_anti_{}".format(uncertainty_name), nbins, binning)
        dir0.cd()
        histo_mt0_anti_sys.SetName("{}_anti_{}".format(name,uncertainty_name))
        histo_mt0_anti_sys.Write()
        dir1.cd()
        histo_mt1_anti_sys.SetName("{}_anti_{}".format(name,uncertainty_name))
        histo_mt1_anti_sys.Write()

    for i in range(len(fake_uncertainty_wfraction)):
        uncertainty_name = str.replace(fake_uncertainty_wfraction[i],"year","2018")
        df_mt0_anti_sys = df_withFR_anti_sys(df_mt0_anti, 0, func_wfraction[i])
        df_mt1_anti_sys = df_withFR_anti_sys(df_mt1_anti, 0, func_wfraction[i])
        histo_mt0_anti_sys = gethisto_anti(df_mt0_anti_sys,"mt0_anti_{}".format(uncertainty_name), nbins, binning)
        histo_mt1_anti_sys = gethisto_anti(df_mt1_anti_sys,"mt1_anti_{}".format(uncertainty_name), nbins, binning)
        dir0.cd()
        histo_mt0_anti_sys.SetName("{}_anti_{}".format(name,uncertainty_name))
        histo_mt0_anti_sys.Write()
        dir1.cd()
        histo_mt1_anti_sys.SetName("{}_anti_{}".format(name,uncertainty_name))
        histo_mt1_anti_sys.Write()
    '''
fout.Close()
