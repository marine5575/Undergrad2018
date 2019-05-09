#!/usr/bin/env python
import os, sys
from ROOT import *
import ROOT
from array import array
import numpy as np
gROOT.SetBatch(True)
gROOT.ProcessLine("gErrorIgnoreLevel = kFatal;")

TMVA.Tools.Instance()

#Channel and version
if len(sys.argv) < 9:
  print("Not enough arguements: Ch (cmutau, ctautau, cnunu), nLep, nJet, nbJet, ntauJet, Ver, file path, name")
  sys.exit()
ch = sys.argv[1]
lep = sys.argv[2]
jet = sys.argv[3]
bjet = sys.argv[4]
taujet = sys.argv[5]
ver = sys.argv[6]
file_path = sys.argv[7]
name = sys.argv[8]


#directory name
rootDir = 'mkNtuple/output'
configDir = './'
weightDir = ch +'_l' + str(lep)+ '_j' + str(jet) + '_b' + str(bjet) + '_tau' + str(taujet) + '_' + str(ver)
scoreDir = 'scores_'+ch +'_l' + str(lep)+ '_j' + str(jet) + '_b' + str(bjet) + '_tau' + str(taujet) + '_' + str(ver)

if not os.path.exists(os.path.join(configDir, scoreDir) ):
  try: os.makedirs(os.path.join(configDir, scoreDir))
  except: pass

# Load data
sig_files = ['hist_LQcmutauLO.root', 'hist_LQctautauLO.root', 'hist_LQcnunuLO.root']
bkg_files = ['hist_DY012JetsM10toinf.root', 'hist_TT012Jets.root',
             'hist_W0JetsToLNu.root', 'hist_W1JetsToLNu.root', 'hist_W2JetsToLNu.root',
             'hist_WW.root', 'hist_WZ.root', 'hist_ZZ.root']

#int_vars = ['njet', 'nbjet', 'ncjet', 'ntaujet',]
float_vars = ['lepton1_pt', 'lepton2_pt', 'met_pt', 'tau1_pt', 'tau2_pt',
              'jet_ht', 'jetlepmet_ht',
              'lep1met_pt', 'lep1tau1_pt', 'tau1tau2_pt', 'tau1_tau2_dr',
              'lep1_lep2_dr', 'tau1_lep1_dr', 'lep1_met_dphi', 'tau1_met_dphi',
              'tau1lep1_met_dphi', 'lep1_b1_dr']

if int(lep) < 2:
  for tmp in ['lepton2_pt', 'lep1_lep2_dr']:
    float_vars.remove(tmp)
if int(bjet) < 1: float_vars.remove('lep1_b1_dr')
if int(taujet) < 2:
  for tmp in ['tau2_pt', 'tau1tau2_pt', 'tau1_tau2_dr',]: float_vars.remove(tmp)
  if int(taujet) < 1:
    for tmp2 in ['tau1_pt',  'lep1tau1_pt',   'tau1_lep1_dr', 'tau1_met_dphi', 'tau1lep1_met_dphi']:
      float_vars.remove(tmp2)

if os.path.exists(os.path.join(configDir, scoreDir, 'score_' + name.split('_')[1])):
  print(scoreDir + "/score_"  + name + (' is already exist!').rjust(50-len(name)))
  sys.exit()

reader = TMVA.Reader("Color:!Silent")
#print(name.split('/')[2])
#chain = ROOT.TChain("tree")
if os.path.exists(os.path.join(rootDir , name.split('/')[2])):
  data = TFile.Open(os.path.join(rootDir, name.split('/')[2]))
  data_tree = data.Get('tree')
  #chain.AddFile(os.path.join(rootDir , name.split('/')[2]))
else:
  print("No input file")
  sys.exit()

outfile = TFile.Open(os.path.join(configDir, scoreDir, 'score_' + name.lstrip(name.split('_')[0]+'_')),'RECREATE')
print(name.lstrip(name.split('_')[0]+'_'))
outtree = TTree("tree","tree")

branches = {}
for branch in data_tree.GetListOfBranches():
  branchName = branch.GetName()
  #if branchName in int_vars:
  #    branches[branchName] = array('f', [-999])
  #    reader.AddVariable(branchName, branches[branchName])
  #    data_tree.SetBranchAddress(branchName, branches[branchName])
  if branchName in float_vars:
      branches[branchName] = array('f', [-999])
      reader.AddVariable(branchName, branches[branchName])
      data_tree.SetBranchAddress(branchName, branches[branchName])

  elif branchName in ["njet", "nbjet"]:
    branches[branchName] = array('f', [-999])
    reader.AddSpectator(branchName, branches[branchName])

reader.BookMVA('BDT', TString(os.path.join(configDir, weightDir, 'weights/TMVAClassification_BDT.weights.xml')))

totalevt = data_tree.GetEntries()
#totalevt = chain.GetEntries()
#print("this sample contains "+str(totalevt)+" combinations")

score = np.zeros(1, dtype=np.float32)
njet  = np.zeros(1, dtype=np.float32)
nbjet = np.zeros(1, dtype=np.float32)

outtree.Branch('score' , score  , 'score/F')
outtree.Branch('njet'  , njet   , 'njet/I')
outtree.Branch('nbjet' , nbjet  , 'nbjet/I')

for i in xrange(totalevt):
  data_tree.GetEntry(i)
  #chain.GetEntry(i)

  if data_tree.nlepton != int(lep): continue
  if data_tree.njet < int(jet): continue
  if data_tree.nbjet < int(bjet): continue
  if data_tree.ntaujet < int(taujet): continue
  #if chain.nlepton != int(lep): continue
  #if chain.njet < int(jet): continue
  #if chain.nbjet < int(bjet): continue
  #if chain.ntaujet < int(taujet): continue

  score[0] = reader.EvaluateMVA('BDT')
  njet[0]  = data_tree.njet
  nbjet[0] = data_tree.nbjet
  #njet[0]  = chain.njet
  #nbjet[0] = chain.nbjet
  outtree.Fill()

  #if i%1000 == 0: print 'processing '+str(i)+'th event\r'

score[0] = -1
njet[0]  = 0
nbjet[0] = 0
outtree.Fill()

outfile.Write()
outfile.Close()
