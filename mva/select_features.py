import sys, os, shutil
import subprocess
import time

#Version of classifier
if len(sys.argv) < 8:
  print("Not enough arguements: Ch, lepton, jet, bJet, tauJet, ver, Recompute")
  sys.exit()
ch = sys.argv[1]
lep = sys.argv[2]
jet = sys.argv[3]
bjet = sys.argv[4]
taujet = sys.argv[5]
ver = sys.argv[6]
era = sys.argv[7]

jetcat = 'l' + str(lep) + '_j' + str(jet) + '_b' + str(bjet) + '_tau' + str(taujet) #will be overidden as 99

print '#####Please Wait#####'

#Run training for check separation
subprocess.call('python training_bdt.py ' + ch + ' ' + lep + ' ' + jet + ' ' + bjet + ' ' + taujet + ' 01 &> ' + 'log_' + ch + '_' + jetcat + '_01', shell = True)


#wait until log file created: for double check!!
while True:
  try:
    log_file = open('./log_' + ch + '_' + jetcat + '_01', 'r')
  except: continue
  else: break

keep_2_lines = False
keep_4_lines = False
flag = 0

while True:
  logline = log_file.readline()
  if keep_2_lines:
    print (''.join(logline.split(':')[1:]).strip())
    keep_2_lines = False
  if keep_4_lines:
    print (''.join(logline.split(':')[1:]).strip())
    if flag == 3:
      keep_4_lines = False
      flag = 0
      print '\n'
    else: flag += 1
  if logline.find('ROC-integ') > 0:
    print (''.join(logline.split(':')[1:]).strip())
    keep_2_lines = True
  if logline.find('Signal efficiency') > 0:
    print (''.join(logline.split(':')[1:]).strip())
    keep_4_lines = True
    flag += 1
  if not logline: break

try: os.remove( os.path.join(era, 'output_' + ch + '_' + jetcat + '*.root') )
except: print "No folder or output file!"
print " "
