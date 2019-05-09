from subprocess import call
import sys
from ROOT import TFile

file_path = sys.argv[1]
file_name = sys.argv[2]

call(["root", "-l", 'run.C("' + file_path + '", "' + file_name + '")'], shell=False)

## save Event Summary histogram ##
f = TFile('./../../analyzer/output/hist_'+file_path.split('/')[-1].replace('sample_',''), "read")
out = TFile(file_name, "update")
hevt = f.Get("EventInfo")
out.cd()
hevt.Write()
out.Write()
out.Close()
