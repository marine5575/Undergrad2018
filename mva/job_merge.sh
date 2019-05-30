FOLDER=$1
rm merged/hist_*

hadd merged/hist_DY012JetsM10toinf.root $FOLDER/hist_DY012JetsM10toinf*.root
hadd merged/hist_W0JetsToLNu.root $FOLDER/hist_W0JetsToLNu*.root
hadd merged/hist_W2JetsToLNu.root $FOLDER/hist_W2JetsToLNu*.root
hadd merged/hist_TT012Jets.root $FOLDER/hist_TT012Jets*.root
hadd merged/hist_WW.root $FOLDER/hist_WW*.root
hadd merged/hist_WZ.root $FOLDER/hist_WZ*.root
hadd merged/hist_ZZ.root $FOLDER/hist_ZZ*.root
hadd merged/hist_LQcmutauLO.root $FOLDER/hist_LQcmutauLO*.root
hadd merged/hist_LQctautauLO.root $FOLDER/hist_LQctautauLO*.root
hadd merged/hist_LQcnunuLO.root $FOLDER/hist_LQcnunuLO*.root
