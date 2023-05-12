if __name__ == "__main__":

    import ROOT
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--year')

    options = parser.parse_args()
    postfixName=[""]

    nbhist=1 

    fVV=ROOT.TFile("output_etau_"+options.year+"/VV.root","r")
    fTT=ROOT.TFile("output_etau_"+options.year+"/TT.root","r")
    fST=ROOT.TFile("output_etau_"+options.year+"/ST.root","r")
    fDY=ROOT.TFile("output_etau_"+options.year+"/DYrescaled.root","r")
    fData=ROOT.TFile("output_etau_"+options.year+"/EGamma.root","r")
    if options.year=="2017" or options.year=="2016pre" or options.year=="2016post": fData=ROOT.TFile("output_etau_"+options.year+"/SingleElectron.root","r")
    fout=ROOT.TFile("output_etau_"+options.year+"/Fake.root","recreate")

    ncat=9
    for j in range(0,ncat):

       dir0=fout.mkdir("et_"+str(j))

       for k in range(0,nbhist):
          postfix=postfixName[k]
          h0=fData.Get("et_"+str(j)+"_anti/data_obs"+postfix)
          h0.Add(fVV.Get("et_"+str(j)+"_anti/VV"+postfix),-1)
	  print("et_"+str(j)+"_anti/ZLL"+postfix)
	  print(fDY.Get("et_"+str(j)+"_anti/ZLL"+postfix).Integral())
          h0.Add(fDY.Get("et_"+str(j)+"_anti/ZLL"+postfix),-1)
          h0.Add(fDY.Get("et_"+str(j)+"_anti/ZTT"+postfix),-1)
          h0.Add(fTT.Get("et_"+str(j)+"_anti/TT"+postfix),-1)
          h0.Add(fST.Get("et_"+str(j)+"_anti/ST"+postfix),-1)
          for i in range(0,h0.GetSize()-2):
              if h0.GetBinContent(i)<0:
                  h0.SetBinError(i,max(0,h0.GetBinError(i)+h0.GetBinError(i)))
                  h0.SetBinContent(i,0)

          fout.cd()
          dir0.cd()
          h0.SetName("Fake"+postfix)
          h0.Write()

