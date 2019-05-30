#! /usr/bin/env python
from ROOT import TStyle, TF1, TFile, TCanvas, gDirectory, TTree, TH1F, TH2F, THStack, TLegend, gROOT 
import ROOT
import os, math
gROOT.SetBatch(1)
from style import *

from collections import OrderedDict
sig1samples=OrderedDict()
sig2samples=OrderedDict()
sig3samples=OrderedDict()
bkgsamples=OrderedDict()

log=False
lumi = 3000000

def AddBkg(fname, name, color, xsection):
  tmp = {}
  f = TFile('merged/'+fname)
  fname = os.path.basename(fname)[:-5]
 
  tmp["file"] = f
  tmp["hname"] = [x.GetName() for x in f.GetListOfKeys()]
  print(tmp)
  if xsection is not 1:
    tmp["hname"].remove("EventInfo")
#    tmp["hname"].remove("tree")
    h = f.Get("EventInfo")
    nevt = h.GetBinContent(1)

  tmp["total"] = nevt 
  tmp["col"] = color
  tmp["xsection"] = xsection
  tmp["name"] = name
  bkgsamples[fname] = tmp

def AddSig1(fname, name, color, xsection):
  tmp = {}
  f = TFile('merged/'+fname)
  fname = os.path.basename(fname)[:-5]

  tmp["file"] = f
  tmp["hname"] = [x.GetName() for x in f.GetListOfKeys()]
  if xsection is not 1:
    tmp["hname"].remove("EventInfo")
#    tmp["hname"].remove("tree")
    h = f.Get("EventInfo")
    nevt = h.GetBinContent(1)

  tmp["total"] = nevt
  tmp["col"] = color
  tmp["xsection"] = xsection
  tmp["name"] = name
  sig1samples[fname] = tmp

def AddSig2(fname, name, color, xsection):
  tmp = {}
  f = TFile('merged/'+fname)
  fname = os.path.basename(fname)[:-5]

  tmp["file"] = f
  tmp["hname"] = [x.GetName() for x in f.GetListOfKeys()]
  if xsection is not 1:
    tmp["hname"].remove("EventInfo")
#    tmp["hname"].remove("tree")
    h = f.Get("EventInfo")
    nevt = h.GetBinContent(1)

  tmp["total"] = nevt
  tmp["col"] = color
  tmp["xsection"] = xsection
  tmp["name"] = name
  sig2samples[fname] = tmp

def AddSig3(fname, name, color, xsection):
  tmp = {}
  f = TFile('merged/'+fname)
  fname = os.path.basename(fname)[:-5]

  tmp["file"] = f
  tmp["hname"] = [x.GetName() for x in f.GetListOfKeys()]
  if xsection is not 1:
    tmp["hname"].remove("EventInfo")
#    tmp["hname"].remove("tree")
    h = f.Get("EventInfo")
    nevt = h.GetBinContent(1)

  tmp["total"] = nevt
  tmp["col"] = color
  tmp["xsection"] = xsection
  tmp["name"] = name
  sig3samples[fname] = tmp

####Users should provide these information
AddBkg("hist_WW.root","VV",617, 118.7)
AddBkg("hist_WZ.root","VV",881, 47.13)
AddBkg("hist_ZZ.root","VV",619, 16.523)
AddBkg("hist_DY012JetsM10toinf.root","DY",ROOT.kBlue+2, 24375.4)
AddBkg("hist_W0JetsToLNu.root","WJets",ROOT.kOrange+1,47071)
AddBkg("hist_W1JetsToLNu.root","WJets",ROOT.kOrange+1,9816)
AddBkg("hist_W2JetsToLNu.root","WJets",ROOT.kOrange+1,3200)
AddBkg("hist_TT012Jets.root","TT",ROOT.kRed-7, 831.76)
AddSig1("hist_LQcmutauLO.root", "#mu#tau", 7, 0.00083176*2)
AddSig2("hist_LQctautauLO.root", "#tau#tau", 3, 0.00083176*2)
AddSig3("hist_LQcnunuLO.root", "#nu#nu", 5, 0.00083176*2)

N_bkgsamples = len(bkgsamples)
N_hist = len(sig1samples[sig1samples.keys()[0]]["hname"])

fNevt = open("Nevt.txt",'w')

for i in range(0, N_hist):

  #printHistName = "nJets"
  #printHistName = "sigTop"
  printHistName = "leptauDR"

  hnames = sig1samples[sig1samples.keys()[0]]["hname"][i].split("_")
  if hnames[1] == printHistName :
    string0 = "%s \n" %hnames
    fNevt.write(string0)

  if hnames[1] == printHistName :
    print hnames[1], " ", hnames[2], " ", hnames[3]  

  hs = THStack()
  l = TLegend(0.15,0.71,0.89,0.87)
  l.SetNColumns(4);
  l.SetTextSize(0.04);
  l.SetLineColor(0);
  l.SetFillColor(0);

  ntotalbkg = 0
  k = 0
  for fname in bkgsamples.keys():
    h_tmp = bkgsamples[fname]["file"].Get(bkgsamples[fname]["hname"][i])
    nbins = h_tmp.GetNbinsX()
    h_tmp.AddBinContent( nbins, h_tmp.GetBinContent( nbins+1 ) ) #overflow
    h_tmp.SetFillColor(bkgsamples[fname]["col"])
    scale = lumi/(bkgsamples[fname]["total"]/bkgsamples[fname]["xsection"])
    #print fname
    #print scale
    h_tmp.Scale(scale)

    ## check if the sample is the same as previous process. 
    if k < N_bkgsamples-1 :
      post_name = bkgsamples.keys()[k+1]
      if bkgsamples[fname]["name"] is bkgsamples[post_name]["name"]:
        h_tmp.SetLineColor(bkgsamples[fname]["col"]) 
      else:
        l.AddEntry(h_tmp, bkgsamples[fname]["name"]  ,"F") 
    else: 
      l.AddEntry(h_tmp, bkgsamples[fname]["name"]  ,"F")
 
    ## print out number of events
    numevt = h_tmp.Integral()
    rawevt = h_tmp.GetEntries()
    ntotalbkg = ntotalbkg + numevt
    if bkgsamples[fname]["name"] == "QCD": numqcd = numevt
    if hnames[1] == printHistName:
      string = "%s :  %s = %d \n"%(fname,bkgsamples[fname]["name"],numevt)
      fNevt.write(string)
      print fname, " : ", bkgsamples[fname]["name"], " = ", "{0:.1g}".format(numevt),  " scale : " ,"{0:.2g}".format(scale)
    hs.Add( h_tmp )
    k = k+1

  h_bkg = hs.GetStack().Last()


  #Signal
  m = 0
  for fname in sig1samples.keys():
    h_sig1 = sig1samples[fname]["file"].Get(sig1samples[fname]["hname"][i])
    nbins = h_sig1.GetNbinsX()
    h_sig1.AddBinContent( nbins, h_sig1.GetBinContent( nbins+1 ) ) 
    h_sig1.SetLineColor(sig1samples[fname]["col"])
    h_sig1.SetFillColorAlpha(sig1samples[fname]["col"],0.0)
    scale = lumi/(sig1samples[fname]["total"]/sig1samples[fname]["xsection"])

    #print fname
    #print scale
    h_sig1.Scale(scale)
    l.AddEntry(h_sig1, sig1samples[fname]["name"]  ,"F")

    ## print out number of events
    numevt = h_sig1.Integral()
    rawevt = h_sig1.GetEntries()
    if hnames[1] == printHistName:
      string = "%s :  %s = %.4f \n"%(fname,sig1samples[fname]["name"],numevt)
      fNevt.write(string)
      print fname, " : ", sig1samples[fname]["name"], " = ", "{0:.1g}".format(numevt),  " scale : " ,"{0:.2g}".format(scale)
    m = m+1
    nsig1 = numevt
  h_sig1.Scale(10000)
  h_sig1.SetLineWidth(2)


  #Signal
  m = 0
  for fname in sig2samples.keys():
    h_sig2 = sig2samples[fname]["file"].Get(sig2samples[fname]["hname"][i])
    nbins = h_sig2.GetNbinsX()
    h_sig2.AddBinContent( nbins, h_sig2.GetBinContent( nbins+1 ) )
    h_sig2.SetLineColor(sig2samples[fname]["col"])
    h_sig2.SetFillColorAlpha(sig2samples[fname]["col"],0.0)
    scale = lumi/(sig2samples[fname]["total"]/sig2samples[fname]["xsection"])

    #print fname
    #print scale
    h_sig2.Scale(scale)
    l.AddEntry(h_sig2, sig2samples[fname]["name"]  ,"F")

    ## print out number of events
    numevt = h_sig2.Integral()
    rawevt = h_sig2.GetEntries()
    if hnames[1] == printHistName:
      string = "%s :  %s = %.4f \n"%(fname,sig2samples[fname]["name"],numevt)
      fNevt.write(string)
      print fname, " : ", sig2samples[fname]["name"], " = ", "{0:.5g}".format(numevt),  " scale : " ,"{0:.1g}".format(scale)
    m = m+1
    nsig2 = numevt
  h_sig2.Scale(10000)
  h_sig2.SetLineWidth(2)

  #Signal
  m = 0
  for fname in sig3samples.keys():
    h_sig3 = sig3samples[fname]["file"].Get(sig3samples[fname]["hname"][i])
    nbins = h_sig3.GetNbinsX()
    h_sig3.AddBinContent( nbins, h_sig3.GetBinContent( nbins+1 ) )
    h_sig3.SetLineColor(sig3samples[fname]["col"])
    h_sig3.SetFillColorAlpha(sig3samples[fname]["col"],0.0)
    scale = lumi/(sig3samples[fname]["total"]/sig3samples[fname]["xsection"])

    #print fname
    #print scale
    h_sig3.Scale(scale)
    l.AddEntry(h_sig3, sig3samples[fname]["name"]  ,"F")

    ## print out number of events
    numevt = h_sig3.Integral()
    rawevt = h_sig3.GetEntries()
    if hnames[1] == printHistName:
      string = "%s :  %s = %.4f \n"%(fname,sig3samples[fname]["name"],numevt)
      fNevt.write(string)
      print fname, " : ", sig3samples[fname]["name"], " = ", "{0:.5g}".format(numevt),  " scale : " ,"{0:.1g}".format(scale)
    m = m+1
    nsig3 = numevt
  h_sig3.Scale(10000)
  h_sig3.SetLineWidth(2)

  if hnames[1] == printHistName :
    if ntotalbkg > 0:
      sigma1 = nsig1 / math.sqrt(ntotalbkg)
      sigma2 = nsig2 / math.sqrt(ntotalbkg)
      sigma3 = nsig3 / math.sqrt(ntotalbkg)
    else: sigma1, sigma2, sigma3 = ("nan","nan","nan")
    string_sigma = "muta, tata, nunu sigma = " +  str(sigma1) +  " " + str(sigma2) + " " + str(sigma3) + '\n'
    fNevt.write(string_sigma)

  #Draw
  if nsig1*nsig2*nsig3 > 0:
    h_sig1.Scale(ntotalbkg/(nsig1*10000))
    h_sig2.Scale(ntotalbkg/(nsig2*10000))
    h_sig3.Scale(ntotalbkg/(nsig3*10000))
  c = TCanvas("c_"+"{}".format(i),"c",1)
  if log and h_bkg.Integral() > 0:
    c.SetLogy()

  max_hs = hs.GetMaximum()
  maxfrac = 0.5
  if log :
    if max_hs > 100000:
      maxfrac = 1000
    else:
      maxfrac = 100
  #hs.SetMaximum(max_hs+max_hs*maxfrac)
  h_sig1.SetMaximum(max_hs+max_hs*maxfrac)
  #if log: hs.SetMinimum(10)
  if log: h_sig1.SetMinimum(10)
  h_sig1.Draw("hist same")
  h_sig1.SetTitle("")
  h_sig1.GetYaxis().SetTitle("Entries")
  h_sig1.GetYaxis().SetTitleOffset(1.5)
  #hs.Draw("hist")
  #hs.SetTitle("")
  #hs.GetYaxis().SetTitle("Entries")
  #hs.GetYaxis().SetTitleOffset(1.5)
  hs.Draw("hist same")
  h_sig1.Draw("hist same")
  h_sig2.Draw("hist same")
  h_sig3.Draw("hist same")
  h_sig1.Draw("axis same")

  l.Draw()
  label = TPaveText()
  label.SetX1NDC(gStyle.GetPadLeftMargin())
  label.SetY1NDC(1.0-gStyle.GetPadTopMargin())
  label.SetX2NDC(1.0-gStyle.GetPadRightMargin())
  label.SetY2NDC(1.0)
  label.SetTextFont(42)
  label.AddText("Delphes Sim, 3000 fb^{-1} at #sqrt{s} = 13 TeV")
  label.SetFillStyle(0)
  label.SetBorderSize(0)
  label.SetTextSize(0.04)
  label.SetTextAlign(32)
  label.Draw("same")

  if hnames[1] == printHistName:
    string1 = "ntotal = %d \n" % ntotalbkg
    fNevt.write(string1)
    print "ntotal = " , "{0:.6g}".format(ntotalbkg)

  logname = ""
  if log:
    logname = "_log"

  #c.Print(datasamples[datasamples.keys()[mode]]["hname"][i]+logname+".pdf")
  h_sig1.SetTitle(hnames[0]+"_"+hnames[1])
  filename = "result"+logname+".pdf"
  if i == 0 and N_hist > 1:
    c.Print( (filename+"(") )
  elif i > 0 and i == N_hist-1:
    c.Print( (filename+")") ) 
  else:
    c.Print(filename)

