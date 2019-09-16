#!/usr/bin/env python
import os, sys
import random

def train_files(ch):
	train_size = 0.8
	rootDir = "/home/user123/work/Undergrad2018/Delphes2Flat/output/"

	list_output = os.listdir("mkNtuple/output/")
	list_output.remove(".gitkeep")
	'''
	bkg_procs = ['DY012JetsM10toinf', 
		'TT012Jets', 'W0JetsToLNu', 'W1JetsToLNu', 'W2JetsToLNu', 'WW', 'WZ', 'ZZ']
	'''
	bkg_procs = ['TT012Jets']

	sig = []

	if ch == "cmutau":
		for sig_file in list_output:
			if ch in sig_file:
				sig.append(sig_file)
				list_output.remove(sig_file)

	elif ch == "ctautau":
		for	sig_file in list_output:
			if ch in sig_file:
				sig.append(sig_file)
				list_output.remove(sig_file)

	elif ch == "cnunu":
		for sig_file in list_output:
			if ch in sig_file:
				sig.append(sig_file)
				list_output.remove(sig_file)

	else: print("Check channel : cmutau, ctautau or cnunu")

	return sig, list_output
