#!/usr/bin/env python
import sys, os, shutil
from ROOT import *
from train_files import train_files

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

train_size = 0.8

nevt = {}
nevt['l1_j3_b0_tau1'] = {'cmutau' : str(int(33178*train_size)), 'ctautau' : str(int(14266*train_size)),
'cnunu' : str(int(790*train_size)), 'bkg' : str(int(48240*train_size))}
nevt['l1_j2_b1_tau0'] = {'cmutau' : str(int(62848*train_size)), 'ctautau' : str(int(23580*train_size)),
'cnunu' : str(int(12248*train_size)), 'bkg' : str(int(326226*train_size))}

sel = 'l' + str(lep) + '_j' + str(jet) + '_b' + str(bjet) + '_tau' + str(taujet)

if sel not in nevt.keys():
	print('Selection must be (lep 1, jet 3, bjet 0, tau 1) or (lep 1, jet 2, bjet 1, tau 0)')
	#sys.exit()

if sel in nevt.keys():
  n_sig = nevt[sel][ch]
  n_bkg = nevt[sel]['bkg']
else:
  n_sig = "0"
  n_bkg = "0"

options = "nTrain_Signal=" + n_sig + ":nTrain_Background=" + n_bkg + ":nTest_Signal=0:nTest_Background=0:SplitMode=Random:NormMode=NumEvents:!V"

sig_files, bkg_files = train_files(ch)

for nTree in [50, 100, 200, 400]:
  for depth in [3, 4, 5]:
    for nCuts in [10, 20, 30]:
      #directory name
      #rootDir = 'mkNtuple/merged/'
      rootDir = 'mkNtuple/output/'
      configDir = './' + ch + '_l' + str(lep) + '_j' + str(jet) + '_b' + str(bjet) + '_tau' + str(taujet) + '_' + str(ver) + '/'  
      weightDir = ch + '_l' + str(lep) + '_j' + str(jet) + '_b' + str(bjet) + '_tau' + str(taujet) + '_' + str(ver) + '_NTree' + str(nTree) + '_MaxDepth' + str(depth) + '_nCuts' + str(nCuts)

      #Check if the model and files already exist
      if not os.path.exists( os.path.join(configDir, weightDir, 'weights') ):
        os.makedirs( os.path.join(configDir, weightDir, 'weights') )
      for item in os.listdir( os.path.join(configDir, weightDir, 'weights') ):
        if item.endswith(".C") or item.endswith(".root") or item.endswith("log"):
          print("Remove previous files or move on to next version!")
          #sys.exit()
      if not os.path.exists( os.path.join(configDir, weightDir, 'training_bdt.py') ):
        shutil.copy2('training_bdt.py', os.path.join(configDir, weightDir, 'training_bdt.py'))

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


      fout = TFile("output_" + weightDir + ".root","recreate")
      factory = TMVA.Factory("TMVAClassification", fout, "!V:!Silent:Color:DrawProgressBar:AnalysisType=Classification" )

      loader = TMVA.DataLoader(configDir + weightDir)
      #for var in int_vars:
      #    loader.AddVariable(var, "F")
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
          '''
          if   'DY012Jets' in fName: fileWeight = 0.287 #54047/118284
          elif 'TT012Jets' in fName: fileWeight = 0.021 #2536/118284
          elif 'W0Jets'    in fName: fileWeight = 1.0
          elif 'W1Jets'    in fName: fileWeight = 0.662 #78271/118284
          elif 'W2Jets'    in fName: fileWeight = 0.413 #48799/118284
          elif 'WW'        in fName: fileWeight = 0.006 #712/118284
          elif 'WZ'        in fName: fileWeight = 0.002 #283/118284
          elif 'ZZ'        in fName: fileWeight = 0.001 #99/118284
          '''
          f = TFile(rootDir+fName)
          t = f.Get("tree")
          loader.AddBackgroundTree(t, fileWeight)
          trees.append([f, t])

      loader.PrepareTrainingAndTestTree(sigCut, bkgCut, options)

      factory.BookMethod(loader, TMVA.Types.kBDT, "BDT", "!H:!V:NTrees=%d:MinNodeSize=5%%:MaxDepth=%d:BoostType=Grad:Shrinkage=0.5:SeparationType=GiniIndex:nCuts=%d" % (nTree, depth, nCuts))

      factory.TrainAllMethods()
      factory.TestAllMethods()
      factory.EvaluateAllMethods()
      fout.Close()

      if not os.path.exists( os.path.join(configDir, weightDir, "output_" + weightDir + ".root") ):
        shutil.move("output_" + weightDir + ".root", os.path.join(configDir, weightDir))
