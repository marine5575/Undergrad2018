#!/usr/bin/env python
import os, sys
from ROOT import *
import ROOT
from array import array
import numpy as np
gROOT.SetBatch(True)
gROOT.ProcessLine("gErrorIgnoreLevel = kFatal;")

#directory name
rootDir = 'mkNtuple/output'
configDir = './'
source = '../analyzer/file_list.txt'

if len(sys.argv) < 7:
  print("Not enough arguements: Ch (cmutau, ctautau, cnunu), nLep, nJet, nbJet, ntauJet, Ver")
  sys.exit()
ch = sys.argv[1]
lep = sys.argv[2]
jet = sys.argv[3]
bjet = sys.argv[4]
taujet = sys.argv[5]
ver = sys.argv[6]

weightDir = ch +'_l' + str(lep)+ '_j' + str(jet) + '_b' + str(bjet) + '_tau' + str(taujet) + '_' + str(ver)
scoreDir = "scores_"+weightDir
histDir = "hist_"+weightDir
if not os.path.exists(os.path.join(configDir, histDir)):
  try: os.makedirs(os.path.join(configDir, histDir))
  except: pass

score_file_list = []
hist_file_list = []
event_file_list = []

with open(source) as fp:
  for line in fp.readlines():
    event_file = line.split(' ')[1]
    event_file = event_file.replace("./output", "../analyzer/output")
    event_file = event_file.rstrip('\n')

    score_file = event_file.replace("./output/hist_", "score_")
    score_file = score_file.rstrip('\n')
    score_file_list.append(score_file)

    hist_file = score_file.replace("score", "hist")
    hist_file_list.append(hist_file)

for i in range(len(score_file_list)):
  fscore = TFile.Open(os.path.join(scoreDir, score_file_list[i]))
  fevt = TFile.Open(event_file)
  fout = TFile.Open(os.path.join(histDir, hist_file_list[i]), "RECREATE")

  tree = fscore.Get("tree")
  hevt = fevt.Get("EventInfo")
  h = TH1F("h_score", "h_score", 20, -1, 1)
#  outtree.Branch("h_score", h, "score/F")
#  outtree.Branch("EventInfo", hevt, "EventInfo/I")

  for j in range(tree.GetEntries()):
    tree.GetEntry(j)
    if tree.score < -1: continue
    h.Fill(tree.score)

  h.Draw()
#  outtree.Write()
  h.Write()
  hevt.Write()
  fout.Close()
