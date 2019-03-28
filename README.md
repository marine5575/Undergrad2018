# Undergrad2018
From Delphes2Flat
```{.Bash}
ssh -Y compute-0-2
cd ./path_to/Delphes2Flat
python create_input_file_list.py
cat file_list.txt | xargs -i -P$(nproc) -n2 python run.py
```

Run analyzer
```{.Bash}
root -l run.C'("input.root","outname.root")' #for one file
python create_input_file_list.py
source compile.sh #compile analyzer
cat file_list.txt | xargs -i -P$(nproc) -n2 python launchAna.py
source job_merge.sh
```

MVA
```{.Bash}
cd mva/mkNtuple
cat file_list.txt | xargs -i -P$(nproc) -n2 python launchAna.py
cd ..
python training_bdt.py cmutau 1 2 1 1 01
```

PlotIt
```{.Bash}
#First make cmssw env.
cd ~
cmsrel CMSSW_9_4_9_cand2
cd CMSSW_9_4_9_cand2/src/
cmsenv
cp -r ~/path_to_plotIt/plotIt ./
cd plotIt
source setup_for_cmsenv.sh
cd external
./build-external.sh
cd ../
make -j4

#How to run
path_to_/plotIt/plotIt -o plots/ path_to_/plotIt/configs/config.yml -y
``
