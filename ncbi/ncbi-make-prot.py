#!/usr/bin/python
import os
import sys

gb_id = sys.argv[1]

def check_file(filename):
    if( not os.access(filename,os.R_OK) ):
        print "%s is not available."%filename
        sys.exit(1)

filename_faa = "%s.faa"%gb_id
filename_ptt = "%s.ptt"%gb_id
check_file(filename_faa)
check_file(filename_ptt)

annot = dict()
is_start = 0
f_ptt = open(filename_ptt,'r')
for line in f_ptt:
    if( line.startswith('Location') ):
        is_start = 1
        continue
    if( is_start == 0 ):
        continue

    tokens = line.strip().split("\t")
    gene_name = 'unnamed'
    if( tokens[4] != '' ):
        gene_name = tokens[4]
    annot[tokens[3]] = '%s|%s|%s|%s'%(gene_name,tokens[3],tokens[0],tokens[1])
f_ptt.close()

seq = dict()
h_seq = ''
f_fa = open(filename_faa,'r')
for line in f_fa:
    if( line.startswith('>') ):
        h_seq = line.split('|')[1]
        seq[h_seq] = ''
    else:
        seq[h_seq] += line.strip()
f_fa.close()

for gi in seq.keys():
    if( not annot.has_key(gi) ):
        sys.stderr.write("No GI: %s\n"%gi)
    print ">%s\n%s"%(annot[gi],seq[gi])
