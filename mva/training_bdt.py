#!/usr/bin/env python
import sys, os, shutil
from ROOT import *

TMVA.Tools.Instance()
TMVA.PyMethodBase.PyInitialize()

#Version of classifier
if len(sys.argv) < 7:
  print("Not enough arguements: Ch (cmutau, ctautau, cnunu), nLep, nJet, nbJet, ntauJet, Ver")
  sys.exit()
ch = sys.argv[1]
lep = sys.argv[2]
jet = sys.argv[3]
bjet = sys.argv[4]
taujet = sys.argv[5]
ver = sys.argv[6]

sigCut = TCut("nlepton == " + str(lep) + " && njet >= " + str(jet) + " && nbjet >= " + str(bjet) + " && ntaujet >= " + str(taujet))
bkgCut = TCut("nlepton == " + str(lep) + " && njet >= " + str(jet) + " && nbjet >= " + str(bjet) + " && ntaujet >= " + str(taujet))

"""
idx = {}
idx['j3b2'] = 0
idx['j3b3'] = 1
idx['j4b2'] = 2
idx['j4b3'] = 3
idx['j4b4'] = 4

nsig_Hct = ['55000', '23000', '50000', '31000', '2600']
nsig_Hut = ['50000', '17000', '52000', '28000', '1150']
nbkg = ['180000', '7100', '280000', '25000', '1300']
"""
#if ch == "Hct":
#  options = "nTrain_Signal=" + nsig_Hct[idx[jetcat]] + ":nTrain_Background=" + nbkg[idx[jetcat]] + ":nTest_Signal=0:nTest_Background=0:SplitMode=Random:NormMode=NumEvents:!V"

options = "nTrain_Signal=0:nTrain_Background=0:SplitMode=Random:NormMode=NumEvents:!V"

#directory name
rootDir = 'mkNtuple/merged/'
configDir = './'
weightDir = ch + '_j' + str(jet) + '_b' + str(bjet) + '_tau' + str(taujet) + '_' + str(ver)

#Check if the model and files already exist
if not os.path.exists( os.path.join(configDir, weightDir, 'weights') ):
  os.makedirs( os.path.join(configDir, weightDir, 'weights') )
for item in os.listdir( os.path.join(configDir, weightDir, 'weights') ):
  if item.endswith(".C") or item.endswith(".root") or item.endswith("log"):
    print("Remove previous files or move on to next version!")
    #sys.exit()
if not os.path.exists( os.path.join(configDir, weightDir, 'training_bdt.py') ):
  shutil.copy2('training_bdt.py', os.path.join(configDir, weightDir, 'training_bdt.py'))

sig_files = ['hist_LQcmutauLO.root', 'hist_LQctautauLO.root', 'hist_LQcnunuLO.root']
bkg_files = ['hist_DY012JetsM10toinf.root', 'hist_TT012Jets.root',
             'hist_W0JetsToLNu.root', 'hist_W1JetsToLNu.root', 'hist_W2JetsToLNu.root',
             'hist_WW.root', 'hist_WZ.root', 'hist_ZZ.root']

int_vars = ['njet', 'nbjet', 'ncjet', 'ntaujet',]
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


fout = TFile("output_" + weightDir + ".root","recreate")
factory = TMVA.Factory("TMVAClassification", fout, "!V:!Silent:Color:DrawProgressBar:AnalysisType=Classification" )

loader = TMVA.DataLoader(weightDir)
for var in int_vars:
    loader.AddVariable(var, "I")
for var in float_vars:
    loader.AddVariable(var, "F")

loader.AddSpectator("njet")
loader.AddSpectator("nbjet")

trees = []
for fName in sig_files:
    fileWeight = 1.0
    if not ch in fName: continue
    f = TFile(rootDir+fName)
    t = f.Get("tree")
    loader.AddSignalTree(t, fileWeight)
    trees.append([f, t])
for fName in bkg_files:
    fileWeight = 1
    if   'DY012Jets' in fName: fileWeight = 0.287 #54047/118284
    elif 'TT012Jets' in fName: fileWeight = 0.021 #2536/118284
    elif 'W0Jets'    in fName: fileWeight = 1.0
    elif 'W1Jets'    in fName: fileWeight = 0.662 #78271/118284
    elif 'W2Jets'    in fName: fileWeight = 0.413 #48799/118284
    elif 'WW'        in fName: fileWeight = 0.006 #712/118284
    elif 'WZ'        in fName: fileWeight = 0.002 #283/118284
    elif 'ZZ'        in fName: fileWeight = 0.001 #99/118284
    f = TFile(rootDir+fName)
    t = f.Get("tree")
    loader.AddBackgroundTree(t, fileWeight)
    trees.append([f, t])

loader.PrepareTrainingAndTestTree(sigCut, bkgCut, options)

factory.BookMethod(loader, TMVA.Types.kBDT, "BDT", "!H:!V:NTrees=100:MinNodeSize=5%:MaxDepth=3:BoostType=Grad:Shrinkage=0.5:SeparationType=GiniIndex:nCuts=20")

factory.TrainAllMethods()
factory.TestAllMethods()
factory.EvaluateAllMethods()
fout.Close()

if not os.path.exists( os.path.join(configDir, weightDir, "output_" + weightDir + ".root") ):
  shutil.move("output_" + weightDir + ".root", os.path.join(configDir, weightDir))
