#define makeTuple_cxx
#include "makeTuple.h"
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>
using namespace std;

void makeTuple::Loop(const std::string outFileName)
{

  if (fChain == 0) return;

  TFile* f = new TFile(outFileName.c_str(), "recreate");
  TTree* tree = new TTree("tree", "ntuple");

  float b_njet, b_nbjet, b_ncjet, b_ntaujet, b_nlepton;
  float b_lepton1_pt, b_lepton1_eta, b_lepton1_phi, b_lepton1_e;
  float b_lepton2_pt, b_lepton2_eta, b_lepton2_phi, b_lepton2_e;
  float b_met_pt, b_met_phi, b_met_e;
  float b_tau1_pt, b_tau1_eta, b_tau1_phi, b_tau1_e;
  float b_tau2_pt, b_tau2_eta, b_tau2_phi, b_tau2_e;
  float b_jet_ht, b_jetlepmet_ht;
  float b_lep1met_pt, b_lep1tau1_pt;
  float b_tau1tau2_pt, b_tau1_tau2_dr, b_lep1_lep2_dr, b_tau1_lep1_dr;
  float b_lep1_met_dphi, b_tau1_met_dphi, b_tau1lep1_met_dphi;
  float b_lep1_b1_dr, b_lep1_c1_dr;

  tree->Branch("njet", &b_njet, "njet/F");
  tree->Branch("nbjet", &b_nbjet, "nbjet/F");
  tree->Branch("ncjet", &b_ncjet, "ncjet/F");
  tree->Branch("ntaujet", &b_ntaujet, "ntaujet/F");

  tree->Branch("nlepton", &b_nlepton, "nlepton/F");
  tree->Branch("lepton1_pt", &b_lepton1_pt, "lepton1_pt/F");
  tree->Branch("lepton1_eta", &b_lepton1_eta, "lepton1_eta/F");
  tree->Branch("lepton1_phi", &b_lepton1_phi, "lepton1_phi/F");
  tree->Branch("lepton1_e", &b_lepton1_e, "lepton1_e/F");
  tree->Branch("lepton2_pt", &b_lepton2_pt, "lepton2_pt/F");
  tree->Branch("lepton2_eta", &b_lepton2_eta, "lepton2_eta/F");
  tree->Branch("lepton2_phi", &b_lepton2_phi, "lepton2_phi/F");
  tree->Branch("lepton2_e", &b_lepton2_e, "lepton2_e/F");
  tree->Branch("met_pt", &b_met_pt, "met_pt/F");
  tree->Branch("met_phi", &b_met_phi, "met_phi/F");
  tree->Branch("met_e", &b_met_e, "met_e/F");
  tree->Branch("tau1_pt", &b_tau1_pt, "tau1_pt/F");
  tree->Branch("tau1_eta", &b_tau1_eta, "tau1_eta/F");
  tree->Branch("tau1_phi", &b_tau1_phi, "tau1_phi/F");
  tree->Branch("tau1_e", &b_tau1_e, "tau1_e/F");
  tree->Branch("tau2_pt", &b_tau2_pt, "tau2_pt/F");
  tree->Branch("tau2_eta", &b_tau2_eta, "tau2_eta/F");
  tree->Branch("tau2_phi", &b_tau2_phi, "tau2_phi/F");
  tree->Branch("tau2_e", &b_tau2_e, "tau2_e/F");

  tree->Branch("jet_ht", &b_jet_ht, "jet_ht/F");
  tree->Branch("jetlepmet_ht", &b_jetlepmet_ht, "jetlepmet_ht/F");
  tree->Branch("lep1met_pt", &b_lep1met_pt, "lep1met_pt/F");
  tree->Branch("lep1tau1_pt", &b_lep1tau1_pt, "lep1tau1_pt/F");
  tree->Branch("tau1tau2_pt", &b_tau1tau2_pt, "tau1tau2_pt/F");
  tree->Branch("tau1_tau2_dr", &b_tau1_tau2_dr, "tau1_tau2_dr/F");
  tree->Branch("lep1_lep2_dr", &b_lep1_lep2_dr, "lep1_lep2_dr/F");
  tree->Branch("tau1_lep1_dr", &b_tau1_lep1_dr, "tau1_lep1_dr/F");
  tree->Branch("lep1_met_dphi", &b_lep1_met_dphi, "lep1_met_dphi/F");
  tree->Branch("tau1_met_dphi", &b_tau1_met_dphi, "tau1_met_dphi/F");
  tree->Branch("tau1lep1_met_dphi", &b_tau1lep1_met_dphi, "tau1lep1_met_dphi/F");
  tree->Branch("lep1_b1_dr", &b_lep1_b1_dr, "lep1_b1_dr/F");
  //tree->Branch("lep1_c1_dr", &b_lep1_c1_dr, "lep1_c1_dr/F");
  //tree->Branch("", &b_, "/F");


  //Event Loop
  Long64_t nentries = fChain->GetEntries();
  Long64_t nbytes = 0, nb = 0;

  for(Long64_t jentry=0; jentry<nentries; jentry++) {
    fChain->GetEntry(jentry);
    //std::cout << jentry << " / " << nentries << '\r';

    //Lepton
    std::vector<int> GoodMuIdx, GoodElecIdx;
    int nGoodMuon = 0;
    int nGoodElectron= 0;
    int tau_idx;

    for(int i = 0; i < nMuon; i++){
      if(GoodMuIdx.size() == 0 && Muon_pt[i] > 30 && std::abs(Muon_eta[i]) < 2.4 && Muon_relIso[i] < 0.15)
        GoodMuIdx.push_back(i);
      else if(GoodMuIdx.size() > 0 && Muon_pt[i] > 25 && std::abs(Muon_eta[i]) < 2.4 && Muon_relIso[i] < 0.15)
        GoodMuIdx.push_back(i);
    }
    for(int i = 0; i < nElectron; i++){
      if(GoodElecIdx.size() == 0 && Electron_pt[i] > 30 && std::abs(Electron_eta[i]) < 2.4 && Electron_relIso[i] < 0.25)
        GoodElecIdx.push_back(i);
      else if(GoodElecIdx.size() > 0 && Electron_pt[i] > 25 && std::abs(Electron_eta[i]) < 2.4 && Electron_relIso[i] < 0.25)
        GoodElecIdx.push_back(i);
    }

    nGoodMuon = GoodMuIdx.size();
    nGoodElectron = GoodElecIdx.size();
    if( nGoodMuon + nGoodElectron < 1 ) continue;

    TLorentzVector lepton[nGoodMuon + nGoodElectron];
    for(int i = 0; i < nGoodMuon; i++){
      int idx = GoodMuIdx.at(i);
      lepton[i].SetPtEtaPhiM(Muon_pt[idx], Muon_eta[idx], Muon_phi[idx], Muon_m[idx]);
    }
    for(int i = nGoodMuon; i < nGoodMuon + nGoodElectron; i++){
      int idx = GoodElecIdx.at(i-nGoodMuon);
      lepton[i].SetPtEtaPhiM(Electron_pt[idx], Electron_eta[idx], Electron_phi[idx], Electron_m[idx]);
    }

    //Also pT sorting
    std::vector<int> GoodLepIdx;
    for( int i = 0; i < nGoodMuon + nGoodElectron; i++ ) GoodLepIdx.push_back(i);
    std::sort(GoodLepIdx.begin(), GoodLepIdx.end(),
              [&](size_t a, size_t b) {return lepton[a].Pt() > lepton[b].Pt();});

    b_nlepton = nGoodMuon + nGoodElectron;
    if( GoodLepIdx.size() > 0 ){
      b_lepton1_pt = lepton[GoodLepIdx[0]].Pt();
      b_lepton1_eta = lepton[GoodLepIdx[0]].Eta();
      b_lepton1_phi = lepton[GoodLepIdx[0]].Phi();
      b_lepton1_e = lepton[GoodLepIdx[0]].E();
      if( GoodLepIdx.size() > 1 ){
        b_lepton2_pt = lepton[GoodLepIdx[1]].Pt();
        b_lepton2_eta = lepton[GoodLepIdx[1]].Eta();
        b_lepton2_phi = lepton[GoodLepIdx[1]].Phi();
        b_lepton2_e = lepton[GoodLepIdx[1]].E();
      }
      else{
        b_lepton2_pt = b_lepton2_eta = b_lepton2_phi = b_lepton2_e = 0;
      }
    }

    TLorentzVector met;
    double MET_x = TMath::Abs(MET_pt)*TMath::Cos(MET_phi);
    double MET_y = TMath::Abs(MET_pt)*TMath::Sin(MET_phi);
    met.SetPxPyPzE( MET_x, MET_y, 0, MET_pt );
    b_met_pt = met.Pt();
    b_met_phi = met.Phi();
    b_met_e = met.E();

    b_lep1met_pt = (lepton[GoodLepIdx[0]] + met).Pt();
    b_lep1_met_dphi = lepton[GoodLepIdx[0]].DeltaPhi(met);
    if( GoodLepIdx.size() > 1 ) b_lep1_lep2_dr = lepton[GoodLepIdx[0]].DeltaR(lepton[GoodLepIdx[1]]);
    


    //Jet
    std::vector<int> tauIdx, bIdx, cIdx, jetIdx;
    TLorentzVector jet;

    b_njet = b_nbjet = b_ncjet = b_ntaujet = 0;
    b_jet_ht = 0;

    for(int i=0; i<nJet; i++){
      if(Jet_pt[i] > 30 && abs(Jet_eta[i]) < 2.4){
        jet.SetPtEtaPhiM(Jet_pt[i], Jet_eta[i], Jet_phi[i], Jet_m[i]);
        b_njet++;
        b_jet_ht += Jet_pt[i];
        jetIdx.push_back(i);

        if(Jet_bTag[i] == 1){
          b_nbjet++;
          bIdx.push_back(i);
        }
        if(Jet_cTag[i] == 2){
          b_ncjet++;
          cIdx.push_back(i);
        }
        if(Jet_tauTag[i] == 1){
          b_ntaujet++;
          tauIdx.push_back(i);
        }
      }
    }
    b_jetlepmet_ht = b_jet_ht + b_lepton1_pt + b_lepton2_pt + b_met_pt;

    //Tau
    TLorentzVector tauJet[2];
    for( unsigned int i = 0; i < tauIdx.size(); i++){
      int j = tauIdx.at(i);
      if( tauJet[0].Pt() == 0 ) tauJet[0].SetPtEtaPhiM(Jet_pt[j],Jet_eta[j],Jet_phi[j], Jet_m[j]);
      else if( tauJet[1].Pt() == 0 ) tauJet[1].SetPtEtaPhiM(Jet_pt[j],Jet_eta[j],Jet_phi[j], Jet_m[j]);
      else continue;
    }
    b_tau1_pt = tauJet[0].Pt();
    b_tau1_eta = tauJet[0].Eta();
    b_tau1_phi = tauJet[0].Phi();
    b_tau1_e = tauJet[0].E();
    b_tau2_pt = tauJet[1].Pt();
    b_tau2_eta = tauJet[1].Eta();
    b_tau2_phi = tauJet[1].Phi();
    b_tau2_e = tauJet[1].E();

    //Even n tau jet = 0, tauJet[i] should be initialized by (0,0,0,0)
    b_lep1tau1_pt = (tauJet[0] + lepton[GoodLepIdx[0]]).Pt();
    b_tau1_lep1_dr = tauJet[0].DeltaR(lepton[GoodLepIdx[0]]);
    b_tau1tau2_pt = (tauJet[0] + tauJet[1]).Pt();
    b_tau1_tau2_dr = tauJet[0].DeltaR(tauJet[1]);
    b_tau1_met_dphi = tauJet[0].DeltaPhi(met);
    b_tau1lep1_met_dphi = (tauJet[0] + lepton[GoodLepIdx[0]]).DeltaPhi(met);

    //b jet
    TLorentzVector bJet[2];
    for( unsigned int i = 0; i < bIdx.size(); i++){
      int j = bIdx.at(i);
      if( bJet[0].Pt() == 0 ) bJet[0].SetPtEtaPhiM(Jet_pt[j],Jet_eta[j],Jet_phi[j], Jet_m[j]);
      else if( bJet[1].Pt() == 0) bJet[1].SetPtEtaPhiM(Jet_pt[j],Jet_eta[j],Jet_phi[j], Jet_m[j]);
      else continue;
    }

    //Even n b jet = 0, bJet[i] should be initialized by (0,0,0,0)
    b_lep1_b1_dr = bJet[0].DeltaR(lepton[GoodLepIdx[0]]);

    tree->Fill();
  }
  tree->Write();

  f->Close();
}
