#!/usr/bin/env python
import os, sys
import random

def train_files(ch):
	rootDir = "/home/user123/work/Undergrad2018/Delphes2Flat/output/"

	sig = []
	bkg = []
	if ch == "cmutau" or ch == "ctautau" or ch == "cnunu":
		for i in range(1, 6):
			sig.append('hist_LQ' + ch + 'LO_00' + str(i) + '.root')

	else: print("Check channel : cmutau, ctautau or cnunu")

	for i in range(1, 10):
		bkg.append('hist_TT012Jets_00' + str(i) + '.root')
	for i in range(10, 51):
		bkg.append('hist_TT012Jets_0' + str(i) + '.root')


	return sig, bkg
