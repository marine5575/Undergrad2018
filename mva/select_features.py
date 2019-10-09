import sys, os, shutil
import subprocess
import time
#from variimport timeables import input_variables_bdt

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
#do_recompute = sys.argv[7] == "True"

jetcat = 'l' + str(lep) + '_j' + str(jet) + '_b' + str(bjet) + '_tau' + str(taujet) #will be overidden as 99

#nfeat = {'l1_j3_b0_tau1':10, 'l1_j2_b1_tau0':10}
#nfeat = {'j3b2':28, 'j3b3':28, 'j4b2':28, 'j4b3':28, 'j4b4':28}
print '####Extracting top N features for ' + ch + '_' + jetcat

#Run training for check separation
#if do_recompute:
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

#if do_recompute:
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

#rank_list = []
##num_evt = []
#
##going to the first line of log file, check NEvents and ranking
#log_file = open('./log_' + ch + '_' + jetcat + '_01', 'r')
##else: log_file = open('Var_logs/' + era + '/log_' + ch + '_' + jetcat + '_99', 'r')
#loglines = log_file.readlines()
#
#for line in loglines:
#  #if any(i in line for i in ['ROC-integ', 'Signal efficiency']):
#    #print line
#  #  pass
#  #if 'Train method' in line: keep_line = False
#  if 'ROC-integ' in line:
#    keep_2_line = True
#    print line
#  if keep_2_line:
#    print line
#    keep_2_line = False
#  if 'Signal efficiency' in line:
#    keep_4_line = True
#    flag = flag + 1
#    print line
#  if keep_4_line:
#    if flag == 3:
#      flag = 0
#      keep_4_line = False
#    else:
#      flag = flag + 1
#    print line
#  #if 'number of events passed' in line: num_evt.append(line.split(':')[3].split('/')[0].strip())
#  #if keep_line and line.count(':') == 3: rank_list.append(line.split(':')[2].strip())
#
##Check number of events for training
##print num_evt
##print 'Signal * 0.8 =', str(int(round(int(num_evt[0]) * 0.8))) #Signal first in TMVA
##print 'Background * 0.8 =', str(int(round(int(num_evt[1]) * 0.8)))
#
##Select top N = nfeat[jetcat] variables and sort by the order of features in root file
##rank_list = rank_list[1:]
##rank_list = rank_list[:nfeat[jetcat]]
##print rank_list
#
##all_vars = input_variables_bdt(jetcat)
##sorted_rank_list = []
##for var in all_vars:
##  if var in rank_list: sorted_rank_list.append(var)
#
##print "  selected['" + ch + '_' + jetcat + '_' + era + "'] = " + str(sorted_rank_list)


try: os.remove( os.path.join(era, 'output_' + ch + '_' + jetcat + '*.root') )
except: print "No folder or output file!"
print " "
